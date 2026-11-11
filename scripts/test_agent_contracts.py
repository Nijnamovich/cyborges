#!/usr/bin/env python3
"""Contract tests: documenter comment pruning and per-seat tool posture."""
import importlib.util
import json
import re
from fnmatch import fnmatchcase
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent.parent
AGENTS = ROOT / "agents"

SPEC = importlib.util.spec_from_file_location(
    "return_checker", Path(__file__).with_name("check-subagent-return.py"))
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)

POSTURE_TOOLS = ("read", "edit", "glob", "grep", "shell", "webfetch", "websearch",
                 "question", "skill", "subagent", "execute", "browser")
MATRIX_TOOLS = POSTURE_TOOLS
# frontmatter key per matrix column
FRONTMATTER_KEY = {"shell": "bash", "subagent": "task"}
# effective posture when the agent declares no rule for that action
INHERITED = {"read": "allow", "edit": "allow", "glob": "allow", "grep": "allow",
             "shell": "allow"}


def text_readme():
    return (ROOT / "readme.md").read_text(encoding="utf-8")


def frontmatter_text(name):
    text = (AGENTS / f"{name}.md").read_text(encoding="utf-8-sig")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---", text, re.DOTALL)
    if not match:
        raise AssertionError(f"{name}: missing frontmatter")
    return text, match.group(1)


def permission_block(name):
    """Parse the 2-space-indented `permission:` map into {action: effect | {pattern: effect}}."""
    _, fm = frontmatter_text(name)
    perm, inside, current = {}, False, None
    for line in fm.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        if indent == 0:
            inside = stripped.startswith("permission:")
            current = None
            continue
        if not inside:
            continue
        key, _, value = stripped.partition(":")
        key = key.strip().strip("'\"")
        value = value.strip().strip("'\"")
        if indent == 2:
            if value:
                perm[key] = value
                current = None
            else:
                perm[key] = {}
                current = key
        elif current:
            perm[current][key] = value
    return perm


def posture_matrix():
    text = (ROOT / "readme.md").read_text(encoding="utf-8")
    section = re.search(r"^### Per-seat tool posture\s*$(.*?)^## ", text, re.MULTILINE | re.DOTALL)
    if not section:
        raise AssertionError("readme.md: missing '### Per-seat tool posture' section")
    lines = [ln.strip() for ln in section.group(1).splitlines() if ln.strip().startswith("|")]
    header = [c.strip() for c in lines[0].strip("|").split("|")]
    rows = {}
    for line in lines[2:]:
        cells = [c.strip() for c in line.strip("|").split("|")]
        rows[cells[0].strip("`")] = dict(zip(header[1:], cells[1:]))
    return header[1:], rows


class CommentPruningContract(unittest.TestCase):
    def test_documenter_section_and_keep_list(self):
        text, _ = frontmatter_text("documenter")
        self.assertIn("## Comment pruning", text)
        for token in ("license", "eslint-disable", "@ts-ignore", "@ts-expect-error",
                      "@generated", "DO NOT EDIT", "TODO", "FIXME", "git diff",
                      "knowledge", "comment-only", "verified", "reverted",
                      "not_required", "blocked"):
            with self.subTest(token=token):
                self.assertIn(token.lower(), text.lower())
        self.assertIn("Never delete files", text)
        # Line-anchored so the inline-code mentions (`## Comment pruning`) in the
        # body do not stand in for the headings themselves.
        self.assertLess(text.index("\n## Post-change documentation audit"),
                        text.index("\n## Comment pruning"))

    def test_schema_fields_are_optional_and_validated(self):
        schema = json.loads((AGENTS / "documenter.schema.json").read_text(encoding="utf-8"))
        for key in ("comments_pruned", "prune_verification"):
            with self.subTest(key=key):
                self.assertIn(key, schema["properties"])
                self.assertNotIn(key, schema["required"])
        self.assertEqual(schema["properties"]["prune_verification"]["enum"],
                         ["verified", "reverted", "not_required", "blocked"])
        base = {"files_changed": [], "files_added": [], "files_removed": [],
                "summary": "s", "confidence": 0.5}
        self.assertEqual(checker.check("documenter", json.dumps(base))[0], 0)
        valid = {**base,
                 "comments_pruned": [{"file": "src/a.ts", "removed": 2}],
                 "prune_verification": "verified"}
        self.assertEqual(checker.check("documenter", json.dumps(valid))[0], 0)
        self.assertEqual(checker.check(
            "documenter", json.dumps({**base, "prune_verification": "looks_fine"}))[0], 1)
        self.assertEqual(checker.check(
            "documenter", json.dumps({**base, "comments_pruned": [{"file": "a"}]}))[0], 1)
        self.assertEqual(checker.check(
            "documenter", json.dumps({**base, "unexpected": 1}))[0], 1)

    def test_orchestrate_names_the_terminus(self):
        text = (ROOT / "protocols" / "orchestrate.md").read_text(encoding="utf-8").lower()
        self.assertIn("comment pruning", text)
        self.assertIn("documenter", text)

    def test_readme_documenter_row_mentions_pruning(self):
        text = (ROOT / "readme.md").read_text(encoding="utf-8")
        section = re.search(r"^## Available agents\s*$(.*?)^## ", text,
                            re.MULTILINE | re.DOTALL)
        self.assertIsNotNone(section, "readme.md: missing '## Available agents' section")
        rows = [ln.strip() for ln in section.group(1).splitlines()
                if ln.strip().startswith("|")]
        documenter_rows = [ln for ln in rows
                           if ln.strip("|").split("|")[0].strip().strip("`") == "documenter"]
        self.assertEqual(len(documenter_rows), 1)
        self.assertIn("prun", documenter_rows[0])


class PerSeatPosture(unittest.TestCase):
    def test_matrix_covers_every_agent_and_tool(self):
        header, rows = posture_matrix()
        self.assertEqual(tuple(header), MATRIX_TOOLS)
        self.assertEqual(len(header), len(MATRIX_TOOLS))
        self.assertEqual(set(rows), {p.stem for p in AGENTS.glob("*.md")})
        self.assertEqual(len(rows), 11)
        section = re.search(r"^### Per-seat tool posture\s*$(.*?)^## ", text_readme(),
                            re.MULTILINE | re.DOTALL)
        data_rows = [ln for ln in section.group(1).splitlines()
                     if ln.strip().startswith("|")][2:]
        self.assertEqual(len(data_rows), len(rows))

    def test_matrix_cells_are_closed_values(self):
        _, rows = posture_matrix()
        for agent, cells in rows.items():
            for tool, cell in cells.items():
                with self.subTest(agent=agent, tool=tool):
                    self.assertIn(cell, {"allow", "ask", "deny"})

    def test_frontmatter_matches_matrix_for_every_tool(self):
        _, rows = posture_matrix()
        for agent in sorted(rows):
            perm = permission_block(agent)
            for tool in POSTURE_TOOLS:
                with self.subTest(agent=agent, tool=tool):
                    key = FRONTMATTER_KEY.get(tool, tool)
                    if key not in perm:
                        value = INHERITED.get(tool)
                        self.assertIsNotNone(
                            value, f"{agent}: no explicit '{key}' posture")
                    elif isinstance(perm[key], dict):
                        effects = set(perm[key].values())
                        if tool == "subagent":
                            # a task map grants dispatch only if some target is allowed
                            value = "allow" if "allow" in effects else "deny"
                        else:
                            value = "allow"
                    else:
                        value = perm[key]
                    self.assertEqual(str(value), rows[agent][tool])

    def test_no_blanket_read_or_edit_allow(self):
        for agent in sorted(p.stem for p in AGENTS.glob("*.md")):
            perm = permission_block(agent)
            with self.subTest(agent=agent, tool="read"):
                self.assertNotEqual(perm.get("read"), "allow")
            with self.subTest(agent=agent, tool="edit"):
                self.assertNotEqual(perm.get("edit"), "allow")

    def test_browser_is_exclusive_to_coder_and_tester(self):
        allowed = {p.stem for p in AGENTS.glob("*.md")
                   if permission_block(p.stem).get("browser") == "allow"}
        self.assertEqual(allowed, {"coder", "tester"})

    def test_question_excludes_the_orchestrator(self):
        self.assertEqual(permission_block("orchestrator").get("question"), "deny")
        self.assertEqual(permission_block("delivery").get("question"), "allow")

    def test_documenter_edit_scope(self):
        edit = permission_block("documenter")["edit"]
        self.assertEqual(edit["*"], "deny")
        self.assertEqual(edit["docs/**"], "allow")
        for glob in ("*.ts", "*.go", "*.css"):
            with self.subTest(glob=glob):
                self.assertEqual(edit[glob], "allow")
        for key in ("agents/*", "protocols/*", "code-lang/*", "scripts/*",
                    "opencode.json", "readme.md"):
            with self.subTest(key=key):
                self.assertEqual(edit[key], "deny")
        self.assertGreater(list(edit).index("agents/*"), list(edit).index("*.ts"))

    def test_documenter_edit_allows_never_reach_protected_paths(self):
        edit = permission_block("documenter")["edit"]
        protected = ("agents/delivery.md", "protocols/orchestrate.md",
                     "code-lang/css/standards.md", "scripts/validate-agent.sh",
                     "readme.md", "opencode.json", "service.json",
                     "app/.env", "app/id.key", "app/id.secret", "app/id.pem",
                     "docs/sub/.env", "docs/sub/id.pem", "docs/sub/id.key")
        rules = list(edit.items())

        def effective(path):
            """Last matching rule wins, as the runtime resolves the permission map."""
            verdict = None
            for pattern, effect in rules:
                if fnmatchcase(path, pattern):
                    verdict = effect
            return verdict

        for pattern, effect in rules:
            if effect != "allow":
                continue
            for path in protected:
                with self.subTest(pattern=pattern, path=path):
                    if not fnmatchcase(path, pattern):
                        continue
                    # An allow may overlap a protected path only if a later deny wins.
                    self.assertEqual(
                        effective(path), "deny",
                        f"allow '{pattern}' reaches protected '{path}'")

    def test_documenter_shell_is_read_only_git(self):
        bash = permission_block("documenter")["bash"]
        self.assertEqual(bash["*"], "deny")
        self.assertEqual({k for k, v in bash.items() if v == "allow"},
                         {"git diff", "git diff *", "git status", "git status *",
                          "git show", "git show *"})
        for key in ("*--output*", "*--ext-diff*", "*;*", "*&&*", "*|*", "*$(*", "*<(*", "*>*"):
            with self.subTest(deny=key):
                self.assertEqual(bash[key], "deny")
        order = list(bash)
        deny_keys = ("*--output*", "*--ext-diff*", "*;*", "*&&*", "*|*", "*$(*", "*<(*", "*>*")
        self.assertEqual(order[0], "*")
        self.assertLess(
            max(order.index(k) for k, v in bash.items() if v == "allow"),
            min(order.index(k) for k in deny_keys))

    def test_documenter_pruning_doctrine_subsections(self):
        text, _ = frontmatter_text("documenter")
        headings = ("## Comment pruning", "### When pruning runs",
                    "### What always stays", "### Knowledge first",
                    "### Comment-only invariant", "### Self-verification")
        offsets = [text.index("\n" + h) for h in headings]
        self.assertEqual(offsets, sorted(offsets))
        for anchor in ("persist it into docs", "report it in `follow_up`",
                       "only statement in a block", "restore every hunk",
                       "diff output in front of you"):
            with self.subTest(anchor=anchor):
                self.assertIn(anchor.lower(), text.lower())


if __name__ == "__main__":
    unittest.main()
