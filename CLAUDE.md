# CLAUDE.md — Project instructions for Claude

This is a collection of [Claude skills](https://www.anthropic.com/news/introducing-agent-skills) for working with the [Codacy CLI](https://github.com/codacy/codacy-cloud-cli).

## Project structure

```
/
├── CLAUDE.md               # This file
├── README.md               # Project overview and installation
├── CONTRIBUTING.md         # How to contribute
├── LICENSE                 # MIT
├── CODE_OF_CONDUCT.md      # Community standards
├── SPECS/                  # Specs and task list
│   └── todo.md             # Task tracker — keep updated
├── .claude-plugin/         # Plugin manifest
│   ├── plugin.json         # Plugin metadata
│   └── marketplace.json    # Marketplace catalog
└── skills/                 # All Agent Skills
    └── <skill-name>/       # One folder per skill
        ├── SKILL.md        # Required — YAML frontmatter + instructions
        └── references/     # Optional — detailed docs
```

## Skill authoring rules

### Structure
- Folder name and `name` field: `kebab-case` only (lowercase, hyphens, no spaces or capitals)
- File must be exactly `SKILL.md` (case-sensitive)
- No `README.md` inside skill folders
- Keep `SKILL.md` under 500 lines; move verbose content to `references/` files

### YAML frontmatter (required fields)
```yaml
---
name: skill-name-in-kebab-case
description: Third-person description of what it does and when to use it. Include trigger phrases.
---
```
- `description`: under 1024 characters, no XML tags (`< >`), written in **third person**
- Do not use reserved names: `anthropic-*`, `claude-*`

### Writing good descriptions
Include: **what** the skill does + **when** to trigger it + key trigger phrases.

Good:
```
Queries Codacy issues, findings, and pull request data using the Codacy CLI.
Use when the user asks about code issues, security findings, pull request analysis,
or wants to run Codacy commands.
```

Bad:
```
Helps with Codacy.
```

### Writing good instructions
- Be specific and actionable — avoid vague directives
- Use numbered steps for ordered workflows
- Set appropriate freedom: exact commands for fragile operations, flexible guidance for context-dependent ones
- Include error handling for common failures
- Reference detailed content via links to `references/` files rather than inlining everything
- Provide concrete examples

## Skills in this project

| Skill | Purpose |
|-------|---------|
| `codacy-cli` | Use the Codacy CLI: authentication, commands, help system |
| `codacy-code-review` | Enrich code reviews with Codacy data |
| `configure-codacy` | Tailor Codacy config to the project, reduce noise |
| `setup-coverage` | Set up test coverage reporting and upload to Codacy |

## Keeping this project up to date

When making changes:
1. Update `SPECS/todo.md` — move completed tasks to the DONE section
2. Update `README.md` if skills are added, removed, or renamed
3. Bump `version` in the skill's YAML frontmatter metadata when its instructions change
4. If the Codacy CLI adds new commands, update `skills/codacy-cli/SKILL.md` and any affected skills

## Codacy CLI basics

- Install: `npm install -g @codacy/codacy-cloud-cli`
- Auth: `export CODACY_API_TOKEN=<token>` (from Codacy > My Account > Access Management)
- Help: `codacy --help`, `codacy <command> --help`
- Output formats: `--output table` (default) or `--output json`
- Provider values: `gh` (GitHub), `gl` (GitLab), `bb` (Bitbucket)
