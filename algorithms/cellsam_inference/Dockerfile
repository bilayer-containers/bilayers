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

# copy our CLI wrapper into the image
COPY ./cellsam_inference.py ./cellsam_inference.py

RUN pixi install -e default

# precompile for faster startup
RUN pixi run --environment default python -m compileall /cellSAM/cellSAM

# in case we decided to bake the weights into the image, we get them here
# RUN --mount=type=secret,id=deepcell_token \
#     DEEPCELL_ACCESS_TOKEN=$(cat /run/secrets/deepcell_token) \
#     pixi run --environment default python -c "from cellSAM import get_model; get_model()"

FROM ubuntu:jammy AS production

# copy pixi binary from the build container
COPY --from=build /usr/local/bin/pixi /usr/local/bin/pixi
# copy the built project and environment (path must match the build stage)
COPY --from=build /cellSAM/ /cellSAM/
# I think this line is redundant since we already copy the whole /cellSAM/ directory, but leaving it here for now
#COPY --from=build /cellSAM/.pixi/envs/default /cellSAM/.pixi/envs/default

WORKDIR /cellSAM

ENV BILAYERS_TOOL_NAME=cellsam
ENV BILAYERS_VENV_MANAGER=pixi
ENV BILAYERS_VENV_NAME=default

# run all commands inside the pixi environment
SHELL ["pixi", "run", "--manifest-path", "/cellSAM/pixi.toml", "--environment", "default", "/bin/bash", "-c"]

ENTRYPOINT ["pixi", "run", "--manifest-path", "/cellSAM/pixi.toml", "--no-progress", "--frozen", "--environment", "default"]

CMD ["/bin/bash"]