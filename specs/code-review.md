# Code Review

Create a new skill that:
- tells Claude to use Codacy data whenever it reviews pull requests (however it is called, via code-review skill, CodeRabbit, etc.)
- when no pre existing skill is used for code review, follows some guidelines to review the code based on Codacy data (issues, security, coverage, duplication, etc.)

In both cases, the skill should also, on top of the review:
- if there is information about the ticket or issue (Jira, GitHub, Linear, local spec, whatever), fetch its information and use it to verify changes are aligned with the ticket or issue.
- fetch data of the pull request (GitHub, GitLab, Bitbucket, etc.), its title and description, use it to verify changes are aligned with the pull request.
- make suggestions to improve both the ticket and the pull request metadata if needed.
- present a proposed test plan to verify the changes are working as expected; once the tests have been suggested, check if the tests are already present in the pull request, by checking the code and Codacy's coverage data

