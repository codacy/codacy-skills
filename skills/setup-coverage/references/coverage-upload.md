# Coverage Upload — Advanced Scenarios

## Multiple reports for the same language

Upload all at once:
```bash
bash <(curl -Ls https://coverage.codacy.com/get.sh) report \
  -l Java -r report1.xml -r report2.xml -r report3.xml
```

Discover reports dynamically:
```bash
bash <(curl -Ls https://coverage.codacy.com/get.sh) report \
  -l Java $(find . -name 'jacoco*.xml' | sed 's,^, -r ,' | xargs echo)
```

## Sequential partial uploads

When reports are generated in separate CI steps or jobs:
```bash
bash <(curl -Ls https://coverage.codacy.com/get.sh) report --partial -l Java -r report1.xml
bash <(curl -Ls https://coverage.codacy.com/get.sh) report --partial -l Java -r report2.xml
bash <(curl -Ls https://coverage.codacy.com/get.sh) final
```

The `--partial` flag is required on every report. The `final` command must be sent after all partial reports are uploaded. Missing the `final` command causes a "Final Report Not Sent" status.

## Multiple languages from a single report

```bash
bash <(curl -Ls https://coverage.codacy.com/get.sh) report --partial -l Javascript -r report.xml
bash <(curl -Ls https://coverage.codacy.com/get.sh) report --partial -l TypeScript -r report.xml
bash <(curl -Ls https://coverage.codacy.com/get.sh) final
```

## Golang coverage

Go coverage files lack standardized naming, so the parser flag is mandatory:
```bash
go test -coverprofile=coverage.out ./...
bash <(curl -Ls https://coverage.codacy.com/get.sh) report \
  --force-coverage-parser go -r coverage.out
```

## Authentication options

### Repository token (single repo)
```bash
export CODACY_PROJECT_TOKEN=<repository API token>
```

### Account token (multi-repo)
```bash
export CODACY_API_TOKEN=<account API token>
export CODACY_ORGANIZATION_PROVIDER=<gh|gl|bb|ghe|gle|bbe>
export CODACY_USERNAME=<org or username>
export CODACY_PROJECT_NAME=<repo name>
```

## Alternative runners

### Docker
```bash
docker run -v $PWD:/code codacy/codacy-coverage-reporter:latest report -r <report-file>
```

### GitHub Action
```yaml
- uses: codacy/codacy-coverage-reporter-action@v1
  with:
    project-token: ${{ secrets.CODACY_PROJECT_TOKEN }}
    coverage-reports: <report-file>
```

### CircleCI Orb
```yaml
orbs:
  codacy: codacy/coverage-reporter@13
```

### Alpine Linux (no bash)
```bash
wget -qO - https://coverage.codacy.com/get.sh | sh -s -- report -r <report-file>
```

### Manual binary download (Linux amd64)
```bash
LATEST_VERSION="$(curl -Ls https://artifacts.codacy.com/bin/codacy-coverage-reporter/latest)"
curl -Ls -o codacy-coverage-reporter \
  "https://artifacts.codacy.com/bin/codacy-coverage-reporter/${LATEST_VERSION}/codacy-coverage-reporter-linux"
chmod +x codacy-coverage-reporter
./codacy-coverage-reporter report -r <report-file>
```

### Java JAR
```bash
LATEST_VERSION="$(curl -Ls https://artifacts.codacy.com/bin/codacy-coverage-reporter/latest)"
curl -Ls -o codacy-coverage-reporter-assembly.jar \
  "https://artifacts.codacy.com/bin/codacy-coverage-reporter/${LATEST_VERSION}/codacy-coverage-reporter-assembly.jar"
java -jar codacy-coverage-reporter-assembly.jar report -r <report-file>
```

## Behavior notes

- Multiple reports covering the same line count as a single covered line (no double-counting)
- For JaCoCo, the merge mojo can combine data before upload: `mvn jacoco:merge jacoco:report`
- Coverage must be uploaded for every push for PR analysis to work correctly
- File paths in reports must be relative to the repository root

## Codacy Self-Hosted

```bash
export CODACY_API_BASE_URL=<your Codacy instance URL>
export CODACY_REPORTER_VERSION=13.10.15
```

Codacy Self-Hosted 15.0.0 requires Coverage Reporter version 13.10.15.
