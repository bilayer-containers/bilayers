

# Slot: section_id


_Section ID of the object_





URI: [https://w3id.org/my-org/validate_schema/:section_id](https://w3id.org/my-org/validate_schema/:section_id)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [TypeOutput](TypeOutput.md) | Outputs of the algorithm to the next step in the workflow |  no  |
| [TypeParameter](TypeParameter.md) | Parameters of a specific Algorithm |  no  |
| [AbstractWorkflowDetails](AbstractWorkflowDetails.md) | Abstract class for details needed to fit config in the workflow |  no  |
| [TypeDisplayOnly](TypeDisplayOnly.md) | Display only parameters of a specific Algorithm |  no  |
| [AbstractUserInterface](AbstractUserInterface.md) | Abstract class for user interface |  no  |
| [TypeInput](TypeInput.md) | Inputs to the algorithm from the last step of the workflow |  no  |







## Properties

* Range: [String](String.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/my-org/validate_schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | https://w3id.org/my-org/validate_schema/:section_id |
| native | https://w3id.org/my-org/validate_schema/:section_id |




## LinkML Source

<details>
```yaml
name: section_id
description: Section ID of the object
from_schema: https://w3id.org/my-org/validate_schema
rank: 1000
alias: section_id
domain_of:
- AbstractWorkflowDetails
- AbstractUserInterface
range: string
required: true

```
</details>