---
name: codacy-cloud-cli
description: Uses the Codacy Cloud CLI to query repositories, issues, security findings, pull requests, tools, and patterns on Codacy Cloud. Use whenever the user mentions Codacy, asks about code quality metrics, wants to check issues or findings in a repo, inspect a pull request analysis, browse security vulnerabilities, enable or disable tools, search patterns, trigger a reanalysis, or interact with any remote Codacy data — even if they don't say "Codacy CLI" explicitly.
license: MIT
metadata:
  author: Codacy
  version: 1.3.0
---

# Codacy Cloud CLI

The Codacy Cloud CLI (`codacy`) is the command-line interface for Codacy Cloud. Use it whenever the user wants to interact with remote Codacy data. This is a different tool from the Codacy Analysis CLI (`codacy-analysis`), which runs static analysis locally.

## Setup

```bash
# Install
npm install -g @codacy/codacy-cloud-cli

# Authenticate — 3 options:
# 1. Set the `CODACY_API_TOKEN` environment variable
export CODACY_API_TOKEN=<token>
# 2. Use the `codacy login` command (interactive login)
codacy login
# 3. Use the `codacy login` command (with token input)
codacy login --token <token>
# Obtain tokens: Codacy > My Account > Access Management > Account API Tokens (https://app.codacy.com/account/access-management)

# Verify
codacy info
```

**Shared session:** The Cloud CLI and the Analysis CLI (`codacy-analysis`) share the same credentials at `~/.codacy/credentials`. Logging in or out with either CLI applies to both — there is no need to authenticate separately.

## Getting help

The CLI is the authoritative source of truth. Always use `--help` to discover available commands, options, and current behavior:

```bash
codacy --help
codacy <command> --help
# e.g. codacy issues --help
```

Use `--output json` on any command for machine-readable output.

## Provider values

| Value | Provider |
|-------|----------|
| `gh`  | GitHub   |
| `gl`  | GitLab   |
| `bb`  | Bitbucket |

## How Codacy data works

- **Data reflects the HEAD commit** — issue lists, coverage, and security findings always show the state of the latest analyzed commit on the branch or pull request. There is no per-file or per-line historical view.
- **Configuration changes are not instant** — enabling/disabling tools or patterns, changing parameters, and ignoring issues only take effect after the next analysis. That means either triggering a reanalysis via `--reanalyze` or waiting for the next commit to be pushed.
- **Organization standards are enforced and cannot be overridden at repository level** — if a pattern is enforced by a Coding Standard at the organization level, its enabled/disabled state and parameters cannot be changed per-repository. To change it, the standard must be updated at the organization level.

### Reanalysis

Use `--reanalyze` on the `repository` or `pull-request` commands to trigger reanalysis of the HEAD commit. Reanalysis may take a few minutes to start (depends on the queue and the organization's plan) and a few minutes to complete.

There is no dedicated status command. To check progress, re-run the same command without `--reanalyze`:
- **Table output:** look at the "Analysis" field — `"Reanalysis in progress..."` means it is still running; `"Finished X ago"` means it is done
- **JSON output:** compare the `startedAnalysis` and `endedAnalysis` timestamps on the commit data. The reanalysis is complete when `startedAnalysis` is after the time you triggered the reanalysis AND `endedAnalysis` > `startedAnalysis`

## Command reference

### Account & repositories

```bash
# Authenticated user and organizations
codacy info

# List repositories in an organization
codacy repositories <provider> <org>
codacy repositories gh my-org --search my-repo

# Repository dashboard (metrics, PRs, issues overview)
codacy repository gh my-org my-repo
codacy repository gh my-org my-repo --add       # add to Codacy
codacy repository gh my-org my-repo --remove    # remove from Codacy
codacy repository gh my-org my-repo --follow    # follow repository
codacy repository gh my-org my-repo --unfollow  # unfollow repository
codacy repository gh my-org my-repo --reanalyze  # trigger reanalysis of HEAD commit
```

### Issues (code quality)

```bash
# List issues with optional filters
codacy issues gh my-org my-repo
codacy issues gh my-org my-repo --branch main --severities Critical,High
codacy issues gh my-org my-repo --categories Security
codacy issues gh my-org my-repo --overview      # totals grouped by category/severity/language

# Full details for a single issue
codacy issue gh my-org my-repo <issueId>

# Ignore / unignore an issue
codacy issue gh my-org my-repo <issueId> --ignore
codacy issue gh my-org my-repo <issueId> --ignore --ignore-reason FalsePositive --ignore-comment "Not applicable here"
codacy issue gh my-org my-repo <issueId> --unignore
```

Filters: `--branch`, `--patterns`, `--severities` (Critical,High,Medium,Minor), `--categories`, `--languages`, `--tags`, `--authors`

Ignore reasons: `AcceptedUse` (default) | `FalsePositive` | `NotExploitable` | `TestCode` | `ExternalCode`

### Security findings

```bash
# List findings
codacy findings gh my-org my-repo
codacy findings gh my-org                       # org-wide
codacy findings gh my-org my-repo --severities Critical,High
codacy findings gh my-org my-repo --statuses Overdue,DueSoon

# Full details for a single finding (includes CVE data)
codacy finding gh my-org my-repo <findingId>

# Ignore / unignore a finding
codacy finding gh my-org my-repo <findingId> --ignore
codacy finding gh my-org my-repo <findingId> --ignore --ignore-reason FalsePositive --ignore-comment "Verified safe"
codacy finding gh my-org my-repo <findingId> --unignore
```

Filters: `--search`, `--severities` (Critical,High,Medium,Low), `--statuses` (Overdue,OnTrack,DueSoon,ClosedOnTime,ClosedLate,Ignored), `--categories`, `--scan-types`, `--dast-targets`

Ignore reasons: `AcceptedUse` (default) | `FalsePositive` | `NotExploitable` | `TestCode` | `ExternalCode`

### Pull requests

```bash
# PR summary (status, issues, coverage, changed files)
codacy pull-request gh my-org my-repo <prNumber>

# Annotated git diff with coverage and inline issues
codacy pull-request gh my-org my-repo <prNumber> --diff

# Full details for a specific issue within the PR
codacy pull-request gh my-org my-repo <prNumber> --issue <issueId>

# Ignore a specific issue in the PR
codacy pull-request gh my-org my-repo <prNumber> --ignore-issue <issueId>
codacy pull-request gh my-org my-repo <prNumber> --ignore-issue <issueId> --ignore-reason FalsePositive
codacy pull-request gh my-org my-repo <prNumber> --unignore-issue <issueId>

# Ignore all potential false positive issues in the PR at once
codacy pull-request gh my-org my-repo <prNumber> --ignore-all-false-positives

# Trigger reanalysis of PR HEAD commit
codacy pull-request gh my-org my-repo <prNumber> --reanalyze
```

### Tools & patterns

```bash
# List all tools (enabled/disabled)
codacy tools gh my-org my-repo

# Enable or disable a tool
codacy tool gh my-org my-repo eslint --enable
codacy tool gh my-org my-repo eslint --disable
codacy tool gh my-org my-repo eslint --configuration-file true

# List patterns for a tool
codacy patterns gh my-org my-repo eslint
codacy patterns gh my-org my-repo eslint --enabled --categories Security
codacy patterns gh my-org my-repo pylint --search W0123

# Enable, disable, or configure a pattern
codacy pattern gh my-org my-repo eslint no-unused-vars --enable
codacy pattern gh my-org my-repo eslint no-unused-vars --disable
codacy pattern gh my-org my-repo eslint max-len --parameter max=120

# Enable or disable all patterns matching specific filters
codacy patterns gh my-org my-repo eslint --categories Security --severities Critical,High --enable-all
codacy patterns gh my-org my-repo pylint --categories CodeStyle --severities Minor --disable-all
```

Pattern search tip: Codacy pattern IDs combine tool prefix and original ID. Use `--search` with the original ID to find them:
```bash
codacy patterns gh my-org my-repo semgrep --search HttpGetHTTPRequest
codacy patterns gh my-org my-repo pylint --search W0123
```

## Common workflows

**Check critical security issues in a repo:**
```bash
codacy findings gh my-org my-repo --severities Critical,High
```

**Review what a PR introduced:**
```bash
codacy pull-request gh my-org my-repo 42
codacy pull-request gh my-org my-repo 42 --diff
```

**Understand a specific issue:**
```bash
codacy issue gh my-org my-repo <issueId>   # includes pattern docs and code context
```

**Trigger reanalysis and check status:**
```bash
# Trigger reanalysis
codacy repository gh my-org my-repo --reanalyze

# Check status (table — look at Analysis field)
codacy repository gh my-org my-repo

# Check status (JSON — compare startedAnalysis vs endedAnalysis)
codacy repository gh my-org my-repo --output json
```
