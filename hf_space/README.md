---
title: CompText Prompt Compression Lab
emoji: 🗜️
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.44.1
app_file: app.py
pinned: false
license: apache-2.0
---

# CompText Prompt Compression Lab

A CPU-friendly Hugging Face Space for evaluating prompt and context compression with Microsoft LLMLingua-2.

## Features

- Compress arbitrary prompts at configurable retention rates
- Compare original and compressed text
- Measure token reduction and runtime
- Check preservation of negations, CLI flags, file paths, JSON keys, version numbers, and code-like symbols
- Run a built-in benchmark suite
- Export results as JSON

## Default model

`microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank`

The first startup can take several minutes because the model must be downloaded.

## Hardware

Designed for Hugging Face Spaces `CPU Basic` (2 vCPU, 16 GB RAM, 50 GB ephemeral storage).

## Safety

This Space does not call external LLM APIs, require runtime secrets, access private repositories, or modify repositories.