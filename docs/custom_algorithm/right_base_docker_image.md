---
title: Choosing the Right Base Docker Image
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---
<!-- Add 2 spaces at the end of the line to get the newlines to be rendered as a list -->
Docker images serve as the backbone for containerized applications, bundling all necessary code, libraries, and dependencies.  
When building modular systems, a ```Base Docker Image``` acts as the foundational layer, setting up the core environment on which other layers can be added.  
This approach allows containers to be built on top of a common base, ensuring consistency and simplifying dependency management.

In Bilayers, choosing the right base image is particularly important.  
The ```Base Docker Image``` — contains all the specific dependencies and settings required for your algorithm to function — referred to here as the ```Algorithm Docker Image``` or ```wrappee image```.  
Bilayers then automatically layers an ```Interface Docker Image```— or ```wrapper image``` — on top, adding dependencies for respective interfaces.

To ensure this layering works seamlessly, Bilayers expects the base image to meet a few key requirements.


<br>

## Requirements for the Algorithm (Base) Docker Image

1. **Public Repository**: Publish the algorithm docker image in a public repository for easy access. Give it a real version tag (rather than `latest`) so Bilayers can pin the exact version of your algorithm.
2. **Python and Pip Installation**: Include `python>=3.9` reachable as either `python` or `python3` on `PATH`, plus a working `pip`, as these are needed for Bilayers to add interface-specific dependencies.
3. **Version Pinning**: Pin the exact base tag you build from (e.g. `python:3.11-slim` rather than `python:latest`) to keep builds repeatable. Although Bilayers only requires `python>=3.9`, that version has reached end of life, so prefer the most recent Python your algorithm supports.
4. **Multi-Stage Builds**: For multi-stage builds, ensure all required dependencies are included in the final stage. This enables the wrapper layer to access and use them.
5. **Virtual Environment Compatibility**: If dependencies live in a virtual environment (e.g., conda, pixi, or mamba), configure the environment so it persists into the next image layer. This ensures consistency in accessing dependencies between the base and interface layers.
6. **Uninterrupted PATH**: Nothing in the image may take `python` or `pip` off `PATH`. An `ENTRYPOINT` that resets or replaces `PATH` at container start hides them from the interface layer, even though they were reachable while the image was being built.


<br>


## Adapting Non-Compliant Base Images

If your algorithm docker image doesn’t initially meet Bilayers requirements, find your case below and use the suggested strategies to make it compliant:

### 1. Your dependencies live in a virtual environment (conda, mamba, pixi)

- If you are using `docker build`, use `SHELL` and `ENTRYPOINT` commands to retain the virtual environment across layers. 

  **[docker] Sample Template (for conda Environment):**
  ```{code} dockerfile
  SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]
  ENTRYPOINT ["conda", "run", "-n", "myenv"]
  ```

  **[docker] Sample Template (for pixi Environment):**
  ```{code} dockerfile
  SHELL ["pixi", "run", "--manifest-path", "<manifest_path>", "--environment", "<env_name>", "/bin/bash", "-c"]
  ENTRYPOINT ["pixi", "run", "--as-is", "--manifest-path", "<manifest_path>", "--no-progress", "--environment", "<env_name>"]
  ```


- If you are using `podman build`, `SHELL` is not inherited by the interface layer. Write `python` and `pip` shims into `/usr/local/bin` that hand off to your environment instead. These are ordinary files in the image, so every downstream layer and every builder sees them. Keep `ENTRYPOINT` as well, for interactive use.

  **[podman] Sample Template (for pixi Environment):**
  ```{code} dockerfile
  RUN printf '#!/bin/sh\nexec pixi run --as-is --manifest-path <manifest_path> --environment <env_name> python "$@"\n' > /usr/local/bin/python \
  && chmod +x /usr/local/bin/python

  RUN printf '#!/bin/sh\nexec pixi run --as-is --manifest-path <manifest_path> --environment <env_name> python -m pip "$@"\n' > /usr/local/bin/pip \
  && chmod +x /usr/local/bin/pip

  ENTRYPOINT ["pixi", "run", "--as-is", "--manifest-path", "<manifest_path>", "--no-progress", "--environment", "<env_name>"]
  ```

### 2. Your image ships no Python, or a Python older than 3.9

Older base images often ship an interpreter that is too old for Bilayers. Rather than relying on the distro's package manager, which pins its own version and may not be present at all, download a standalone Python distribution into the image and put it on `PATH`. This works on any base image.

**Sample Template:**
```{code} dockerfile
FROM <upstream_image>:<tag>

# download a standalone Python distribution and unpack it into /opt
ADD <standalone_python_url> /tmp/python.tar.gz
RUN tar -xzf /tmp/python.tar.gz -C /opt && rm /tmp/python.tar.gz

ENV PATH=/opt/python/bin:$PATH
```

### 3. You cannot or do not want to modify the published image
Build an intermediate image instead: start from a base you control, add Python as above, then copy your algorithm's binaries out of the published image. This also leaves the upstream `ENTRYPOINT` behind, which is often what breaks the layering in the first place.

**Sample Template:**

```{code} dockerfile
FROM <base_you_control>:<tag>
# add a standalone Python, as in the previous section
ENV PATH=/opt/python/bin:$PATH

# symlink as well, so the interpreter survives a PATH reset
RUN ln -s /opt/python/bin/python3 /usr/local/bin/python \
    && ln -s /opt/python/bin/pip3 /usr/local/bin/pip

# copy the algorithm out of the published image
COPY --from=<upstream_image>:<tag> <binary_path> <binary_path>
COPY --from=<upstream_image>:<tag> <library_path> <library_path>
```

<br>

## Verify Image Compatibility
You can run these templates to check if your base image is compatible with the Bilayers wrappers:
```{code} bash
# is Python and pip reachable at build time?
docker run --rm --entrypoint sh <your_image> -c 'PY=$(command -v python || command -v python3); echo "$PY"; "$PY" -m pip --version

# are they still reachable after ENTRYPOINT runs?
docker run --rm <your_image> sh -c 'PY=$(command -v python || command -v python3); echo "$PY"; "$PY" --version; "$PY" -m pip --version
```