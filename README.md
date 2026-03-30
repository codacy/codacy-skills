# Codacy Skills for Claude

A collection of [Claude skills](https://www.anthropic.com/news/introducing-agent-skills) that teach Claude how to use the [Codacy CLI](https://github.com/codacy/codacy-cloud-cli) to improve code quality workflows.

## Skills

| Skill | Description |
|-------|-------------|
| [`codacy-cloud-cli`](skills/codacy-cloud-cli/SKILL.md) | Use the Codacy Cloud CLI to query issues, findings, pull requests, tools, and patterns |
| [`codacy-code-review`](skills/codacy-code-review/SKILL.md) | Enrich code reviews with Codacy data — issues, coverage, security, duplication |
| [`configure-codacy`](skills/configure-codacy/SKILL.md) | Tailor Codacy configuration to your project and reduce noise |
| [`setup-coverage`](skills/setup-coverage/SKILL.md) | Set up test coverage reporting and upload to Codacy |
| [`codacy-analysis-cli`](skills/codacy-analysis-cli/SKILL.md) | Run local static analysis using the Codacy Analysis CLI |

## Requirements

- [Codacy CLI](https://github.com/codacy/codacy-cloud-cli) installed (`npm install -g @codacy/codacy-cloud-cli`)
- [Codacy Analysis CLI](https://www.npmjs.com/package/@codacy/analysis-cli) installed (`npm install -g @codacy/analysis-cli`)
- `CODACY_API_TOKEN` environment variable set (obtain from Codacy > My Account > Access Management > Account API Tokens) or use the `codacy login` command (interactive login)

## Installation

### Claude Code (recommended)

Install all Codacy skills in one step via the plugin marketplace:

```sh
claude plugin marketplace add codacy/codacy-skills
claude plugin install codacy-skills@codacy
```

Or install from a local clone:

```sh
git clone https://github.com/codacy/codacy-skills
claude plugin marketplace add ./codacy-skills
claude plugin install codacy-skills@codacy
```

### Claude.ai

1. Download the skill folder you want (e.g. `codacy-cloud-cli/`)
2. Zip it
3. Go to Claude.ai > Settings > Capabilities > Skills > Upload skill

## Local development

If you installed the plugin from the marketplace, Claude Code will use the published version — not your local edits. To test local changes, use `--plugin-dir` to load the plugin directly from your working copy:

```sh
# from the repo directory
claude --plugin-dir .

# or from anywhere, using the path
claude --plugin-dir /path/to/codacy-skills
```

This bypasses the marketplace entirely. Your local `SKILL.md` files are what Claude sees.

### Development workflow

1. Start Claude Code with `--plugin-dir` as above
2. Edit your skill files under `skills/`
3. Run `/reload-plugins` inside the session to pick up changes (no restart needed)
4. Test your skills

### Avoiding conflicts with the marketplace version

If you have the marketplace plugin installed and want to be sure you're always hitting local code, uninstall the marketplace copy:

```sh
claude plugin uninstall codacy-skills@codacy
```

Reinstall it when you're done developing:

```sh
claude plugin install codacy-skills@codacy
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for more on testing and submitting changes.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).
