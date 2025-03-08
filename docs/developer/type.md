

# Slot: type


_Type of the inputs, parameters and outputs_





URI: [https://w3id.org/my-org/bilayers_schema/:type](https://w3id.org/my-org/bilayers_schema/:type)



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

* Range: [TypeEnum](TypeEnum.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/my-org/bilayers_schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | https://w3id.org/my-org/bilayers_schema/:type |
| native | https://w3id.org/my-org/bilayers_schema/:type |




## LinkML Source

<details>
```yaml
name: type
description: Type of the inputs, parameters and outputs
from_schema: https://w3id.org/my-org/bilayers_schema
rank: 1000
alias: type
domain_of:
- AbstractWorkflowDetails
- AbstractUserInterface
range: TypeEnum
required: true

```
</details>