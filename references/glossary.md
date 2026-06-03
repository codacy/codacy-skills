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
