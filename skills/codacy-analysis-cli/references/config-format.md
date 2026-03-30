# Configuration File Format

The file `.codacy/codacy.config.json` controls which tools run, which patterns are enabled, and what files are excluded.

## Top-level structure

```json
{
  "version": 1,
  "metadata": { ... },
  "tools": [ ... ],
  "exclude": [ ... ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `version` | number | Always `1` |
| `metadata` | object | How and when the config was generated (see below) |
| `tools` | array | Per-tool configuration — patterns, excludes, local config (see below) |
| `exclude` | string[] | Global file exclusion globs (e.g., `"docs/**"`, `"CHANGELOG.md"`) |

## metadata

Describes how the config was initialized. Avoid editing this manually.

| Field | Type | Description |
|-------|------|-------------|
| `source` | string | `"local"`, `"default"`, or `"remote"` — the init mode used |
| `provider` | string? | Provider slug (e.g., `"gh"`). Present when source is `"remote"` |
| `organization` | string? | Org name. Present when source is `"remote"` |
| `repositoryName` | string? | Repo name |
| `languages` | string[] | Detected languages |
| `createdAt` | string | ISO 8601 timestamp |
| `updatedAt` | string | ISO 8601 timestamp |

## tools[]

Each entry configures one tool.

```json
{
  "toolId": "Ruff",
  "patterns": [
    { "patternId": "Ruff_E501", "parameters": { "max-line-length": "120" } },
    { "patternId": "Ruff_F401" }
  ],
  "exclude": ["tests/fixtures/**"],
  "useLocalConfigurationFile": false,
  "localConfigurationFile": ".ruff.toml"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `toolId` | string | Tool identifier (case-sensitive, e.g., `"Ruff"`, `"ESLint9"`, `"Semgrep"`) |
| `patterns` | array | Which patterns (rules) are enabled. Only listed patterns run — removing a pattern disables it |
| `exclude` | string[] | Per-tool file exclusion globs |
| `useLocalConfigurationFile` | boolean | When `true`, the tool uses its native config file (e.g., `.eslintrc`) instead of the patterns listed here |
| `localConfigurationFile` | string? | Path to the native config file in the repo |

### patterns[]

Each entry enables one pattern (rule). Only patterns listed in this array are active — to disable a pattern, remove it from the array.

| Field | Type | Description |
|-------|------|-------------|
| `patternId` | string | Pattern identifier (e.g., `"Ruff_E501"`, `"Semgrep_javascript.lang.security.audit.xss"`) |
| `parameters` | object? | Parameter overrides as key-value string pairs (e.g., `{ "max-line-length": "120" }`) |

## Examples

### Exclude files globally

```json
{
  "exclude": ["CHANGELOG.md", "docs/**", "**/*.generated.ts"]
}
```

### Exclude files for a specific tool

```json
{
  "toolId": "markdownlint",
  "patterns": [ ... ],
  "exclude": ["CHANGELOG.md", "docs/api/**"]
}
```

### Tune a pattern's parameters

```json
{
  "patternId": "Lizard_CCN",
  "parameters": { "threshold": "15" }
}
```

### Use the project's native config instead of Codacy patterns

```json
{
  "toolId": "ESLint9",
  "useLocalConfigurationFile": true,
  "localConfigurationFile": "eslint.config.js",
  "patterns": []
}
```

When `useLocalConfigurationFile` is `true`, the `patterns` array is ignored — the tool runs with its own config file.

### Disable a tool

Remove the tool entry from the `tools` array entirely. There is no `enabled: false` flag.

### Disable a pattern

Remove the pattern entry from the tool's `patterns` array. There is no `enabled: false` flag.
