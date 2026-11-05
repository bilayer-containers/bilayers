---
title: Core Data Flow
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

This page follows one config from the moment you run `bilayers_cli generate` to the moment a user clicks **Run** in the finished app. The running example is `gaussian_smoothing` from `bilayers-algorithms`, because it is small enough to follow by hand.

## The whole journey

```{mermaid}
flowchart LR
    A["config.yaml<br/>(bilayers-algorithms)"]
    subgraph orch["bilayers"]
        direction TB
        B["1 · Parse<br/>parse.py"] --> C["2 · CLI sequence<br/>build_cli_sequence"] --> D["3 · InterfaceInput<br/>generate.py"]
    end
    subgraph tg["bilayers-targets"]
        direction TB
        E["4 · Render<br/>generate(interface_input)"] --> F["dist/&lt;interface&gt;/&lt;algorithm&gt;/"]
    end
    subgraph dk["Docker build"]
        direction TB
        G["5 · base image<br/>+ interface layer"] --> H["bilayer/&lt;algorithm&gt;:<br/>&lt;version&gt;-&lt;interface&gt;"]
    end
    A --> orch
    orch -- "InterfaceInput" --> tg
    tg -- "generated file" --> dk
```

Steps 1 to 3 happen in the orchestrator (`bilayers`) and take a fraction of a second. Step 4 lives in `bilayers-targets`, which only ever sees the plain `InterfaceInput` dictionary. Step 5 is the Docker build, which runs in CI or through `nox`. The sections below take each step in turn, then look at what happens when someone actually uses the app (step 6).

## 1. Parse

`parse.py:parse_config` reads the YAML. In the file, `inputs`, `outputs`, `parameters`, `display_only`, `citations`, and `exec_function.hidden_args` are written as lists, which is easy to type but awkward to look things up in. The parser turns each list into a dictionary keyed by the entry's `name`:

```{mermaid}
flowchart LR
    subgraph yaml["config.yaml (lists)"]
        direction TB
        y1["parameters:<br/>- name: sigma_size ...<br/>- name: save_dir ..."]
    end
    subgraph py["parsed (name-keyed dicts)"]
        direction TB
        p1["parameters = {<br/>'sigma_size': {...},<br/>'save_dir': {...} }"]
    end
    yaml --> py
```

`safe_parse_config` then fills in defaults and returns the same nine values every time: inputs, outputs, parameters, display_only, exec_function, algorithm_folder_name, citations, docker_image, and the CLI sequence. Everything downstream works from that tuple, never from the raw YAML.

## 2. Build the CLI sequence

A tool's command is made of its base command (`exec_function.cli_command`) followed by arguments. Those arguments can come from three places: **inputs** (where the files are), **parameters** (the settings a user picks), and **hidden_args** (fixed flags the user never sees). `parse.py:build_cli_sequence` merges all three into one ordered dictionary.

```{mermaid}
flowchart LR
    I["inputs"] --> M{"merge"}
    P["parameters"] --> M
    H["hidden_args"] --> M
    DO["display_only"] -. "never added" .-> X(("✕"))
    M --> S["sort by cli_order"]
    S --> Q["cli_sequence"]
```

The order is set by `cli_order`. Positive values come first, in ascending order. Next comes everything with `0` or no `cli_order`, keeping its original order: inputs first, then parameters, then hidden args, each as written in the file. Negative values go last, so `-1` is the very end of the command:

```{mermaid}
flowchart LR
    a["cli_order: 1"] --> b["cli_order: 2"] --> c["cli_order: 0 / unset"] --> d["cli_order: -2"] --> e["cli_order: -1"]
```

Doing this once, here, means no interface has to work out argument order on its own. Every generated app builds the same command for the same choices.

For `gaussian_smoothing`, the sequence is `input_images` (`--folder`), then `sigma_size` (`--sigma_size`), then `save_dir` (`--save_dir`), and the command with default values is:

```bash
python -m gaussian_smoothing --folder /bilayers/input_images --sigma_size 5 --save_dir /bilayers/output_images
```

You can print this for any config with `bilayers_cli generate <config.yaml> --cli`. It's the quickest way to check a config before generating anything.

:::{important}
`display_only` fields show up in the UI, but they are **never** part of the command. Anything the tool needs to receive, including the output folder (the parameter with `output_dir_set: True`), must be an `input` or a `parameter`. See [The Config Model](../custom_algorithm/understanding_config.md).
:::

## 3. Hand off to a generator

`generate.py` packs the parsed values into an `InterfaceInput` dictionary, adds `output_dir` (where the files should be written), and asks `interface_loader.py:InterfaceLoader` for the generator by name. The loader is a thin wrapper around `bilayers_targets.available_ifaces`.

```{mermaid}
flowchart LR
    subgraph orch["bilayers (orchestrator)"]
        G["generate.py"] --> L["InterfaceLoader"]
    end
    subgraph targets["bilayers-targets"]
        R["registry.py<br/>available_ifaces"]
        R --> g1["gradio"]
        R --> g2["jupyter"]
        R --> g3["streamlit"]
        R --> g4["cellprofiler_plugin"]
    end
    L -- "load_module(name)" --> R
    G -- "generate(interface_input)" --> g1
```

`bilayers_cli generate <config>` loops over every registered interface. If one fails (for example, the CellProfiler plugin rejects an input/output combination it can't map), the error is printed and the others still generate. `bilayers_cli generate <config> -i <name>` runs a single interface and stops with an error if it fails.

The `InterfaceInput` dictionary is the entire contract between the two repositories:

| Key | What it holds |
| --- | --- |
| `output_dir` | Folder to write into: `dist/<interface>/<algorithm_folder_name>/` |
| `inputs`, `outputs`, `parameters`, `display_only` | The name-keyed dictionaries from step 1 |
| `exec_function` | Base command and hidden args |
| `citations` | Citations to show in the app's header |
| `docker_image` | The algorithm's base image (used by the CellProfiler plugin at run time) |
| `cli_sequence` | The ordered arguments from step 2 |

## 4. Render

Each generator renders one or more Jinja2 templates with those values and writes the result into `output_dir`:

| Interface | File written |
| --- | --- |
| Gradio | `app.py` |
| Jupyter | `generated_notebook.ipynb` |
| Streamlit | `streamlit_app.py` |
| CellProfiler plugin | `run<algorithmname>.py` (e.g. `rungaussiansmoothing.py`) |

What goes on inside a generator, and how each target differs, is covered in [Inside bilayers-targets](targets.md).

(package-image)=
## 5. Package into a Docker image

An interface image is built **on top of** the algorithm's own image. The algorithm image already has the tool and its dependencies; the interface Dockerfile adds the UI library and the generated file.

```{mermaid}
flowchart TB
    subgraph img["bilayer/gaussian_smoothing:&lt;version&gt;-gradio"]
        direction TB
        L3["CMD: python app.py, port 7878"]
        L2["Interface layer (Gradio.Dockerfile)<br/>pip install gradio ... + COPY app.py"]
        L1["Algorithm base image<br/>bilayer/gaussian_smoothing:1.0.0<br/>(the tool + its dependencies)"]
        L3 --- L2 --- L1
    end
```

The build happens in two `nox` sessions:

```{mermaid}
sequenceDiagram
    participant N as nox
    participant H as DockerHub
    participant D as Docker / Podman
    N->>H: build_algorithm: is the base image published?
    alt published
        H-->>D: pull base image
    else not published
        N->>D: build it from the algorithm's Dockerfile
    end
    N->>D: build_interface: build a candidate image<br/>(BASE_IMAGE + Gradio.Dockerfile)
    N->>H: fetch digest of the latest #lt;version#gt;-gradio tag
    alt digests match
        N->>D: reuse that tag (nothing changed)
    else digests differ
        N->>D: tag with a bumped version (minor by default)
    end
```

Because the tag only changes when the image contents change, the same tag always means the same software. See [Versioning & Reproducibility](../versioning/versioning.md) for more.

## 6. At run time

Once the container is running, the generated app does the same thing every time a user clicks **Run**. Here it is for Gradio; Streamlit and Jupyter follow the same steps with their own widgets.

```{mermaid}
sequenceDiagram
    actor U as User (browser)
    participant A as app.py (in container)
    participant T as The tool (same container)
    U->>A: upload images, set sigma_size, click Run
    A->>A: generate_cli_command(cli_sequence, choices)
    Note over A: python -m gaussian_smoothing --folder ... --sigma_size 5 --save_dir ...
    A->>T: subprocess.run(command)
    T-->>A: writes results into the output folder
    A->>A: collect files, zip them
    A-->>U: show results + "Download All (zip)"
```

The tool and the app share one container, so the app simply calls the tool as a command, exactly as you would in a terminal. That's also why the output-folder parameter matters: the app reads the results back from the folder it passed to the tool.

## Try it yourself

```bash
# Print the command a config produces (generates nothing):
pixi run -e dev bilayers_cli generate <config.yaml> --cli

# Generate every interface into dist/:
pixi run -e dev bilayers_cli generate <config.yaml>

# Generate one interface:
pixi run -e dev bilayers_cli generate <config.yaml> -i gradio

# Validate a config against the schema:
pixi run -e dev bilayers_cli validate <config.yaml>
```

## Why generators can't import the orchestrator

Generators in `bilayers-targets` must not import `bilayers.parse`, `bilayers.generate`, or `project_path` from `bilayers`. Everything they need arrives in `InterfaceInput`. That one rule is what lets `bilayers-targets` be versioned and released on its own, and it means a new interface can be written and tested without touching the orchestrator.
