# CompText Skills System

Skills are capability packs, not random prompts. A skill should package repeatable operating knowledge for a bounded kind of work.

## Skill contents

Each skill may include:

- `SKILL.md`
- checklists
- command recipes
- templates
- validation rules
- anti-patterns

## Proposed directory shape

```text
skills/
  python/
    SKILL.md
  git/
    SKILL.md
  github/
    SKILL.md
  docs/
    SKILL.md
  evidence/
    SKILL.md
  provider-gateway/
    SKILL.md
```

This repository does not implement a full skill marketplace yet. Skill files are documentation-first operating guides until a runtime loader exists.

## Skill requirements

- Keep each skill scoped to one capability area.
- Include when to use it and when not to use it.
- List required local checks and safety notes.
- Link to related CompText docs instead of duplicating architecture.
- Avoid provider calls, network assumptions, and secret access unless an explicit future policy permits them.
