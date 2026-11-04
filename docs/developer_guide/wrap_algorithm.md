---
title: Wrap a New Algorithm
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

Wrapping an algorithm means describing its command-line behavior in a Bilayers
`config.yaml` so the pipeline can generate interfaces for it. Algorithms now live in
their **own repository**, [`bilayers-algorithms`](https://github.com/bilayer-containers/bilayers-algorithms)
— not inside `bilayers`.

:::{note}
This changed with the repository restructure. Older docs referenced
`src/bilayers/algorithms` inside the `bilayers` repo — that location no longer exists.
Algorithms are added to `bilayers-algorithms`.
:::

## 1. Fork and clone `bilayers-algorithms`

```bash
git clone https://github.com/your-username/bilayers-algorithms.git
cd bilayers-algorithms
git remote add upstream https://github.com/bilayer-containers/bilayers-algorithms.git
```

## 2. Add your algorithm folder

Create a folder under `src/bilayers_algorithms/<your_algorithm>/`. Use the naming
convention `<name>_inference` or `<name>_training` based on the task. Add:

- `__init__.py` — an empty file, so the folder ships as part of the
  `bilayers_algorithms` package
- `config.yaml` — the Bilayers spec for your tool (see skeleton below)
- a `Dockerfile` — only if there is no published image for your tool
- any helper script the `Dockerfile` copies in (for example `classical_segmentation.py`)

```{code} yaml
:filename: config.yaml
citations:
  - name: ""
    doi: ""
    license: ""
    description: ""

docker_image:
  org:
  name:
  tag:
  platform:

algorithm_folder_name: "<your_algorithm>"

exec_function:
  name: "generate_cli_command"
  cli_command: ""
  hidden_args:

inputs:
outputs:
parameters:
display_only:
```

- See [The Config Model](../custom_algorithm/understanding_config.md) for what each
  field means.
- See [Choosing a Base Docker Image](../custom_algorithm/right_base_docker_image.md)
  for the image selection.

:::{important}
Anything the tool needs on the command line must be an `input` or `parameter`.
Fields under `display_only` are shown in the UI but **never passed to the CLI**. In
particular the **output-path** field (the one with `output_dir_set`) must be a
`parameter`, or the interfaces won't know where to collect results.
:::

## 3. Register the algorithm name

The orchestrator's test suite discovers every algorithm in the installed
`bilayers_algorithms` package on its own. Two scripts in `bilayers/` still keep explicit
lists, so add your algorithm name to them in a PR to `bilayers`:

- `scripts/validate.sh` — the `ALGORITHM_NAMES` array, so `validate.sh` checks your config
- `scripts/build_docker.sh` — the default `ALGORITHM_NAMES` list, used when the script runs
  with no `--algorithm` argument

The `Docker Build` workflow in `bilayers` builds one algorithm × interface at a time from
the name you pick when triggering it, so it needs no list.

## 4. Validate and generate locally

Validation and generation run from the `bilayers` orchestrator. Both commands below
take a config path, so they work on your checkout directly:

```bash
# from bilayers/
pixi run -e dev bilayers_cli validate ../bilayers-algorithms/src/bilayers_algorithms/<your_algorithm>/config.yaml
pixi run -e dev bilayers_cli generate ../bilayers-algorithms/src/bilayers_algorithms/<your_algorithm>/config.yaml
pixi run -e dev bilayers_cli generate <config> --cli   # inspect the generated command
```

Confirm all four interfaces generate into `dist/` and the CLI command looks right.

To run the full test suite or `scripts/validate.sh` against your new folder, the
environment needs to see your checkout rather than the git version: either point it at
`../bilayers-algorithms` (see [Local Setup](dev_setup.md)) or, for `validate.sh` only,
set `ALGORITHMS_PATH=../bilayers-algorithms/src/bilayers_algorithms`.

## 5. Verify the container behavior

The generated interfaces run your tool inside its Docker image. Build the base image
and an interface image and run one end-to-end (see the
[Testing Guide](../testing/developer_testing.md)) to confirm real inputs produce the
expected outputs.

## 6. Open a pull request

Push your branch to `bilayers-algorithms` and open a PR against `main`. Describe the
tool, its inputs/outputs/parameters, and link the image. On approval, the Bilayers
team publishes the images to DockerHub for the community.
