

# Slot: optional


_Optional value of the object_





URI: [https://w3id.org/my-org/bilayers_schema/:optional](https://w3id.org/my-org/bilayers_schema/:optional)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [TypeParameter](TypeParameter.md) | Parameters of a specific Algorithm |  no  |
| [TypeDisplayOnly](TypeDisplayOnly.md) | Display only parameters of a specific Algorithm |  no  |
| [TypeOutput](TypeOutput.md) | Outputs of the algorithm to the next step in the workflow |  no  |
| [TypeInput](TypeInput.md) | Inputs to the algorithm from the last step of the workflow |  no  |
| [AbstractWorkflowDetails](AbstractWorkflowDetails.md) | Abstract class for details needed to fit config in the workflow |  no  |
| [AbstractUserInterface](AbstractUserInterface.md) | Abstract class for user interface |  no  |







## Properties

* Range: [Boolean](Boolean.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/my-org/bilayers_schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | https://w3id.org/my-org/bilayers_schema/:optional |
| native | https://w3id.org/my-org/bilayers_schema/:optional |




## LinkML Source

<details>
```yaml
name: optional
description: Optional value of the object
from_schema: https://w3id.org/my-org/bilayers_schema
rank: 1000
alias: optional
domain_of:
- AbstractWorkflowDetails
- AbstractUserInterface
range: boolean
required: true

```
</details>