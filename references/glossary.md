# Codacy Glossary

Shared definitions for all Codacy agent skills. When writing responses, prefer the **primary term** but recognize the listed synonyms in user input.

---

## Platform

### Codacy

An automated code quality and security platform. Codacy integrates with Git providers, analyzes source code on every push and pull request, and reports on issues, security findings, coverage, duplication, and complexity. It supports 40+ programming languages.

### Provider

> Synonyms: **git provider**, **integration**, **SCM provider**

The source code hosting service connected to Codacy. Supported providers:

| Provider | CLI value |
|----------|-----------|
| GitHub (Cloud & Enterprise) | `gh` |
| GitLab (Cloud & Enterprise) | `gl` |
| Bitbucket (Cloud & Server) | `bb` |

Codacy syncs organizations, repositories, and members from the provider in real time.

---

## Organizational structure

### Organization

> Synonyms: **owner**

A Codacy entity that maps 1:1 to a Git provider organization (or user account for personal repos). Organizations contain repositories and members. Codacy automatically syncs organization changes from the provider—renaming, member additions/removals, and deletions.

The organization with the same name as a user's Git provider username contains that user's personal repositories.

### Repository

> Synonyms: **repo**, **project**

A source code repository added to a Codacy organization. Repositories can be:

- **Private** — only organization members can view analysis results; Codacy requires members to be added for analysis to process their commits.
- **Public** — analysis results are visible to anyone with the repository link.

Repository visibility syncs from the Git provider, though sync timing varies by provider.

### Branch

A Git branch within a repository. Codacy can analyze multiple branches, but one is designated the **main branch** (the default branch from the provider). Metrics on the repository dashboard reflect the main branch. Other branches can be enabled for analysis individually.

### User

> Synonyms: **account**, **member**

A person who accesses Codacy, authenticated through a Git provider. Key roles and distinctions:

- **Organization member** — a user who has joined a Codacy organization and can view its repositories.
- **Organization admin** — a member with permissions to manage settings, coding standards, gate policies, and people.
- **Committer** — a contributor whose commits are analyzed by Codacy. On paid plans, committers consume seats (auto-assigned; 90-day inactivity threshold for deactivation). A committer may or may not be a Codacy member.
- **Author** — the person attributed as the author of a code change (Git author field). May or may not be a Codacy member.

---

## Code analysis

### Analysis

The process of scanning source code to detect issues, security vulnerabilities, duplication, and complexity. Codacy supports two modes:

- **Cloud analysis** (server-side) — runs automatically on Codacy's servers when code is pushed. This is the default and requires no setup beyond adding the repository.
- **Local analysis** (client-side) — runs tools on the developer's machine or CI build server using the Codacy Analysis CLI. Useful for pre-push checks, CI pipelines, or environments where code cannot leave the network.

See also: [Codacy Cloud CLI](#codacy-cloud-cli), [Codacy Analysis CLI](#codacy-analysis-cli).

### Tool

> Synonyms: **linter**, **analyzer**, **algorithm**

A static analysis engine that scans code for issues. Examples: ESLint, Pylint, PMD, SpotBugs, Semgrep, Trivy, RuboCop. Codacy bundles and runs these tools automatically based on the languages detected in the repository.

Tools can be enabled or disabled per repository. When a tool's configuration file (e.g., `.eslintrc`, `.rubocop.yml`) is present in the repository, Codacy uses it to control which patterns are active.

### Pattern

> Synonyms: **rule**, **code pattern**, **check**

A specific check within a tool that detects a particular type of issue. For example, ESLint's `no-unused-vars` is a pattern that flags unused variables. Each pattern has:

- A **severity** (Critical, High, Medium, or Minor).
- A **category** (e.g., Security, Error Prone, Code Style).
- Optional **parameters** that fine-tune behavior (thresholds, allowed values, etc.).

Patterns can be individually enabled or disabled. Codacy marks some patterns as **recommended** based on tool defaults or Codacy's own curation.

### Pattern parameters

Configuration values for a specific pattern that adjust its behavior. For example, a maximum line length pattern might accept a `maxLength` parameter. Parameters are set per-repository through the Codacy UI, API, or coding standards.

### Language

> Synonyms: **programming language**

A programming language supported by Codacy for analysis. Codacy auto-detects languages in a repository and enables the relevant tools. Over 40 languages are supported, including JavaScript, TypeScript, Python, Java, C#, Go, Ruby, PHP, Scala, Kotlin, and Swift.

---

## Quality concepts

### Issue

> Synonyms: **quality issue**, **code issue**, **violation**

A problem detected in source code by a tool's pattern. Issues represent violations of rules, standards, conventions, or best practices—ranging from style inconsistencies to potential bugs and security risks.

**Severity levels:**

| Severity | Icon | Meaning |
|----------|------|---------|
| Critical | Red | Most dangerous — potential security vulnerabilities, crashes, or serious compatibility problems |
| High | Orange | Serious problems that should be fixed — likely bugs or high-impact violations |
| Medium | Yellow | Violations of coding standards and conventions |
| Minor | Blue | Least critical — code style, formatting, minor suggestions |

**Categories:**

- Code Style
- Error Prone
- Code Complexity
- Performance
- Compatibility
- Unused Code
- Security (issues in this category are also surfaced as [security findings](#finding))
- Documentation
- Best Practice
- Comprehensibility

Issues are measured as a density: **issues per thousand lines of code (kLoC)** for cross-repository comparison.

### Issue counts on a diff: Total, New, Fixed

> Synonyms: **delta**, **delta issues**, **introduced/resolved issues**

Codacy reports three numbers for a commit or pull request, and they are **not** related by arithmetic. Total is a snapshot of the whole codebase; New and Fixed are properties of the **diff**. Before trying to reconcile them, read [Why New and Fixed are not deltas between totals](#why-new-and-fixed-are-not-deltas-between-totals).

#### Total

The issues attached to the commit — the whole codebase at that point, not a delta. It needs no parent and no diff, so it is reported even when New and Fixed cannot be computed.

#### Issue identity

New and Fixed are set differences over an issue **identity** (`uuid`): an MD5 hash of the filename, the pattern's internal ID, the line text with all whitespace removed, and the tool's `sourceId` where it provides one (the CVE, for Trivy/SCA).

Identity deliberately excludes the **line number** and the **message**:

- Code moving up or down a file does not re-identify its issues.
- Two identical lines flagged by the same pattern in one file collapse to a single identity.
- Editing a flagged line's text *does* re-identify it — the source of most Fixed/New churn.

Line text is truncated at 512 characters before hashing, so on very long lines (minified assets, lock files) distinct issues can share an identity.

#### How New and Fixed are computed

The baseline is the **first parent** for a commit, the **destination (base) commit** for a pull request.

1. **Scope to changed files.** Both issue sets are filtered to the files the diff touched. This filter is applied *before* everything else, so an issue in an untouched file cannot reach **any** of the four buckets — not Fixed, and not Possible fixed either, however the set changed.
2. **Raw set difference** by identity: raw new = in head, not in baseline; raw fixed = in baseline, not in head.
3. **Diff-line confirmation** — the defining step. A raw new issue is **New** only if its start line is a line the diff **added**; a raw fixed issue is **Fixed** only if its start line is a line the diff **removed** (baseline numbering).
4. **Cancellation.** If the same pattern, file and start line appears in both raw sets, both are dropped from the confirmed buckets (they fall through to the possible ones).

#### Possible New / Possible Fixed

> Synonyms: **potential issues**, `onlyPotential`

Whatever steps 3 and 4 rejected, stored as their own delta types (`PossibleNewIssue`, `PossibleFixedIssue`):

- **Possible new** — appeared in a changed file, but not on a line the diff added.
- **Possible fixed** — disappeared from a changed file, but not because a line carrying it was removed.

**Possible is still scoped to the changed files** — it inherits step 1's filter, and is only ever the leftovers of steps 3 and 4. So the three tiers are:

| Where the issue lives | Bucket |
|---|---|
| In a changed file, on a line the diff added/removed | **New** / **Fixed** |
| In a changed file, but not on such a line (or cancelled at step 4) | **Possible new** / **Possible fixed** |
| In a file the diff did not touch | **Nothing at all** — invisible to every bucket |

That third tier is the one that surprises people: an issue can vanish between two commits and be reported *nowhere*, because possible is not a catch-all for "everything else that changed" — only for "everything else **in the changed files**".

"Possible" therefore means **the issue set changed inside the diff's files, but the diff's lines do not explain it** — not a lower-confidence issue, and nothing to do with suggested fixes. Typical causes: the issue shifted because of edits elsewhere in the file, the surrounding code was reflowed, the tool version or configuration changed, or a pattern was enabled or disabled.

#### What "Fixed" does and does not mean

**Fixed does not mean the issue is gone.** It means *a line carrying it was deleted in this diff*:

- Deleting code, or a whole file, counts as Fixed for every issue on the removed lines — nothing was repaired.
- Disabling a pattern produces **no** Fixed: untouched files are out of scope, and in changed files it lands in Possible fixed.
- An issue that genuinely went away may be absent from Fixed entirely — as Possible fixed if its file was touched, and as nothing at all if it was not.
- Rewriting a flagged line usually yields Fixed **and** New — the same problem under a new identity.

#### Headline counters vs. the issue lists

The overview counters — a commit's `newIssues`/`fixedIssues`, PR summaries, and [quality gate](#quality-gate) thresholds — count **only confirmed** New and Fixed. The possible buckets are excluded from all of them.

#### Why New and Fixed are not deltas between totals

The recurring question is *"the parent had 500 issues, this commit has 400 — why is Fixed only 50?"*, and sometimes its opposite, *"Fixed is bigger than the drop"*. Both are expected: **Fixed is a diff-attributed event count, not a subtraction.** An issue counts as Fixed only if it lived in a file the diff touched, vanished, **and** sat on a line the diff removed. Everything else changes Total while the counters stay put.

**Fixed smaller than the drop in Total**

- **Untouched files are out of scope** — disabling a pattern or tool, a coding-standard change, a tool upgrade, or a change to ignored paths or detected languages all reduce Total with **zero** Fixed *and zero Possible fixed*. This is normally the bulk of an unexplained drop, and no query against the delta will surface it.
- **Ignoring an issue deletes it** from the snapshot at the next analysis, so it leaves Total without ever being Fixed.
- **Possible fixed is excluded** from the counters — including the pairs cancellation moved there.
- **Renames drop the fixed side.** Diff rows are keyed to the *new* path and `fileDataId` is per `(project, filename)`, so a renamed file's old-path issues are out of scope entirely, while its new-path issues are re-identified (filename is hashed) and count as New or Possible new. A pure rename with no content change emits no diff chunks, so it produces neither.
- **Deltas may not have run at all** — see [When New and Fixed are missing altogether](#when-new-and-fixed-are-missing-altogether).

**Fixed larger than the drop in Total**

Almost always **identity churn**: the same problem re-identified, contributing 1 Fixed *and* 1 New for no net change. Any of the four hashed inputs can trigger it.

| Changed input | Typical trigger |
|---|---|
| Filename | File moved or renamed → every issue in it |
| Pattern internal ID | Tool upgrade renames a rule → every issue from that rule |
| Line text | The flagged line edited, reformatted or requoted; a formatter run |
| `sourceId` | A tool starts, stops or changes what it reports (e.g. Trivy CVEs) |

Whether a churned pair is *counted* comes down to step 4: editing a line **in place** puts both halves on the same start line, so they cancel — but the same edit **after lines were inserted or removed above it** shifts the start line, cancellation misses, and the pair counts as 1 New + 1 Fixed. That is the main engine behind inflated Fixed counts.

Related traps:

- **The message is a red herring.** A churned pair often shows different messages on the Fixed and New rows, which reads like the message caused it. It cannot: the message is not hashed, and a changed message is written in place onto the existing identity. Differing messages are *evidence* of churn — look for a renamed rule or an edited line instead.
- **A historical mass event.** Adding `sourceId` to the hash (UUID v1 → v2, rolled out to all customers) re-identified every issue from every tool that reports one, so commits spanning that rollout show large Fixed/New pairs that say nothing about the code.
- **Copied-forward (`dirty`) results.** A file that fails analysis has its previous results carried forward so the snapshot stays complete. These take part in deltas like real results, so a file that errors on one commit and succeeds on the next churns from the pipeline, not the code.

**Practical guidance**

- Read Fixed as *"issues on lines this diff deleted"*, never *"issues resolved"*.
- To reconcile a Total drop, compare the two snapshots directly rather than subtracting, and ask separately whether configuration changed between them.
- When New and Fixed are both unexpectedly large, suspect a rename, a tool or pattern-set change, or a reformat before treating either as signal.
- Include the possible buckets (a second call with `onlyPotential=true`) whenever the question is "what changed?" rather than "what did the gate count?".

#### Aggregating Fixed over a period

Everything above concerns a **single** commit or pull request. Summing Fixed across a date range is a further step, and it breaks in its own way: **Fixed is recorded per commit, so a period total counts events, not distinct issues.**

Every analyzed commit gets its own delta against its first parent. So one removal is attributed repeatedly:

- each commit of a pull request, **and** the merge commit that lands it, are separate deltas over overlapping content;
- a rebase or force-push replays the same content as new commits, each with its own delta;
- an issue that keeps being re-identified ([churn](#why-new-and-fixed-are-not-deltas-between-totals)) contributes one Fixed event per commit that touches it.

A period total therefore has **no ceiling related to the repository's issue count**: a repo holding 40 issues can legitimately report thousands of Fixed in a month, and a repo holding zero issues at both ends of a window can report a non-zero total.

Consequences for reporting:

- **Period Fixed is not a remediation KPI** and cannot be reconciled against `Total(start) − Total(end)`. The two answer different questions and are not in the same units.
- To measure whether the issue burden fell, compare **Total** at the two dates. To count distinct issues actually resolved, compare the issue **identities** present at each date — Fixed does not provide this.
- `Total(start) − Total(end)` is also not a floor for "issues resolved": a repo that adds 100 and removes 100 nets zero while genuinely removing 100.

#### API surface

The confirmed/possible split is expressed by two independent request parameters, not by the response:

| Parameter | Values | Meaning |
|-----------|--------|---------|
| `status` | `all`, `new`, `fixed` | Which side of the delta to return (default `all`) |
| `onlyPotential` | `true`, `false` | `false` (default) returns only **confirmed**; `true` returns **only the possible ones** |

`onlyPotential` is a **switch, not an "include"** — there is no single call that returns confirmed and possible together; issue two calls and merge.

The public `deltaType` enum has only `Added` and `Fixed`: `PossibleNewIssue` collapses onto `Added` and `PossibleFixedIssue` onto `Fixed`. **A returned `deltaType` therefore cannot tell you whether an issue was confirmed or possible** — only the `onlyPotential` value you sent can.

Endpoints carrying both parameters: `listCommitDeltaIssues`, `listPullRequestIssues`, `listCommitClones`, `listPullRequestClones`.

#### When New and Fixed are missing altogether

Delta computation is **skipped** — leaving New and Fixed at 0 while Total is still reported — when:

- the baseline commit no longer holds full data (data retention has trimmed it), or
- no diff is available for the comparison.

A `0 / 0` delta on an analyzed commit is therefore ambiguous: it can mean "nothing changed" or "we could not tell". Check whether the commit was analyzed and whether a baseline exists before reading it as a clean diff.

#### Clones

[Clones](#clone) have their own New/Fixed delta, matched by code hash over the changed files. There are **no possible variants** for clones, so `onlyPotential=true` on the clone endpoints returns nothing.

### Finding

> Synonyms: **security finding**, **security issue**, **vulnerability**

A security-specific problem detected through one of Codacy's security scan types. Findings have their own lifecycle and tracking, separate from general quality issues. Every finding has:

**Severity levels** (shared scale with issues, but with associated remediation deadlines):

| Severity | Deadline |
|----------|----------|
| Critical | 30 days |
| High | 60 days |
| Medium | 90 days |
| Low | 120 days |

**Status:**

- **Open** — further classified as *Overdue*, *Due soon*, or *On track* based on the remediation deadline.
- **Closed** — *Closed late* or *Closed on time* relative to the deadline.
- **Ignored** — the finding has been reviewed and accepted as a known risk.

**Categories** (a superset of the Security issue subcategories):

Authentication, Authorization, Command Injection, Cryptography, CSRF, Denial of Service, File Access, HTTP, Improper Access Control, Injection, Input Validation, Insecure Storage, Mass Assignment, Regex, SQL Injection, SSL/TLS, XSS, and others.

**Scan type** (how the finding was detected):

| Scan type | Description |
|-----------|-------------|
| Code scanning (SAST) | Static analysis of source code for vulnerabilities, without executing it |
| Software Composition Analysis (SCA) | Analysis of third-party libraries and dependencies for known vulnerabilities, malicious packages, or outdated versions |
| Exposed Secrets | Detection of credentials, API keys, tokens, or other sensitive data committed to code |
| Infrastructure as Code | Detection of misconfigurations in IaC files (Terraform, CloudFormation, etc.) |
| Penetration Testing | Results from security penetration testing imported into Codacy |
| App Scanning (DAST) | Dynamic testing by simulating attacks against a running application |

### Severity

A classification shared by both issues and findings that indicates how critical a problem is. The scale is **Critical > High > Medium > Low** for findings and **Critical > High > Medium > Minor** for quality issues. Severity is assigned by the pattern definition and can influence quality gate rules.

### Duplication

A repository-level metric measuring the percentage of files that contain duplicated code. A file is considered **duplicated** when the number of clones it contains exceeds a configurable threshold (set via [quality goals](#quality-goal)).

### Clone

A block of duplicate source code that exists in at least two places in the repository. Clones are the unit that the duplication metric counts. On pull requests and commits, Codacy reports the number of **new clones introduced** by the change.

### Coverage

> Synonyms: **test coverage**, **code coverage**

The degree to which source code is exercised by automated tests. Codacy uses **line coverage**: the percentage of coverable lines that are covered by at least one test.

Key metrics:

- **Repository coverage** — overall percentage of covered lines across the codebase.
- **Coverage variation** — the change in overall coverage percentage caused by a commit or pull request (positive = improvement, negative = regression).
- **Diff coverage** — the percentage of *new or modified* coverable lines in a pull request that are covered by tests. Shown as `∅` when a PR introduces no coverable lines.

Coverage data is **not computed by Codacy itself**. It must be generated by a test framework (e.g., Jest, pytest-cov, JaCoCo) and uploaded to Codacy from a CI/CD pipeline using the Codacy Coverage Reporter.

### Complexity

A metric based on **cyclomatic complexity** — the number of linearly independent paths through a method's source code. More control flow statements (if/else, loops, switch cases) mean higher complexity.

- **File complexity** = sum of cyclomatic complexity of all methods in the file.
- A file is considered **complex** when its complexity exceeds a configurable threshold (set via quality goals).
- **Repository complexity** = percentage of complex files.
- **PR/commit complexity** = sum of complexity increases for changed files (only counted when the increase is ≥ 4).

Note: Codacy surfaces complexity both as a **metric** (on dashboards and quality gates) and as **issues** (patterns in the Code Complexity category that flag overly complex methods).

---

## Configuration & governance

### Coding Standard

A reusable configuration that defines which tools and patterns should be active. Coding standards enforce consistent analysis rules across multiple repositories in an organization.

- Up to 10 coding standards per organization.
- Multiple standards can apply to the same repository; their configurations are merged.
- Coding standards marked as **default** are automatically applied to new repositories.
- Tools and patterns enforced by a coding standard cannot be overridden at the repository level.

### Quality Gate

> Synonyms: **gate**, **gate policy**

A set of rules that determine whether a pull request or commit passes or fails. Quality gate rules can set thresholds for:

- Number of new issues (optionally filtered by minimum severity)
- Number of new security issues (optionally filtered by minimum severity)
- Complexity increase
- New clones (duplication)
- Coverage variation (minimum allowed decrease)
- Diff coverage (minimum required percentage)

When a pull request violates any gate rule, it is marked as **Not up to standards**. Gate policies can be defined at the organization level and applied across multiple repositories for consistency.

### Quality Goal

> Synonyms: **goal**, **target**, **threshold**

Dashboard thresholds that define acceptable quality levels for monitoring repository health over time. Goals include:

- Maximum issues (per kLoC)
- Maximum complexity
- File complexity threshold (above which a file is considered complex)
- Maximum duplication percentage
- File duplication threshold (above which a file is considered duplicated)
- Minimum coverage percentage

Quality goals are visualized on repository dashboards and evolution charts. They are informational targets — unlike quality gates, they do not block pull requests.

### Status Check

Reports sent by Codacy to the Git provider indicating whether a pull request passes quality gates. Codacy sends up to three separate status checks:

1. **Quality metrics** — covers issues, complexity, and duplication gates.
2. **Coverage variation** — covers the overall coverage change threshold.
3. **Diff coverage** — covers the diff coverage threshold.

These checks appear in the Git provider's pull request UI and can be configured as **required status checks** in branch protection rules, effectively blocking merges that don't meet quality standards.

---

## Security-specific terms

### SAST

**Static Application Security Testing.** Analysis of source code for security vulnerabilities without executing it. This is the primary scan type in Codacy — tools like Semgrep, SpotBugs, and Bandit perform SAST by analyzing code patterns.

### DAST

**Dynamic Application Security Testing.** Security testing that simulates attacks against a running application to find vulnerabilities that only manifest at runtime. DAST results can be imported into Codacy as security findings.

### SCA

**Software Composition Analysis.** Analysis of third-party libraries and dependencies for known vulnerabilities, malicious packages, outdated versions, and license compliance issues. In Codacy, SCA is performed by tools like Trivy.

### Pentesting

> Synonyms: **penetration testing**

Manual or automated security testing where testers simulate real-world attacks against an application. Pentesting results can be imported into Codacy as security findings of scan type "Penetration Testing."

### Dependency

An external library, package, or module used by a repository. Codacy tracks dependencies across an organization and scans them via SCA for:

- Known security vulnerabilities (CVEs)
- Malicious packages
- Outdated versions
- License compliance

The Dependencies view in Codacy shows all dependencies across organization repositories, with usage counts, versions, and associated security findings.

---

## CLI tools

### Codacy Cloud CLI

A command-line tool (`@codacy/codacy-cloud-cli`) for querying and interacting with the Codacy Cloud platform remotely. Used to:

- List and inspect repositories, issues, findings, and pull requests
- Search, enable, or disable tools and patterns
- Trigger reanalysis
- Manage organization and repository configurations

Install: `npm install -g @codacy/codacy-cloud-cli`. Requires a `CODACY_API_TOKEN` for authentication.

### Codacy Analysis CLI

A command-line tool for running Codacy's static analysis tools **locally** — on a developer's machine or in a CI/CD pipeline. It pulls tool configurations from the repository's `.codacy/codacy.config.json`, runs the selected tools via Docker containers, and outputs results in JSON format.

Use cases: pre-push validation, CI pipeline integration, offline analysis, reproducing Cloud analysis results locally.

---

## Git & workflow concepts

### Commit

A Git commit analyzed by Codacy. When a commit is pushed to an analyzed branch, Codacy reports the issues introduced and resolved, complexity changes, new clones, and coverage variation caused by that commit.

### Pull Request

> Synonyms: **PR**, **merge request** (GitLab)

A proposed code change from one branch into another. Codacy analyzes pull requests to report:

- New issues introduced (not present in the target branch)
- Complexity and duplication changes
- Diff coverage and coverage variation
- Quality gate pass/fail status

Pull request analysis is incremental — Codacy only flags problems introduced by the PR, not pre-existing issues in the codebase.
