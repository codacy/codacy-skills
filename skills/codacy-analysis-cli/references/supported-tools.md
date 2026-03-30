# Supported Tools

The Codacy Analysis CLI ships with the following tool adapters. Use the **Tool ID** (case-sensitive) with the `--tool` flag.

| Tool ID | Display Name | Languages |
|---------|-------------|-----------|
| `jackson` | Jackson | JSON |
| `markdownlint` | markdownlint | Markdown |
| `shellcheck` | ShellCheck | Shell |
| `Hadolint` | Hadolint | Dockerfile |
| `Ruff` | Ruff | Python |
| `cppcheck` | Cppcheck | C, C++ |
| `Trivy` | Trivy | Multi-language |
| `Semgrep` | Opengrep | 30+ languages |
| `Stylelint` | Stylelint | CSS, SCSS, Less |
| `spectral` | Spectral | OpenAPI, AsyncAPI |
| `ESLint9` | ESLint 9 | JS, TS, JSX, TSX, Vue |
| `flawfinder` | Flawfinder | C, C++ |
| `Bandit` | Bandit | Python |
| `PyLintPython3` | Pylint | Python |
| `Checkov` | Checkov | Terraform, CloudFormation, K8s, Docker |
| `Lizard` | Lizard | 30+ languages |
| `Checkstyle` | Checkstyle | Java |
| `PMD7` | PMD 7 | Java, Apex, Visualforce |
| `detekt` | detekt | Kotlin |
| `RuboCop` | RuboCop | Ruby |
| `Reek` | Reek | Ruby |
| `Brakeman` | Brakeman | Ruby |


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
