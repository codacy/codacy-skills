# Codacy Skills

A collection of skills that teach your AI coding assistant how to use the [Codacy CLI](https://github.com/codacy/codacy-cloud-cli) to improve code quality workflows.

Compatible with Claude Code, OpenAI Codex, GitHub Copilot, Gemini CLI, and any agent that supports the [Agent Skills](https://agentskills.io/) standard.

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

Claude Code pulls updates automatically whenever you run `claude plugin update`. No manual steps needed to stay on the latest version.

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

### OpenAI Codex

Codex discovers skills from `.agents/skills/` directories following the [Agent Skills](https://agentskills.io/) standard. The `SKILL.md` files in this repository are fully compatible.

Clone the repo and symlink the skills directory into your project or home directory:

```sh
git clone https://github.com/codacy/codacy-skills ~/.codacy-skills

# Per-project (recommended)
mkdir -p .agents/skills
ln -s ~/.codacy-skills/skills/codacy-cloud-cli .agents/skills/codacy-cloud-cli
ln -s ~/.codacy-skills/skills/codacy-code-review .agents/skills/codacy-code-review

# Or install all skills globally
mkdir -p ~/.agents/skills
ln -s ~/.codacy-skills/skills/* ~/.agents/skills/
```

To get updates, pull the latest changes:

```sh
git -C ~/.codacy-skills pull
```

If your Codex setup uses an `AGENTS.md` fallback instead of `.agents/skills/`, copy or symlink [`agents/AGENTS.md`](agents/AGENTS.md) to your repo root:

```sh
cp ~/.codacy-skills/agents/AGENTS.md ./AGENTS.md
# or
ln -s ~/.codacy-skills/agents/AGENTS.md ./AGENTS.md
```

### GitHub Copilot

GitHub Copilot coding agent reads `AGENTS.md` from your repository root. Copy the pre-built bundle into your project:

```sh
curl -o AGENTS.md https://raw.githubusercontent.com/codacy/codacy-skills/master/agents/AGENTS.md
```

Or add it via a symlink if you've cloned the repo locally:

```sh
git clone https://github.com/codacy/codacy-skills ~/.codacy-skills
ln -s ~/.codacy-skills/agents/AGENTS.md ./AGENTS.md
```

To pull in updates later:

```sh
git -C ~/.codacy-skills pull
# then re-copy or re-symlink AGENTS.md if needed
```

Alternatively, paste the skill instructions into your project's `.github/copilot-instructions.md` to give Copilot persistent context across all sessions.

### Gemini CLI

This repository includes `gemini-extension.json` for Gemini CLI integration.

Install from the GitHub URL:

```sh
gemini extensions install https://github.com/codacy/codacy-skills.git --consent
```

Or from a local clone:

```sh
git clone https://github.com/codacy/codacy-skills
gemini extensions install ./codacy-skills --consent
```

See the [Gemini CLI extensions docs](https://geminicli.com/docs/extensions/#installing-an-extension) for more help.

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

After editing skills, regenerate the Codex/Copilot bundle to keep it in sync:

```sh
python scripts/generate_agents.py
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for more on testing and submitting changes.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).
