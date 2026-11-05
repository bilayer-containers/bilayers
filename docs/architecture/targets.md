---
title: Inside bilayers-targets
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

[`bilayers-targets`](https://github.com/bilayer-containers/bilayers-targets) holds the code that turns a parsed config into something a person can use: a Gradio app, a Jupyter notebook, a Streamlit app, or a CellProfiler module. This page walks through how that repository is organized, what every generator has in common, and where the four targets differ.

If you only want to know which target to pick, see [Supported Interfaces](../custom_algorithm/supported_interfaces.md). For what happens before a generator is called, see [Core Data Flow](data_flow.md).

## Where it sits

```{mermaid}
flowchart LR
    subgraph orch["bilayers"]
        P["parse.py"] --> G["generate.py"]
    end
    subgraph tg["bilayers-targets"]
        R["registry.py"]
        GEN["&lt;target&gt;/generate.py"]
        TPL["*.j2 templates"]
        DF["*.Dockerfile"]
        R --> GEN --> TPL
    end
    G -- "InterfaceInput (a plain dict)" --> R
    GEN --> OUT["dist/&lt;target&gt;/&lt;algorithm&gt;/"]
    DF -. "used later by nox build_interface" .-> IMG["interface image"]
    OUT -. "copied into" .-> IMG
```

The orchestrator never reaches into a generator's internals, and a generator never imports the orchestrator. The `InterfaceInput` dictionary is the only thing that crosses the boundary. That's why `bilayers-targets` can be tested and released on its own, and why its only Bilayers dependency is `bilayers-schema` (for the `TypedDict` types).

## Repository layout

```
src/bilayers_targets/
├── registry.py                     # name -> generator module
├── shared/
│   └── utils.py                    # generate_top_level_text (title + citations)
├── interfaces/                     # self-contained apps, each shipped as an image
│   ├── gradio/
│   │   ├── generate.py
│   │   ├── gradio_template.py.j2
│   │   └── Gradio.Dockerfile
│   ├── jupyter/
│   │   ├── generate.py
│   │   ├── jupyter_template.py.j2                    # widgets cell
│   │   ├── jupyter_final_validation_template.py.j2   # validation cell
│   │   ├── jupyter_shell_command_template.py.j2      # run cell
│   │   └── Jupyter.Dockerfile
│   └── streamlit/
│       ├── generate.py
│       ├── streamlit_template.py.j2
│       └── Streamlit.Dockerfile
└── plugins/                        # source files for a tool the user already has
    └── cellprofiler_plugin/
        ├── generate.py
        └── cellprofiler_plugin_template.py.j2        # no Dockerfile
```

The split between `interfaces/` and `plugins/` reflects how the result is delivered. An interface is a complete app, so it gets a Dockerfile and is published as an image. A plugin is a file you drop into another program, so it has no Dockerfile of its own.

## The registry

`registry.py` maps each target name to its module and tries to import each one:

```python
_INTERFACE_MODULES = {
    "gradio": "bilayers_targets.interfaces.gradio.generate",
    "jupyter": "bilayers_targets.interfaces.jupyter.generate",
    "streamlit": "bilayers_targets.interfaces.streamlit.generate",
    "cellprofiler_plugin": "bilayers_targets.plugins.cellprofiler_plugin.generate",
}
```

If an import fails with `ModuleNotFoundError`, that target is left out of `available_ifaces` and everything else keeps working. This is how optional dependencies work: the Jupyter generator needs `nbformat`, and if you installed `bilayers-targets` without the `jupyter` extra, Jupyter simply doesn't appear. Any other error (a typo or bug in a generator) is raised, so broken generators don't silently disappear.

```{mermaid}
flowchart TB
    S["for each name in _INTERFACE_MODULES"] --> T{"import succeeds?"}
    T -- yes --> A["add to available_ifaces"]
    T -- "ModuleNotFoundError<br/>(missing optional dep)" --> K["skip it"]
    T -- "any other error" --> E["raise: it's a real bug"]
```

The extras in `bilayers-targets/pyproject.toml` are `gradio`, `jupyter`, `streamlit`, `cellprofiler_plugin`, plus the groups `interfaces`, `plugins`, and `all`.

## Anatomy of a generator

Every target exposes one function:

```python
def generate(interface_input: InterfaceInput) -> None: ...
```

It receives the dictionary, writes one file into `interface_input["output_dir"]`, and returns nothing. The four existing generators all follow the same steps inside:

```{mermaid}
flowchart LR
    A["unpack<br/>InterfaceInput"] --> B["adjust parameters<br/>(target-specific)"]
    B --> C["build title + citations<br/>shared/utils.py"]
    C --> D["render Jinja2<br/>template(s)"]
    D --> E["write file to<br/>output_dir"]
```

1. **Unpack** `inputs`, `outputs`, `parameters`, `display_only`, `exec_function`, `citations`, `docker_image`, and `cli_sequence`.
2. **Adjust parameters** where the target needs it (see the next section).
3. **Build the header.** `shared/utils.py:generate_top_level_text` combines the target's own citation (each `generate.py` defines a `CITATION` constant for Gradio, Jupyter, or Streamlit), the Bilayers citation, and the citations from the config into a title and a "please cite" block with licenses. This is why every generated app opens with the same citation text.
4. **Render** the Jinja2 template, passing the values plus two small filters, `lower` and `replace`, used to turn names into valid Python identifiers.
5. **Write** the result.

Nothing requires a new target to use Jinja2. The contract is only the `generate()` signature and the file it writes; the existing generators use Jinja2 because it's a convenient way to emit Python source.

### A shared trick: optional numbers

Some tools take a number that may be left unset, written in the config as a `float` or `integer` parameter with `default: None`. A plain number widget can't be empty, so the Gradio and CellProfiler generators split such a parameter in two: a **"Set a value for …?"** toggle and the number field itself. The number only reaches the command when the toggle is on.

```{mermaid}
flowchart LR
    P["parameter: min_size<br/>type: integer<br/>default: None"] --> S["set_min_size<br/>'Set a value for min size?'"]
    P --> N["min_size<br/>(number field)"]
    S -- "on" --> C["--min_size N added to command"]
    S -- "off" --> X["flag left out"]
```

## Two phases: generation time and run time

The most useful thing to keep in mind when reading this repo is that there are **two programs** per target, and they run at different times on different machines:

```{mermaid}
flowchart LR
    subgraph gen["Generation time · developer machine or CI"]
        direction TB
        G1["generate.py<br/>(Python + Jinja2)"] --> G2["template.py.j2"]
    end
    subgraph run["Run time · inside the container"]
        direction TB
        R1["app.py<br/>(plain Python, no Jinja)"] --> R2["the tool"]
    end
    gen -- "writes" --> run
```

- **`generate.py` + the template** run once, when you call `bilayers_cli generate`. Their job is to write Python source code.
- **The generated file** runs every time a user opens the app. It has no idea a config ever existed.

Everything from the config is **baked into the generated file as literals**. Widget labels, defaults, and options become arguments to `gr.Radio(...)` or `st.selectbox(...)`. The whole `cli_sequence` is written into the file as a Python list (`cli_sequence = [{...}, {...}]`). So when something looks wrong in a running app, there are two places to look: the template decides *what code* is written, and the generated file shows *exactly what was written*. Opening `dist/gradio/<algorithm>/app.py` is usually the fastest way to debug.

## Dissecting a generated app

Using Gradio's `app.py` as the reference, a generated file has six parts, top to bottom:

```{mermaid}
flowchart LR
    A["1 · Helpers"] --> B["2 · on_submit"] --> C["3 · Widgets"] --> D["4 · all_parameters"] --> E["5 · gr.Blocks layout"] --> F["6 · launch"]
```

| Part | What it contains |
| --- | --- |
| 1 · Helpers | `option_to_append`, `cli_tag_is_valid`, `generate_cli_command`, `create_zip_from_files` |
| 2 · `on_submit(...)` | One argument per widget. Builds the command, runs the tool, collects outputs, zips them. |
| 3 · Widgets | One `gr.*` component per input, parameter, and display-only entry |
| 4 · `all_parameters` | The widgets in the same order as `on_submit`'s arguments, which is how Gradio matches values to arguments |
| 5 · `gr.Blocks` layout | Left column: widgets and **Run**. Right column: output files and **Download All (zip)**. Wires Run → `on_submit`, and each `set_*` toggle → its number field's visibility. |
| 6 · `app.launch` | `server_port=7878`, `share=True` |

Streamlit's file follows the same order with Streamlit widgets inside an `st.form`. Jupyter splits the same responsibilities across three cells, and the CellProfiler module spreads them across the methods CellProfiler expects (`create_settings`, `settings`, `visible_settings`, `run`).

### From config field to widget

The `type` of each input, parameter, or display-only entry picks the widget:

| Config `type` | Gradio | Streamlit | Jupyter | CellProfiler |
| --- | --- | --- | --- | --- |
| `image`, `file`, `measurement`, `array`, `executable` (inputs) | `gr.Files` | `st.file_uploader` | `FileUpload`, or a "Using Mounted Directory" notice | image/object picker from the pipeline |
| `integer`, `float` | `gr.Number` | `st.number_input` | `IntText` / `FloatText` | `Integer` / `Float` |
| `textbox` | `gr.Textbox` | `st.text_input` | `Textarea` | `Text` |
| `checkbox` | `gr.Checkbox` | `st.checkbox` | `Checkbox` | `Binary` |
| `radio` | `gr.Radio` | `st.radio` | `RadioButtons` | `Choice` |
| `dropdown` | `gr.Dropdown` (`multiselect` honored) | `st.selectbox`, or `st.multiselect` | `Dropdown` (single choice) | `Choice` (single choice) |

`display_only` entries use the same widgets with editing switched off and a "display only" label. Their values are passed to `on_submit` but never reach the command (see below).

### From widget value to command-line flag

When the user clicks Run, `on_submit` collects every widget value and calls `generate_cli_command(cli_sequence, **values)`. That function starts from `exec_function.cli_command` and walks the baked-in `cli_sequence` in order. For each entry it decides what, if anything, to append. This is the Gradio/Streamlit version; Jupyter's `construct_cli_command` applies the same rules except for the run subfolder:

```{mermaid}
flowchart TB
    S["next entry in cli_sequence"] --> H{"hidden arg?"}
    H -- yes --> HV["use its fixed value"]
    H -- no --> UV["use the widget value<br/>(or the default)"]
    HV --> E{"empty?"}
    UV --> E
    E -- "empty + optional" --> SKIP["skip"]
    E -- "empty + required" --> ERR["stop: '… is Mandatory!'"]
    E -- "has a value" --> T{"what kind?"}
    T -- "bool" --> B{"append_value?"}
    B -- yes --> B1["--flag True / False"]
    B -- no --> B2["--flag only if True"]
    T -- "uploaded files" --> F1["copy files into folder_name<br/>pass the folder path"]
    T -- "textbox with output_dir_set" --> O1["create &lt;value&gt;/run_&lt;timestamp&gt;_&lt;id&gt;/<br/>pass that folder"]
    T -- "'ignore' (radio/dropdown)" --> SKIP
    T -- "anything else" --> V1["format with cli_tag"]
```

Formatting with `cli_tag` (`option_to_append`) has three forms, plus one way to say "no flag":

| `cli_tag` | Value | Appended |
| --- | --- | --- |
| `--sigma_size` | `5` | `--sigma_size 5` |
| `--sigma_size=` | `5` | `--sigma_size=5` |
| `""` (empty) | `5` | `5` (a bare positional argument) |
| `None` or `"None"` | anything | nothing |

Two details worth knowing:

- **In Gradio and Streamlit, each run gets a fresh output folder.** The output-path parameter isn't passed as typed. The app creates a `run_<timestamp>_<4 hex chars>` subfolder under it, so repeated runs never overwrite each other, and the app knows exactly which folder to read results from. Jupyter passes the path as typed, so a second run writes into the same folder.
- **The command is a single shell string**, run with `subprocess.run(..., shell=True)`. If it fails, the app shows the tool's `stderr` and asks the user to report the error on GitHub.

### Getting files in

Uploaded files have to land where the tool expects them, which is the input's `folder_name` (for example `/bilayers/input_images`):

```{mermaid}
flowchart LR
    U["user's files"] --> GR["Gradio: gr.Files"]
    U --> STU["Streamlit: st.file_uploader"]
    U --> JU{"Jupyter: is folder_name<br/>mounted and non-empty?"}
    GR -- "copy" --> FN["folder_name"]
    STU -- "write" --> FN
    JU -- "yes" --> FN
    JU -- "no: FileUpload" --> TMP["temp folder"]
    FN --> CMD["--input_flag &lt;folder&gt;"]
    TMP --> CMD
```

Jupyter is the only target that checks for a mounted folder: if you start the container with `-v /your/data:/bilayers/input_images`, the notebook skips uploading and uses your files in place. This avoids pushing large datasets through the browser.

### Getting results out

| Target | Where it looks | If that folder is missing |
| --- | --- | --- |
| Gradio | every file in the run folder | copies every non-code file under the working directory into `outputs/` |
| Streamlit | every file in the run folder | files that appeared or changed in the input folders during the run |
| Jupyter | nothing collected; results stay wherever the tool wrote them (the output path you set) | n/a |
| CellProfiler | files in `output/` whose names contain each output's `unique_string` and match its `format` | the output is left empty, with a warning |

Gradio and Streamlit then zip what they found for download. Note that the web interfaces don't use `unique_string`. It only matters to the CellProfiler plugin today.

## Which config fields each target uses

Not every field in the schema affects every target. This is the current state of the templates on `main`:

| Field | Gradio | Streamlit | Jupyter | CellProfiler |
| --- | --- | --- | --- | --- |
| `type`, `label`, `description`, `default`, `optional` | ✓ | ✓ | ✓ | ✓ |
| `cli_tag`, `cli_order` (via `cli_sequence`) | ✓ | ✓ | ✓ | ✓ |
| `folder_name` | ✓ | ✓ | ✓ | ✓ (container mount points) |
| `output_dir_set` | ✓ (run subfolder) | ✓ (run subfolder) | | ✓ |
| `options` | ✓ | ✓ | ✓ | ✓ |
| `multiselect` | ✓ | ✓ | | |
| `append_value` | ✓ | ✓ | ✓ | ✓ |
| `file_count` | ✓ (inputs) | always multiple | always multiple | ✓ (outputs) |
| `mode` (`beginner` / `advanced`) | | | ✓ (Beginner's / Advanced sections) | |
| `unique_string`, `format` | | | | ✓ (finding outputs) |
| `subtype` | | | | ✓ (`label` → objects) |
| `docker_image` | | | | ✓ (the image it runs) |
| `section_id` | | | | |

`section_id` is validated by the schema but not yet used by any template. Gaps like these are where the schema and the generators can drift; the [Contributing](../developer_guide/contributing.md) page describes how spec changes and generator changes are kept in step.

### The command builder exists in more than one place

There is no shared runtime library: each generated file must run on its own inside the container, so each template carries its **own copy** of the command-building logic. Gradio and Streamlit each have `generate_cli_command`, Jupyter has `construct_cli_command`, and the CellProfiler template builds its `docker run` command inline. The orchestrator has a fifth, `bilayers/src/bilayers/cli_generator.py`, which backs `bilayers_cli generate --cli`.

```{mermaid}
flowchart TB
    SEQ["cli_sequence<br/>(ordered once, in parse.py)"]
    SEQ --> C0["cli_generator.py<br/>bilayers_cli --cli"]
    SEQ --> C1["gradio_template: generate_cli_command"]
    SEQ --> C2["streamlit_template: generate_cli_command"]
    SEQ --> C3["jupyter_template: construct_cli_command"]
    SEQ --> C4["cellprofiler template: docker run … inline"]
```

The *order* can't drift, because it's decided once in `parse.py`. The *formatting rules* (the `cli_tag` forms, `append_value`, `"ignore"`, output folders) can. If you change how a flag is formatted, change it in all five places and regenerate the golden files; otherwise `--cli` and the apps will quietly disagree.

## How each target differs

| | Gradio | Jupyter | Streamlit | CellProfiler plugin |
| --- | --- | --- | --- | --- |
| **Templates** | 1 | 3 (one per cell) | 1 | 1 |
| **File written** | `app.py` | `generated_notebook.ipynb` | `streamlit_app.py` | `run<algorithm>.py` |
| **Dockerfile** | `Gradio.Dockerfile` | `Jupyter.Dockerfile` | `Streamlit.Dockerfile` | none |
| **Port** | 7878 | 7878 | 8501 | n/a |
| **Runs the tool by** | `subprocess` inside the container | `subprocess` inside the container | `subprocess` inside the container | starting the algorithm image with `docker run` / `podman run` |
| **Results returned as** | file list + zip download | files in the output folder | zip download | images/objects added to the CellProfiler workspace |

### Gradio, Streamlit, Jupyter: the app and the tool share a container

The three interfaces work the same way at run time. Their Dockerfile starts `FROM` the algorithm's image, installs the UI library, and copies in the generated file. So the app and the tool end up in the same container, and the app runs the tool as an ordinary command.

```{mermaid}
flowchart TB
    subgraph c["one container: bilayer/&lt;algorithm&gt;:&lt;version&gt;-&lt;interface&gt;"]
        direction LR
        UI["generated app<br/>(app.py / notebook / streamlit_app.py)"] -- "subprocess.run(command)" --> TOOL["the tool<br/>(from the base image)"]
        TOOL -- "writes files" --> OUTD["output folder"]
        OUTD -- "read back + zip" --> UI
    end
    B["browser"] <-- "port 7878 / 8501" --> UI
```

The command itself is built inside the app by a function called `generate_cli_command`, which walks the `cli_sequence` baked into the file at generation time and fills in the user's choices. The ordering was decided once, in the orchestrator; the app only substitutes values.

**Gradio** (`app.py`) lays out inputs, parameters, and display-only fields as Gradio components, runs the command when you click submit, then lists the result files and offers **Download All (zip)**. It launches with `share=True`, so Gradio also prints a temporary public link. If the tool's output folder can't be found, it falls back to gathering every non-code file under the working directory into `outputs/`.

**Streamlit** (`streamlit_app.py`) follows the same pattern with Streamlit widgets: upload, run, then a **Download results** button for `outputs.zip`.

**Jupyter** is built differently. The generator assembles the notebook with `nbformat` from three separately rendered templates, and hides the code of each cell so the user sees widgets rather than code:

```{mermaid}
flowchart TB
    T["# Title + citations (markdown)"] --> C1
    C1["Cell 1 (hidden): widgets + live command preview<br/>jupyter_template.py.j2"] --> C2
    C2["Cell 2 (hidden): check every required field has a value<br/>jupyter_final_validation_template.py.j2"] --> C3
    C3["Cell 3 (hidden): run the command<br/>jupyter_shell_command_template.py.j2"]
```

If the command fails, cell 3 prints the full error and shows a **Report Issue** button that opens a GitHub issue on `bilayers` with the stack trace already filled in. Anyone who wants to see or change what's happening can expand a cell, which is the main reason to choose Jupyter over the web apps.

### CellProfiler plugin: a module that starts a container

The plugin is not packaged into an image. The generator writes one Python file, a CellProfiler module class named `Run` + the algorithm name in CamelCase (`gaussian_smoothing` becomes `RunGaussianSmoothing` in `rungaussiansmoothing.py`; CellProfiler requires the file name to match the class name in lowercase).

**Choosing a module category.** CellProfiler groups modules into categories, so the generator works one out from the config. Each input and output type is reduced to *image*, *object* (an image whose `subtype` includes `label`), or *measurement*, and the pair (input kinds, output kinds) is looked up in a table:

```{mermaid}
flowchart LR
    IN["input kinds"] --> L{"lookup table"}
    OUT2["output kinds"] --> L
    L -- "image → image" --> IP["Image Processing"]
    L -- "image → object" --> IS["Image Segmentation"]
    L -- "object → image/object" --> OP["Object Processing"]
    L -- "anything → measurement only" --> M["Measurement"]
    L -- "measurement → image/object" --> NS["not supported:<br/>generation stops with an error"]
```

These are the common cases; the full table is `CATEGORY_MATRIX` in `plugins/cellprofiler_plugin/generate.py`. The unsupported case (internally called "Decoder") only stops the plugin; the other targets still generate.

**At run time** the module does the container work itself:

```{mermaid}
sequenceDiagram
    participant CP as CellProfiler
    participant M as Run#lt;Algorithm#gt; module
    participant D as Docker / Podman
    CP->>M: run(workspace)
    M->>M: find docker or podman (PATH + common install paths)
    M->>M: make temp input/ and output/ folders
    M->>M: save the pipeline's images into input/
    M->>D: docker run --rm -v input:... -v output:... #lt;docker_image#gt; #lt;command#gt;
    D-->>M: tool writes results into output/
    M->>M: match files by each output's unique_string
    M-->>CP: add images / objects to the workspace
```

Because it runs `docker_image` from the config directly, the plugin uses the algorithm's base image, not an interface image. The user needs Docker or Podman installed and running, and picks which one in the module's settings.

## From generated file to image

The Dockerfiles in `bilayers-targets` are templates in their own right: each takes `BASE_IMAGE`, `FOLDER_NAME`, and `INTERFACE` as build arguments. `nox -s build_interface` finds the right one by capitalizing the target name (`gradio` → `Gradio.Dockerfile`), points it at the algorithm image, and copies in the file from `dist/`. See [Core Data Flow → Package](data_flow.md#package-image) for the build and tagging steps.

## Adding a target

A new target is a new folder with a `generate.py` (and, for an interface, a `<Name>.Dockerfile`), one line in `registry.py`, and an optional-dependency extra. The step-by-step version is in [Add a New Interface](../developer_guide/add_interface.md). The Gradio generator is the best one to copy from: it's a single template and shows the optional-number split.
