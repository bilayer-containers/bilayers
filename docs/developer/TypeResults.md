

# Class: TypeResults


_Results of a specific Algorithm_





URI: [https://w3id.org/my-org/validate_schema/:TypeResults](https://w3id.org/my-org/validate_schema/:TypeResults)






```mermaid
 classDiagram
    class TypeResults
    click TypeResults href "../TypeResults"
      AbstractUserInterface <|-- TypeResults
        click AbstractUserInterface href "../AbstractUserInterface"
      
      TypeResults : append_value
        
      TypeResults : cli_tag
        
      TypeResults : description
        
      TypeResults : file_count
        
          
    
    
    TypeResults --> "0..1" FileTypeEnum : file_count
    click FileTypeEnum href "../FileTypeEnum"

        
      TypeResults : folder_name
        
      TypeResults : interactive
        
      TypeResults : label
        
          
    
    
    TypeResults --> "1" Any : label
    click Any href "../Any"

        
      TypeResults : mode
        
          
    
    
    TypeResults --> "1" ModeEnum : mode
    click ModeEnum href "../ModeEnum"

        
      TypeResults : multiselect
        
      TypeResults : name
        
      TypeResults : optional
        
      TypeResults : options
        
          
    
    
    TypeResults --> "*" RadioOptions : options
    click RadioOptions href "../RadioOptions"

        
      TypeResults : output_dir_set
        
      TypeResults : section_id
        
      TypeResults : type
        
          
    
    
    TypeResults --> "1" TypeEnum : type
    click TypeEnum href "../TypeEnum"

        
      
```





## Inheritance
* [AbstractUserInterface](AbstractUserInterface.md)
    * **TypeResults**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [cli_tag](cli_tag.md) | 1 <br/> [String](String.md) | CLI tag of the object | direct |
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
| [Container](Container.md) | [results](results.md) | range | [TypeResults](TypeResults.md) |




## Aliases


* results



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/my-org/validate_schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | https://w3id.org/my-org/validate_schema/:TypeResults |
| native | https://w3id.org/my-org/validate_schema/:TypeResults |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: TypeResults
description: Results of a specific Algorithm
from_schema: https://w3id.org/my-org/validate_schema
aliases:
- results
is_a: AbstractUserInterface
slots:
- cli_tag

```
</details>

### Induced

<details>
```yaml
name: TypeResults
description: Results of a specific Algorithm
from_schema: https://w3id.org/my-org/validate_schema
aliases:
- results
is_a: AbstractUserInterface
attributes:
  cli_tag:
    name: cli_tag
    description: CLI tag of the object
    from_schema: https://w3id.org/my-org/validate_schema
    rank: 1000
    alias: cli_tag
    owner: TypeResults
    domain_of:
    - TypeParameter
    - TypeResults
    - HiddenArgs
    range: string
    required: true
  name:
    name: name
    description: Name of the docker_image, algorithm, parameter, display_only, results
    from_schema: https://w3id.org/my-org/validate_schema
    rank: 1000
    alias: name
    owner: TypeResults
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
    owner: TypeResults
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
    owner: TypeResults
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
    owner: TypeResults
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
    owner: TypeResults
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
    owner: TypeResults
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
    owner: TypeResults
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
    owner: TypeResults
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
    owner: TypeResults
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
    owner: TypeResults
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
    owner: TypeResults
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
    owner: TypeResults
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
    owner: TypeResults
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
    owner: TypeResults
    domain_of:
    - AbstractUserInterface
    range: boolean
    required: false

```
</details>