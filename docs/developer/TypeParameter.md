

# Class: TypeParameter


_Parameters of a specific Algorithm_





URI: [https://w3id.org/my-org/validate_schema/:TypeParameter](https://w3id.org/my-org/validate_schema/:TypeParameter)






```mermaid
 classDiagram
    class TypeParameter
    click TypeParameter href "../TypeParameter"
      AbstractUserInterface <|-- TypeParameter
        click AbstractUserInterface href "../AbstractUserInterface"
      
      TypeParameter : append_value
        
      TypeParameter : cli_order
        
      TypeParameter : cli_tag
        
      TypeParameter : default
        
          
    
    
    TypeParameter --> "1" Any : default
    click Any href "../Any"

        
      TypeParameter : description
        
      TypeParameter : file_count
        
          
    
    
    TypeParameter --> "0..1" FileTypeEnum : file_count
    click FileTypeEnum href "../FileTypeEnum"

        
      TypeParameter : folder_name
        
      TypeParameter : interactive
        
      TypeParameter : label
        
          
    
    
    TypeParameter --> "1" Any : label
    click Any href "../Any"

        
      TypeParameter : mode
        
          
    
    
    TypeParameter --> "1" ModeEnum : mode
    click ModeEnum href "../ModeEnum"

        
      TypeParameter : multiselect
        
      TypeParameter : name
        
      TypeParameter : optional
        
      TypeParameter : options
        
          
    
    
    TypeParameter --> "*" RadioOptions : options
    click RadioOptions href "../RadioOptions"

        
      TypeParameter : output_dir_set
        
      TypeParameter : section_id
        
      TypeParameter : type
        
          
    
    
    TypeParameter --> "1" TypeEnum : type
    click TypeEnum href "../TypeEnum"

        
      
```





## Inheritance
* [AbstractUserInterface](AbstractUserInterface.md)
    * **TypeParameter**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [default](default.md) | 1 <br/> [Any](Any.md) | Default value of the parameter | direct |
| [cli_tag](cli_tag.md) | 1 <br/> [String](String.md) | CLI tag of the object | direct |
| [cli_order](cli_order.md) | 0..1 <br/> [Integer](Integer.md) | Order of the CLI arguments | direct |
| [name](name.md) | 1 <br/> [String](String.md) | Name of the docker_image, algorithm, parameter, display_only, results | [AbstractUserInterface](AbstractUserInterface.md) |
| [type](type.md) | 1 <br/> [TypeEnum](TypeEnum.md) | Type of the parameter | [AbstractUserInterface](AbstractUserInterface.md) |
| [label](label.md) | 1 <br/> [Any](Any.md) | Label of the object, but also Radio button's label | [AbstractUserInterface](AbstractUserInterface.md) |
| [description](description.md) | 0..1 <br/> [String](String.md) | Description of the Algorithm | [AbstractUserInterface](AbstractUserInterface.md) |
| [optional](optional.md) | 1 <br/> [Boolean](Boolean.md) | Optional value of the object | [AbstractUserInterface](AbstractUserInterface.md) |
| [section_id](section_id.md) | 1 <br/> [String](String.md) | Section ID of the object | [AbstractUserInterface](AbstractUserInterface.md) |
| [mode](mode.md) | 1 <br/> [ModeEnum](ModeEnum.md) | Mode of the object | [AbstractUserInterface](AbstractUserInterface.md) |
| [output_dir_set](output_dir_set.md) | 0..1 <br/> [Boolean](Boolean.md) | Output directory set | [AbstractUserInterface](AbstractUserInterface.md) |
| [folder_name](folder_name.md) | 0..1 <br/> [String](String.md) | Folder name of the object | [AbstractUserInterface](AbstractUserInterface.md) |
| [file_count](file_count.md) | 0..1 <br/> [FileTypeEnum](FileTypeEnum.md) | Type of Number of files | [AbstractUserInterface](AbstractUserInterface.md) |
| [options](options.md) | * <br/> [RadioOptions](RadioOptions.md) | Options of the Radio button in parameters, display_only, results | [AbstractUserInterface](AbstractUserInterface.md) |
| [interactive](interactive.md) | 0..1 <br/> [Boolean](Boolean.md) | Whether the object is interactive on UI | [AbstractUserInterface](AbstractUserInterface.md) |
| [append_value](append_value.md) | 0..1 <br/> [Boolean](Boolean.md) | Append value of the hidden argument | [AbstractUserInterface](AbstractUserInterface.md) |
| [multiselect](multiselect.md) | 0..1 <br/> [Boolean](Boolean.md) | Multiselect value of the dropdown | [AbstractUserInterface](AbstractUserInterface.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Container](Container.md) | [parameters](parameters.md) | range | [TypeParameter](TypeParameter.md) |




## Aliases


* parameters



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/my-org/validate_schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | https://w3id.org/my-org/validate_schema/:TypeParameter |
| native | https://w3id.org/my-org/validate_schema/:TypeParameter |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: TypeParameter
description: Parameters of a specific Algorithm
from_schema: https://w3id.org/my-org/validate_schema
aliases:
- parameters
is_a: AbstractUserInterface
slots:
- default
- cli_tag
- cli_order
rules:
- preconditions:
    slot_conditions:
      type:
        name: type
        equals_string: files
  postconditions:
    slot_conditions:
      folder_name:
        name: folder_name
        required: true
  description: Extra flags needed iff type is files

```
</details>

### Induced

<details>
```yaml
name: TypeParameter
description: Parameters of a specific Algorithm
from_schema: https://w3id.org/my-org/validate_schema
aliases:
- parameters
is_a: AbstractUserInterface
attributes:
  default:
    name: default
    description: Default value of the parameter
    from_schema: https://w3id.org/my-org/validate_schema
    rank: 1000
    alias: default
    owner: TypeParameter
    domain_of:
    - TypeParameter
    - TypeDisplayOnly
    range: Any
    required: true
  cli_tag:
    name: cli_tag
    description: CLI tag of the object
    from_schema: https://w3id.org/my-org/validate_schema
    rank: 1000
    alias: cli_tag
    owner: TypeParameter
    domain_of:
    - TypeParameter
    - TypeResults
    - HiddenArgs
    range: string
    required: true
  cli_order:
    name: cli_order
    description: Order of the CLI arguments
    from_schema: https://w3id.org/my-org/validate_schema
    rank: 1000
    alias: cli_order
    owner: TypeParameter
    domain_of:
    - TypeParameter
    - HiddenArgs
    range: integer
    required: false
  name:
    name: name
    description: Name of the docker_image, algorithm, parameter, display_only, results
    from_schema: https://w3id.org/my-org/validate_schema
    rank: 1000
    alias: name
    owner: TypeParameter
    domain_of:
    - AbstractUserInterface
    - ExecFunction
    - DockerImage
    - TypeAlgorithmFromCitation
    range: string
    required: true
  type:
    name: type
    description: Type of the parameter
    from_schema: https://w3id.org/my-org/validate_schema
    rank: 1000
    alias: type
    owner: TypeParameter
    domain_of:
    - AbstractUserInterface
    range: TypeEnum
    required: true
  label:
    name: label
    description: Label of the object, but also Radio button's label
    from_schema: https://w3id.org/my-org/validate_schema
    rank: 1000
    alias: label
    owner: TypeParameter
    domain_of:
    - AbstractUserInterface
    - RadioOptions
    range: Any
    required: true
  description:
    name: description
    description: Description of the Algorithm
    from_schema: https://w3id.org/my-org/validate_schema
    rank: 1000
    alias: description
    owner: TypeParameter
    domain_of:
    - AbstractUserInterface
    - TypeAlgorithmFromCitation
    range: string
  optional:
    name: optional
    description: Optional value of the object
    from_schema: https://w3id.org/my-org/validate_schema
    rank: 1000
    alias: optional
    owner: TypeParameter
    domain_of:
    - AbstractUserInterface
    range: boolean
    required: true
  section_id:
    name: section_id
    description: Section ID of the object
    from_schema: https://w3id.org/my-org/validate_schema
    rank: 1000
    alias: section_id
    owner: TypeParameter
    domain_of:
    - AbstractUserInterface
    range: string
    required: true
  mode:
    name: mode
    description: Mode of the object
    from_schema: https://w3id.org/my-org/validate_schema
    rank: 1000
    alias: mode
    owner: TypeParameter
    domain_of:
    - AbstractUserInterface
    range: ModeEnum
    required: true
  output_dir_set:
    name: output_dir_set
    description: Output directory set
    from_schema: https://w3id.org/my-org/validate_schema
    rank: 1000
    alias: output_dir_set
    owner: TypeParameter
    domain_of:
    - AbstractUserInterface
    range: boolean
    required: false
  folder_name:
    name: folder_name
    description: Folder name of the object
    from_schema: https://w3id.org/my-org/validate_schema
    rank: 1000
    alias: folder_name
    owner: TypeParameter
    domain_of:
    - AbstractUserInterface
    range: string
    required: false
  file_count:
    name: file_count
    description: Type of Number of files
    from_schema: https://w3id.org/my-org/validate_schema
    rank: 1000
    alias: file_count
    owner: TypeParameter
    domain_of:
    - AbstractUserInterface
    range: FileTypeEnum
    required: false
  options:
    name: options
    description: Options of the Radio button in parameters, display_only, results
    from_schema: https://w3id.org/my-org/validate_schema
    rank: 1000
    alias: options
    owner: TypeParameter
    domain_of:
    - AbstractUserInterface
    range: RadioOptions
    required: false
    multivalued: true
  interactive:
    name: interactive
    description: Whether the object is interactive on UI
    from_schema: https://w3id.org/my-org/validate_schema
    rank: 1000
    alias: interactive
    owner: TypeParameter
    domain_of:
    - AbstractUserInterface
    range: boolean
    required: false
  append_value:
    name: append_value
    description: Append value of the hidden argument
    from_schema: https://w3id.org/my-org/validate_schema
    rank: 1000
    alias: append_value
    owner: TypeParameter
    domain_of:
    - AbstractUserInterface
    - HiddenArgs
    range: boolean
    required: false
  multiselect:
    name: multiselect
    description: Multiselect value of the dropdown
    from_schema: https://w3id.org/my-org/validate_schema
    rank: 1000
    alias: multiselect
    owner: TypeParameter
    domain_of:
    - AbstractUserInterface
    range: boolean
    required: false
rules:
- preconditions:
    slot_conditions:
      type:
        name: type
        equals_string: files
  postconditions:
    slot_conditions:
      folder_name:
        name: folder_name
        required: true
  description: Extra flags needed iff type is files

```
</details>