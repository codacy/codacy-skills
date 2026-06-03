# JSON Output Format

When using `--output-format json`, the CLI outputs the full `AnalysisResult` object as pretty-printed JSON.

## Top-level structure

```json
{
  "metadata": { ... },
  "capability": { ... },
  "issues": [ ... ],
  "errors": [ ... ],
  "toolResults": [ ... ]
}
```

## metadata

Execution metadata for the analysis run.

| Field | Type | Description |
|-------|------|-------------|
| `startedAt` | string | ISO 8601 timestamp |
| `completedAt` | string | ISO 8601 timestamp |
| `durationMs` | number | Total duration in milliseconds |
| `repositoryRoot` | string | Absolute path to the analyzed repository |
| `executionMode` | string | `"standard"`, `"strict"`, `"auto-install"`, or `"inspect"` |

## capability

Tool availability report. Always present, even in non-inspect runs.

### capability.ready[]

Tools that were available and ran (or could run in inspect mode).

| Field | Type | Description |
|-------|------|-------------|
| `toolId` | string | Tool identifier (e.g., `"Ruff"`, `"ESLint9"`) |
| `displayName` | string? | Human-readable name |
| `version` | string | Detected tool version |
| `installation` | string | `"bundled"`, `"global"`, or `"codacy"` |
| `configSource` | string? | `"local"` (native config file) or `"codacy"` (Codacy patterns) |
| `configPath` | string? | Path to native config file, when configSource is `"local"` |
| `filesRouted` | number? | Number of files routed to this tool |
| `dependencies` | array? | Resolved prerequisite statuses (`name`, `version`, `installation`) |
| `runner` | string | `"local"` or `"container"` |

### capability.unavailable[]

Tools that could not run.

| Field | Type | Description |
|-------|------|-------------|
| `toolId` | string | Tool identifier |
| `displayName` | string? | Human-readable name |
| `reason` | string | Why the tool is unavailable |
| `remediation` | string? | How to fix (e.g., install command) |
| `availableVia` | string? | `"cloud"`, `"container"`, or `"manual-install"` |

## issues[]

Array of issues found during analysis.

| Field | Type | Description |
|-------|------|-------------|
| `filePath` | string | Relative path from repository root |
| `patternId` | string | Rule identifier (e.g., `"Ruff_E501"`) |
| `toolId` | string | Which tool found this issue |
| `line` | number | 1-based start line |
| `column` | number | 1-based start column |
| `endLine` | number? | 1-based end line (if range) |
| `endColumn` | number? | 1-based end column (if range) |
| `message` | string | Human-readable description |
| `lineContent` | string | Source code on the issue's line |
| `multilineContent` | string[]? | All source lines for multiline issues |
| `category` | string | Issue classification (see below) |
| `severity` | string | Issue severity (see below) |
| `suggestion` | string? | Suggested fix, if the tool provides one |
| `confidence` | number? | 1 = low, 2 = medium, 3 = high |

### Severity values

See [glossary.md](../../../references/glossary.md#severity) for full severity definitions. The JSON field values map as follows:

| Value | UI equivalent | Description |
|-------|---------------|-------------|
| `"Error"` | Critical | Must fix |
| `"High"` | High | Should fix |
| `"Warning"` | Medium | Consider fixing |
| `"Info"` | Minor | Informational |

### Category values

See [glossary.md](../../../references/glossary.md#issue) for full category definitions.

`"Security"`, `"ErrorProne"`, `"CodeStyle"`, `"Compatibility"`, `"Performance"`, `"UnusedCode"`, `"Complexity"`, `"BestPractice"`, `"Documentation"`

## errors[]

Pipeline errors (not code issues — tool crashes, parse failures, etc.).

| Field | Type | Description |
|-------|------|-------------|
| `toolId` | string | Which tool failed |
| `phase` | string | `"requirementCheck"`, `"requirementInstall"`, `"toolInstall"`, `"toolConfig"`, `"toolInvoke"`, `"outputParse"` |
| `kind` | string | Machine-readable error kind (e.g., `"MalformedOutput"`, `"NonZeroExit"`) |
| `message` | string | Error description |
| `level` | string | `"info"`, `"warning"`, or `"error"` |
| `filePath` | string? | File where the error occurred, if applicable |

## toolResults[]

Per-tool execution summary.

| Field | Type | Description |
|-------|------|-------------|
| `toolId` | string | Tool identifier |
| `status` | string | `"success"`, `"partial"`, `"failed"`, or `"skipped"` |
| `issueCount` | number | Issues found by this tool |
| `errorCount` | number | Errors from this tool |
| `durationMs` | number | Execution time in milliseconds |
| `filesAnalyzed` | number | Files this tool processed |

## Example: parsing results for agentic workflows

Filter critical and high-severity issues:
```bash
codacy-analysis analyze --output-format json | jq '.issues | map(select(.severity == "Error" or .severity == "High"))'
```

Get per-tool summary:
```bash
codacy-analysis analyze --output-format json | jq '.toolResults'
```

List unavailable tools with remediation:
```bash
codacy-analysis analyze --inspect --output-format json | jq '.capability.unavailable[] | {toolId, reason, remediation}'
```
