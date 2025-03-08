

# Slot: mode


_Mode of the object_





URI: [https://w3id.org/my-org/bilayers_schema/:mode](https://w3id.org/my-org/bilayers_schema/:mode)



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

* Range: [ModeEnum](ModeEnum.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/my-org/bilayers_schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | https://w3id.org/my-org/bilayers_schema/:mode |
| native | https://w3id.org/my-org/bilayers_schema/:mode |




## LinkML Source

<details>
```yaml
name: mode
description: Mode of the object
from_schema: https://w3id.org/my-org/bilayers_schema
rank: 1000
alias: mode
domain_of:
- AbstractWorkflowDetails
- AbstractUserInterface
range: ModeEnum
required: true

```
</details>