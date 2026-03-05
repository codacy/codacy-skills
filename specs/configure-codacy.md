# Configure Codacy

Create a new skill that:
- tailors Codacy configuration to the project and user needs
- reduces noise in code reviews and in the repository

## Tailored configuration
- traverse the repository and code identifying practices, coding conventions, frameworks, libraries, tools, etc.
- get the tools available from Codacy 
- suggest tools and patterns to:
  - keep the code secure, clean, and maintainable
  - keep the code aligned with the current coding conventions, practices, and patterns found in the code
  - avoid noise (no need for useless patterns or rules that don't match the project current conventions, practices, and patterns)

## Reducing noise
- when checking issues totals in a repository, in a commit, or in a pull request, check if there are too many issues:
  - too many of the same pattern, signaling wrong configuration or unmatched conventions
  - some with false positives of the same pattern, signaling wrong configuration or unmatched conventions

- always have in consideration the category and severity of the detected noisy patterns, and evaluate checking the project code to verify the pattern can be safely disabled.
- after verifying the pattern can be safely disabled, suggest to disable it.


## Using the CLI

You can use the CLI to:
- enable patterns
- customize patterns parameters
- disable patterns

If patterns were enabled in a Coding Standard (organization scope, not repository), then inform the user that those patterns need to be disabled at the organization level in the Coding Standard.

Codacy integrates with OSS tools. Use your knowledge of the tools to suggest which patterns should be enabled based on the project code. Patterns in Codacy have unique IDs compound by a tool's prefix (many times including version information) and the pattern original ID (e.g. `Semgrep_java_crypto_rule-HttpGetHTTPRequest`, `PyLintPython3_W0123`).

When trying to find a specific pattern, you can use the CLI to search for it (e.g. `codacy patterns gh acme project-alpha pylint --search W0123`, `codacy patterns gh acme project-alpha semgrep --search HttpGetHTTPRequest`).

