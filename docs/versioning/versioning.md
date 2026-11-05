---
title: Versioning & Reproducibility
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

How Bilayers versions its Docker images and manages dependencies across the four repos.

## Four things with versions

"Which version?" can mean four different things in Bilayers, and they move independently:

```{mermaid}
flowchart LR
    subgraph img["What a user runs"]
        direction TB
        I["interface image<br/>bilayer/gaussian_smoothing:1.0.0-gradio"]
        B["base (algorithm) image<br/>bilayer/gaussian_smoothing:1.0.0"]
        I -- "built FROM" --> B
    end
    subgraph code["What builds it"]
        direction TB
        R["bilayers release<br/>v1.0.0rc1"]
        L["pixi.lock<br/>sibling commits"]
        R --- L
    end
    code -- "generates + builds" --> img
```

| What | Example | Set by | Changes when |
| --- | --- | --- | --- |
| Interface image tag | `bilayer/classical_segmentation:1.0.0-gradio` | the build pipeline | the built image's contents change |
| Base image tag | `bilayer/classical_segmentation:1.0.0` | the algorithm's `docker_image.tag` in `config.yaml` | the algorithm author publishes a new image |
| `bilayers` release | `v1.0.0rc1` | a GitHub release (archived on Zenodo) | the team cuts a release |
| Sibling commits | recorded in `pixi.lock` | `pixi update` | someone updates and commits the lockfile |

A Gradio image at `1.2.0` doesn't mean the algorithm or Bilayers is at `1.2.0`. To see exactly what's inside an image, use its tag together with the base image named in the algorithm's `config.yaml`.

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

## Releases

`bilayers` publishes releases on GitHub, and each is archived on Zenodo with a DOI (see
[Cite Bilayers](../resources/talks_tutorials.md#cite-bilayers)). The current one,
**`v1.0.0rc1`** (November 2025), is a pre-release from **before** the four-repo split:
at that point the algorithms and interfaces still lived inside `bilayers`. The three
sibling repos don't have release tags yet, so for now `pixi.lock` is the only record of
which sibling commits a given `bilayers` commit was built and tested with.

:::{note}
Before `1.0.0`, the plan is to tag the sibling repos and pin `bilayers` to those
immutable tags, so a published image can be traced back to a tagged version of every repo.
:::

## Working rule of thumb

- Change a dependency in `pyproject.toml` → expect `pixi.lock` to change → commit both.
- Want the latest sibling code → `pixi update`, then commit `pixi.lock`.
- Didn't touch dependencies → the lock won't move.
- Changing a sibling repo and testing through `bilayers`? Point the env at your local
  checkout — see [Local Setup](../developer_guide/dev_setup.md).
