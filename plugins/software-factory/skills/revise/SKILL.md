---
name: revise
description: Address a specific GitHub pull request review in the current checkout.
disable-model-invocation: true
---

Read [the revision instructions](references/prompt.md) from this skill's directory. Apply them to the supplied review feedback in the current checkout. Use the supplied pull request details and diff context to interpret the feedback.

Commit the changes made for the review and push the commit to the pull request's head branch.
