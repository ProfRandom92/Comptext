# Codex Desktop Prompts

These reusable prompts keep CompText Codex Desktop sessions aligned with the repository workflow. Replace placeholder branch names and task names before use.

## Start Next Task

```text
Implement the next CompText task.

Repository: ProfRandom92/Comptext
Base branch: main
Create branch: codex/<task-name>

Before editing:
- fetch the latest main
- switch to main
- update main to origin/main
- create the task branch from main

Use the CompText Token Saver plugin if available:
- check compact project state first
- use Codebase Memory before broad file reads
- run noisy commands through RTK when available
- summarize command output

Keep the change scoped. Do not push, auto-push, merge, or open a PR unless I explicitly ask.
```

## Fix Review Comments

```text
Fix the review comments on the current CompText pull request.

Requirements:
- inspect all Gemini/review threads
- fix every actionable in-scope comment
- resolve every completed review thread
- do not resolve unresolved, ambiguous, blocked, or out-of-scope comments
- summarize remaining blockers

Use the CompText Token Saver plugin if available, and keep command output summarized.
Do not push, auto-push, merge, or enable auto-merge unless I explicitly ask.
```

## Prepare PR

```text
Prepare this CompText branch for a pull request against main.

Check:
- worktree status
- branch name and base branch
- diff scope
- relevant tests or documentation validation
- remaining risks and follow-up

Draft the PR body with:
- Summary
- What changed
- Boundaries
- Validation
- Risks
- Follow-up

Do not push or open the PR unless I explicitly ask.
```

## Merge Readiness Check

```text
Check whether this CompText pull request is ready to merge into main.

Review:
- branch is current enough with main or divergence is understood
- all actionable review comments are addressed
- every completed review thread is resolved
- unresolved, ambiguous, blocked, or out-of-scope threads remain open and are summarized
- required checks and relevant tests are passing or failures are explained
- merge strategy is merge commit unless I explicitly request otherwise

Do not merge, enable auto-merge, or push unless I explicitly ask.
```
