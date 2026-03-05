---
name: codacy-code-review
description: Enriches pull request code reviews with Codacy data — quality issues, security findings, coverage, and duplication. Use when reviewing a pull request, when a code-review skill is active (e.g. CodeRabbit), or when the user asks to review a PR, check PR quality, verify coverage, or find issues introduced by a PR. Works alongside other code review skills.
license: MIT
metadata:
  author: Codacy
  version: 1.2.0
---

# Codacy Code Review

This skill enriches code reviews with Codacy data. It works alongside any existing code review process (a code-review skill, CodeRabbit, manual review, etc.) — it adds Codacy-specific data on top.

## Prerequisites

The `codacy-cli` skill must be available (or the Codacy CLI must be installed and authenticated). See `codacy-cli` for setup.

## How Codacy PR data works

- **Data reflects the HEAD commit of the PR** — the analysis shown is always for the latest push to the PR branch, not a specific commit.
- **Ignoring issues takes effect immediately** but any other configuration changes (patterns, tools) only apply after the next analysis or push.
- **Stale or missing analysis** — if the PR analysis appears outdated or incomplete, trigger a reanalysis: `codacy pull-request <provider> <org> <repo> <prNumber> --reanalyze`. Then re-run the pull-request command to check if analysis has completed before proceeding with the review.

## Review workflow

When reviewing a pull request, follow these steps. Always complete all steps — do not skip.

```
Code Review Progress:
- [ ] Step 1: Gather PR context (title, description, linked ticket)
- [ ] Step 2: Fetch Codacy PR analysis
- [ ] Step 3: Check introduced issues
- [ ] Step 4: Check coverage
- [ ] Step 5: Verify alignment with ticket and PR description
- [ ] Step 6: Propose test plan and check coverage gaps
- [ ] Step 7: Summarize and suggest improvements
```

### Step 1: Gather PR context

Fetch the pull request metadata from the source provider (GitHub, GitLab, Bitbucket):
- PR title and description
- Linked ticket or issue (Jira, GitHub Issues, Linear, local spec, etc.) — look in the description, branch name, and commit messages

If there is a linked ticket, fetch its content as well.

### Step 2: Fetch Codacy PR analysis

```bash
codacy pull-request <provider> <org> <repo> <prNumber>
```

This returns: up-to-standards status, new issues introduced, coverage delta, complexity delta, duplication delta, and changed files.

For the annotated diff with inline issue and coverage annotations:
```bash
codacy pull-request <provider> <org> <repo> <prNumber> --diff
```

### Step 3: Check introduced issues and security findings

For each issue introduced by the PR:
- Note the severity, category, and file location
- If details are needed: `codacy pull-request <provider> <org> <repo> <prNumber> --issue <issueId>`
- Flag Critical and High severity issues as blockers

If issues look like false positives, suggest ignoring them:
```bash
# Ignore a specific issue in this PR
codacy pull-request <provider> <org> <repo> <prNumber> --ignore-issue <issueId> --ignore-reason FalsePositive

# Ignore all issues Codacy identified as potential false positives in one go
codacy pull-request <provider> <org> <repo> <prNumber> --ignore-all-false-positives

# Unignore if needed
codacy pull-request <provider> <org> <repo> <prNumber> --unignore-issue <issueId>
```

If the same false positive pattern keeps appearing across PRs, suggest disabling the pattern via `configure-codacy` instead.


### Step 4: Check coverage

From the PR analysis output, review:
- Overall coverage delta (did it go up or down?)
- Files with uncovered lines introduced by the PR
- Use `--diff` output to see which specific lines lack coverage (✘ markers)

Flag files with new uncovered lines as needing tests.

### Step 5: Verify alignment

**With the ticket/issue:** Check that the code changes address the stated requirements. Note any functionality described in the ticket that is not present in the changes. Note any changes that go beyond the scope of the ticket.

**With the PR description:** Verify the description accurately reflects what was changed. Note discrepancies.

If the ticket or PR description is missing, incomplete, or inaccurate, note specific improvements to suggest.

### Step 6: Propose test plan

Based on the changed code and coverage data:
1. List the scenarios that should be tested (happy path, edge cases, error cases)
2. For each scenario, check whether a test already exists in the PR diff
3. Flag scenarios with no corresponding test and no coverage in Codacy

### Step 7: Summary

Present a structured review summary:

```
## Codacy Review Summary

### Quality gate
[Pass / Fail — from Codacy PR analysis]

### Issues introduced
[List issues by severity, or "None"]

### Coverage
[Delta, uncovered lines in new code]

### Alignment
- Ticket: [aligned / gaps noted]
- PR description: [accurate / suggestions]

### Test plan
[Proposed scenarios and whether tests exist]

### Suggested improvements
- PR description: [if applicable]
- Ticket/issue: [if applicable]
```

## When another code review skill is active

If a code review skill (e.g. `code-review` skill, CodeRabbit) has already performed a review, add a **Codacy data section** to that review rather than replacing it. Follow steps 2–6 above and append the Codacy findings.
