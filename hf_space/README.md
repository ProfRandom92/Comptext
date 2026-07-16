---
title: CompText Universe
emoji: 🧭
colorFrom: indigo
colorTo: blue
sdk: gradio
python_version: 3.10.13
sdk_version: 5.44.1
app_file: app.py
fullWidth: true
header: mini
pinned: false
license: apache-2.0
short_description: Explore CompText architecture, contracts and safe context compression.
models:
  - microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank
tags:
  - context-engineering
  - prompt-compression
  - software-engineering
  - gradio
preload_from_hub:
  - microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank
---

# CompText Universe

> Models are providers. Context is the product. Evidence is the trust layer. CompText is the kernel.

A public, experimental showcase for the CompText local engineering-orchestration architecture. The real CompText runtime remains local; this Space visualizes architecture and contracts, builds non-executable AIR and simulated Evidence previews, and tests fail-closed context compression.

## Included surfaces

- Static seven-layer architecture explorer
- Explicit capability maturity matrix
- Workspace skill and safety-boundary explorer
- Fail-closed hybrid LLMLingua-2 compression
- Deterministic, non-executable AIR previews
- Simulated, non-persistent Evidence previews
- CompText-specific benchmark and JSON exports

## Hard boundaries

- No provider calls
- No repository writes
- No runtime GitHub access
- No API keys or runtime secrets
- No AIR execution
- No persistent prompt storage
- No claim that planned or scaffolded components are production-ready

## Runtime

Only compression callbacks request ZeroGPU. Universe navigation, preview construction, contract views and secret-pattern checks are CPU-only and deterministic. The model is preloaded from the Hub during build to reduce first-request latency.
