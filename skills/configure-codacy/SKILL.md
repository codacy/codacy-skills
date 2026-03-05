---
name: configure-codacy
description: Tailors Codacy configuration to a project by suggesting tools and patterns aligned with the codebase, and reduces noise by identifying and disabling rules that produce too many false positives or mismatched results. Use when the user wants to configure Codacy, reduce noise in code reviews, set up tools or patterns, fix false positives, or align Codacy rules with their project's conventions.
license: MIT
metadata:
  author: Codacy
  version: 1.2.0
---

# Configure Codacy

This skill helps tailor Codacy configuration to a project's actual coding conventions, reducing noise and improving the signal-to-noise ratio of code reviews.

## Prerequisites

The `codacy-cli` skill must be available (or the Codacy CLI must be installed and authenticated). See `codacy-cli` for setup.

## Important: how configuration changes take effect

- **Changes are not instant.** Enabling or disabling tools or patterns, changing parameters, and ignoring issues only take effect after the next analysis. The current issues list reflects the last analyzed commit; it won't update until a new commit is pushed or a reanalysis is triggered via `--reanalyze`.
- **Organization standards take precedence.** If a pattern is enforced by a Coding Standard at the organization level, it cannot be enabled, disabled, or have its parameters changed at the repository level. Attempting to do so will fail. To change those patterns, the organization's Coding Standard must be updated directly (not possible via the CLI — requires access to Codacy organization settings in the UI).

## Tailored configuration workflow

```
Configuration Progress:
- [ ] Step 1: Analyse the repository
- [ ] Step 2: Get tools available in Codacy
- [ ] Step 3: Suggest tools to enable/disable
- [ ] Step 4: Suggest patterns to enable/disable
- [ ] Step 5: Apply changes using the CLI
- [ ] Step 6: Reanalyse and verify changes
```

### Step 1: Analyse the repository

Traverse the repository to identify:
- Languages and frameworks in use
- Build tools, package managers, test frameworks
- Coding conventions (naming, formatting, patterns found in the code)
- Existing linter/static analysis configuration files (`.eslintrc`, `pylintrc`, `semgrep.yml`, etc.)
- Security-sensitive areas (auth, payment, data handling)

### Step 2: Get tools available in Codacy

```bash
# See which tools are currently enabled or disabled
codacy tools <provider> <org> <repo>
```

### Step 3: Suggest tools

For each language or framework found:
- Identify the most relevant Codacy tool(s)
- Enable tools that match the project's stack, disable tools that don't apply
- Use configuration files when available where appropriate (`--configuration-file true`)

```bash
codacy tool <provider> <org> <repo> <toolName> --enable
codacy tool <provider> <org> <repo> <toolName> --disable
codacy tool <provider> <org> <repo> <toolName> --configuration-file true
```

### Step 4: Suggest patterns

For each enabled tool, review the active patterns:

```bash
codacy patterns <provider> <org> <repo> <toolName> --enabled
```

Suggest enabling patterns that:
- Enforce conventions already present in the codebase
- Cover known security risks for the frameworks in use
- Catch real bugs based on the languages and patterns observed

Suggest disabling patterns that:
- Contradict coding conventions found in the code
- Are not relevant to the detected languages or frameworks
- Are consistently triggered as false positives (see Noise reduction below)

To find a specific pattern by its original tool ID:
```bash
codacy patterns <provider> <org> <repo> <toolName> --search <originalPatternId>
# e.g. codacy patterns gh my-org my-repo pylint --search W0123
# e.g. codacy patterns gh my-org my-repo semgrep --search HttpGetHTTPRequest
```

Enable, disable, or configure individual patterns:
```bash
codacy pattern <provider> <org> <repo> <toolName> <patternId> --enable
codacy pattern <provider> <org> <repo> <toolName> <patternId> --disable
codacy pattern <provider> <org> <repo> <toolName> <patternId> --parameter name=value
```

### Step 5: Apply changes

After reviewing the suggestions with the user, apply them one by one. Confirm each change before proceeding to the next.

**Note:** If the CLI returns an error when changing a pattern, it is likely enforced by an organization Coding Standard and cannot be changed at the repository level — inform the user.

### Step 6: Reanalyse and verify changes

After all configuration changes have been applied, trigger a reanalysis so the new settings take effect on the current HEAD commit, then verify the results.

#### 6a. Trigger reanalysis

Record the current time (`requestedAt`) before triggering, then run:

```bash
codacy repository <provider> <org> <repo> --reanalyze
```

If the command fails, check that the repository exists on Codacy and the token has write access.

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

Once reanalysis is complete, verify the configuration changes had the desired effect:

1. **If tools were enabled or disabled**, confirm with:
   ```bash
   codacy tools <provider> <org> <repo>
   ```
   Check that the enabled/disabled state matches what was configured.

2. **If patterns were changed**, check the issue distribution:
   ```bash
   codacy issues <provider> <org> <repo> --overview
   ```
   Compare against the distribution from Step 1. Disabled patterns should no longer produce new issues. Enabled patterns may show new issues.

3. **If noise reduction was the goal**, compare total issue counts before and after. The noisy patterns identified earlier should appear with significantly fewer hits or not at all.

Report the before/after comparison to the user. If results are unexpected (e.g., a disabled pattern still shows issues), the pattern may be enforced by an organization Coding Standard.

## Noise reduction workflow

Use this when the user reports too many issues, false positives, or unhelpful warnings.

### Detect noisy patterns

```bash
# Get an overview of issue counts grouped by pattern
codacy issues <provider> <org> <repo> --overview

# Focus on high-volume categories
codacy issues <provider> <org> <repo> --categories <category> --overview
```

A pattern is likely noisy if:
- It accounts for a disproportionately large number of issues
- Multiple instances have been marked as false positives
- The violation contradicts conventions consistently found throughout the codebase

### Verify before disabling

Before recommending to disable a pattern:
1. Check the category and severity — be more conservative with Security and Error Prone patterns
2. Review actual instances in the code to confirm they are false positives or mismatched conventions
3. Check if the pattern could be configured (parameters adjusted) rather than disabled entirely

```bash
# See full details including pattern docs and code context
codacy issue <provider> <org> <repo> <issueId>
```

Only suggest disabling after verifying the pattern is consistently unhelpful for this specific codebase.

### Disable noisy patterns

```bash
codacy pattern <provider> <org> <repo> <toolName> <patternId> --disable
```

If the CLI returns an error, the pattern is likely enforced by an organization Coding Standard — inform the user it must be changed at organization level.

### Verify noise reduction

After disabling noisy patterns, trigger a reanalysis and verify the issue counts dropped. Follow the same approach as Step 6 in the tailored configuration workflow: trigger `--reanalyze`, poll for completion with a background subagent, then compare the issues overview before and after.
