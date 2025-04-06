

# Slot: default


_Default value of the parameter_





URI: [https://w3id.org/my-org/bilayers_schema/:default](https://w3id.org/my-org/bilayers_schema/:default)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [TypeInput](TypeInput.md) | Inputs to the algorithm from the last step of the workflow |  no  |
| [TypeDisplayOnly](TypeDisplayOnly.md) | Display only parameters of a specific Algorithm |  no  |
| [AbstractWorkflowDetails](AbstractWorkflowDetails.md) | Abstract class for details needed to fit config in the workflow |  no  |
| [TypeParameter](TypeParameter.md) | Parameters of a specific Algorithm |  no  |
| [TypeOutput](TypeOutput.md) | Outputs of the algorithm to the next step in the workflow |  no  |







## Properties

* Range: [Any](Any.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/my-org/bilayers_schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | https://w3id.org/my-org/bilayers_schema/:default |
| native | https://w3id.org/my-org/bilayers_schema/:default |




## LinkML Source

<details>
```yaml
name: default
description: Default value of the parameter
from_schema: https://w3id.org/my-org/bilayers_schema
rank: 1000
alias: default
domain_of:
- AbstractWorkflowDetails
- TypeParameter
- TypeDisplayOnly
range: Any
required: true

```
</details>