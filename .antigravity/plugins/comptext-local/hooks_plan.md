# CompText local hooks plan

This document details the planned events and pre/post action hooks for the `comptext-local` plugin.

## Planned hooks
To prevent unintended execution or automatic mutation, hooks are documented as planned only and are not active in `hooks.json`.

### 1. `pre-final-report`
- **Purpose**: Verify that `/diff` or `git status` checks have been done before writing the final report.
- **Allowed action**: Prompt a check reminder list to the developer.
- **Trigger**: Prior to generating final response to user.

### 2. `diff-reminder`
- **Purpose**: Remind the developer to run `git diff --check` to find trailing whitespace.
- **Allowed action**: Text notification inside TUI status line.
- **Trigger**: Immediately after code edit operations.

### 3. `verify-reminder`
- **Purpose**: Prompt to run `comptext verify --dry-run` when files under `schemas/` or `examples/` are modified.
- **Allowed action**: Print a verification reminder block.
- **Trigger**: Immediately after writing JSON files.
