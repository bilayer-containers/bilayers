

# Class: TypeCitations


_Citations of the Algorithm_





URI: [https://w3id.org/my-org/bilayers_schema/:TypeCitations](https://w3id.org/my-org/bilayers_schema/:TypeCitations)






```mermaid
 classDiagram
    class TypeCitations
    click TypeCitations href "../TypeCitations"
      TypeCitations : description
        
      TypeCitations : doi
        
      TypeCitations : license
        
      TypeCitations : name
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [name](name.md) | 1 <br/> [String](String.md) | Name of the docker_image, algorithm, parameter, display_only | direct |
| [doi](doi.md) | 0..1 <br/> [String](String.md) | DOI of the Algorithm | direct |
| [license](license.md) | 0..1 <br/> [String](String.md) | License of the Algorithm | direct |
| [description](description.md) | 0..1 <br/> [String](String.md) | Description of the Algorithm | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [SpecContainer](SpecContainer.md) | [citations](citations.md) | range | [TypeCitations](TypeCitations.md) |




## Aliases


* citations



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/my-org/bilayers_schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | https://w3id.org/my-org/bilayers_schema/:TypeCitations |
| native | https://w3id.org/my-org/bilayers_schema/:TypeCitations |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: TypeCitations
description: Citations of the Algorithm
from_schema: https://w3id.org/my-org/bilayers_schema
aliases:
- citations
slots:
- name
- doi
- license
- description

```
</details>

### Induced

<details>
```yaml
name: TypeCitations
description: Citations of the Algorithm
from_schema: https://w3id.org/my-org/bilayers_schema
aliases:
- citations
attributes:
  name:
    name: name
    description: Name of the docker_image, algorithm, parameter, display_only
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: name
    owner: TypeCitations
    domain_of:
    - AbstractWorkflowDetails
    - AbstractUserInterface
    - ExecFunction
    - DockerImage
    - TypeCitations
    range: string
    required: true
  doi:
    name: doi
    description: DOI of the Algorithm
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: doi
    owner: TypeCitations
    domain_of:
    - TypeCitations
    range: string
  license:
    name: license
    description: License of the Algorithm
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: license
    owner: TypeCitations
    domain_of:
    - TypeCitations
    range: string
  description:
    name: description
    description: Description of the Algorithm
    from_schema: https://w3id.org/my-org/bilayers_schema
    rank: 1000
    alias: description
    owner: TypeCitations
    domain_of:
    - AbstractWorkflowDetails
    - AbstractUserInterface
    - TypeCitations
    range: string

```
</details>