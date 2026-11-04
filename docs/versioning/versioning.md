---
title: Versioning & Reproducibility
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

How Bilayers versions its Docker images and manages dependencies across the four repos.

## Interface image tags

Published interface images are tagged:

```
bilayer/<algorithm>:<version>-<interface>
```

where `<algorithm>` is the config's `algorithm_folder_name`, for example
`bilayer/classical_segmentation:1.0.0-gradio`. The version is decided by the build
pipeline (`nox -s build_interface`): it compares the digest of the freshly built image
with the latest published `<version>-<interface>` tag. If they are identical, that tag is
reused; otherwise the version is bumped (`major` / `minor` / `patch`, default `minor`).
An algorithm with no published tag for that interface starts at `1.0.0`.

:::{note}
Some images published before this scheme use older names and tags (for example
`bilayer/cellpose:1.0.1-gradio` or `bilayer/instanseg:1.0.2_pixi_gradio`). See
[Run a Bilayers Image](../tool_user/steps_to_run.md) for what is currently published.
:::

## Base (algorithm) images

`nox -s build_algorithm` first tries to **pull** the image named in the config's
`docker_image` block from DockerHub. If the pull fails, it **builds locally** from the
algorithm's `Dockerfile`. The locally built base image is used only as the
`BASE_IMAGE` for the interface build.

## Sibling dependencies come from git, pinned by the lockfile

The orchestrator declares the sibling packages as git dependencies on each repo's
default branch (`main`), with no branch or tag in the URL:

```
bilayers-schema     @ git+https://github.com/bilayer-containers/bilayers-schema.git
bilayers-targets    @ git+https://github.com/bilayer-containers/bilayers-targets.git
bilayers-algorithms @ git+https://github.com/bilayer-containers/bilayers-algorithms.git
```

`pixi.lock` records the exact commit each one resolved to, and CI installs with
**`locked: true`**, so every CI run uses the commits in the lockfile, not whatever is
on `main` at that moment. To pick up newer sibling commits, run `pixi update` (or
`pixi update bilayers-targets` for one package) and commit the updated `pixi.lock`.

:::{note}
Before a `1.0.0` release, the plan is to pin the siblings to immutable release tags so
that published images can be traced back to tagged versions of every repo.
:::

## Working rule of thumb

- Change a dependency in `pyproject.toml` → expect `pixi.lock` to change → commit both.
- Want the latest sibling code → `pixi update`, then commit `pixi.lock`.
- Didn't touch dependencies → the lock won't move.
- Changing a sibling repo and testing through `bilayers`? Point the env at your local
  checkout — see [Local Setup](../developer_guide/dev_setup.md).
