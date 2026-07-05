# CompText Hooks System

Hooks are planned contracts for auditable workflow events. No runtime hook engine is implemented yet.

## Planned events

- `WorkspaceOpen`
- `WorkspaceClose`
- `RunStart`
- `RunEnd`
- `ToolStart`
- `ToolEnd`
- `DiffReady`
- `TestsPassed`
- `TestsFailed`
- `ReviewCommentFound`
- `ReviewCommentResolved`
- `MergeReady`
- `ApprovalGranted`
- `ApprovalDenied`
- `ProviderChanged`
- `ModelChanged`

## Contract intent

Hooks should let CompText record or react to important workflow moments without hiding behavior from the user.

A future hook contract should define:

- event type
- actor
- timestamp
- workspace
- redaction rules
- input summary
- output summary
- approval requirement
- evidence reference
- status

## Safety requirements

- Hooks must be safe and auditable.
- Hooks must not read or emit secrets.
- Hooks must not perform provider calls unless explicitly configured and approved.
- Hooks must not auto-push, auto-merge, release, or run destructive commands.
- Hook output should be suitable for Evidence after redaction.
