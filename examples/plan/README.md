# Plan

You can see a complete GitHub Actions workflow example at [`plan.yml`](./plan.yml). This workflow assumes it has
been started from a GitHub issue being labelled (either at issue creation or subsequently) with the label
`factory:plan`.

The following issue template may be useful if you're struggling for inspiration:
```yaml
name: Factory task
description: A scoped unit of work for the factory to plan and execute
labels: ["factory:plan"]
body:
  - type: input
    id: goal
    attributes:
      label: Goal
      description: Describe the desired outcome in 1-3 sentences.
    validations:
      required: true
  - type: textarea
    id: description
    attributes:
      label: Description
      description: Any further detail you think is useful.
    validations:
      required: false
  - type: textarea
    id: constraints
    attributes:
      label: Constraints
      description: List the constraints the agent must follow and what it should leave untouched.
    validations:
      required: true
  - type: textarea
    id: done-definition
    attributes:
      label: Definition of done
      description: Define how to verify the task is complete.
    validations:
      required: true
```
