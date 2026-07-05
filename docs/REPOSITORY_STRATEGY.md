# Repository Strategy

## Public product repository

The clean public product repository should be:

```text
ProfRandom92/comptext
```

It should contain only the product-relevant CompText foundation: docs, schemas, examples, local dry-run modules, tests, Windows scripts, hooks, skills, subagents, MCP descriptors, and product assets.

## Suggested public repositories

Keep the public surface small and coherent. A recommended public set is:

1. `comptext` — main product repository.
2. `comptext-air` — AIR schemas and Agent Intermediate Representation work.
3. `comptext-evidence` — Evidence / Replay / Verify engine when extracted cleanly.
4. `comptext-vault` — Memory, Context Packs, CAS, and Knowledge Graph ideas when cleaned.
5. `comptext-town` — showcase or visual demo, not core runtime.

## Repositories to make private or archive

Older experimental repositories should be private or archived unless they are cleaned and renamed around the CompText product model. They may remain useful as internal references, but should not define product branding.

Categories:

- legacy CLI prototypes,
- research prototypes,
- compression experiments,
- old lab workspaces,
- medical or domain-specific archives,
- cancelled competition or short-term project material.

## Naming rules

Use only these names in product-facing surfaces:

- `CompText` for the product name,
- `comptext` for package, CLI, directory, and repository names,
- `COMPTEXT` for environment variable prefixes or all-caps document titles.

Avoid old project names as product names, module names, command names, or repo names inside the clean public product.

## Migration rule

Historical sources can inform design, but the clean repository should not expose historical working names as first-class product modules. If a concept is retained, rename it into the CompText architecture: Runtime, AIR, Evidence, Gateway, Provider Registry, Context Pack, Memory, Skill, Hook, Subagent, or MCP Fabric.
