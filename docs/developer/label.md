

# Slot: label


_Label of the object, but also Radio button's label_





URI: [https://w3id.org/my-org/bilayers_schema/:label](https://w3id.org/my-org/bilayers_schema/:label)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [AbstractUserInterface](AbstractUserInterface.md) | Abstract class for user interface |  no  |
| [RadioOptions](RadioOptions.md) | Options of the Radio button in parameters, display_only |  no  |
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
| self | https://w3id.org/my-org/bilayers_schema/:label |
| native | https://w3id.org/my-org/bilayers_schema/:label |




## LinkML Source

<details>
```yaml
name: label
description: Label of the object, but also Radio button's label
from_schema: https://w3id.org/my-org/bilayers_schema
rank: 1000
alias: label
domain_of:
- AbstractWorkflowDetails
- AbstractUserInterface
- RadioOptions
range: Any
required: true

```
</details>