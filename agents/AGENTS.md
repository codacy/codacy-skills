<skills>

You have access to Codacy skills that teach you how to use the Codacy CLI to improve code quality workflows.

These skills are:
 - codacy-analysis-cli -> "skills/codacy-analysis-cli/SKILL.md"
 - codacy-cloud-cli -> "skills/codacy-cloud-cli/SKILL.md"
 - codacy-code-review -> "skills/codacy-code-review/SKILL.md"
 - configure-codacy -> "skills/configure-codacy/SKILL.md"
 - setup-coverage -> "skills/setup-coverage/SKILL.md"

IMPORTANT: You MUST read the SKILL.md file whenever the description of a skill matches the user's intent or may help accomplish their task.

<available_skills>

codacy-analysis-cli: `Uses the Codacy Analysis CLI to run local static analysis on repositories or specific files. Handles installation, initialization, dependency management, dry-runs, and analysis with JSON output. Use whenever the user wants to analyze code locally, run static analysis, scan for bugs or security issues, lint files, check code quality without pushing to Codacy, or run tools like ESLint, Ruff, Semgrep, RuboCop, or any other supported analyzer on their machine. Also trigger when the user asks to analyze staged changes, scan a PR locally, or set up local Codacy analysis.`

codacy-cloud-cli: `Uses the Codacy Cloud CLI to query repositories, issues, security findings, pull requests, tools, and patterns on Codacy Cloud. Use whenever the user mentions Codacy, asks about code quality metrics, wants to check issues or findings in a repo, inspect a pull request analysis, browse security vulnerabilities, enable or disable tools, search patterns, trigger a reanalysis, or interact with any remote Codacy data — even if they don't say "Codacy CLI" explicitly.`

codacy-code-review: `Enriches pull request code reviews with Codacy data — quality issues, security findings, coverage, and duplication. Use whenever the user asks to review a PR, check what a pull request introduced, verify PR coverage, look at PR quality, or find new issues in a PR. Also use when another code-review skill is active (e.g. CodeRabbit) to layer Codacy data on top. Trigger this skill for any pull request review workflow, even if the user just says "review PR 42" or "what's wrong with this PR".`

configure-codacy: `Tailors Codacy configuration to a project by suggesting tools and patterns aligned with the codebase, and reduces noise by identifying and disabling rules that produce too many false positives or mismatched results. Use whenever the user wants to configure Codacy, reduce noise, fix false positives, enable or disable tools or patterns, tune code quality rules, deal with too many warnings, or align Codacy with their project's conventions. Also trigger when the user complains about irrelevant issues, noisy linters, or wants to set up Codacy for the first time on a repo.`

setup-coverage: `Sets up test coverage reporting in a repository and configures upload to Codacy. Detects testing frameworks, CI/CD pipelines, and coverage gaps, then adds the missing pieces to generate and upload coverage reports. Use whenever the user wants to set up coverage, add coverage reporting, integrate coverage with Codacy, fix missing coverage uploads, troubleshoot coverage not showing up, or configure CI to send coverage data. Also trigger when the user mentions test coverage, code coverage, coverage reports, or wants to know why Codacy shows no coverage for their repo.`

</available_skills>

Paths referenced within skill folders are relative to that skill folder. For example, `codacy-cloud-cli`'s `references/api.md` would be referenced as `skills/codacy-cloud-cli/references/api.md`.

</skills>
