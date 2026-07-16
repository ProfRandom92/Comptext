# CompText Universe + Compression Lab Design

Date: 2026-07-16
Status: Approved for implementation
Scope boundary: **Only `hf_space/**` may change.**

## 1. Goal

Turn the existing Hugging Face Space into a safe public CompText showcase and context-engineering laboratory without modifying or emulating the local CompText runtime.

The Space has three roles:

1. **Universe Explorer** — explain architecture, capabilities, contracts, skills, maturity, and safety boundaries.
2. **Context Engineering Lab** — preserve the existing fail-closed hybrid compression and add CompText-specific profiles and diagnostics.
3. **Contract Preview Sandbox** — generate deterministic, non-executable AIR and simulated Evidence previews.

The Space is not a hosted CompText runtime. It performs no provider calls, repository writes, agent execution, MCP activity, or persistent evidence storage.

## 2. Hard Scope Boundary

Allowed changes:

- `hf_space/**`

Forbidden changes:

- `.github/**`
- `modules/**`
- `schemas/**`
- `examples/**`
- `docs/**` outside `hf_space/docs/**`
- CLI, runtime, gateway, provider, TUI, plugin, skill, and workspace-state implementation

Repository content outside `hf_space/**` may be read to create a manually curated static snapshot, but it must not be modified.

## 3. Architecture

```text
Curated CompText source knowledge
        |
        v
hf_space/data/*.json
        |
        v
Universe loader + validation
        |
        +--> Overview / Architecture / Capabilities / Skills / Contracts
        +--> AIR Preview / Simulated Evidence Preview
        +--> Compression Lab / Benchmarks
```

The deployed Space performs no live GitHub reads. All CompText knowledge used by the UI is shipped as static JSON under `hf_space/data/`.

## 4. Modules

```text
hf_space/
├── app.py
├── README.md
├── requirements.txt
├── compression.py
├── protected_segments.py
├── safety_checks.py
├── metrics.py
├── benchmark_cases.json
├── universe/
│   ├── __init__.py
│   ├── loader.py
│   ├── models.py
│   └── validation.py
├── previews/
│   ├── __init__.py
│   ├── air_preview.py
│   ├── evidence_preview.py
│   └── redaction.py
├── ui/
│   ├── __init__.py
│   ├── overview.py
│   ├── architecture.py
│   ├── capabilities.py
│   ├── compression_lab.py
│   ├── previews.py
│   └── contracts.py
├── data/
│   ├── universe_snapshot.json
│   ├── architecture_graph.json
│   ├── capability_matrix.json
│   ├── skills_catalog.json
│   ├── contracts_catalog.json
│   └── provenance_manifest.json
├── tests/
│   ├── test_universe_data.py
│   ├── test_air_preview.py
│   ├── test_evidence_preview.py
│   ├── test_redaction.py
│   └── test_compression_profiles.py
└── docs/
    └── 2026-07-16-comptext-universe-design.md
```

`app.py` remains the composition root. Domain logic belongs in focused modules.

## 5. Universe Data Model

### 5.1 Product snapshot

Required fields:

- snapshot version
- product name
- maturity status (`local-dry-run-mvp`)
- core claim
- source repository
- source commit
- generated timestamp
- explicit limitations

### 5.2 Architecture entities

Each layer or service contains:

- stable ID
- display name
- purpose
- maturity status
- inputs
- outputs
- relationships
- security notes
- source references

Allowed maturity vocabulary:

- `implemented`
- `scaffolded`
- `experimental`
- `planned`
- `future`
- `disabled`
- `not_configured`

The UI must never imply that planned or scaffolded functionality is production-ready.

### 5.3 Capability matrix

Each capability records:

- name
- surface
- status
- network requirement
- provider requirement
- mutation behavior
- approval requirement
- summary

## 6. User Experience

Tabs:

1. **Overview** — product claim, maturity, boundaries, snapshot provenance.
2. **Architecture** — seven-layer navigation and relationships.
3. **Capabilities** — filterable capability matrix.
4. **Compression Lab** — protected hybrid compression with profiles.
5. **AIR Preview** — deterministic non-executable AIR-shaped output.
6. **Evidence Preview** — explicitly simulated evidence output.
7. **Contracts & Skills** — human-readable catalogs and validation expectations.
8. **Benchmarks** — CompText-specific safety and reduction results.
9. **About & Boundaries** — explicit non-goals and privacy behavior.

The initial page must state:

- experimental public demonstration
- no provider calls
- no repository writes
- no secrets
- no production-runtime claim

## 7. Compression Lab

### 7.1 Profiles

- Natural prose
- Engineering task
- AIR context
- Evidence summary
- Workspace description
- CLI instruction
- Configuration
- Mixed technical context

Profiles adjust protection rules and minimum useful reduction. They do not weaken the fail-closed safety requirement.

### 7.2 Segment classes

- `PROTECTED`
- `COMPRESSIBLE`
- `STRUCTURED`
- `UNSAFE_TO_TRANSFORM`

Protected content includes negations, prohibitions, CLI flags, commands, paths, URLs, JSON/YAML/TOML-like blocks, environment variable names, versions, hashes, IDs, code symbols, schema fields, permission terms, approval boundaries, and CompText status vocabulary.

### 7.3 Acceptance rule

A compressed candidate is accepted only when:

- all relevant protected items are preserved
- structure validation passes
- no secret pattern is detected
- net reduction meets the profile threshold

Otherwise the exact original input is returned.

### 7.4 Metrics

- original tokens
- candidate tokens
- output tokens
- gross reduction
- net reduction
- protected segments
- compressed segments
- relevant safety checks
- candidate safety
- final safety
- decision
- fallback reason
- runtime
- model
- snapshot commit

## 8. AIR Preview

The AIR preview is deterministic and non-executable. It may extract:

- intent
- goal
- context
- files
- tools mentioned
- constraints
- permissions
- expected outputs
- review and approval hints

Every result includes:

```json
{
  "execution": {
    "enabled": false
  },
  "preview": true
}
```

The preview must not call agents, tools, providers, GitHub, or the local runtime.

## 9. Evidence Preview

Evidence output is always labeled `simulation: true` and may contain:

- synthetic event type
- actor `hf-space-demo`
- input and output hashes
- summary
- compression metrics
- redaction status

It must never claim that a real CompText action occurred.

## 10. Security and Privacy

- no API keys or provider integrations
- no live GitHub connection
- no database
- no prompt persistence
- no raw input logging by application code
- temporary exports only
- deterministic secret-pattern blocking before compression or preview generation
- user input is treated only as data, never as executable instruction

Secret detection covers common provider keys, GitHub and Hugging Face tokens, bearer tokens, private-key blocks, AWS-style credentials, and suspicious environment assignments.

## 11. Hugging Face Runtime

- Gradio Space
- ZeroGPU used only for LLMLingua compression functions
- Universe, previews, validation, hashing, and redaction remain CPU-only
- keep ZeroGPU duration conservative to avoid quota rejection
- preserve the currently compatible PyTorch version
- model loading remains lazy unless preload is proven stable
- Space metadata clearly lists the LLMLingua model and experimental status

## 12. Tests and Validation

All validation must be runnable from within `hf_space/**` without changing other repository files.

Required checks:

```bash
python -m compileall hf_space
python -m pytest hf_space/tests
```

Test requirements:

- all shipped JSON files parse and satisfy internal validators
- all relationships reference existing IDs
- maturity values use the approved vocabulary
- AIR output is always non-executable
- Evidence output is always simulated
- secret-like inputs are blocked
- protected technical items survive accepted compression
- unsafe or unprofitable candidates return the exact original
- existing benchmark behavior does not regress

## 13. Delivery Strategy

Implementation occurs on `plugin/hf-comptext-universe` and changes only `hf_space/**`.

Logical increments:

1. static data model and validators
2. Universe loader and UI
3. AIR and Evidence previews
4. modular compression UI and profiles
5. security hardening and tests
6. README metadata and final integration

No pull request or merge is performed without explicit user approval after implementation and validation.

## 14. Success Criteria

A visitor can answer:

- What is CompText?
- Why is context central?
- What are AIR and Evidence?
- Which capabilities exist today versus being planned?
- How does protected compression save tokens safely?
- Why does the real CompText runtime remain local?

The Space must remain useful even when ZeroGPU is unavailable: all Universe and preview features continue to work, while compression reports a clear runtime limitation.