---
title: Developer Guide
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

The Developer Guide is for people who want to **extend or contribute to** Bilayers —
wrap a new algorithm, add an interface, evolve the schema, or work on the orchestrator.

## Start here

- **[Local Setup (pixi)](dev_setup.md)** — clone the repos, run the pipeline and tests.
- **[Before You Wrap an Algorithm](../custom_algorithm/custom_algorithm.md)** — the
  pieces you need in place first: a compatible base image, a target, and a config.
- **[Wrap a New Algorithm](wrap_algorithm.md)** — add a tool to `bilayers-algorithms`.
- **[Add a New Interface](add_interface.md)** — add a generator to `bilayers-targets`.
- **[Contributing](contributing.md)** — workflow, PR expectations, keeping repos in sync.

For the *why* behind the layout, read the [Architecture](../architecture/overview.md)
section — especially [How Bilayers is Organized](../architecture/overview.md) and
[Core Data Flow](../architecture/data_flow.md).

## The mental model in one line

A tool is described once in a `config.yaml`; the orchestrator turns that into interface
code via standalone generators; each pairing is baked into a Docker image. Four repos,
one spec.
