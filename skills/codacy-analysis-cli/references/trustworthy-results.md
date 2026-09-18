# Trustworthy results: when "no issues" actually means clean

A clean-looking result has two very different causes: the tools ran and found nothing, or the tools never ran. By default these are indistinguishable from the exit code and the `issues` array alone.

## The silent-skip failure mode

A tool that cannot run (missing binary or runtime) is skipped by default, and the run reports success:

```console
$ codacy-analysis analyze --staged --output-format json
EXIT=0
{"issues": 0, "errors": 0, "toolResults": [{"toolId": "Trivy", "status": "success"}]}
```

Seven scanners were unavailable in that run. With them present the same files yield real findings, including `Bandit_B307` (`eval()`). Nothing in `issues`, `errors`, or the exit code shows the gap — only `capability.unavailable` does.

## Strict mode (`--fail-if-missing`)

Strict mode stops the run *before* analysis:

```console
$ codacy-analysis analyze --staged --fail-if-missing --output-format json
EXIT=2
```

```json
{
  "metadata": { "executionMode": "strict" },
  "errors": [{
    "toolId": "runner",
    "phase": "requirementCheck",
    "kind": "UnavailableTools",
    "message": "Strict mode: the following tools are unavailable: Semgrep, Bandit"
  }],
  "toolResults": [],
  "issues": []
}
```

Stdout stays valid JSON, so match on `errors[].kind == "UnavailableTools"` rather than the exit code, which is overloaded (conflicting flags and an unresolvable `--diff` base also exit `2`).

### Flag exclusivity

`--inspect`, `--install-dependencies`, and `--fail-if-missing` are mutually exclusive — combining any two fails with `Error: Flags --inspect, --install-dependencies, and --fail-if-missing are mutually exclusive`. Use them in sequence:

```bash
codacy-analysis analyze --inspect --output-format json                    # 1. what's ready?
codacy-analysis analyze --install-dependencies --output-format json       # 2. install + run
codacy-analysis analyze --staged --fail-if-missing --output-format json   # 3. gate
```

### The check is repo-wide, not diff-scoped

Strict mode checks every tool enabled in the config, whatever files are being analyzed — a Python-only staged diff still fails if the Ruby toolchain is missing. `--tool` narrows it, which keeps a gate usable when only part of the toolchain is installed:

```bash
# Passes despite missing Ruby tooling, because only Trivy is required
codacy-analysis analyze --diff main --tool Trivy --fail-if-missing --output-format json
```

Prefer installing the full toolchain, and state which tools the gate actually covered.

## What strict mode does not catch

It only detects tools that are *configured but unavailable*. A config with no tools — which a plain `init` can produce — passes:

```console
$ jq '.tools' .codacy/codacy.config.json
[]
$ codacy-analysis analyze --staged --fail-if-missing --output-format json
EXIT=0
{"issues": 0, "errors": [], "toolResults": [], "capability": {"ready": [], "unavailable": []}}
```

Exit `0`, no issues, strict mode satisfied, nothing scanned. **Empty `toolResults` is the only reliable signal.**

## Verification checklist

```bash
codacy-analysis analyze --fail-if-missing --output-format json \
  | jq '{blocked: [.errors[].kind], executed: [.toolResults[].toolId], skipped: [.capability.unavailable[].toolId]}'
```

| Observation | Meaning | Action |
|-------------|---------|--------|
| `blocked` non-empty | Strict mode stopped the run | Install the tools; report no result |
| `executed` empty | Nothing was scanned | Treat as **unverified**; re-run `init` |
| `skipped` non-empty (non-strict run) | Partial coverage | Name the gaps in the report |
| `executed` non-empty, no issues | Genuinely clean | Report clean **and list the tools** |

Never report a clean result without naming the tools that produced it: "No issues found" reads identically whether seven scanners passed or seven never started.
