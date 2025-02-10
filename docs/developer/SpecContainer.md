

# Class: SpecContainer


_SpecContianer class which holds all the high_level keywords from config.yaml file of specific algorithm_





URI: [https://w3id.org/my-org/bilayers_schema/:SpecContainer](https://w3id.org/my-org/bilayers_schema/:SpecContainer)






```mermaid
 classDiagram
    class SpecContainer
    click SpecContainer href "../SpecContainer"
      SpecContainer : algorithm_folder_name
        
      SpecContainer : citations
        
          
    
    
    SpecContainer --> "1" TypeCitations : citations
    click TypeCitations href "../TypeCitations"

        
      SpecContainer : display_only
        
          
    
    
    SpecContainer --> "*" TypeDisplayOnly : display_only
    click TypeDisplayOnly href "../TypeDisplayOnly"

        
      SpecContainer : docker_image
        
          
    
    
    SpecContainer --> "0..1" DockerImage : docker_image
    click DockerImage href "../DockerImage"

        
      SpecContainer : exec_function
        
          
    
    
    SpecContainer --> "1" ExecFunction : exec_function
    click ExecFunction href "../ExecFunction"

        
      SpecContainer : inputs
        
          
    
    
    SpecContainer --> "1..*" TypeInput : inputs
    click TypeInput href "../TypeInput"

        
      SpecContainer : outputs
        
          
    
    
    SpecContainer --> "1..*" TypeOutput : outputs
    click TypeOutput href "../TypeOutput"

        
      SpecContainer : parameters
        
          
    
    
    SpecContainer --> "1..*" TypeParameter : parameters
    click TypeParameter href "../TypeParameter"

        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [inputs](inputs.md) | 1..* <br/> [TypeInput](TypeInput.md) | Inputs to the algorithm from the last step of the workflow | direct |
| [outputs](outputs.md) | 1..* <br/> [TypeOutput](TypeOutput.md) | Outputs of the algorithm to the next step in the workflow | direct |
| [parameters](parameters.md) | 1..* <br/> [TypeParameter](TypeParameter.md) | Parameters of a specific Algorithm | direct |
| [display_only](display_only.md) | * <br/> [TypeDisplayOnly](TypeDisplayOnly.md) | Display only parameters of a specific Algorithm | direct |
| [exec_function](exec_function.md) | 1 <br/> [ExecFunction](ExecFunction.md) | Function to execute the Algorithm | direct |
| [docker_image](docker_image.md) | 0..1 <br/> [DockerImage](DockerImage.md) | Description of docker_image for the specific algorithm | direct |
| [algorithm_folder_name](algorithm_folder_name.md) | 0..1 <br/> [String](String.md) | Main folder name of the algorithm to put the generated files in the folder | direct |
| [citations](citations.md) | 1 <br/> [TypeCitations](TypeCitations.md) | Citations of the Algorithm | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/my-org/bilayers_schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | https://w3id.org/my-org/bilayers_schema/:SpecContainer |
| native | https://w3id.org/my-org/bilayers_schema/:SpecContainer |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: SpecContainer
description: SpecContianer class which holds all the high_level keywords from config.yaml
  file of specific algorithm
from_schema: https://w3id.org/my-org/bilayers_schema
slots:
- inputs
- outputs
- parameters
- display_only
- exec_function
- docker_image
- algorithm_folder_name
- citations

```
</details>

### Induced

<details>
```yaml
name: SpecContainer
description: SpecContianer class which holds all the high_level keywords from config.yaml
  file of specific algorithm
from_schema: https://w3id.org/my-org/bilayers_schema
attributes:
  inputs:
    name: inputs
    description: Inputs to the algorithm from the last step of the workflow
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: inputs
    owner: SpecContainer
    domain_of:
    - SpecContainer
    range: TypeInput
    required: true
    multivalued: true
  outputs:
    name: outputs
    description: Outputs of the algorithm to the next step in the workflow
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: outputs
    owner: SpecContainer
    domain_of:
    - SpecContainer
    range: TypeOutput
    required: true
    multivalued: true
  parameters:
    name: parameters
    description: Parameters of a specific Algorithm
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: parameters
    owner: SpecContainer
    domain_of:
    - SpecContainer
    range: TypeParameter
    required: true
    multivalued: true
  display_only:
    name: display_only
    description: Display only parameters of a specific Algorithm
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: display_only
    owner: SpecContainer
    domain_of:
    - SpecContainer
    range: TypeDisplayOnly
    multivalued: true
  exec_function:
    name: exec_function
    description: Function to execute the Algorithm
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: exec_function
    owner: SpecContainer
    domain_of:
    - SpecContainer
    range: ExecFunction
    required: true
  docker_image:
    name: docker_image
    description: Description of docker_image for the specific algorithm
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: docker_image
    owner: SpecContainer
    domain_of:
    - SpecContainer
    range: DockerImage
  algorithm_folder_name:
    name: algorithm_folder_name
    description: Main folder name of the algorithm to put the generated files in the
      folder
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: algorithm_folder_name
    owner: SpecContainer
    domain_of:
    - SpecContainer
    range: string
  citations:
    name: citations
    description: Citations of the Algorithm
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: citations
    owner: SpecContainer
    domain_of:
    - SpecContainer
    range: TypeCitations
    required: true

```
</details>