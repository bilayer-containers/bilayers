---
title: Contributing
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

Bilayers is open-source and welcomes contributions. Because it spans four repos, a
change often touches more than one — this page is about keeping them in sync.

## Which repo for which change

| You want to… | Repo |
| --- | --- |
| Wrap a new tool | `bilayers-algorithms` |
| Add/modify an interface or plugin | `bilayers-targets` |
| Change the spec (slots, types, validation) | `bilayers-schema` |
| Change orchestration, CLI, or build/CI | `bilayers` |

## General workflow

1. Fork the repo and create a branch off `main`.
2. Make the change; run the relevant tests via pixi (see
   [Developer Testing](../testing/developer_testing.md)).
3. Open a PR against `main`. Keep commits scoped and messages descriptive.

## Keeping the spec and generators in sync

A schema change can ripple into the generated types, the algorithm configs, and the
interface generators. To keep drift minimal:

- Update the `types.py` mirror in `bilayers-schema` when you change `schema.yaml`
  (the drift test enforces this).
- **Link the corresponding generator update** (`bilayers-targets`) from a spec-change
  PR — or explicitly note that no generator change is needed. A PR-template checklist
  is planned to require this.
- Validate downstream against your branch before merge (see
  [Developer Testing → Testing a schema change](../testing/developer_testing.md)).

:::{note}
Flesh this out with the concrete PR-template checklist and review expectations once
they're finalized.
:::
