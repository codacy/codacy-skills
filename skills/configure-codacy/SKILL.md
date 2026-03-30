---
name: configure-codacy
description: Tailors Codacy configuration to a project by suggesting tools and patterns aligned with the codebase, and reduces noise by identifying and disabling rules that produce too many false positives or mismatched results. Use whenever the user wants to configure Codacy, reduce noise, fix false positives, enable or disable tools or patterns, tune code quality rules, deal with too many warnings, or align Codacy with their project's conventions. Also trigger when the user complains about irrelevant issues, noisy linters, or wants to set up Codacy for the first time on a repo.
license: MIT
metadata:
  author: Codacy
  version: 1.4.0
---

# Configure Codacy

This skill helps tailor Codacy configuration to a project's actual coding conventions, reducing noise and improving the signal-to-noise ratio of code reviews.

## Prerequisites

- **Codacy Analysis CLI** (`codacy-analysis`) — for testing configuration changes locally before applying them. See `codacy-analysis-cli` for setup.
- **Codacy Cloud CLI** (`codacy`) — for querying current Cloud config, importing local config, and managing tools/patterns remotely. See `codacy-cloud-cli` for setup.

Both CLIs share credentials at `~/.codacy/credentials`, so a single login covers both.

## How configuration works

There are two approaches to configuring Codacy, and this skill uses both:

| Approach | How it works | Speed |
|----------|-------------|-------|
| **Local-first** (preferred) | Edit `.codacy/codacy.config.json` locally, test with the Analysis CLI, then import to Cloud | Instant feedback — no push or reanalysis needed |
| **Cloud-direct** | Change tools/patterns via the Cloud CLI, trigger reanalysis, wait for results | Minutes — requires reanalysis after each change |

**Prefer the local-first approach** because it gives instant feedback: you can tweak the config, run analysis, see the results, and iterate — all without waiting for remote reanalysis. Once the configuration looks good locally, import it to Codacy Cloud in one step.

Fall back to the cloud-direct approach when:
- The tool or pattern you need is not supported by the Analysis CLI (check with `codacy-analysis analyze --inspect`)
- You need to manage organization-level Coding Standards
- The user specifically wants to configure Cloud without local testing

**Organization standards take precedence.** If a pattern is enforced by a Coding Standard at the organization level, it cannot be changed at the repository level. The import will succeed but the organization standard will override the local config for those patterns.

## Tailored configuration workflow

The key principle: **run first, tune second**. Don't try to configure perfectly upfront. Initialize with good defaults, run analysis, then use the issue distribution to decide what to adjust. The data tells you exactly what to disable or tune.

```
Configuration Progress:
- [ ] Step 1: Analyse the repository
- [ ] Step 2: Initialize local configuration
- [ ] Step 3: Run baseline analysis
- [ ] Step 4: Tune tools and patterns based on results
- [ ] Step 5: Import configuration to Codacy Cloud
- [ ] Step 6: Verify changes on Cloud
```

### Step 1: Analyse the repository

Traverse the repository to identify:
- Languages and frameworks in use
- Build tools, package managers, test frameworks
- Coding conventions (naming, formatting, patterns found in the code)
- Existing linter/static analysis configuration files (`.eslintrc`, `pylintrc`, `semgrep.yml`, etc.)
- Security-sensitive areas (auth, payment, data handling)

Also check whether the repo is already on Codacy Cloud:
```bash
codacy repository <provider> <org> <repo>
```

### Step 2: Initialize local configuration

**If the repo is on Codacy** — pull its existing config so you start from what's already configured:
```bash
codacy-analysis init --remote <provider> <org> <repo>
```

**If the repo is not on Codacy** — use `--default` to get recommended tools and patterns for the detected languages:
```bash
codacy-analysis init --default
```

Always use `--remote` or `--default` — bare `codacy-analysis init` only detects local config files (e.g., if you have an `.eslintrc` it picks up ESLint but nothing else). `--default` pulls Codacy's full recommended pattern set from the API, giving a much richer starting point with tools like Semgrep, Trivy, Lizard, markdownlint, etc.

This creates `.codacy/codacy.config.json` in the repo root. All subsequent local changes are made to this file. Read [the config format reference](../codacy-analysis-cli/references/config-format.md) for the full schema before editing — field names matter (e.g., the exclusion field is `exclude`, not `excludePaths`).

### Step 3: Run baseline analysis

Run analysis with the default config before making any changes — the results tell you what to tune:

```bash
codacy-analysis analyze --install-dependencies --output-format json
```

Then group issues by pattern to identify noise:
```bash
codacy-analysis analyze --output-format json | jq '[.issues | group_by(.patternId) | .[] | {pattern: .[0].patternId, tool: .[0].toolId, count: length}] | sort_by(-.count)'
```

This distribution is the basis for Step 4. Patterns with disproportionately high counts are candidates for disabling or tuning.

### Step 4: Tune tools and patterns based on results

Work through the results from Step 3. For each high-count pattern, decide whether to:
- **Disable it** — if it contradicts the project's conventions or is irrelevant. **NEVER disable Security patterns** — see the security rule below.
- **Tune its parameters** — if the rule is valuable but the thresholds are too strict
- **Exclude specific files** — if the pattern is valuable but fires on files where it doesn't apply (e.g., test fixtures, generated files, changelogs)
- **Keep it** — if the issues are real and the team should address them

> **⚠️ IMPORTANT: Never disable security patterns.** Patterns in the Security category (e.g., hard-coded credentials, SQL injection, XSS, dangerouslySetInnerHTML) must stay enabled even if they produce false positives. Instead, exclude specific files where appropriate, or leave the false positives for the user to triage in Codacy Cloud. Disabling a security pattern to reduce noise risks missing real vulnerabilities in future code.

Edit `.codacy/codacy.config.json` directly for all changes, then re-run analysis to verify the noise dropped:

```bash
codacy-analysis analyze --output-format json
```

If the config was initialized with `--remote`, you can run `codacy-analysis update-config` to re-sync with the remote configuration. Don't use `update-config` if you initialized with `--default` — it would overwrite your local changes with defaults.

**Iterate** this loop until the results are clean. It's fast because it's entirely local.

#### Excluding files vs disabling patterns

When a pattern is valuable but a specific file triggers false positives (e.g., a unicode-detection rule on an emoji data file), **exclude the file** rather than disabling the pattern. The pattern stays active for real source code:

```json
{
  "exclude": ["path/to/problematic-file.json"]
}
```

See **Per-tool tuning tips** below for tool-specific guidance.

Once the user is happy with the local results, proceed to import.

### Step 5: Import configuration to Codacy Cloud

Import the tested local configuration to Codacy Cloud:

```bash
codacy repository <provider> <org> <repo> --import .codacy/codacy.config.json
```

This updates the Cloud configuration to match the local config — tools, patterns, and parameters are all synced.

**For tools only available on Cloud** (not supported by the Analysis CLI), configure them directly via the Cloud CLI:
```bash
codacy tool <provider> <org> <repo> <toolName> --enable
codacy tool <provider> <org> <repo> <toolName> --disable
codacy patterns <provider> <org> <repo> <toolName> --enabled
codacy pattern <provider> <org> <repo> <toolName> <patternId> --enable
codacy pattern <provider> <org> <repo> <toolName> <patternId> --disable
codacy pattern <provider> <org> <repo> <toolName> <patternId> --parameter name=value
```

**Note:** If the CLI returns an error when importing or changing a pattern, it is likely enforced by an organization Coding Standard and cannot be changed at the repository level — inform the user.

### Step 6: Verify changes on Cloud

After importing, trigger a reanalysis so the new settings take effect on the current HEAD commit:

#### 6a. Trigger reanalysis

Record the current time (`requestedAt`) before triggering, then run:

```bash
codacy repository <provider> <org> <repo> --reanalyze
```

#### 6b. Poll for completion using a background subagent

Launch a background subagent (use the Agent tool with `model: "haiku"` and `run_in_background: true`) to poll for reanalysis completion. Provide the subagent with these instructions:

1. Wait 1 minute before the first check
2. Run: `codacy repository <provider> <org> <repo> --output json`
3. Parse the JSON and check **two conditions**:
   - `startedAnalysis` timestamp is **after** `requestedAt` (analysis actually started after our request — not stale from a previous run)
   - `endedAnalysis` timestamp is **after** `startedAnalysis` (analysis finished)
4. If either condition is not met, wait 1 minute and repeat from step 2
5. Stop after 10 attempts (~10 minutes). If not complete, return a message saying reanalysis is taking longer than expected and the user should check manually
6. When complete, run the verification commands from Step 6c and return their output

While the subagent polls, inform the user that reanalysis has been triggered and you will report back when results are ready.

#### 6c. Verify changes took effect

Once reanalysis is complete:

1. **Compare Cloud results against local results** from Step 3. They should be broadly similar for tools available locally. Differences may come from tools only available on Cloud or from organization-level overrides.

2. **Check the issue distribution:**
   ```bash
   codacy issues <provider> <org> <repo> --overview
   ```

3. **If noise reduction was the goal**, compare total issue counts before and after.

Report the before/after comparison to the user. If results are unexpected (e.g., a disabled pattern still shows issues), the pattern may be enforced by an organization Coding Standard.

## Per-tool tuning tips

### Semgrep

Semgrep defaults include patterns for every language it supports (Apex, Bash, C, Clojure, etc.). For most projects this means hundreds of irrelevant patterns. After init, **scope Semgrep patterns to the project's actual languages** — disable patterns for languages not present in the repo. This cuts noise and analysis runtime significantly.

### Lizard (complexity)

Lizard has rules for cyclomatic complexity (CCN), lines of code (NLOC), and parameter count. Each rule has three severity levels (Critical, Medium, Minor), each with its own configurable threshold.

For **established/mature codebases**, the default Medium thresholds (e.g., CCN=8, NLOC=50) tend to produce hundreds of hits on legacy code that isn't going to be refactored. Options:
- Disable Medium-level rules and keep only Critical (catches truly extreme complexity)
- Or raise the Medium thresholds to values that match the project's reality (e.g., CCN=15, NLOC=100) — this is better if you still want visibility into moderately complex code

For **greenfield projects**, the default Medium thresholds are reasonable.

### ESLint9

ESLint loads the project's own config file (e.g., `eslint.config.js`), which may import packages like `@eslint/js` or framework-specific plugins. If the project has an existing ESLint config, **install the project's dependencies first** (`npm install` or equivalent) before running analysis, or ESLint will fail with an `InvocationError`.

This only applies when the project has a pre-existing ESLint configuration file. For projects without one, the bundled ESLint defaults work out of the box.

### markdownlint

Rules like MD034 (bare URLs), MD024 (duplicate headings), MD010 (hard tabs), MD004 (list style), MD033 (inline HTML), and MD036 (emphasis as heading) fire heavily on CHANGELOG files and auto-generated docs. These are stylistic rules, not bugs. Consider either:
- Excluding changelog/generated markdown files via `exclude`
- Disabling the noisiest rules if the project doesn't follow strict markdown conventions

### Stylelint

Review the results in context — some CSS rules that look like violations may be intentional depending on the project type (e.g., apps that override third-party styles often need `!important` and qualified selectors).

## Noise reduction workflow

Use this when the user reports too many issues, false positives, or unhelpful warnings.

### Detect noisy patterns

Start by identifying the noisiest patterns. Use both local and Cloud data:

```bash
# Local: run analysis and group issues by pattern
codacy-analysis analyze --output-format json | jq '.issues | group_by(.patternId) | map({pattern: .[0].patternId, tool: .[0].toolId, count: length}) | sort_by(-.count)'

# Cloud: overview of issue counts
codacy issues <provider> <org> <repo> --overview
```

A pattern is likely noisy if:
- It accounts for a disproportionately large number of issues
- Multiple instances have been marked as false positives
- The violation contradicts conventions consistently found throughout the codebase

### Verify before disabling

Before recommending to disable a pattern:
1. Check the category — **never disable Security patterns** (exclude files or leave for Cloud triage instead)
2. Review actual instances in the code to confirm they are false positives or mismatched conventions
3. Check if the pattern could be configured (parameters adjusted) rather than disabled entirely

Only suggest disabling after verifying the pattern is consistently unhelpful for this specific codebase.

### Test locally, then import

1. Disable the noisy patterns in `.codacy/codacy.config.json`
2. Re-run local analysis to confirm the noise dropped:
   ```bash
   codacy-analysis analyze --output-format json
   ```
3. Once satisfied, import the config to Cloud:
   ```bash
   codacy repository <provider> <org> <repo> --import .codacy/codacy.config.json
   ```
4. Trigger a reanalysis and verify (follow Step 6 from the tailored configuration workflow)

For patterns on Cloud-only tools, disable them directly:
```bash
codacy pattern <provider> <org> <repo> <toolName> <patternId> --disable
```

If the CLI returns an error, the pattern is likely enforced by an organization Coding Standard — inform the user it must be changed at organization level.
