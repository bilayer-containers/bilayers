

# Slot: description


_Description of the Algorithm_





URI: [https://w3id.org/my-org/validate_schema/:description](https://w3id.org/my-org/validate_schema/:description)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [TypeOutput](TypeOutput.md) | Outputs of the algorithm to the next step in the workflow |  no  |
| [TypeAlgorithmFromCitation](TypeAlgorithmFromCitation.md) | Algorithm's citations |  no  |
| [TypeParameter](TypeParameter.md) | Parameters of a specific Algorithm |  no  |
| [AbstractWorkflowDetails](AbstractWorkflowDetails.md) | Abstract class for details needed to fit config in the workflow |  no  |
| [TypeDisplayOnly](TypeDisplayOnly.md) | Display only parameters of a specific Algorithm |  no  |
| [AbstractUserInterface](AbstractUserInterface.md) | Abstract class for user interface |  no  |
| [TypeInput](TypeInput.md) | Inputs to the algorithm from the last step of the workflow |  no  |







## Properties

* Range: [String](String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/my-org/validate_schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | https://w3id.org/my-org/validate_schema/:description |
| native | https://w3id.org/my-org/validate_schema/:description |




## LinkML Source

<details>
```yaml
name: description
description: Description of the Algorithm
from_schema: https://w3id.org/my-org/validate_schema
rank: 1000
alias: description
domain_of:
- AbstractWorkflowDetails
- AbstractUserInterface
- TypeAlgorithmFromCitation
range: string

```
</details>