---
name: review
description: Review a checkout with Software Factory and report findings against a supplied Git base ref.
disable-model-invocation: true
---

Read [the review instructions](references/prompt.md) from this skill's directory. Resolve the Git base ref supplied by the user and compare the checkout against its merge base with `HEAD`. Include staged and unstaged changes and relevant untracked files. Read the supplied base ref's `AGENTS.md` from Git when present. If the base ref is missing or cannot be resolved, ask the user for it.

Apply the review instructions to those inputs and report findings in chat. Use read-only operations in the checkout.
