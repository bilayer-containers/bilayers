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

| What | Where | Checks |
| --- | --- | --- |
| Config validation | `tests/test_config/` | Every shipped algorithm config (from the installed `bilayers_algorithms`) validates against the schema, and bad configs are rejected |
| CLI-command generation | `tests/cli/test_cli_generator.py` | The command built by `bilayers_cli --cli`: argument order, hidden args, checkboxes with and without `append_value`, file inputs, missing required values |
| Interface loading | `tests/cli/test_interface_loader.py` | The `bilayers-targets` registry loads; a missing interface fails with an install hint; a module without a callable `generate()` is rejected |
| Golden regression | `tests/regression/test_generate_regression.py` | **Byte-exact** comparison of the generated files for one representative config against `tests/fixtures/golden/` |
| Generate smoke | `tests/regression/test_generate_smoke.py` | For **every** algorithm, generation succeeds and each interface writes a **non-empty** file |

## Running part of the suite

`nox -s test_pytest` installs the package into a fresh nox environment first. For a faster loop, call pytest directly inside the pixi environment:

```bash
# from bilayers/
pixi run -e dev pytest tests/cli/test_cli_generator.py                  # one file
pixi run -e dev pytest tests/cli/test_cli_generator.py::test_order_of_arguments   # one test
pixi run -e dev pytest tests/regression -k gaussian_smoothing           # tests matching a name
```

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

The `.py` files are compared byte for byte. Notebook cell IDs change on every run, so
the test strips them before comparing the notebook, and that churn doesn't need reviewing.

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

(container-testing)=
## Testing in a container (end to end)

The test suite stops at generated files. To confirm the tool actually runs and writes
the outputs you expect, build an interface image and use it.

`scripts/build_docker.sh` runs the whole chain for each algorithm × interface you name:
parse → generate → `nox -s build_algorithm` (pull the base image, or build it from the
algorithm's `Dockerfile`) → `nox -s build_interface` (layer the interface on top and tag it).

```bash
# from bilayers/ (use -e dev instead for Podman)
pixi run -e dockerdev bash scripts/build_docker.sh --algorithm gaussian_smoothing --interface gradio

docker images bilayer/gaussian_smoothing          # find the tag it just created
docker run --rm -p 7878:7878 bilayer/gaussian_smoothing:<tag>
```

Then open `http://localhost:7878`, run it on a few real images, and check the results
against what the tool produces from the command line
(`bilayers_cli generate <config.yaml> --cli` shows the exact command the app runs).

A few things to know:

- `build_docker.sh` reads configs from the **installed** `bilayers_algorithms`. To build a
  new algorithm from your checkout, point the environment at `../bilayers-algorithms`
  first (see [Local Setup](../developer_guide/dev_setup.md)).
- `build_interface` compares the new image's digest with the latest published tag on
  DockerHub to choose the version, so it needs network access. It only tags locally;
  nothing is pushed.
- If a run fails, open the generated file in `dist/<interface>/<algorithm>/`. It's plain
  Python with the config baked in (see
  [Inside bilayers-targets](../architecture/targets.md#two-phases-generation-time-and-run-time)).

## Checking the docs

If you edited anything under `docs/` or `myst.yml`, build the site and look for warnings:

```bash
# from bilayers/
npx mystmd build --html     # warnings name the file and line
npx mystmd start            # live preview at http://localhost:3000
```

Mermaid diagrams are drawn in the browser, so the build won't catch a broken one. Check
pages with diagrams in the preview.

## Linting & formatting

```bash
pixi run -e dev nox -s lint     # ruff check
pixi run -e dev nox -s format   # ruff format
```

## CI

CI runs on pixi. On every push and pull request, the `Test` workflow in `bilayers`
runs `scripts/test_docker.sh` and then `nox -s test_pytest`, in the pixi `dev`
environment with `locked: true`, so sibling repos are tested at the commits recorded in
`pixi.lock`. Despite its name, `test_docker.sh` doesn't build any images: it runs
`nox -s test_parse` and `nox -s test_generate` on
`tests/test_algorithm/correct_validation_config.yaml`. Images are built only by the
manually triggered `Docker Build` workflow.

Each sibling repo has its own `Test` workflow that runs its unit tests:

```bash
# from bilayers-schema/, bilayers-targets/, or bilayers-algorithms/
pixi run -e dev pytest tests/ -v
```

When a pull request into `bilayers-schema`'s `main` is closed, its `notify-downstream`
workflow sends a `schema-updated` event to `bilayers-targets` and `bilayers-algorithms`.
In each, `update-schema` re-runs `pixi lock`. If the lockfile changed, it opens an
**"Auto-update pixi.lock (schema change)"** pull request, and that PR's `Test` run is
what checks the repo against the new schema. `bilayers` itself isn't notified: move it
to the new schema with `pixi update` and commit the lockfile.
