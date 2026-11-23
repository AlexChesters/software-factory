# Alex's Software Factory

## Dependencies
- Claude Platform API access
- Typesafe AI API access

## Usage

### Plan
```yaml
- name: Create plan
  uses: AlexChesters/software-factory/actions/plan@main
  with:
    github-token: ${{ ??? }} # GitHub token that can be used to write a comment on an existing issue
    anthropic-token: ${{ ??? }} # JWT from GitHub Actions OIDC (https://platform.claude.com/docs/en/manage-claude/wif-reference#environment-variables)
```
