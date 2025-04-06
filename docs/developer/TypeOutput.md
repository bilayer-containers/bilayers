

# Class: TypeOutput


_Outputs of the algorithm to the next step in the workflow_





URI: [https://w3id.org/my-org/bilayers_schema/:TypeOutput](https://w3id.org/my-org/bilayers_schema/:TypeOutput)






```mermaid
 classDiagram
    class TypeOutput
    click TypeOutput href "../TypeOutput"
      AbstractWorkflowDetails <|-- TypeOutput
        click AbstractWorkflowDetails href "../AbstractWorkflowDetails"
      
      TypeOutput : cli_order
        
      TypeOutput : cli_tag
        
      TypeOutput : default
        
          
    
    
    TypeOutput --> "1" Any : default
    click Any href "../Any"

        
      TypeOutput : depth
        
      TypeOutput : description
        
      TypeOutput : file_count
        
          
    
    
    TypeOutput --> "0..1" FileTypeEnum : file_count
    click FileTypeEnum href "../FileTypeEnum"

        
      TypeOutput : folder_name
        
      TypeOutput : format
        
      TypeOutput : label
        
          
    
    
    TypeOutput --> "1" Any : label
    click Any href "../Any"

        
      TypeOutput : mode
        
          
    
    
    TypeOutput --> "1" ModeEnum : mode
    click ModeEnum href "../ModeEnum"

        
      TypeOutput : name
        
      TypeOutput : optional
        
      TypeOutput : pyramidal
        
      TypeOutput : section_id
        
      TypeOutput : subtype
        
          
    
    
    TypeOutput --> "*" SubTypeEnum : subtype
    click SubTypeEnum href "../SubTypeEnum"

        
      TypeOutput : tiled
        
      TypeOutput : timepoints
        
      TypeOutput : type
        
          
    
    
    TypeOutput --> "1" TypeEnum : type
    click TypeEnum href "../TypeEnum"

        
      
```





## Inheritance
* [AbstractWorkflowDetails](AbstractWorkflowDetails.md)
    * **TypeOutput**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [name](name.md) | 1 <br/> [String](String.md) | Name of the docker_image, algorithm, parameter, display_only | [AbstractWorkflowDetails](AbstractWorkflowDetails.md) |
| [type](type.md) | 1 <br/> [TypeEnum](TypeEnum.md) | Type of the inputs, parameters and outputs | [AbstractWorkflowDetails](AbstractWorkflowDetails.md) |
| [label](label.md) | 1 <br/> [Any](Any.md) | Label of the object, but also Radio button's label | [AbstractWorkflowDetails](AbstractWorkflowDetails.md) |
| [description](description.md) | 0..1 <br/> [String](String.md) | Description of the Algorithm | [AbstractWorkflowDetails](AbstractWorkflowDetails.md) |
| [cli_tag](cli_tag.md) | 1 <br/> [String](String.md) | CLI tag of the object | [AbstractWorkflowDetails](AbstractWorkflowDetails.md) |
| [cli_order](cli_order.md) | 0..1 <br/> [Integer](Integer.md) | Order of the CLI arguments | [AbstractWorkflowDetails](AbstractWorkflowDetails.md) |
| [default](default.md) | 1 <br/> [Any](Any.md) | Default value of the parameter | [AbstractWorkflowDetails](AbstractWorkflowDetails.md) |
| [optional](optional.md) | 1 <br/> [Boolean](Boolean.md) | Optional value of the object | [AbstractWorkflowDetails](AbstractWorkflowDetails.md) |
| [format](format.md) | * <br/> [String](String.md) | Format of the inputs and outputs | [AbstractWorkflowDetails](AbstractWorkflowDetails.md) |
| [folder_name](folder_name.md) | 0..1 <br/> [String](String.md) | Folder name of the object | [AbstractWorkflowDetails](AbstractWorkflowDetails.md) |
| [file_count](file_count.md) | 0..1 <br/> [FileTypeEnum](FileTypeEnum.md) | Type of Number of files | [AbstractWorkflowDetails](AbstractWorkflowDetails.md) |
| [section_id](section_id.md) | 1 <br/> [String](String.md) | Section ID of the object | [AbstractWorkflowDetails](AbstractWorkflowDetails.md) |
| [mode](mode.md) | 1 <br/> [ModeEnum](ModeEnum.md) | Mode of the object | [AbstractWorkflowDetails](AbstractWorkflowDetails.md) |
| [subtype](subtype.md) | * <br/> [SubTypeEnum](SubTypeEnum.md) | Subtype of the inputs and outputs | [AbstractWorkflowDetails](AbstractWorkflowDetails.md) |
| [depth](depth.md) | 0..1 <br/> [Boolean](Boolean.md) | whether z-dimension i | [AbstractWorkflowDetails](AbstractWorkflowDetails.md) |
| [timepoints](timepoints.md) | 0..1 <br/> [Boolean](Boolean.md) | whether t-dimension i | [AbstractWorkflowDetails](AbstractWorkflowDetails.md) |
| [tiled](tiled.md) | 0..1 <br/> [Boolean](Boolean.md) | whether tiled images are accepted via tool | [AbstractWorkflowDetails](AbstractWorkflowDetails.md) |
| [pyramidal](pyramidal.md) | 0..1 <br/> [Boolean](Boolean.md) | whether pyramidal images are accepted via tool | [AbstractWorkflowDetails](AbstractWorkflowDetails.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [SpecContainer](SpecContainer.md) | [outputs](outputs.md) | range | [TypeOutput](TypeOutput.md) |




## Aliases


* outputs



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/my-org/bilayers_schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | https://w3id.org/my-org/bilayers_schema/:TypeOutput |
| native | https://w3id.org/my-org/bilayers_schema/:TypeOutput |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: TypeOutput
description: Outputs of the algorithm to the next step in the workflow
from_schema: https://w3id.org/my-org/bilayers_schema
aliases:
- outputs
is_a: AbstractWorkflowDetails
rules:
- preconditions:
    slot_conditions:
      type:
        name: type
        equals_string: image
  postconditions:
    slot_conditions:
      subtype:
        name: subtype
        required: true
      depth:
        name: depth
        required: true
      timepoints:
        name: timepoints
        required: true
      tiled:
        name: tiled
        required: true
      pyramidal:
        name: pyramidal
        required: true
  description: Extra flags needed iff type is image

```
</details>

### Induced

<details>
```yaml
name: TypeOutput
description: Outputs of the algorithm to the next step in the workflow
from_schema: https://w3id.org/my-org/bilayers_schema
aliases:
- outputs
is_a: AbstractWorkflowDetails
attributes:
  name:
    name: name
    description: Name of the docker_image, algorithm, parameter, display_only
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: name
    owner: TypeOutput
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
    owner: TypeOutput
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
    owner: TypeOutput
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
    owner: TypeOutput
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
    owner: TypeOutput
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
    owner: TypeOutput
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
    owner: TypeOutput
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
    owner: TypeOutput
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
    owner: TypeOutput
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
    owner: TypeOutput
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
    owner: TypeOutput
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
    owner: TypeOutput
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
    owner: TypeOutput
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
    owner: TypeOutput
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
    owner: TypeOutput
    domain_of:
    - AbstractWorkflowDetails
    range: boolean
  timepoints:
    name: timepoints
    description: whether t-dimension i.e. timepoints are accepted via tool
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: timepoints
    owner: TypeOutput
    domain_of:
    - AbstractWorkflowDetails
    range: boolean
  tiled:
    name: tiled
    description: whether tiled images are accepted via tool
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: tiled
    owner: TypeOutput
    domain_of:
    - AbstractWorkflowDetails
    range: boolean
  pyramidal:
    name: pyramidal
    description: whether pyramidal images are accepted via tool
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: pyramidal
    owner: TypeOutput
    domain_of:
    - AbstractWorkflowDetails
    range: boolean
rules:
- preconditions:
    slot_conditions:
      type:
        name: type
        equals_string: image
  postconditions:
    slot_conditions:
      subtype:
        name: subtype
        required: true
      depth:
        name: depth
        required: true
      timepoints:
        name: timepoints
        required: true
      tiled:
        name: tiled
        required: true
      pyramidal:
        name: pyramidal
        required: true
  description: Extra flags needed iff type is image

```
</details>