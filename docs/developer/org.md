

# Slot: org


_Organization of the docker image_





URI: [https://w3id.org/my-org/validate_schema/:org](https://w3id.org/my-org/validate_schema/:org)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DockerImage](DockerImage.md) | Description of docker_image for the specific algorithm |  no  |







## Properties

* Range: [String](String.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/my-org/validate_schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | https://w3id.org/my-org/validate_schema/:org |
| native | https://w3id.org/my-org/validate_schema/:org |




## LinkML Source

<details>
```yaml
name: org
description: Organization of the docker image
from_schema: https://w3id.org/my-org/validate_schema
rank: 1000
alias: org
domain_of:
- DockerImage
range: string
required: true

```
</details>