# Contributing to CompText

Thank you for your interest in contributing! CompText is currently a developer preview and local dry-run MVP.

## Developer Boundaries & Constraints

Please keep in mind the following boundaries during local development:
- **No Provider Calls**: Do not perform live LLM provider or routing queries.
- **No Secrets**: Never read, store, or log secrets, API keys, or raw environment variables.
- **No Network**: Do not make outbound network requests or call external APIs (such as GitHub) unless explicitly required and approved.
- **No Production Claims**: Avoid making production, security, compliance, or forensic claims.

## Local Setup and Validation

Before proposing changes, ensure you have set up your development environment and run the validation suite:

1. **Install Development Dependencies**
   ```bash
   python -m pip install -e ".[dev]"
   ```

2. **Verify CLI Status**
   ```bash
   comptext status --dry-run
   ```

3. **Run Doctor Diagnostics**
   ```bash
   comptext doctor --dry-run
   ```

4. **Run Unit Tests**
   ```bash
   python -m pytest
   ```

5. **Format/Style Check**
   ```bash
   git diff --check
   ```

All checks must pass cleanly. These same validation checks are automatically run on GitHub Actions CI for every push and pull request.
