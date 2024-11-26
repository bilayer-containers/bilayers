

# Slot: platform


_Platform on which the docker image was built_





URI: [https://w3id.org/my-org/validate_schema/:platform](https://w3id.org/my-org/validate_schema/:platform)



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
| self | https://w3id.org/my-org/validate_schema/:platform |
| native | https://w3id.org/my-org/validate_schema/:platform |




## LinkML Source

<details>
```yaml
name: platform
description: Platform on which the docker image was built
from_schema: https://w3id.org/my-org/validate_schema
rank: 1000
alias: platform
domain_of:
- DockerImage
range: string
required: true

```
</details>