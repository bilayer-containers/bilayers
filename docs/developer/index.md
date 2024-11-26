# validate_schema

Validate each of the incoming Algorithm's spec file

URI: https://w3id.org/my-org/validate_schema

Name: validate_schema



## Classes

| Class | Description |
| --- | --- |
| [AbstractUserInterface](AbstractUserInterface.md) | Abstract class for user interface |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[TypeDisplayOnly](TypeDisplayOnly.md) | Display only parameters of a specific Algorithm |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[TypeParameter](TypeParameter.md) | Parameters of a specific Algorithm |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[TypeResults](TypeResults.md) | Results of a specific Algorithm |
| [Any](Any.md) | Any type |
| [Container](Container.md) | Container class which holds all the high_level keywords from config.yaml file of specific algorithm |
| [DockerImage](DockerImage.md) | Description of docker_image for the specific algorithm |
| [ExecFunction](ExecFunction.md) | Function to execute the Algorithm |
| [HiddenArgs](HiddenArgs.md) | Hidden arguments for the Algorithm |
| [RadioOptions](RadioOptions.md) | Options of the Radio button in parameters, display_only, results |
| [TypeAlgorithmFromCitation](TypeAlgorithmFromCitation.md) | Algorithm's citations |
| [TypeCitations](TypeCitations.md) | Citations of the Algorithm |



## Slots

| Slot | Description |
| --- | --- |
| [algorithm](algorithm.md) | Algorithm's citations |
| [algorithm_folder_name](algorithm_folder_name.md) | Main folder name of the algorithm to put the generated files in the folder |
| [append_value](append_value.md) | Append value of the hidden argument |
| [citations](citations.md) | Citations of the Algorithm |
| [cli_command](cli_command.md) | CLI command to execute the Algorithm |
| [cli_order](cli_order.md) | Order of the CLI arguments |
| [cli_tag](cli_tag.md) | CLI tag of the object |
| [default](default.md) | Default value of the parameter |
| [description](description.md) | Description of the Algorithm |
| [display_only](display_only.md) | Display only parameters of a specific Algorithm |
| [docker_image](docker_image.md) | Description of docker_image for the specific algorithm |
| [doi](doi.md) | DOI of the Algorithm |
| [exec_function](exec_function.md) | Function to execute the Algorithm |
| [file_count](file_count.md) | Type of Number of files |
| [folder_name](folder_name.md) | Folder name of the object |
| [hidden_args](hidden_args.md) | Hidden arguments for the Algorithm |
| [interactive](interactive.md) | Whether the object is interactive on UI |
| [label](label.md) | Label of the object, but also Radio button's label |
| [mode](mode.md) | Mode of the object |
| [module](module.md) | Module to execute the Algorithm |
| [multiselect](multiselect.md) | Multiselect value of the dropdown |
| [name](name.md) | Name of the docker_image, algorithm, parameter, display_only, results |
| [optional](optional.md) | Optional value of the object |
| [options](options.md) | Options of the Radio button in parameters, display_only, results |
| [org](org.md) | Organization of the docker image |
| [output_dir_set](output_dir_set.md) | Output directory set |
| [parameters](parameters.md) | Parameters of a specific Algorithm |
| [platform](platform.md) | Platform on which the docker image was built |
| [results](results.md) | Results of a specific Algorithm |
| [script](script.md) | Script to execute the Algorithm |
| [section_id](section_id.md) | Section ID of the object |
| [tag](tag.md) | Tag of the docker image |
| [type](type.md) | Type of the parameter |
| [value](value.md) | Value of the hidden argument or RadioButton Option's Value |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [FileTypeEnum](FileTypeEnum.md) | Type of Number of files |
| [ModeEnum](ModeEnum.md) | Mode of the parameters, display_only, results |
| [TypeEnum](TypeEnum.md) | Type of the parameters, display_only, results |


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
