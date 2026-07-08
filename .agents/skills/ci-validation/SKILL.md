---
name: ci-validation
description: Manage GitHub Actions validation workflows and Python compatibility.
---

# CI Validation Skill

Manage and edit local-validation-only GitHub Actions workflows and matrix configurations.

## Use when
- Editing or creating local-validation GitHub Actions workflows (e.g. `.github/workflows/ci.yml`).
- Modifying offline validation command configurations in documentation or workflows.
- Testing Python version matrix compatibility (`3.10`, `3.11`, `3.12`).
- Adding or updating CI badges or validation wording in contributor guidelines.

## Do not use when
- Configuring hosted environments, CD pipelines, or deployment targets.
- Setting up release automation, package publishing, or library uploading.
- Injecting LLM provider credentials or environment secrets into the CI environment.
- Weakening or disabling existing unit tests to bypass validation errors.

## Inputs
- GitHub Actions workflow configurations: `.github/workflows/ci.yml`.
- Dependencies and options configuration: `pyproject.toml`.
- Verification suites: `tests/`.

## Safety boundaries
- Local dry-run checks and offline validation only.
- Strict least-privilege permissions (`contents: read`).
- No provider credentials or environment secrets.
- No network connections except for GitHub Actions dependency installation.
- No automatic branch merging, pushes, or pull request creation.

## Workflow
1. Verify that the workflow file triggers on the desired branches/actions (`push`, `pull_request`).
2. Confirm the permission block uses least-privilege `contents: read`.
3. Check the Python version matrix (`3.10`, `3.11`, `3.12`) is intact.
4. Run all validation steps locally before committing changes to the workflow.

## Validation
- `python -m pip install -e ".[dev]"`
- `comptext status --dry-run`
- `comptext doctor --dry-run`
- `python -m pytest`
- `git diff --check`

## Final report
- Summary of workflow modifications, matrix configuration status, local test results, and validation checklist.
