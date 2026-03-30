# Contributing

Contributions are welcome! This project follows the [Codacy Code of Conduct](CODE_OF_CONDUCT.md).

## Adding or improving a skill

1. Fork the repository
2. Create a branch: `git checkout -b my-skill-name`
3. Follow the [skill structure](#skill-structure) guidelines below
4. Test your skill (see [Testing locally](#testing-locally))
5. Open a pull request

## Skill structure

Each skill lives in its own folder under `skills/`:

```
skills/skill-name/
├── SKILL.md          # Required — instructions with YAML frontmatter
├── references/       # Optional — detailed docs loaded on demand
└── assets/           # Optional — templates or other static files
```

Rules:
- Folder name and `name` field must be `kebab-case` (lowercase, hyphens, no spaces)
- `SKILL.md` is case-sensitive — no variations accepted
- No `README.md` inside the skill folder
- The `description` field must explain **what** the skill does and **when** to use it, written in third person, under 1024 characters
- No XML angle brackets (`< >`) anywhere in the frontmatter

## Writing instructions

- Be concise — only add context Claude doesn't already have
- Keep SKILL.md under 500 lines; move detailed content to `references/`
- Use numbered steps for ordered workflows
- Include concrete examples, not abstract descriptions
- Add a troubleshooting section for common errors

## Testing locally

Use `--plugin-dir` to load your local copy instead of the marketplace version:

```sh
# from the repo root
claude --plugin-dir .
```

This tells Claude Code to use your local skill files directly, bypassing any installed marketplace version. After editing a `SKILL.md`, run `/reload-plugins` inside the session to pick up the changes without restarting.

If you also have the marketplace plugin installed, uninstall it first to avoid confusion:

```sh
claude plugin uninstall codacy-skills@codacy
```

### What to check

- The skill triggers on obvious and paraphrased requests
- The skill does **not** trigger on unrelated topics
- The workflow runs end-to-end at least once
- Output is consistent across multiple runs

## Updating existing skills

When the Codacy CLI adds new commands or changes behavior, update the affected skill(s) and bump the `version` in the frontmatter metadata.
