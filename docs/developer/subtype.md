

# Slot: subtype


_Subtype of the inputs and outputs_





URI: [https://w3id.org/my-org/validate_schema/:subtype](https://w3id.org/my-org/validate_schema/:subtype)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [TypeOutput](TypeOutput.md) | Outputs of the algorithm to the next step in the workflow |  no  |
| [TypeInput](TypeInput.md) | Inputs to the algorithm from the last step of the workflow |  no  |
| [AbstractWorkflowDetails](AbstractWorkflowDetails.md) | Abstract class for details needed to fit config in the workflow |  no  |







## Properties

* Range: [SubTypeEnum](SubTypeEnum.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/my-org/validate_schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | https://w3id.org/my-org/validate_schema/:subtype |
| native | https://w3id.org/my-org/validate_schema/:subtype |




## LinkML Source

<details>
```yaml
name: subtype
description: Subtype of the inputs and outputs
from_schema: https://w3id.org/my-org/validate_schema
rank: 1000
alias: subtype
domain_of:
- AbstractWorkflowDetails
range: SubTypeEnum
multivalued: true

```
</details>