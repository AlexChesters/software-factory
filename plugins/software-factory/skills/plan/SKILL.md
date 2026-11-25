---
name: plan
description: Write a Software Factory implementation plan from a task description for later approval and execution.
disable-model-invocation: true
---

Read [the planning instructions](references/prompt.md) from this skill's directory and apply them to the task in the file named by the user. Use the current checkout for repository context.

Write the plan to `plan.md` in the current checkout or to the path the user requests. If that file already exists, ask before replacing it. Return the plan's path or report what needs clarification. Limit workspace edits to the plan file.
