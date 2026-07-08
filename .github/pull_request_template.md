## Description

Briefly describe the purpose of this pull request.

## Safety & Boundaries Verification

Please verify that these changes comply with the CompText safety contract:
- [ ] **No Provider Calls**: This PR does not add or run live provider/routing calls.
- [ ] **No Secrets**: This PR does not read, write, or leak secrets or API keys.
- [ ] **No Network**: This PR does not perform any outbound network calls.
- [ ] **No Production Claims**: This PR does not make any production, security, compliance, or forensic claims.

## Local Validation Results

Please paste the output of the following verification commands below:

- `comptext status --dry-run`
- `comptext doctor --dry-run`
- `python -m pytest`
- `git diff --check`

```text
<Paste validation results here>
```
