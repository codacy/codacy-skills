# Supported Tools

The Codacy Analysis CLI ships with the following tool adapters. Use the **Tool ID** (case-sensitive) with the `--tool` flag.

| Tool ID | Display Name | Languages | Strategy |
|---------|-------------|-----------|----------|
| `jackson` | Jackson | JSON | Native |
| `markdownlint` | markdownlint | Markdown | Library |
| `shellcheck` | ShellCheck | Shell | CLI |
| `Hadolint` | Hadolint | Dockerfile | CLI |
| `Ruff` | Ruff | Python | CLI |
| `cppcheck` | Cppcheck | C, C++ | CLI |
| `Trivy` | Trivy | Multi-language | CLI |
| `Semgrep` | Opengrep | 30+ languages | CLI |
| `Stylelint` | Stylelint | CSS, SCSS, Less | Library |
| `spectral` | Spectral | OpenAPI, AsyncAPI | Library |
| `ESLint9` | ESLint 9 | JS, TS, JSX, TSX, Vue | Library |
| `flawfinder` | Flawfinder | C, C++ | CLI |
| `Bandit` | Bandit | Python | CLI |
| `PyLintPython3` | Pylint | Python | CLI |
| `Checkov` | Checkov | Terraform, CloudFormation, K8s, Docker | CLI |
| `Lizard` | Lizard | 30+ languages | CLI |
| `Checkstyle` | Checkstyle | Java | CLI |
| `PMD7` | PMD 7 | Java, Apex, Visualforce | CLI |
| `detekt` | detekt | Kotlin | CLI |

## Tool IDs are case-sensitive

Use the exact ID from the table above. Examples:

```bash
# Correct
codacy-analysis analyze --tool Ruff --output-format json
codacy-analysis analyze --tool ESLint9 --output-format json
codacy-analysis analyze --tool PyLintPython3 --output-format json

# Wrong — these will not match
codacy-analysis analyze --tool ruff
codacy-analysis analyze --tool eslint9
codacy-analysis analyze --tool pylint
```

## Restricting to specific tools

Use `--tool` (repeatable) to run only specific tools:

```bash
# Single tool
codacy-analysis analyze --tool Ruff --output-format json

# Multiple tools
codacy-analysis analyze --tool Ruff --tool Bandit --output-format json

# Combine with file targeting
codacy-analysis analyze --tool ESLint9 --files "src/**/*.ts" --output-format json
```

When `--tool` is not specified, the CLI runs all tools that match the detected languages.

## Execution strategies

- **Native** — Pure TypeScript analysis, no external binary needed (e.g., Jackson)
- **Library** — Calls a Node.js API directly, bundled with the CLI (e.g., ESLint 9, markdownlint)
- **CLI** — Spawns an external binary; may need installation via `--install-dependencies` (e.g., Ruff, ShellCheck)

Library and Native tools are always available. CLI tools may require installation.
