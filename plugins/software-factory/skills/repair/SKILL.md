---
name: repair
description: Diagnose and fix failed GitHub pull request checks in the current checkout using check results, logs, or annotations.
disable-model-invocation: true
---

Read [the repair instructions](references/prompt.md). Use the supplied failure details when available. Otherwise, look up the supplied PR number or URL, or resolve the PR for the current branch.

Apply the repair instructions in the current checkout. Leave changes in the working tree and report the outcome in chat.
