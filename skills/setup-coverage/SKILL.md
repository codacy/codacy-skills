---
name: setup-coverage
description: Sets up test coverage reporting in a repository and configures upload to Codacy. Detects testing frameworks, CI/CD pipelines, and coverage gaps, then adds the missing pieces to generate and upload coverage reports. Use when the user wants to set up coverage, add coverage reporting, integrate coverage with Codacy, or fix missing coverage uploads.
license: MIT
metadata:
  author: Codacy
  version: 1.0.0
---

# Setup Coverage

This skill sets up test coverage reporting in a repository and configures automatic upload to Codacy. It detects what exists, identifies what is missing, and fills the gaps.

## Prerequisites

- `CODACY_PROJECT_TOKEN` or `CODACY_API_TOKEN` must be available for coverage uploads (see [Authentication](#authentication))
- The repository must be added to Codacy

## Workflow

```
Coverage Setup Progress:
- [ ] Step 1: Detect testing setup
- [ ] Step 2: Detect CI/CD pipeline
- [ ] Step 3: Identify coverage gaps
- [ ] Step 4: Add coverage generation
- [ ] Step 5: Add Codacy coverage upload
- [ ] Step 6: Verify the setup
```

### Step 1: Detect testing setup

Scan the repository to identify:

- **Languages** in use (check file extensions, build files, package manifests)
- **Test frameworks** (look for test directories, test files, framework configs):
  - JavaScript/TypeScript: Jest, Vitest, Mocha, NYC/Istanbul, c8
  - Python: pytest, unittest, coverage.py
  - Java/Kotlin: JUnit, JaCoCo, Maven Surefire/Failsafe
  - Go: native `go test`
  - Ruby: RSpec, SimpleCov, Minitest
  - C#/.NET: xUnit, NUnit, MSTest, Coverlet, dotCover
  - Scala: sbt-jacoco, scoverage
  - PHP: PHPUnit
  - Swift/Obj-C: XCTest, Xcode Code Coverage
- **Existing coverage configuration** (NYC config, Jest `collectCoverage`, `pytest.ini` coverage settings, JaCoCo plugin in pom.xml/build.gradle, etc.)
- **Existing coverage reports** (look for `coverage/`, `lcov.info`, `cobertura.xml`, `jacoco*.xml`, etc.)

Report findings to the user before proceeding.

### Step 2: Detect CI/CD pipeline

Identify which CI/CD system is in use:

| CI/CD | Detection files |
|-------|-----------------|
| GitHub Actions | `.github/workflows/*.yml` |
| GitLab CI | `.gitlab-ci.yml` |
| CircleCI | `.circleci/config.yml` |
| Travis CI | `.travis.yml` |
| Bitbucket Pipelines | `bitbucket-pipelines.yml` |
| Jenkins | `Jenkinsfile` |
| Azure DevOps | `azure-pipelines.yml` |

Read the CI config to understand:
- Which step runs tests
- Whether coverage is already being generated
- Whether there is already a coverage upload step
- What environment variables or secrets are configured

### Step 3: Identify coverage gaps

Based on steps 1 and 2, determine what is missing:

1. **No tests at all** — inform the user that tests are needed first. Offer to set up the testing framework skeleton but clarify that actual tests must be written.
2. **Tests exist but no coverage generation** — coverage tooling needs to be added (Step 4).
3. **Coverage is generated but not uploaded to Codacy** — upload step needs to be added (Step 5).
4. **Coverage is generated and uploaded but not working** — troubleshoot using the [Troubleshooting](#troubleshooting) section.

Present the gap analysis to the user and confirm the plan before making changes.

### Step 4: Add coverage generation

Add the minimal configuration to generate coverage reports in a format Codacy supports. Choose the format based on the language and tooling. See [references/coverage-formats.md](references/coverage-formats.md) for the full format reference.

#### Language-specific setup

**JavaScript/TypeScript (Jest):**
```json
// In package.json or jest.config.js
{
  "collectCoverage": true,
  "coverageReporters": ["lcov"]
}
```
Or run: `npx jest --coverage --coverageReporters=lcov`

**JavaScript/TypeScript (Vitest):**
```js
// vitest.config.ts
{ test: { coverage: { reporter: ['lcov'] } } }
```

**Python (pytest + coverage.py):**
```bash
pip install pytest-cov
pytest --cov --cov-report=xml:cobertura.xml
```

**Java (Maven + JaCoCo):**
Add the JaCoCo Maven plugin to `pom.xml`:
```xml
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <execution>
      <goals><goal>prepare-agent</goal></goals>
    </execution>
    <execution>
      <id>report</id>
      <phase>test</phase>
      <goals><goal>report</goal></goals>
    </execution>
  </executions>
</plugin>
```

**Java (Gradle + JaCoCo):**
```gradle
plugins { id 'jacoco' }
jacocoTestReport { dependsOn test }
```
Run: `./gradlew test jacocoTestReport`

**Go:**
```bash
go test -coverprofile=coverage.out ./...
```

**Ruby (SimpleCov):**
```ruby
# At the top of spec/spec_helper.rb or test/test_helper.rb
require 'simplecov'
SimpleCov.start
SimpleCov.formatter = SimpleCov::Formatter::CoberturaFormatter
```
Requires `simplecov` and `simplecov-cobertura` gems.

**C#/.NET (Coverlet):**
```bash
dotnet test --collect:"XPlat Code Coverage" -- DataCollectionRunSettings.DataCollectors.DataCollector.Configuration.Format=cobertura
```

**Scala (sbt-jacoco):**
Add to `project/plugins.sbt`:
```scala
addSbtPlugin("com.github.sbt" % "sbt-jacoco" % "3.5.0")
```
Run: `sbt jacoco`

**PHP (PHPUnit):**
```bash
phpunit --coverage-clover clover.xml
```

### Step 5: Add Codacy coverage upload

Add a coverage upload step to the CI/CD pipeline **after** the test/coverage step.

#### Authentication

The upload requires one of:

**Option A — Repository token (single repo, simpler):**
- Set `CODACY_PROJECT_TOKEN` as a CI/CD secret
- Obtain from: Codacy > Repository Settings > Coverage > Repository API Token

**Option B — Account token (multiple repos):**
- Set these CI/CD secrets:
  - `CODACY_API_TOKEN` — from Codacy > My Account > Access Management
  - `CODACY_ORGANIZATION_PROVIDER` — `gh`, `gl`, or `bb`
  - `CODACY_USERNAME` — organization or username
  - `CODACY_PROJECT_NAME` — repository name

Always remind the user to add the appropriate token as a CI/CD secret.

#### Upload command

The standard upload command:
```bash
bash <(curl -Ls https://coverage.codacy.com/get.sh) report -r <coverage-report-file>
```

For **Go** coverage, add the parser flag:
```bash
bash <(curl -Ls https://coverage.codacy.com/get.sh) report \
  --force-coverage-parser go -r coverage.out
```

For **multiple reports** (e.g., monorepos or multi-module projects):
```bash
bash <(curl -Ls https://coverage.codacy.com/get.sh) report \
  -r report1.xml -r report2.xml
```

Or use partial uploads:
```bash
bash <(curl -Ls https://coverage.codacy.com/get.sh) report --partial -r report1.xml
bash <(curl -Ls https://coverage.codacy.com/get.sh) report --partial -r report2.xml
bash <(curl -Ls https://coverage.codacy.com/get.sh) final
```

#### CI/CD-specific integration

**GitHub Actions:**
```yaml
- name: Upload coverage to Codacy
  env:
    CODACY_PROJECT_TOKEN: ${{ secrets.CODACY_PROJECT_TOKEN }}
  run: bash <(curl -Ls https://coverage.codacy.com/get.sh) report -r <report-file>
```

Or use the official action:
```yaml
- name: Upload coverage to Codacy
  uses: codacy/codacy-coverage-reporter-action@v1
  with:
    project-token: ${{ secrets.CODACY_PROJECT_TOKEN }}
    coverage-reports: <report-file>
```

**GitLab CI:**
```yaml
upload-coverage:
  stage: test
  script:
    - bash <(curl -Ls https://coverage.codacy.com/get.sh) report -r <report-file>
  variables:
    CODACY_PROJECT_TOKEN: $CODACY_PROJECT_TOKEN
```

**CircleCI (using orb):**
```yaml
orbs:
  codacy: codacy/coverage-reporter@13
workflows:
  main:
    jobs:
      - test
      - codacy/upload_coverage:
          requires: [test]
```

**Travis CI:**
```yaml
after_success:
  - bash <(curl -Ls https://coverage.codacy.com/get.sh) report -r <report-file>
```

**Bitbucket Pipelines:**
```yaml
- step:
    name: Upload coverage
    script:
      - bash <(curl -Ls https://coverage.codacy.com/get.sh) report -r <report-file>
```

**Alpine Linux (no bash):**
```bash
wget -qO - https://coverage.codacy.com/get.sh | sh -s -- report -r <report-file>
```

See [references/coverage-upload.md](references/coverage-upload.md) for advanced upload scenarios.

### Step 6: Verify the setup

After making changes:

1. **Confirm the CI config is valid** — check for YAML syntax errors and logical issues
2. **List what the user needs to do manually:**
   - Add `CODACY_PROJECT_TOKEN` (or account token variables) as a CI/CD secret
   - Push the changes to trigger a CI run
   - Check Codacy for coverage data after the pipeline completes
3. **Provide a verification checklist:**
   ```
   After pushing, verify:
   - [ ] CI pipeline passes (tests run, coverage report generated)
   - [ ] Coverage upload step succeeds (no errors in CI logs)
   - [ ] Codacy shows coverage data for the commit
   ```

## Troubleshooting

Common issues and their solutions:

| Status | Cause | Fix |
|--------|-------|-----|
| **Commit Not Found** | Webhook not received or wrong commit SHA | Wait 5-10 min; verify the commit SHA matches |
| **Pending** | File paths in report don't match repo structure | Ensure paths are relative to repo root (e.g., `src/index.js`, not `/home/ci/project/src/index.js`) |
| **Final Report Not Sent** | Used `--partial` without `final` | Add `bash <(curl -Ls https://coverage.codacy.com/get.sh) final` after all partial uploads |
| **Branch Not Enabled** | Coverage uploaded for unanalyzed branch | Enable the branch in Codacy repository settings |
| **No coverage shown on PRs** | Missing coverage for common ancestor commit | Ensure coverage runs on all branches, not just PRs |

## Important notes

- Coverage must be uploaded for **every push** to be useful for PR analysis — configure it to run on all branches, not just main
- For PR coverage metrics, Codacy needs coverage for both the PR head commit **and** the common ancestor commit with the target branch
- File paths in coverage reports must be **relative to the repository root**
- Coverage for multiple languages requires separate `-l <Language>` flags or partial uploads with language specification
