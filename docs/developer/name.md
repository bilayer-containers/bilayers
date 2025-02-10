

# Slot: name


_Name of the docker_image, algorithm, parameter, display_only_





URI: [https://w3id.org/my-org/bilayers_schema/:name](https://w3id.org/my-org/bilayers_schema/:name)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [TypeAlgorithmFromCitation](TypeAlgorithmFromCitation.md) | Algorithm's citations |  no  |
| [ExecFunction](ExecFunction.md) | Function to execute the Algorithm |  no  |
| [TypeParameter](TypeParameter.md) | Parameters of a specific Algorithm |  no  |
| [TypeDisplayOnly](TypeDisplayOnly.md) | Display only parameters of a specific Algorithm |  no  |
| [TypeInput](TypeInput.md) | Inputs to the algorithm from the last step of the workflow |  no  |
| [TypeOutput](TypeOutput.md) | Outputs of the algorithm to the next step in the workflow |  no  |
| [DockerImage](DockerImage.md) | Description of docker_image for the specific algorithm |  no  |
| [AbstractWorkflowDetails](AbstractWorkflowDetails.md) | Abstract class for details needed to fit config in the workflow |  no  |
| [AbstractUserInterface](AbstractUserInterface.md) | Abstract class for user interface |  no  |







## Properties

* Range: [String](String.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/my-org/bilayers_schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | https://w3id.org/my-org/bilayers_schema/:name |
| native | https://w3id.org/my-org/bilayers_schema/:name |




## LinkML Source

<details>
```yaml
name: name
description: Name of the docker_image, algorithm, parameter, display_only
from_schema: https://w3id.org/my-org/bilayers_schema
rank: 1000
alias: name
domain_of:
- AbstractWorkflowDetails
- AbstractUserInterface
- ExecFunction
- DockerImage
- TypeAlgorithmFromCitation
range: string
required: true

```
</details>