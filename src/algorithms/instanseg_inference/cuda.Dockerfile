FROM ghcr.io/prefix-dev/pixi:0.31.0-jammy-cuda-12.3.1 AS build

RUN apt-get update && apt-get upgrade -y && apt-get install -y git

# copy source code, pixi.toml and pixi.lock to the container
RUN git clone https://github.com/instanseg/instanseg.git

WORKDIR /instanseg

# last known working state as of Nov 8, 2024
RUN git checkout 740d9da0

# env.yml is outdated and not kept in sync with deps in pyproject.toml
RUN rm env.yml
# pyproject.toml only installs from pypi and has some conflicts
RUN rm pyproject.toml
# replace with dep-free pyproject.toml for editible install of instanseg-torch
COPY ./pyproject.toml ./pyproject.toml
# install deps from pixi.toml
COPY ./pixi.toml ./pixi.toml

RUN pixi install -e cudaenv

# convert all .py files to .pyc files for faster initial startup and run times
RUN pixi run --environment cudaenv python -m compileall /instanseg/.pixi/envs/cudaenv/lib/python3.9/site-packages
RUN pixi run --environment cudaenv python -m compileall /instanseg/instanseg

FROM nvidia/cuda:12.3.1-base-ubuntu22.04 AS production

# copy pixi binary from the build container
COPY --from=build /usr/local/bin/pixi /usr/local/bin/pixi
# copy the production environment into prod container
# please note that the "prefix" (path) needs to stay the same as in the build container
COPY --from=build /instanseg/ /instanseg/
COPY --from=build /instanseg/.pixi/envs/cudaenv /instanseg/.pixi/envs/cudaenv

WORKDIR /instanseg

ENV BILAYERS_TOOL_NAME=instanseg
ENV BILAYERS_VENV_MANAGER=pixi
ENV BILAYERS_VENV_NAME=cudaenv

# set shell to run commands in default pixi environment
SHELL ["pixi", "run", "--manifest-path", "/instanseg/pixi.toml", "--environment", "cudaenv", "/bin/bash", "-c"]

# set entrypoint to run pixi commands in pixi environment
ENTRYPOINT ["pixi", "run", "--manifest-path", "/instanseg/pixi.toml", "--no-progress", "--no-lockfile-update", "--environment", "cudaenv"]

# default command runs bash
CMD ["/bin/bash"]
