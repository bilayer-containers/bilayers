---
title: Understanding config.yaml file
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

To create your interface, you need to understand the structure of the config.yaml file and its key components:

The config.yaml file defines how the interface interacts with your algorithm. At the code level, it's located at `bilayers/src/algorithms/algorithm_name/config.yaml`. The algorithm_name should reflect the task, such as cellpose_inference or cellpose_training, so name it accordingly.

Each config.yaml contains key sections: `parameters`, `display_only`, `results`, `exec_function`, `docker_image`, `algorithm_folder_name`, and `citations`. You can copy the basic structure from an existing example.

This file is then converted into a CLI command, where user-provided inputs are passed as command-line arguments, enabling the retrieval of the desired output.
- **parameters**: These are key in building command-line arguments. Each object under this keyword forms part of the command line, with arguments either taken from the user or using default values.
- **display_only**: These fields are displayed on the interface but aren’t included in the CLI command. No cli_tag should be passed to these objects; otherwise, they function like parameters.
- **results**: Similar to parameters, but they define the expected output type and label it on the UI as the output. Typically, this is a file type.
- **exec_function**: Defines the function that converts the config.yaml into a Gradio or Jupyter Notebook interface. It also includes the initial part of the CLI command and a special hidden_args section if applicable.
- **docker_image**: Contains details of the base image (organization, name, and tag) used to build the Docker image for each interface.
- **algorithm_folder_name**: Specifies the folder where the generated Gradio and Jupyter Notebook files are stored.
- **citations**: Used to reference relevant research or materials related to the algorithm.

```{code} yaml
:filename: config.yml
parameters:

display_only:

results:
  
exec_function:
 name: "generate_cli_command"
 script:
 module:
 cli_command:
 hidden_args:

docker-image:
 org:
 name:
 tag:

algorithm_folder_name:

citations:
 Algorithm:
   - name: ""
     doi: xxxx
     description: ""
```

Before you start working on the `config.yaml` file, we recommend reviewing the command-line usage of the specific algorithm you're building an interface for. This will help you determine what should go in `parameters`, `display_only`, `results`, and `exec_function`'s `hidden_args`.

## Understanding `cli_command`

The `cli_command` is the starting point for executing the command line, like `python -m cellpose`, which is then followed by appending parameters and their arguments. We will cover more about `cli_command` in the context of the `exec_function`, but for now, it's important to understand its role.

## Organizing Parameters from the Algorithm's Command-Line Usage

- parameters: If the parameter and its argument need to be passed in the command line, include them in `parameters`.
- display_only: If you want to show some information to the user without appending it to the command line, include it in `display_only`.
- results: Anything that you want to appear as output should go under `results`. For these, you can set the `cli_tag` as `None`.

## Defining parameters

Each `parameter` object has mandatory tags, some of which depend on the parameter type. While the order of tags should generally be maintained, it’s okay if they are slightly rearranged.
```{code} yaml
:filename: config.yml
name: 
type: 
label: ""
description: ""
default: 
cli_tag: ""
cli_order: 0
optional: True
section_id: ""
mode: ""
```

- **name**: This should be a simple name, ideally matching the `cli_tag` (without hyphens). Use underscores instead of spaces. 
  Example: ```name: use_gpu```

- **type**: This defines how the parameter will appear on the user interface. For example, if you want a Checkbox, the `type` should be set to `checkbox`.
  Example: ```type: checkbox```

    Below is a list of supported types and how they will appear in Gradio or Jupyter Notebook.

    :::{table} supported type in config.yaml
    :label: tbl:areas-html

    <table>
    <tr>
        <th rowspan="1">type(in config.yaml file)</th>
        <th rowspan="1">Gradio</th>
        <th rowspan="1">Jupyter Notebook</th>
    </tr>

    <tr>
        <td>checkbox</td>
        <td>Checkbox</td>
        <td>Checkbox</td>
    </tr>

    <tr>
        <td>integer</td>
        <td>Number (decimal values allowed)</td>
        <td>IntText (allows to put Integer values)</td>
    </tr>

    <tr>
        <td>float</td>
        <td>Number (decimal value allowed)</td>
        <td>FloatText (allows to put Float values)</td>
    </tr>

    <tr>
        <td>files</td>
        <td>Drag & Drop your files from local system</td>
        <td>Volume Mount supported (no need to put in files thru UI)</td>
    </tr>

    <tr>
        <td>radio</td>
        <td>Radio</td>
        <td>RadioButtons</td>
    </tr>

    <tr>
        <td>dropdown</td>
        <td>Dropdown</td>
        <td>Dropdown</td>
    </tr>
    
    </table>
    :::

    #### Details on the `type` Tag
    `type` is the whole world in itself!

    With the different `type` there are certain extra flags that you need to put in depending on the value of the flag `type`.

    :::{table} Understanding which extra flags are needed and their purpose
    :label: tbl:areas-html

    <table>
    <tr>
        <th rowspan="1">type</th>
        <th rowspan="1">Extra flag</th>
        <th rowspan="1">Accepted Values</th>
        <th rowspan="1">Purpose</th>
    </tr>

    <tr>
        <td>checkbox</td>
        <td>append_value</td>
        <td>True | False</td>
        <td>Determines how the CLI command is constructed:
            - If append_value: True:
                - If user input is True: --cli_tag True
                - If user input is False: --cli_tag False
            - If append_value: False:
                - If user input is True: --cli_tag
                - If user input is False: No command appended.</td>
    </tr>

    <tr>
        <td>integer</td>
    </tr>

    <tr>
        <td>float</td>
    </tr>

    <tr>
        <td>files</td>
        <td>file_count</td>
        <td>single | multiple</td>
        <td>Defines how many files should be accepted:
        <b>Note:</b>
            - If file_count: multiple, the default must be "directory".
            - If file_count: single, the default must be "single".</td>
    </tr>

    <tr>
        <td>files</td>
        <td>folder_name</td>
        <td>"/bilayers/.."</td>
        <td>Since the CLI argument only takes a folder name, specify it explicitly. This should also match the volume mount path when running the container.</td>
    </tr>

    <tr>
        <td>textbox</td>
        <td>output_dir_set (This is conditional and used only if output’s folder_path is specified through this flag. Additionally, set the default value to the folder path.)</td>
        <td>True | False</td>
        <td>Determines whether the user can modify the folder path:
            - If True: The user can change the folder path.
            - If False: The path is fixed and cannot be modified, but the user can still view it.
        </td>
    </tr>

    <tr>
        <td>radio</td>
        <td>

            options:
                - label: GRAY
                value: 0
                - label: RED
                value: 1
                - label: GREEN
                value: 2

    </td>
        <td>List of labels and values</td>
        <td>Each option has a label and value:
        - label: Displayed on the UI
        - value: Attached to the cli_tag based on the selected label.</td>
    </tr>

    <tr>
        <td>dropdown</td>
        <td>

            options:
                - label: GRAY
                  value: 0
                - label: RED
                  value: 1
                - label: GREEN
                  value: 2
    
    </td>
        <td>List of labels and values</td>
        <td>Each option has a label and value:
            - label: Displayed on the UI
            - value: Attached to the cli_tag based on the selected label.</td>
    </tr>

    <tr>
        <td>dropdown</td>
        <td>multiselect</td>
        <td>False</td>
        <td>It as of now only supports 1 value to be attached with a cli_tag</td>
    </tr>

    </table>

    Also, here’s a collection of templates for each type that you can copy and paste directly into your config.yaml file.

    You can find all types of templates listed below:

    :::{dropdown} type: checkbox
    :open:
    ```{code} yaml
    -   name: 
        type: checkbox
        label: ""
        description: ""
        default: False
        cli_tag: ""
        cli_order: 0
        optional: True
        append_value: False
        section_id: ""
        mode: ""
    ```
    :::

    :::{dropdown} type: integer
    :open:
    ```{code} yaml
    -   name: 
        type: integer
        label: ""
        description: ""
        default: 0
        cli_tag: ""
        cli_order: 0
        optional: True
        section_id: ""
        mode: ""
    ```
    :::

    :::{dropdown} type: float
    :open:
    ```{code} yaml
    -   name: 
        type: float
        label: ""
        description: ""
        default: 
        cli_tag: ""
        cli_order: 0
        optional: True
        section_id: ""
        mode: ""
    ```
    :::

    :::{dropdown} type: files, file_count: single
    :open:
    ```{code} yaml
    -   name: 
        type: files
        label: ""
        description: ""
        file_count: "single"
        default: "single"
        cli_tag: ""
        cli_order: 0
        optional: True
        section_id: ""
        folder_name: ""
        mode: ""
    ```
    :::

    :::{dropdown} type: files, file_count: multiple
    :open:
    ```{code} yaml
    -   name: 
        type: files
        label: ""
        description: ""
        file_count: "multiple"
        default: "directory"
        cli_tag: ""
        cli_order: 0
        optional: True
        section_id: ""
        folder_name: ""
        mode: ""
    ```
    :::
    
    :::{dropdown} type: textbox (standard textbox)
    :open:
    ```{code} yaml
    -   name: 
        type: textbox
        label: ""
        description: ""
        default: ""
        cli_tag: ""
        cli_order: 0
        optional: True
        section_id: ""
        mode: "" 
    ```
    :::

    :::{dropdown} type: textbox (specifying folder path in default)
    :open:
    ```{code} yaml
    -   name: 
        type: textbox
        label: ""
        description: ""
        output_dir_set: True
        default: "/bilayers/my_folder_name"
        cli_tag: ""
        cli_order: 0
        optional: True
        section_id: ""
        mode: 
    ```
    :::

    :::{dropdown} type: radio
    :open:
    ```{code} yaml
    -   name: 
        type: radio
        label: ""
        description: ""
        options: 
        - label: 
          value: 
        - label: 
          value: 
        default: 
        cli_tag: ""
        cli_order: 0
        optional: True
        section_id: ""
        mode: ""
    ```
    :::

    :::{dropdown} type: dropdown
    :open:
    ```{code} yaml
    -   name: 
        type: dropdown
        label: ""
        description: ""
        options: 
        - label: 
          value: 
        - label:
          value: 
        default: True
        multiselect: False
        cli_tag: ""
        cli_order: 0
        optional: True
        section_id: ""
        mode: ""
    ```
    :::


## Defining display_only

`display_only` functions similarly to `parameters`, but the key difference is that these objects are only displayed in the user interface and are not appended to the `cli_command`. They are non-interactive, meaning users cannot modify the values, which will always reflect the default specified in the `config.yaml` file.

Since they are not part of the `cli_command`, you can omit `cli_tag` and `cli_order`. For the rest of the structure, you can reuse the template from `parameters` based on the object type.

## Defining results
`results` represent the outputs or results generated after executing the command. In most cases, this will be defined as `type: files`. The structure follows the same format as `parameters`, but currently, Bilayers only supports `type: files`. If you require additional result types, please submit a feature request here.

For `results`, the `cli_tag` should always be set to "None," and there's no need to specify `cli_order`.

Note that `results` are not typically sourced from the documentation. 

```{code} yaml
:filename: config.yml
results:
  - name: output_dir
    type: Files
    label: "Download Outputs"
    description: ""
    cli_tag : "None"
    optional: True
    section_id: "output-section"
    mode: ""
```

## Defining exec_function
exec_function is instrumental in converting the yaml file to desired interface. It defines the specific function responsible for this conversion. The `exec_function` consists of the following components: `name`, `script`, `module`, `cli_command`, and `hidden_args`.

Below is the template to attach directly to your configuration file, followed by a breakdown:
```{code} yaml
:filename: config.yml
exec_function:
 name: "generate_cli_command"
 script: ""
 module: "Algorithms."
 cli_command: ""
 hidden_args:
   # dummy example
   # - cli_tag: "--save_png"
   #   value: "True"
   #   append_value: False
   #   cli_order: 3
```

Below is an example to follow, along with a breakdown of each component:
```{code} yaml
:filename: config.yml
exec_function:
 name: "generate_cli_command"
 script: "cellpose_inference"
 module: "Algorithms.cellpose_inference"
 cli_command: "python -m cellpose --verbose"
 hidden_args:
   # dummy example
   # - cli_tag: "--save_png"
   #   value: "True"
   #   append_value: False
   #   cli_order: 3
```
- name: This is the name of the function that converts the `yaml` file into the interface dynamically. It remains the same for all algorithms, so no changes are needed. 
 name: "generate_cli_command"

- script: The name of the algorithm’s parent folder, which can either be `algorithm_inference` or `algorithm_training`.  
Example: script: "cellpose_inference"

- module: The module name for the algorithm, followed by the script name, separated by a dot.
Example: module: "Algorithms.cellpose_inference"

- cli_command: As mentioned earlier, the cli_command refers to the `module execution` in the documentation. This serves as the starting point, and the cli_tag and argument pairs are appended to it. Refer to the documentation for proper configuration.

In command-line systems, there are several common command line patterns used for constructing a cli_command. Here, we support several widely used patterns: [Explore the full discussion here](https://github.com/bilayer-containers/bilayers/issues/37)
1. someexecutable --unordered_flag_1 unordered_value_1  --unordered_flag_2 unordered_value_2
2. someexecutable unordered_value_1 unordered_value_2
3. someexecutable ordered_value_1 unordered_value_2
4. someexecutable --ordered_flag_1 ordered_value_1 unordered_value_2
5. someexecutable ordered_value_1 --unordered_flag_2 unordered_value_2
6. someexecutable --unordered_flag_1=unordered_value_1 --unordered_flag_2 unordered_value_2
7. someexecutable --ordered_flag_1=ordered_value_1 unordered_value_2

#### What are ordered_flag and unordered_flag?
In some cases, cli_command requires flags in fixed positions (e.g., always the 1st or last argument). To handle this, we use the cli_order flag. Here's how it works:
- Specify a positive number (1 to n) in cli_order to fix the position of the cli_flag and argument pair.
- If cli_order is set to 0 or not specified, it will be treated as an unordered_flag, and all such flags will appear after ordered ones.
- Negative numbers in cli_order will place the flag in the last position, after all unordered flags.

#### How to specify --flag_1=value_1?
By default, flags and their arguments are appended with a space between them. If you want to use = between the flag and value, simply add an = at the end of cli_tag.
For example, 
cli_tag: “--savedir=”
default: “/bilayers/my_outputs”
This will generate: someexecutable --savedir=/bilayers/my_outputs

#### hidden_args: Need of hidden_args?
Sometimes, certain `cli_tag` and argument values should always be included in the `cli_command`, but you don’t want to expose them in the user interface. In these cases, use `hidden_args`.

#### Where can it be used?
A potential use case for hidden_args is ensuring output files are saved to a specific folder without allowing the user to modify it. If the algorithm's command-line usage includes a specific cli_tag for this, you can define it as a hidden_arg. Use the following fields to configure hidden_args:

  - `cli_tag`: The command-line tag to be used.
  - `value`: The fixed value for the tag.
  - `append_value`: (Optional) Used for checkbox type to specify whether the value should be appended with the cli_tag.
  - `cli_order`: (Optional) Specifies the order in which this tag should appear in the `cli_command`. If not set, it will appear after all ordered tags but before any negatively indexed ones.

## Defining docker_image
Each interface’s Docker image is built on top of the base Docker image specific to the algorithm. Therefore, it's highly recommended to choose an algorithm with a pre-built Docker image available on DockerHub.

For guidance on selecting a compatible base image, refer [Choosing the Right Base Docker Image](right_base_docker_image)

To specify the image, select one from DockerHub. Here's how it works with an example:  
For instance, `cellprofiler/runcellpose_no_pretrained:0.1` can be broken down into three parts:

- **org**: The part before `/` is the username or organization (e.g., `cellprofiler`).
- **name**: The part between `/` and `:` is the image name (e.g., `runcellpose_no_pretrained`).
- **tag**: The part after `:` is the tag, which can be a version number or a term like `latest` (e.g., `0.1`).

To learn more about docker image naming, refer to [What are Docker tags?](https://medium.com/free-code-camp/an-introduction-to-docker-tags-9b5395636c2a)

Also, here’s the template to directly paste in your config.yaml file
```{code} yaml
:filename: config.yml
docker-image:
 org: 
 name: 
 tag: 
```

## Defining algorithm_folder_name
This specifies the folder where the generated Gradio and Jupyter Notebook interface files will be stored. The folder name should follow the convention of the `config.yaml`'s parent folder, such as `algorithm_inference` or `algorithm_training`.  
Example: algorithm_folder_name: "cellpose_inference"

## Defining citations
Citations are used to credit the relevant works associated with the algorithm. Include the correct name, DOI, and description of the algorithm. Guidelines on how to find citations can be found here. Note that interface citations are added dynamically, so you don’t need to include them manually.
```{code} yaml
:filename: config.yml
citations:
 Algorithm:
   - name: "cite-1"
     doi: 
     description: ""
   - name: "cite-2"
     doi: 
     description: ""
```

Sample Example:
```{code} yaml
:filename: config.yml
citations:
 Algorithm:
   - name: "Cellpose"
     doi: 10.1038/s41592-020-01018-x
     description: "Deep Learning algorithm for cell segmentation in microscopy images"
```