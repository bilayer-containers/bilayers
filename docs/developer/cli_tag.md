

# Slot: cli_tag


_CLI tag of the object_





URI: [https://w3id.org/my-org/bilayers_schema/:cli_tag](https://w3id.org/my-org/bilayers_schema/:cli_tag)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [TypeParameter](TypeParameter.md) | Parameters of a specific Algorithm |  no  |
| [TypeOutput](TypeOutput.md) | Outputs of the algorithm to the next step in the workflow |  no  |
| [TypeInput](TypeInput.md) | Inputs to the algorithm from the last step of the workflow |  no  |
| [AbstractWorkflowDetails](AbstractWorkflowDetails.md) | Abstract class for details needed to fit config in the workflow |  no  |
| [HiddenArgs](HiddenArgs.md) | Hidden arguments for the Algorithm |  no  |







## Properties

* Range: [String](String.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/my-org/bilayers_schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | https://w3id.org/my-org/bilayers_schema/:cli_tag |
| native | https://w3id.org/my-org/bilayers_schema/:cli_tag |




## LinkML Source

<details>
```yaml
name: cli_tag
description: CLI tag of the object
from_schema: https://w3id.org/my-org/bilayers_schema
rank: 1000
alias: cli_tag
domain_of:
- AbstractWorkflowDetails
- TypeParameter
- HiddenArgs
range: string
required: true

```
</details>