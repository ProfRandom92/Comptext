---
name: comptext-local-autonomy
description: Offline local-only autonomous workflow in CompText.
---

# CompText Local Autonomy Skill

This skill guides the one-unit-at-a-time offline development workflow within the `comptext` repository.

## Safe Autonomous Workflow Loop

Always operate using a strict step-by-step loop:

1. **Inspect**: Read the request, look up existing implementation patterns, and verify the current codebase status.
2. **Plan**: Write down the exact steps to implement, including safety boundaries and validation strategy.
3. **Implement**: Write or edit the code local-only. Focus on exactly one logical unit at a time.
4. **Test**: Run focused tests for the changed files.
5. **Validate**: Run repository-wide checks:
   - `python -m pytest`
   - `git diff --check`
6. **Commit**: If validation passes, create a single clean local commit.
7. **Stop**: Finish and report the status.

## Required Validation
Before finishing or proposing any commit, ensure these commands pass cleanly:
- Focused tests for the modified module
- `python -m pytest` for full suite validation
- `git diff --check` to verify no whitespace or conflict marker issues

## Forbidden Behavior
To ensure local dry-run safety, the following actions are strictly forbidden:
- **No Network / Provider Calls**: Never communicate over network or invoke external LLM provider APIs.
- **No GitHub Writes / PRs**: Do not push branches, open pull requests, merge, or call GitHub APIs.
- **No Secrets / Env Access**: Do not read `.env` files, environment variables, or retrieve secrets.
- **No Server Operations**: Do not start background servers or bind network ports.
- **No Broad Docs Expansion**: Do not bloat or write unnecessary documentation. Keep documentation changes precise.
