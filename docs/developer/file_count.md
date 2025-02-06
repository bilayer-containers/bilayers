

# Slot: file_count


_Type of Number of files_





URI: [https://w3id.org/my-org/validate_schema/:file_count](https://w3id.org/my-org/validate_schema/:file_count)



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

* Range: [FileTypeEnum](FileTypeEnum.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/my-org/validate_schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | https://w3id.org/my-org/validate_schema/:file_count |
| native | https://w3id.org/my-org/validate_schema/:file_count |




## LinkML Source

<details>
```yaml
name: file_count
description: Type of Number of files
from_schema: https://w3id.org/my-org/validate_schema
rank: 1000
alias: file_count
domain_of:
- AbstractWorkflowDetails
- AbstractUserInterface
range: FileTypeEnum
required: false

```
</details>