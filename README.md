# Alex's Software Factory

## Dependencies
- Claude Platform API access
- Typesafe AI API access

## API

### Plan
```yaml
- name: Create plan
  uses: AlexChesters/software-factory/actions/plan@main
  with:
    github-token: ${{ ??? }} # GitHub token issued by a GitHub app
    anthropic-token: ${{ ??? }} # JWT from GitHub Actions OIDC (https://platform.claude.com/docs/en/manage-claude/wif-reference#environment-variables)
```

### Execute
```yaml
- name: Execute plan
  uses: AlexChesters/software-factory/actions/execute@main
  with:
    github-token: ${{ ??? }} # GitHub token issued by a GitHub app
    github-app-client-id: ${{ ??? }} # Client ID of the GitHub app used to write the plan
    anthropic-token: ${{ ??? }} # JWT from GitHub Actions OIDC (https://platform.claude.com/docs/en/manage-claude/wif-reference#environment-variables)
```

### Review
```yaml
- name: Review change
  uses: AlexChesters/software-factory/actions/review@main
  with:
    github-token: ${{ ??? }} # GitHub token issued by a GitHub app
    anthropic-token: ${{ ??? }} # JWT from GitHub Actions OIDC (https://platform.claude.com/docs/en/manage-claude/wif-reference#environment-variables)
```
