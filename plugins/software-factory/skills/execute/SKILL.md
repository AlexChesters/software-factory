---
name: execute
description: Implement an approved Software Factory plan in the current checkout and verify the resulting changes.
disable-model-invocation: true
---

Read [the execution instructions](references/prompt.md) from this skill's directory. Use the plan file named by the user as the approved plan. If the path is missing or unreadable, ask the user for the plan.

Apply the execution instructions in the current checkout. Leave the changes in the working tree for inspection and report the outcome in chat.
