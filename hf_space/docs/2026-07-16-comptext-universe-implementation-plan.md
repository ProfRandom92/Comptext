# CompText Universe Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Turn the existing Hugging Face compression lab into a static CompText Universe explorer with safe context compression, deterministic AIR previews, simulated Evidence previews, contract/capability views, and isolated tests.

**Architecture:** Keep every change under `hf_space/**`. The Space loads a committed static snapshot and never reads GitHub at runtime. Gradio composes read-only Universe views with the existing fail-closed LLMLingua pipeline; only compression receives ZeroGPU allocation.

**Tech Stack:** Python 3.10, Gradio 5.44.1, pandas, LLMLingua 0.2.2, PyTorch 2.8.0, pytest.

## Global Constraints

- Modify only `hf_space/**`.
- No provider calls, repository writes, runtime GitHub access, secrets, persistence, or execution of generated AIR.
- Mark the product state as `local-dry-run-mvp` and previews as non-executable/simulated.
- Compression must return the exact original input whenever safety or minimum-reduction gates fail.
- ZeroGPU is used only for compression callbacks.

---

### Task 1: Static Universe Data and Loader

**Files:**
- Create: `hf_space/data/universe_snapshot.json`
- Create: `hf_space/universe.py`
- Create: `hf_space/tests/test_universe.py`

**Interfaces:**
- Produces: `load_universe() -> dict`, `layers_frame(data) -> pandas.DataFrame`, `capabilities_frame(data) -> pandas.DataFrame`, `skills_frame(data) -> pandas.DataFrame`.

- [ ] Write tests asserting required product status, seven architecture layers, capability statuses, source provenance, and deterministic dataframe columns.
- [ ] Implement the static snapshot and loader.
- [ ] Run `python -m pytest hf_space/tests/test_universe.py -q` and expect PASS.

### Task 2: Deterministic AIR and Evidence Previews

**Files:**
- Create: `hf_space/previews.py`
- Create: `hf_space/tests/test_previews.py`

**Interfaces:**
- Produces: `build_air_preview(text, compression=None) -> dict`, `build_evidence_preview(original, output, decision, metrics) -> dict`, `scan_secrets(text) -> list[str]`.

- [ ] Write tests for file/flag/constraint extraction, disabled execution, simulated Evidence, stable SHA-256 hashes, and secret blocking.
- [ ] Implement deterministic preview builders with no external calls.
- [ ] Run `python -m pytest hf_space/tests/test_previews.py -q` and expect PASS.

### Task 3: Space UI Composition

**Files:**
- Modify: `hf_space/app.py`
- Modify: `hf_space/README.md`

**Interfaces:**
- Consumes: Universe loader, hybrid compression, AIR/Evidence previews.
- Produces: Gradio tabs `Overview`, `Architecture`, `Capabilities`, `Compression Lab`, `AIR & Evidence`, `Skills`, and `Benchmarks`.

- [ ] Replace the single-purpose UI with the modular Universe composition while preserving compression and benchmark behavior.
- [ ] Add explicit maturity and safety notices.
- [ ] Update Space metadata and documentation.
- [ ] Run `python -m compileall -q hf_space` and expect exit code 0.

### Task 4: Regression and Boundary Tests

**Files:**
- Create: `hf_space/tests/test_boundaries.py`

**Interfaces:**
- Verifies: no files referenced outside the allowed snapshot provenance; no provider-key configuration; preview execution is always disabled; Evidence is always simulated.

- [ ] Add boundary tests.
- [ ] Run `python -m pytest hf_space/tests -q` and expect PASS.
- [ ] Verify the branch diff contains only `hf_space/**`.

### Task 5: Review and Delivery

- [ ] Compare branch against `main` and confirm every changed path begins with `hf_space/`.
- [ ] Create a pull request summarizing features, safety boundaries, and validation.
- [ ] Merge only after the path-boundary check passes.
