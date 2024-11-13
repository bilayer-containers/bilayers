---
title: Choosing the Right Base Docker Image
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

Docker images serve as the backbone for containerized applications, bundling all necessary code, libraries, and dependencies. When building modular systems, a ```Base Docker Image``` acts as the foundational layer, setting up the core environment on which other layers can be added. This approach allows containers to be built on top of a common base, ensuring consistency and simplifying dependency management.

In Bilayers, choosing the right base image is particularly important. The ```Base Docker Image``` — contains all the specific dependencies and settings required for your algorithm to function — referred to here as the ```Algorithm Docker Image``` or ```wrappee image```. Bilayers then automatically layers an ```Interface Docker Image```— or ```wrapper image``` — on top, adding dependencies for respective interfaces.

To ensure this layering works seamlessly, Bilayers expects the base image to meet a few key requirements:

## Requirements for the Algorithm (Base) Docker Image

1. **Public Repository**: Publish the algorithm docker image on DockerHub in a public repository for easy access.
2. **Python and Pip Installation**: Include `python>=3.9` and `pip` in your base image, as these are needed for Bilayers to add interface-specific dependencies.
3. **Multi-Stage Builds**: For multi-stage builds, ensure all required dependencies are included in the final stage. This enables the wrapper layer to access and use them.
4. **Virtual Environment Compatibility**: If dependencies are within a virtual environment (e.g., conda, pixi, or mamba), configure the environment so it persists into the next image layer. This ensures consistency in accessing dependencies between the base and interface layers.

## Adapting Non-Compliant Base Images

If your algorithm docker image doesn’t initially meet Bilayers requirements, use these strategies to make it compliant:
**Virtual Environment Persistence**:
Use `SHELL` and `ENTRYPOINT` commands to retain the virtual environment across layers. [Learn more about why it works](https://github.com/bilayer-containers/bilayers/issues/65#issuecomment-2450625527)

**Sample Template (for mamba Environment):**
```{code} yaml
# Set SHELL to ensure commands run in the Mamba environment
SHELL ["micromamba", "run", "-n", "myenv", "/bin/bash", "-c"]

# Set ENTRYPOINT to ensure the container starts in the Mamba environment
ENTRYPOINT ["micromamba", "run", "-n", "myenv"]
```

**Sample Template (for conda Environment):**
```{code} yaml
# Set SHELL to ensure commands run in the Conda environment
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

# Set ENTRYPOINT to automatically enter the Conda environment on startup
ENTRYPOINT ["conda", "run", "-n", "myenv"]
```

**Sample Template (for pixi Environment):**
```{code} yaml
# Set SHELL to ensure all commands execute within the specified environment
SHELL ["<env_manager>", "run", "--manifest-path", "<manifest_path>", "--environment", "<env_name>", "/bin/bash", "-c"]

# Set ENTRYPOINT to keep the environment active when the container starts
ENTRYPOINT ["<env_manager>", "run", "--manifest-path", "<manifest_path>", "--no-progress", "--no-lockfile-update", "--environment", "<env_name>"]
```