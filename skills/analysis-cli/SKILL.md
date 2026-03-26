---
name: analysis-cli
description: Uses the Codacy Analysis CLI to run local static analysis on repositories or specific files. Handles installation, initialization, dependency management, dry-runs, and analysis with JSON output. Use when the user asks to analyze code locally, run static analysis, check for issues, scan for security problems, or set up local Codacy analysis.
license: MIT
metadata:
  author: Codacy
  version: 1.0.0
---

# Codacy Analysis CLI

The Codacy Analysis CLI (`codacy-analysis`) runs static analysis locally on a repository. It detects languages, selects tools, and reports issues — without pushing code to Codacy. This is a different tool from the Codacy Cloud CLI (`codacy`), which queries remote Codacy data.

Always use `--output-format json` for structured output in agentic workflows.

## Setup

```bash
# Install
npm i -g @codacy/analysis-cli

# Verify
codacy-analysis --help
```

### Authentication (optional)

Authentication is only required for `init --remote` (fetching config from a Codacy repository). Local analysis works without authentication.

```bash
# Option 1: Interactive login
codacy-analysis login

# Option 2: Token flag
codacy-analysis login --token <your-api-token>

# Option 3: Environment variable
export CODACY_API_TOKEN=<your-api-token>

# Obtain tokens: Codacy > My Account > Access Management
# Remove credentials
codacy-analysis logout
```

**Shared session:** The Analysis CLI and the Cloud CLI (`codacy`) share the same credentials at `~/.codacy/credentials`. Logging in or out with either CLI applies to both — there is no need to authenticate separately.

## Getting help

```bash
codacy-analysis --help
codacy-analysis <command> --help
# e.g. codacy-analysis analyze --help
```

## Filesystem conventions

The CLI uses two managed locations:

| Location | Scope | Contents |
|----------|-------|----------|
| `.codacy/` (in repo root) | Per-project | `codacy.config.json`, `generated/` (tool configs), `.gitignore` (auto-created) |
| `~/.codacy/` (home dir) | Machine-wide | Runtimes, tool binaries, caches, logs, credentials |

The analyzed repository is **never modified outside of `.codacy/`**. The `.codacy/.gitignore` is auto-created to exclude `generated/`, logs, and other transient files.

### Key files

- `.codacy/codacy.config.json` — Main configuration: tools, patterns, excludes, metadata
- `.codacy/generated/<ToolId>/` — Materialized tool-specific configs (gitignored)
- `~/.codacy/credentials` — Stored API token
- `~/.codacy/logs/` — Structured logs (JSON lines, rotated at 10 MB)

## Provider values

Used with `init --remote`:

| Value | Provider |
|-------|----------|
| `gh` | GitHub |
| `gl` | GitLab |
| `bb` | Bitbucket |
| `ghe` | GitHub Enterprise |
| `gle` | GitLab Enterprise |
| `bbe` | Bitbucket Enterprise |

## Analysis workflow

```
Analysis Progress:
- [ ] Step 1: Initialize configuration
- [ ] Step 2: Inspect tool availability (dry-run)
- [ ] Step 3: Install missing dependencies
- [ ] Step 4: Run analysis
- [ ] Step 5: Interpret results
```

### Step 1: Initialize configuration

Choose the init mode based on the repository's situation:

**Repository is in Codacy and you want its exact config:**
```bash
# Requires authentication (login or CODACY_API_TOKEN)
codacy-analysis init --remote <provider> <org> <repo>
# e.g. codacy-analysis init --remote gh my-org my-repo
```

**Repository is in Codacy but you just want sensible defaults:**
```bash
# No token needed — uses the public Codacy API for default patterns
codacy-analysis init --default
```

**Repository is not in Codacy (local-only analysis):**
```bash
# Detects languages and tools based on local files and config
codacy-analysis init
```

**A specific directory (not the current one):**
```bash
codacy-analysis init /path/to/repo
```

All modes create `.codacy/codacy.config.json` in the repo root. If a `.codacy.yaml` (or `.codacy.yml`) exists, its `exclude_paths` are automatically merged into the config.

#### Updating an existing configuration

When the config already exists and you want to refresh it (e.g., after adding new languages or files):

```bash
codacy-analysis update-config
```

This re-runs the same init mode that was originally used (stored in `metadata.source`). For remote configs, it re-fetches from the same Codacy repository.

### Step 2: Inspect tool availability (dry-run)

Before running analysis, check which tools are available and which are missing:

```bash
codacy-analysis analyze --inspect --output-format json
```

This produces a capability report without running any analysis. Parse the JSON output:

```bash
# See which tools are ready
codacy-analysis analyze --inspect --output-format json | jq '.capability.ready[] | {toolId, version, installation}'

# See which tools are missing and how to fix them
codacy-analysis analyze --inspect --output-format json | jq '.capability.unavailable[] | {toolId, reason, remediation}'
```

**Decision point:**
- If all needed tools are in `capability.ready` → skip to Step 4
- If tools are in `capability.unavailable` → proceed to Step 3

### Step 3: Install missing dependencies

**Preferred: use `--install-dependencies`** — installs tools into the `.codacy/` / `~/.codacy/` scope without affecting the rest of the machine:

```bash
codacy-analysis analyze --install-dependencies --output-format json
```

This installs missing tools and then runs analysis in a single command. The installed binaries go to `~/.codacy/` (machine-scoped, reused across repositories).

**Dry-run install check** — combine `--inspect` with `--install-dependencies` to install without running analysis:

```bash
codacy-analysis analyze --inspect --install-dependencies --output-format json
```

**Last resort: manual installation** — if `--install-dependencies` fails for a specific tool, install it manually on the machine (e.g., `brew install shellcheck`, `pip install ruff`). See [references/supported-tools.md](references/supported-tools.md) for tool details.

### Step 4: Run analysis

Always use `--output-format json` for agentic workflows.

#### Analyze the entire repository

```bash
codacy-analysis analyze --output-format json
```

#### Analyze specific files or paths

```bash
# Single file (positional argument)
codacy-analysis analyze ./src/main.py --output-format json

# Multiple files by path or glob (--files flag)
codacy-analysis analyze --files src/a.py src/b.py --output-format json

# Glob pattern (always quote to prevent shell expansion)
codacy-analysis analyze --files "src/**/*.ts" --output-format json

# Subdirectory
codacy-analysis analyze ./src/api/ --output-format json
```

#### Restrict to specific tools

Tool IDs are **case-sensitive**. See [references/supported-tools.md](references/supported-tools.md) for the full list.

```bash
# Single tool
codacy-analysis analyze --tool Ruff --output-format json

# Multiple tools
codacy-analysis analyze --tool Ruff --tool Bandit --output-format json

# Combine with file targeting
codacy-analysis analyze --tool ESLint9 --files "src/**/*.ts" --output-format json
```

#### Performance tuning

```bash
# Run up to 4 tools in parallel
codacy-analysis analyze --parallel-tools 4 --output-format json

# Increase timeout for slow tools (default: 300000ms = 5 min)
codacy-analysis analyze --tool-timeout 600000 --output-format json
```

#### Strict mode

Fail immediately if any configured tool is unavailable (instead of skipping it):

```bash
codacy-analysis analyze --fail-if-missing --output-format json
```

#### Save output to file

```bash
codacy-analysis analyze --output-format json --output results.json
```

#### Debugging

```bash
# Verbose logging to stderr
codacy-analysis analyze --log-level debug --output-format json

# Disable log file writing (e.g., in CI)
codacy-analysis analyze --no-log --output-format json
```

### Step 5: Interpret results

The JSON output contains the full `AnalysisResult`. See [references/output-format.md](references/output-format.md) for the complete schema.

**Quick reference for parsing:**

```bash
# Count issues by severity
codacy-analysis analyze --output-format json | jq '.issues | group_by(.severity) | map({severity: .[0].severity, count: length})'

# Get critical/high issues only
codacy-analysis analyze --output-format json | jq '[.issues[] | select(.severity == "Error" or .severity == "High")]'

# Issues grouped by file
codacy-analysis analyze --output-format json | jq '.issues | group_by(.filePath) | map({file: .[0].filePath, count: length})'

# Check for tool errors
codacy-analysis analyze --output-format json | jq '.errors'

# Per-tool summary
codacy-analysis analyze --output-format json | jq '.toolResults | map({toolId, status, issueCount, durationMs})'
```

**Exit codes:**
- `0` — Success, no issues found
- `1` — Issues found
- `2` — Execution error (tool crash, missing dependency, etc.)

## Common workflows

### Quick scan of a repository not in Codacy

```bash
codacy-analysis init
codacy-analysis analyze --install-dependencies --output-format json
```

### Scan only changed files (e.g., before a commit)

```bash
# Get changed files from git, pass them to --files
codacy-analysis analyze --files $(git diff --name-only HEAD) --output-format json
```

### Reproduce Codacy remote analysis locally

```bash
codacy-analysis login --token <token>
codacy-analysis init --remote gh my-org my-repo
codacy-analysis analyze --install-dependencies --output-format json
```

### Check a single file for issues

```bash
codacy-analysis analyze ./src/main.py --output-format json
```

### Re-scan after configuration changes

```bash
codacy-analysis update-config
codacy-analysis analyze --output-format json
```

### Run only security-focused tools

```bash
codacy-analysis analyze --tool Bandit --tool Trivy --tool Semgrep --tool Checkov --output-format json
```

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| `Tool X not found` / tool in `unavailable` | Tool binary not installed | Run with `--install-dependencies`; if that fails, install the tool manually |
| Analysis produces no results | No tools enabled or no matching files | Re-run `codacy-analysis init` or check `.codacy/codacy.config.json` has tools configured |
| Wrong tools detected | Language detection missed files | Use `--tool <id>` to force specific tools |
| Tool timeout | Analysis takes too long on large codebase | Increase `--tool-timeout <ms>` (default 300000) |
| Config outdated after adding new languages | Init was run before new files existed | Run `codacy-analysis update-config` |
| `Config already exists` on init | `.codacy/codacy.config.json` already present | Use `update-config` instead, or delete `.codacy/codacy.config.json` first |
| Remote init fails with auth error | Missing or invalid API token | Run `codacy-analysis login` or set `CODACY_API_TOKEN` |
| Permission errors on `~/.codacy/` | Directory ownership mismatch | Check permissions: `ls -la ~/.codacy/` |
| Inspect shows tool as `bundled` but it fails | Bundled library tool has dependency issue | Check `--log-level debug` output; may need `npm rebuild` |
| Different results than Codacy Cloud | Different tool versions or pattern config | Use `init --remote` to sync config; check tool versions in inspect output |

### Reading logs

Logs are written to `~/.codacy/logs/` in JSON lines format:

```bash
# View latest log
cat ~/.codacy/logs/*.log | jq .

# Filter for errors
cat ~/.codacy/logs/*.log | jq 'select(.level == "error")'
```

Use `--log-level debug` for the most verbose output when troubleshooting tool issues.
