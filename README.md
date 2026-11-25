# Alex's Software Factory

## Overview

The factory is built around several flows, or lines to keep up the factory analogy.

### Issue -> Plan
The [`plan`](./actions/plan/action.yml) action is designed to be invoked with reference to a particular GitHub
issue. You may choose to invoke it for all GitHub issues or, more commonly, when issues are labelled with a
particular label.

The plan station will write its proposed plan for the change back to the invoking issue.

Use the `opened` activity type of the `issues` event to create a plan for every new issue. To create a plan only
for issues with a specific label, use the `labeled` activity type and filter for that label. Don't include both
types or you will see two workflows triggered for issues created with a label.

### Plan -> PR
The [`execute`](./actions/execute/action.yml) action is also designed to be invoked with reference to a particular
issue. To run it after approval, use the `created` activity type of the `issue_comment` event and check for an
approval comment such as `/approve`. The event fires for comments on both issues and pull requests. Add
`!github.event.issue.pull_request` to the job's `if` condition to run only for issue comments.

Execute selects the most recently posted plan comment on the issue from the GitHub App associated with its
installation token, even if the approval refers to an older plan. The execution station will create a pull request
when the change is ready.

N.B. You should ensure that the comment indicating the plan should be executed originates from a trusted source.
Use `github.event.comment.author_association` to check the commenter’s relationship to the repository.

### PR -> Review
The [`review`](./actions/review/action.yml) station is designed to be invoked with a reference to a particular PR.
This PR may or may not have been written by the factory.

The review station will comment on the pull request with its findings, but it will not explicitly approve/request
changes.

### Review -> Revised PR

The [`revise`](./actions/revise/action.yml) action addresses a submitted pull request review that requests
changes. It uses the review summary and inline comments to revise the code, then commits and pushes any
changes to the branch of the existing pull request.

## Usage

### GitHub Actions

The factory is primarily designed to be used in GitHub Actions workflows. The factory is used to build and improve
the factory itself, so take a look at the [`.github`](.github/) folder and this repository's issues and pull
requests to see how the factory can be used.

#### Dependencies
| Dependency    | Used for      |
| ------------- | ------------- |
| Claude Platform API  | Primary LLM for creating plans, implementing changes, reviewing pull requests, and revising changes  |
| TypeSafe API  | System One model decision for which model is used for the Claude Platform (only used when no model is specified) |

#### Permissions and credentials

##### GitHub
The factory assumes that the GitHub credentials it uses have been issued by a
[GitHub application](https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps/about-creating-github-apps).
The Plan and Execute stations require installation tokens minted from the same GitHub App.
The Execute station uses its token to verify that the same app the Execute station runs as is the same app that
produced the plan.

The application in question needs the following permissions:
- Read access to metadata
- Read and write access to code, issues, and pull requests

You can mint tokens with the minimum permissions required for the task at hand (e.g. the planning station only
needs write access to issues, not code/pull requests).

##### Anthropic
The factory makes use of Anthropic's
[Workload Identity Federation](https://platform.claude.com/docs/en/manage-claude/workload-identity-federation).
As a result, you don't need to create an API key but you do need to create a service account and a federation
identity rule.

You don't need to explicitly provide these to the action, instead set the following environment variables in your
workflow:
- `ANTHROPIC_ORGANIZATION_ID`
- `ANTHROPIC_SERVICE_ACCOUNT_ID`
- `ANTHROPIC_FEDERATION_RULE_ID`

Ensure your workflow has the `id-token: write` permission. The factory use this permission to request a GitHub
OIDC token for Anthropic authentication.

###### TypeSafeAI
The factory's access to the TypeSafe AI API is controlled with an API key. Your workflow is responsible for making
this API key available in the environment variable `TYPESAFE_API_KEY`.

The API key is only required when no `model` is given. If you specify a `model`, TypeSafe is not used.

#### API

Every station accepts the following optional inputs:
- `model`: the Claude model to use. When set, TypeSafe is not used to choose a model.
- `effort`: the effort level to use. Optional, and defaults to `medium` when a `model` is set.

An `effort` cannot be specified without a `model`. Claude validates the model and effort combination.

Execute and Revise optionally accept `allowed-bash-commands`: one bash command per line. Each line becomes a
`Bash(<command>)` allow rule. Plan and Review stay read-only. The list is not exclusive.

##### Plan
```yaml
- name: Create plan
  uses: AlexChesters/software-factory/actions/plan@v0
  with:
    github-token: ${{ ??? }} # GitHub token issued by a GitHub app
    model: claude-sonnet-5-5 # optional, skips TypeSafe model selection
    effort: medium # optional, requires model, defaults to medium
```

##### Execute
```yaml
- name: Execute plan
  uses: AlexChesters/software-factory/actions/execute@v0
  with:
    github-token: ${{ ??? }} # GitHub token issued by a GitHub app
    model: claude-sonnet-5-5 # optional, skips TypeSafe model selection
    effort: medium # optional, requires model, defaults to medium
    allowed-bash-commands: |
      npm t
      npm test
      npm run build
```

##### Review
Run the review action on a `pull_request` event. Before running the action, check out the repository with enough
Git history to find the merge base and compute the pull request diff. In the
[factory itself](.github/workflows/factory-review.yml), we set `fetch-depth: 0` to fetch the full history.

The pull request's base commit must contain an `AGENTS.md` file at the repository root.

```yaml
- name: Review change
  uses: AlexChesters/software-factory/actions/review@v0
  with:
    github-token: ${{ ??? }} # GitHub token issued by a GitHub app
    model: claude-sonnet-5-5 # optional, skips TypeSafe model selection
    effort: medium # optional, requires model, defaults to medium
```

##### Revise

Run the revise action on `pull_request_review` with `types: [submitted]`. Gate the job on
`github.event.review.state == 'changes_requested'` and check `github.event.review.author_association` to
restrict execution to trusted reviewers. The factory's workflow accepts reviews from the repository owner.

Check out the pull request's exact head commit before running the action. The GitHub App installation token
must be able to read the pull request's review comments and push to its source branch.

```yaml
- uses: actions/checkout@v7
  with:
    repository: ${{ github.event.pull_request.head.repo.full_name }}
    ref: ${{ github.event.pull_request.head.sha }}
    persist-credentials: false
- name: Revise pull request
  uses: AlexChesters/software-factory/actions/revise@v0
  with:
    github-token: ${{ steps.factory-app.outputs.token }} # GitHub App installation token
    model: claude-sonnet-5-5 # optional, skips TypeSafe model selection
    effort: medium # optional, requires model, defaults to medium
    allowed-bash-commands: |
      npm t
      npm test
      npm run build
```

### Codex and Claude Code

Install the Software Factory plugin to get all three stations in your local harness.

```sh
# Codex
codex plugin marketplace add AlexChesters/software-factory
codex plugin add software-factory@alexchesters

# Claude Code
claude plugin marketplace add AlexChesters/software-factory
claude plugin install software-factory@alexchesters
```

To install from a local Software Factory checkout, run the same commands from its root and use `"$PWD"` as the marketplace source.

| Station | Codex skill | Claude Code command |
| --- | --- | --- |
| Write a plan | `$software-factory:plan task.md` | `/software-factory:plan task.md` |
| Implement an approved plan | `$software-factory:execute plan.md` | `/software-factory:execute plan.md` |
| Review changes against a base ref | `$software-factory:review main` | `/software-factory:review main` |

Run the skills in the checkout you want to work on. Planning writes `plan.md`. Review or edit that file before explicitly running the execution skill. Execution leaves the changes in your working tree, and review reports its findings in chat.
