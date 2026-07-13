FROM ghcr.io/prefix-dev/pixi:0.70.2-jammy AS build

RUN apt-get update && apt-get upgrade -y && apt-get install -y git

# clone CellSAM source
RUN git clone https://github.com/vanvalenlab/cellSAM.git

WORKDIR /cellSAM

# pin a known working commit (replace with the one you tested)
RUN git checkout 362a8e5

# provide our own pixi environment definition
COPY ./pixi.toml ./pixi.toml
COPY ./pixi.lock ./pixi.lock

RUN pixi install -e default

# convert all .py files to .pyc for faster startup.
# -x skips version-shim modules that use newer-Python syntax
# alternative to completely removing this line
RUN pixi run --environment default python -m compileall -q \
    -x 'py3(1[1-9]|[2-9][0-9])_intrinsics\.py' \
    /cellSAM/.pixi/envs/default/lib/python3.10/site-packages
RUN pixi run --environment default python -m compileall -q /cellSAM/cellSAM

FROM ubuntu:jammy AS production

# copy pixi binary from the build container
COPY --from=build /usr/local/bin/pixi /usr/local/bin/pixi
# copy the built project and environment (path must match the build stage)
COPY --from=build /cellSAM/ /cellSAM/
COPY --from=build /cellSAM/.pixi/envs/default /cellSAM/.pixi/envs/default

WORKDIR /cellSAM

# copy our CLI wrapper into the image
COPY ./cellsam_inference.py /bilayers/cellsam_inference.py

ENV BILAYERS_TOOL_NAME=cellsam
ENV BILAYERS_VENV_MANAGER=pixi
ENV BILAYERS_VENV_NAME=default

# provide python/pip shims that dispatch into the pixi environment
# (replaces reliance on SHELL, which does not survive podman / the UI image)
RUN printf '#!/bin/sh\nexec pixi run --manifest-path /cellSAM/pixi.toml --environment default python "$@"\n' > /usr/local/bin/python \
 && chmod +x /usr/local/bin/python

RUN printf '#!/bin/sh\nexec pixi run --manifest-path /cellSAM/pixi.toml --environment default python -m pip "$@"\n' > /usr/local/bin/pip \
 && chmod +x /usr/local/bin/pip

ENTRYPOINT ["pixi", "run", "--manifest-path", "/cellSAM/pixi.toml", "--no-progress", "--frozen", "--environment", "default"]

CMD ["/bin/bash"]