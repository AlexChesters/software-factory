# Alex's Software Factory

## Dependencies
| Dependency    | Used for      |
| ------------- | ------------- |
| Cloud Platform API  | Primary LLM for creating plans, executing changes and reviewing changes  |
| TypeSafe API  | System One model decision for which model is used for the Claude Platform (only used when no model is specified) |

## Usage

The factory is built around several flows, or lines to keep up the factory anology.

### Issue -> Plan
The [`plan`](./actions/plan/action.yml) action is designed to be invoked with reference to a particular GitHub
issue. You may choose to invoke it for all GitHub issues or, more commonly, when issues are labelled with a
particular label.

The plan station will write its proposed plan for the change back to the invoking issue.

N.B. You do not want to create a workflow that is triggered for both the `labeled` and `created` events. When a
GitHub issue is created with a particular label, the workflow will be invoked twice. If you are making use of
labels to run the factory against a subset of GitHub issues, stick to the `labeled` event.

### Plan -> PR
The [`execute`](./actions/execute/action.yml) action is also designed to be invoked with reference to a particular
issue. You should invoke it in response to an issue comment (e.g. `/approve`) which indicates the plan should be
taken and used to create a pull request.

The execution station will create a pull request when the change is ready.

N.B. You should ensure that the comment indicating the plan should be executed originates from a trusted source.
The `issue_comment` actions triggers allow you to assert on `github.event.comment.author_association`.

### PR -> Review
The [`review`](./actions/review/action.yml) station is designed to be invoked with a reference to a particular PR.
This PR may or may not have been written by the factory.

The review station will comment on the pull request with its findings, but it will not explicitly approve/request
changes.

## Permissions and credentials

### GitHub
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

### Anthropic
The factory makes use of Anthropic's
[Workload Identity Federation](https://platform.claude.com/docs/en/manage-claude/workload-identity-federation).
As a result, you don't need to create an API key but you do need to create a service account and a federation
identity rule.

You don't need to explicitly provide these to the action, instead set the following environment variables in your
workflow:
- `ANTHROPIC_ORGANIZATION_ID`
- `ANTHROPIC_SERVICE_ACCOUNT_ID`
- `ANTHROPIC_FEDERATION_RULE_ID`

# TypeSafeAI
The factory's access to the TypeSafe AI API is controlled with an API key. Your workflow is responsible for making
this API key available in the environment variable `TYPESAFE_API_KEY`.

The API key is only required when no `model` is given. If you specify a `model`, TypeSafe is not used.

## API

Every station accepts the following optional inputs:
- `model`: the Claude model to use. When set, TypeSafe is not used to choose a model.
- `effort`: the effort level to use. Optional, and defaults to `medium` when a `model` is set.

An `effort` cannot be specified without a `model`; this is rejected. Combinations of model and effort that are not
valid are reported by the Claude platform.

### Plan
```yaml
- name: Create plan
  uses: AlexChesters/software-factory/actions/plan@main
  with:
    github-token: ${{ ??? }} # GitHub token issued by a GitHub app
    model: claude-sonnet-5-5 # optional, skips TypeSafe model selection
    effort: medium # optional, requires model, defaults to medium
```

### Execute
```yaml
- name: Execute plan
  uses: AlexChesters/software-factory/actions/execute@main
  with:
    github-token: ${{ ??? }} # GitHub token issued by a GitHub app
    model: claude-sonnet-5-5 # optional, skips TypeSafe model selection
    effort: medium # optional, requires model, defaults to medium
```

### Review
```yaml
- name: Review change
  uses: AlexChesters/software-factory/actions/review@main
  with:
    github-token: ${{ ??? }} # GitHub token issued by a GitHub app
    model: claude-sonnet-5-5 # optional, skips TypeSafe model selection
    effort: medium # optional, requires model, defaults to medium
```

## Examples
You can see complete examples for each station in the [`examples/`](./examples/) folder.
