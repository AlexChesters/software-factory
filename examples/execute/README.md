# Execute

You can see a complete GitHub Actions workflow example at [`execute.yml`](./execute.yml). This workflow assumes it
has been started from a GitHub issue comment. This comment must:
- Not be on a pull request
- Be on an issue with a `factory:plan` labelled attached
- Start with `/approve`
- Be made by the owner of the repository
  - You may wish to be more liberal with this, e.g. allowing prior contributors
