#!/usr/bin/env python3
"""Regenerate agents/AGENTS.md from all skills/*/SKILL.md files.

Run this after adding or updating a skill to keep the Codex/Copilot bundle in sync:

    python scripts/generate_agents.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = ROOT / "agents" / "AGENTS.md"

HEADER = """<skills>

You have access to Codacy skills that teach you how to use the Codacy CLI to improve code quality workflows.

These skills are:
"""

FOOTER = """
IMPORTANT: You MUST read the SKILL.md file whenever the description of a skill matches the user's intent or may help accomplish their task.

<available_skills>

{available_skills}
</available_skills>

Paths referenced within skill folders are relative to that skill folder. For example, `codacy-cloud-cli`'s `references/api.md` would be referenced as `skills/codacy-cloud-cli/references/api.md`.

</skills>
"""


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.search(r"^---\s*\n(.*?)\n---\s*", text, re.DOTALL)
    if not match:
        return {}
    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        data[key.strip()] = value.strip()
    return data


def collect_skills() -> list[dict[str, str]]:
    skills = []
    for skill_md in sorted(ROOT.glob("skills/*/SKILL.md")):
        meta = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        name = meta.get("name")
        description = meta.get("description")
        if not name or not description:
            print(f"Warning: missing name or description in {skill_md}", file=sys.stderr)
            continue
        skills.append(
            {
                "name": name,
                "description": description,
                "path": str(skill_md.parent.relative_to(ROOT)),
            }
        )
    return skills


def render(skills: list[dict[str, str]]) -> str:
    skill_list = "\n".join(
        f' - {s["name"]} -> "{s["path"]}/SKILL.md"' for s in skills
    )
    available = "\n".join(
        f'{s["name"]}: `{s["description"]}`\n' for s in skills
    )
    return HEADER + skill_list + FOOTER.format(available_skills=available.rstrip())


def main() -> None:
    skills = collect_skills()
    if not skills:
        print("No skills found.", file=sys.stderr)
        sys.exit(1)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(render(skills), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH} with {len(skills)} skill(s).")


if __name__ == "__main__":
    main()
