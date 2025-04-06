# bilayers_schema

Validate each of the incoming Algorithm's spec file

URI: https://w3id.org/my-org/bilayers_schema

Name: bilayers_schema



## Classes

| Class | Description |
| --- | --- |
| [AbstractUserInterface](AbstractUserInterface.md) | Abstract class for user interface |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[TypeDisplayOnly](TypeDisplayOnly.md) | Display only parameters of a specific Algorithm |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[TypeParameter](TypeParameter.md) | Parameters of a specific Algorithm |
| [AbstractWorkflowDetails](AbstractWorkflowDetails.md) | Abstract class for details needed to fit config in the workflow |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[TypeInput](TypeInput.md) | Inputs to the algorithm from the last step of the workflow |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[TypeOutput](TypeOutput.md) | Outputs of the algorithm to the next step in the workflow |
| [Any](Any.md) | Any type |
| [DockerImage](DockerImage.md) | Description of docker_image for the specific algorithm |
| [ExecFunction](ExecFunction.md) | Function to execute the Algorithm |
| [HiddenArgs](HiddenArgs.md) | Hidden arguments for the Algorithm |
| [RadioOptions](RadioOptions.md) | Options of the Radio button in parameters, display_only |
| [SpecContainer](SpecContainer.md) | SpecContianer class which holds all the high_level keywords from config.yaml file of specific algorithm |
| [TypeCitations](TypeCitations.md) | Citations of the Algorithm |



## Slots

| Slot | Description |
| --- | --- |
| [algorithm_folder_name](algorithm_folder_name.md) | Main folder name of the algorithm to put the generated files in the folder |
| [append_value](append_value.md) | Append value of the hidden argument |
| [citations](citations.md) | Citations of the Algorithm |
| [cli_command](cli_command.md) | CLI command to execute the Algorithm |
| [cli_order](cli_order.md) | Order of the CLI arguments |
| [cli_tag](cli_tag.md) | CLI tag of the object |
| [default](default.md) | Default value of the parameter |
| [depth](depth.md) | whether z-dimension i |
| [description](description.md) | Description of the Algorithm |
| [display_only](display_only.md) | Display only parameters of a specific Algorithm |
| [docker_image](docker_image.md) | Description of docker_image for the specific algorithm |
| [doi](doi.md) | DOI of the Algorithm |
| [exec_function](exec_function.md) | Function to execute the Algorithm |
| [file_count](file_count.md) | Type of Number of files |
| [folder_name](folder_name.md) | Folder name of the object |
| [format](format.md) | Format of the inputs and outputs |
| [hidden_args](hidden_args.md) | Hidden arguments for the Algorithm |
| [inputs](inputs.md) | Inputs to the algorithm from the last step of the workflow |
| [interactive](interactive.md) | Whether the object is interactive on UI |
| [label](label.md) | Label of the object, but also Radio button's label |
| [license](license.md) | License of the Algorithm |
| [mode](mode.md) | Mode of the object |
| [multiselect](multiselect.md) | Multiselect value of the dropdown |
| [name](name.md) | Name of the docker_image, algorithm, parameter, display_only |
| [optional](optional.md) | Optional value of the object |
| [options](options.md) | Options of the Radio button in parameters, display_only |
| [org](org.md) | Organization of the docker image |
| [output_dir_set](output_dir_set.md) | Output directory set |
| [outputs](outputs.md) | Outputs of the algorithm to the next step in the workflow |
| [parameters](parameters.md) | Parameters of a specific Algorithm |
| [path](path.md) | Path of the inputs and outputs |
| [platform](platform.md) | Platform on which the docker image was built |
| [pyramidal](pyramidal.md) | whether pyramidal images are accepted via tool |
| [section_id](section_id.md) | Section ID of the object |
| [subtype](subtype.md) | Subtype of the inputs and outputs |
| [tag](tag.md) | Tag of the docker image |
| [tiled](tiled.md) | whether tiled images are accepted via tool |
| [timepoints](timepoints.md) | whether t-dimension i |
| [type](type.md) | Type of the inputs, parameters and outputs |
| [value](value.md) | Value of the hidden argument or RadioButton Option's Value |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [FileTypeEnum](FileTypeEnum.md) | Type of Number of files |
| [ModeEnum](ModeEnum.md) | Mode of the parameters, display_only |
| [SubTypeEnum](SubTypeEnum.md) | Subtype of the inputs and outputs, iff type is image |
| [TypeEnum](TypeEnum.md) | Type of the parameters, display_only |


## Types

| Type | Description |
| --- | --- |
| [Boolean](Boolean.md) | A binary (true or false) value |
| [Curie](Curie.md) | a compact URI |
| [Date](Date.md) | a date (year, month and day) in an idealized calendar |
| [DateOrDatetime](DateOrDatetime.md) | Either a date or a datetime |
| [Datetime](Datetime.md) | The combination of a date and time |
| [Decimal](Decimal.md) | A real number with arbitrary precision that conforms to the xsd:decimal speci... |
| [Double](Double.md) | A real number that conforms to the xsd:double specification |
| [Float](Float.md) | A real number that conforms to the xsd:float specification |
| [Integer](Integer.md) | An integer |
| [Jsonpath](Jsonpath.md) | A string encoding a JSON Path |
| [Jsonpointer](Jsonpointer.md) | A string encoding a JSON Pointer |
| [Ncname](Ncname.md) | Prefix part of CURIE |
| [Nodeidentifier](Nodeidentifier.md) | A URI, CURIE or BNODE that represents a node in a model |
| [Objectidentifier](Objectidentifier.md) | A URI or CURIE that represents an object in the model |
| [Sparqlpath](Sparqlpath.md) | A string encoding a SPARQL Property Path |
| [String](String.md) | A character string |
| [Time](Time.md) | A time object represents a (local) time of day, independent of any particular... |
| [Uri](Uri.md) | a complete URI |
| [Uriorcurie](Uriorcurie.md) | a URI or a CURIE |


## Subsets

| Subset | Description |
| --- | --- |
