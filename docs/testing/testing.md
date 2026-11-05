---
title: Testing Guide
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

Testing in Bilayers has two audiences:

- **[User Testing](user_testing.md)** — you are running a pre-built Bilayers image and
  want to confirm it works and produces the outputs you expect.
- **[Developer Testing](developer_testing.md)** — you changed a config, a template, or
  the schema, and want to confirm nothing downstream broke.

Because Bilayers is four repositories, tests are split accordingly: each repo has its
own unit tests, and the `bilayers` orchestrator holds the **integration** tests that
validate configs and smoke-test generation across every algorithm × interface.
