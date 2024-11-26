

# Slot: name


_Name of the docker_image, algorithm, parameter, display_only, results_





URI: [https://w3id.org/my-org/validate_schema/:name](https://w3id.org/my-org/validate_schema/:name)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [TypeParameter](TypeParameter.md) | Parameters of a specific Algorithm |  no  |
| [AbstractUserInterface](AbstractUserInterface.md) | Abstract class for user interface |  no  |
| [DockerImage](DockerImage.md) | Description of docker_image for the specific algorithm |  no  |
| [ExecFunction](ExecFunction.md) | Function to execute the Algorithm |  no  |
| [TypeResults](TypeResults.md) | Results of a specific Algorithm |  no  |
| [TypeDisplayOnly](TypeDisplayOnly.md) | Display only parameters of a specific Algorithm |  no  |
| [TypeAlgorithmFromCitation](TypeAlgorithmFromCitation.md) | Algorithm's citations |  no  |







## Properties

* Range: [String](String.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/my-org/validate_schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | https://w3id.org/my-org/validate_schema/:name |
| native | https://w3id.org/my-org/validate_schema/:name |




## LinkML Source

<details>
```yaml
name: name
description: Name of the docker_image, algorithm, parameter, display_only, results
from_schema: https://w3id.org/my-org/validate_schema
rank: 1000
alias: name
domain_of:
- AbstractUserInterface
- ExecFunction
- DockerImage
- TypeAlgorithmFromCitation
range: string
required: true

```
</details>