---
title: Developer Testing
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

How to confirm a change didn't break the pipeline. Run everything through pixi.

## The orchestrator test suite

```bash
# from bilayers/
pixi run -e dev nox -s test_pytest
```

This covers:

- **Config validation** — every shipped algorithm config validates against the schema.
- **CLI-command generation** — the command string is built correctly.
- **Golden regression** (`tests/regression/test_generate_regression.py`) — a **byte-exact**
  comparison of generated output for a representative config against committed golden
  fixtures in `tests/fixtures/golden/`.
- **Generate smoke** (`tests/regression/test_generate_smoke.py`) — for **every**
  algorithm, generation runs and each interface produces a **non-empty** output file.

### When you intentionally change generator output

If you change a template or the generation logic, the **golden fixtures** must be
regenerated, or the regression test will fail. The representative config is
`tests/fixtures/classical_segmentation/config.yaml`. Generate it with the environment
pointed at your `bilayers-targets` checkout (see [Local Setup](../developer_guide/dev_setup.md)),
then copy the four outputs over the goldens:

```bash
# from bilayers/
pixi run -e dev bilayers_cli generate tests/fixtures/classical_segmentation/config.yaml
G=tests/fixtures/golden/classical_segmentation
cp dist/gradio/classical_segmentation/app.py                                  $G/
cp dist/jupyter/classical_segmentation/generated_notebook.ipynb               $G/
cp dist/streamlit/classical_segmentation/streamlit_app.py                     $G/
cp dist/cellprofiler_plugin/classical_segmentation/runclassicalsegmentation.py $G/
git diff $G   # review: every change should be one you intended
```

Notebook cell IDs change on every run; the test normalizes them away, so that churn
doesn't need reviewing.

:::{tip}
Golden vs smoke coverage: smoke checks *every* algorithm×interface but only that the
output is non-empty; the byte-exact golden covers *one* representative config deeply.
So a content change that only affects a param type the golden config doesn't have
(e.g. integer/checkbox) can pass CI while still being wrong — spot-check an algorithm
that *does* exercise those types.
:::

## Testing a schema change end-to-end

A schema change can ripple three ways: the `types.py` mirror drifts, algorithm configs
stop validating, or generators produce wrong output. Test it in two layers.

**Layer 1 — inside `bilayers-schema`:**

```bash
pixi run -e dev pytest tests/ -v   # test_schema.py + test_types.py
```

`test_types.py` is the **drift guard**: it fails if `schema.yaml` (the source of truth)
and the hand-maintained `types.py` mirror disagree. If you edit `schema.yaml`, update
`types.py` to match.

**Layer 2 — downstream, from `bilayers`:** point the environment at your schema branch
(pixi-native — see [Local Setup](../developer_guide/dev_setup.md)) by temporarily
setting a path dependency, then run the integration suite:

```bash
# bilayers/pyproject.toml → [tool.pixi.pypi-dependencies]:
#   bilayers-schema = { path = "../bilayers-schema", editable = true }
pixi install -e dev
pixi run -e dev nox -s test_pytest
pixi run -e dev bash scripts/validate.sh
# when done: git checkout -- pyproject.toml pixi.lock && pixi install -e dev
```

## Linting & formatting

```bash
pixi run -e dev nox -s lint     # ruff check
pixi run -e dev nox -s format   # ruff format
```

## CI

CI runs on pixi. On every push and pull request, the `Test` workflow in `bilayers`
runs `scripts/test_docker.sh` (parse + generate on a test config) and then
`nox -s test_pytest`, in the pixi `dev` environment with `locked: true`, so sibling
repos are tested at the commits recorded in `pixi.lock`.

Each sibling repo has its own `Test` workflow that runs its unit tests:

```bash
# from bilayers-schema/, bilayers-targets/, or bilayers-algorithms/
pixi run -e dev pytest tests/ -v
```

When `schema.yaml` changes on `bilayers-schema`'s `main`, its `notify-downstream`
workflow triggers `update-schema` in `bilayers-targets` and `bilayers-algorithms`, so
both re-test against the new schema.
