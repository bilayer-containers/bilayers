

# Class: AbstractWorkflowDetails


_Abstract class for details needed to fit config in the workflow_




* __NOTE__: this is an abstract class and should not be instantiated directly


URI: [https://w3id.org/my-org/bilayers_schema/:AbstractWorkflowDetails](https://w3id.org/my-org/bilayers_schema/:AbstractWorkflowDetails)






```mermaid
 classDiagram
    class AbstractWorkflowDetails
    click AbstractWorkflowDetails href "../AbstractWorkflowDetails"
      AbstractWorkflowDetails <|-- TypeInput
        click TypeInput href "../TypeInput"
      AbstractWorkflowDetails <|-- TypeOutput
        click TypeOutput href "../TypeOutput"
      
      AbstractWorkflowDetails : cli_order
        
      AbstractWorkflowDetails : cli_tag
        
      AbstractWorkflowDetails : default
        
          
    
    
    AbstractWorkflowDetails --> "1" Any : default
    click Any href "../Any"

        
      AbstractWorkflowDetails : depth
        
      AbstractWorkflowDetails : description
        
      AbstractWorkflowDetails : file_count
        
          
    
    
    AbstractWorkflowDetails --> "0..1" FileTypeEnum : file_count
    click FileTypeEnum href "../FileTypeEnum"

        
      AbstractWorkflowDetails : folder_name
        
      AbstractWorkflowDetails : format
        
      AbstractWorkflowDetails : label
        
          
    
    
    AbstractWorkflowDetails --> "1" Any : label
    click Any href "../Any"

        
      AbstractWorkflowDetails : mode
        
          
    
    
    AbstractWorkflowDetails --> "1" ModeEnum : mode
    click ModeEnum href "../ModeEnum"

        
      AbstractWorkflowDetails : name
        
      AbstractWorkflowDetails : optional
        
      AbstractWorkflowDetails : pyramidal
        
      AbstractWorkflowDetails : section_id
        
      AbstractWorkflowDetails : subtype
        
          
    
    
    AbstractWorkflowDetails --> "*" SubTypeEnum : subtype
    click SubTypeEnum href "../SubTypeEnum"

        
      AbstractWorkflowDetails : tiled
        
      AbstractWorkflowDetails : timepoints
        
      AbstractWorkflowDetails : type
        
          
    
    
    AbstractWorkflowDetails --> "1" TypeEnum : type
    click TypeEnum href "../TypeEnum"

        
      
```





## Inheritance
* **AbstractWorkflowDetails**
    * [TypeInput](TypeInput.md)
    * [TypeOutput](TypeOutput.md)



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [name](name.md) | 1 <br/> [String](String.md) | Name of the docker_image, algorithm, parameter, display_only | direct |
| [type](type.md) | 1 <br/> [TypeEnum](TypeEnum.md) | Type of the inputs, parameters and outputs | direct |
| [label](label.md) | 1 <br/> [Any](Any.md) | Label of the object, but also Radio button's label | direct |
| [description](description.md) | 0..1 <br/> [String](String.md) | Description of the Algorithm | direct |
| [cli_tag](cli_tag.md) | 1 <br/> [String](String.md) | CLI tag of the object | direct |
| [cli_order](cli_order.md) | 0..1 <br/> [Integer](Integer.md) | Order of the CLI arguments | direct |
| [default](default.md) | 1 <br/> [Any](Any.md) | Default value of the parameter | direct |
| [optional](optional.md) | 1 <br/> [Boolean](Boolean.md) | Optional value of the object | direct |
| [format](format.md) | * <br/> [String](String.md) | Format of the inputs and outputs | direct |
| [folder_name](folder_name.md) | 0..1 <br/> [String](String.md) | Folder name of the object | direct |
| [file_count](file_count.md) | 0..1 <br/> [FileTypeEnum](FileTypeEnum.md) | Type of Number of files | direct |
| [section_id](section_id.md) | 1 <br/> [String](String.md) | Section ID of the object | direct |
| [mode](mode.md) | 1 <br/> [ModeEnum](ModeEnum.md) | Mode of the object | direct |
| [subtype](subtype.md) | * <br/> [SubTypeEnum](SubTypeEnum.md) | Subtype of the inputs and outputs | direct |
| [depth](depth.md) | 0..1 <br/> [Boolean](Boolean.md) | whether z-dimension i | direct |
| [timepoints](timepoints.md) | 0..1 <br/> [Boolean](Boolean.md) | whether t-dimension i | direct |
| [tiled](tiled.md) | 0..1 <br/> [Boolean](Boolean.md) | whether tiled images are accepted via tool | direct |
| [pyramidal](pyramidal.md) | 0..1 <br/> [Boolean](Boolean.md) | whether pyramidal images are accepted via tool | direct |







## Aliases


* inputs
* outputs



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/my-org/bilayers_schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | https://w3id.org/my-org/bilayers_schema/:AbstractWorkflowDetails |
| native | https://w3id.org/my-org/bilayers_schema/:AbstractWorkflowDetails |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: AbstractWorkflowDetails
description: Abstract class for details needed to fit config in the workflow
from_schema: https://w3id.org/my-org/bilayers_schema
aliases:
- inputs
- outputs
abstract: true
slots:
- name
- type
- label
- description
- cli_tag
- cli_order
- default
- optional
- format
- folder_name
- file_count
- section_id
- mode
- subtype
- depth
- timepoints
- tiled
- pyramidal

```
</details>

### Induced

<details>
```yaml
name: AbstractWorkflowDetails
description: Abstract class for details needed to fit config in the workflow
from_schema: https://w3id.org/my-org/bilayers_schema
aliases:
- inputs
- outputs
abstract: true
attributes:
  name:
    name: name
    description: Name of the docker_image, algorithm, parameter, display_only
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: name
    owner: AbstractWorkflowDetails
    domain_of:
    - AbstractWorkflowDetails
    - AbstractUserInterface
    - ExecFunction
    - DockerImage
    - TypeCitations
    range: string
    required: true
  type:
    name: type
    description: Type of the inputs, parameters and outputs
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: type
    owner: AbstractWorkflowDetails
    domain_of:
    - AbstractWorkflowDetails
    - AbstractUserInterface
    range: TypeEnum
    required: true
  label:
    name: label
    description: Label of the object, but also Radio button's label
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: label
    owner: AbstractWorkflowDetails
    domain_of:
    - AbstractWorkflowDetails
    - AbstractUserInterface
    - RadioOptions
    range: Any
    required: true
  description:
    name: description
    description: Description of the Algorithm
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: description
    owner: AbstractWorkflowDetails
    domain_of:
    - AbstractWorkflowDetails
    - AbstractUserInterface
    - TypeCitations
    range: string
  cli_tag:
    name: cli_tag
    description: CLI tag of the object
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: cli_tag
    owner: AbstractWorkflowDetails
    domain_of:
    - AbstractWorkflowDetails
    - TypeParameter
    - HiddenArgs
    range: string
    required: true
  cli_order:
    name: cli_order
    description: Order of the CLI arguments
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: cli_order
    owner: AbstractWorkflowDetails
    domain_of:
    - AbstractWorkflowDetails
    - TypeParameter
    - HiddenArgs
    range: integer
    required: false
  default:
    name: default
    description: Default value of the parameter
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: default
    owner: AbstractWorkflowDetails
    domain_of:
    - AbstractWorkflowDetails
    - TypeParameter
    - TypeDisplayOnly
    range: Any
    required: true
  optional:
    name: optional
    description: Optional value of the object
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: optional
    owner: AbstractWorkflowDetails
    domain_of:
    - AbstractWorkflowDetails
    - AbstractUserInterface
    range: boolean
    required: true
  format:
    name: format
    description: Format of the inputs and outputs
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: format
    owner: AbstractWorkflowDetails
    domain_of:
    - AbstractWorkflowDetails
    range: string
    multivalued: true
  folder_name:
    name: folder_name
    description: Folder name of the object
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: folder_name
    owner: AbstractWorkflowDetails
    domain_of:
    - AbstractWorkflowDetails
    range: string
    required: false
  file_count:
    name: file_count
    description: Type of Number of files
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: file_count
    owner: AbstractWorkflowDetails
    domain_of:
    - AbstractWorkflowDetails
    range: FileTypeEnum
    required: false
  section_id:
    name: section_id
    description: Section ID of the object
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: section_id
    owner: AbstractWorkflowDetails
    domain_of:
    - AbstractWorkflowDetails
    - AbstractUserInterface
    range: string
    required: true
  mode:
    name: mode
    description: Mode of the object
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: mode
    owner: AbstractWorkflowDetails
    domain_of:
    - AbstractWorkflowDetails
    - AbstractUserInterface
    range: ModeEnum
    required: true
  subtype:
    name: subtype
    description: Subtype of the inputs and outputs
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: subtype
    owner: AbstractWorkflowDetails
    domain_of:
    - AbstractWorkflowDetails
    range: SubTypeEnum
    multivalued: true
  depth:
    name: depth
    description: whether z-dimension i.e. depth is accepted via tool
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: depth
    owner: AbstractWorkflowDetails
    domain_of:
    - AbstractWorkflowDetails
    range: boolean
  timepoints:
    name: timepoints
    description: whether t-dimension i.e. timepoints are accepted via tool
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: timepoints
    owner: AbstractWorkflowDetails
    domain_of:
    - AbstractWorkflowDetails
    range: boolean
  tiled:
    name: tiled
    description: whether tiled images are accepted via tool
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: tiled
    owner: AbstractWorkflowDetails
    domain_of:
    - AbstractWorkflowDetails
    range: boolean
  pyramidal:
    name: pyramidal
    description: whether pyramidal images are accepted via tool
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: pyramidal
    owner: AbstractWorkflowDetails
    domain_of:
    - AbstractWorkflowDetails
    range: boolean

```
</details>