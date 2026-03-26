# Codacy Skills for Claude

A collection of [Claude skills](https://www.anthropic.com/news/introducing-agent-skills) that teach Claude how to use the [Codacy CLI](https://github.com/codacy/codacy-cloud-cli) to improve code quality workflows.

## Skills

| Skill | Description |
|-------|-------------|
| [`codacy-cli`](codacy-cli/) | Use the Codacy CLI to query issues, findings, pull requests, tools, and patterns |
| [`codacy-code-review`](codacy-code-review/) | Enrich code reviews with Codacy data — issues, coverage, security, duplication |
| [`configure-codacy`](configure-codacy/) | Tailor Codacy configuration to your project and reduce noise |
| [`setup-coverage`](setup-coverage/) | Set up test coverage reporting and upload to Codacy |
| [`analysis-cli`](analysis-cli/) | Run local static analysis using the Codacy Analysis CLI |

## Requirements

- [Codacy CLI](https://github.com/codacy/codacy-cloud-cli) installed (`npm install -g @codacy/codacy-cloud-cli`)
- `CODACY_API_TOKEN` environment variable set (obtain from Codacy > My Account > Access Management > Account API Tokens)

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

1. Download the skill folder you want (e.g. `codacy-cli/`)
2. Zip it
3. Go to Claude.ai > Settings > Capabilities > Skills > Upload skill

## Working locally

To test changes without installing, load the plugin directly with the `--plugin-dir` flag:

```sh
claude --plugin-dir ./codacy-skills
```

Or if you're already inside the repo directory:

```sh
claude --plugin-dir .
```

Skills are available as namespaced commands inside that session:

```
/codacy-skills:codacy-cli
/codacy-skills:codacy-code-review
/codacy-skills:configure-codacy
```

Restart the Claude session to pick up any edits to `SKILL.md` files.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).
