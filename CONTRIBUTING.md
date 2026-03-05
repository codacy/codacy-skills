# Contributing

Contributions are welcome! This project follows the [Codacy Code of Conduct](CODE_OF_CONDUCT.md).

## Adding or improving a skill

1. Fork the repository
2. Create a branch: `git checkout -b my-skill-name`
3. Follow the [skill structure](#skill-structure) guidelines below
4. Test your skill (see [Testing](#testing))
5. Open a pull request

## Skill structure

Each skill lives in its own folder at the root of the repository:

```
skill-name/
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

## Testing

Before submitting:
- Test that the skill triggers on obvious and paraphrased requests
- Test that it does **not** trigger on unrelated topics
- Run through the workflow end-to-end at least once
- Check for consistent output across multiple runs

## Updating existing skills

When the Codacy CLI adds new commands or changes behavior, update the affected skill(s) and bump the `version` in the frontmatter metadata.
