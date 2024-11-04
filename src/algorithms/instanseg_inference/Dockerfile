FROM ghcr.io/prefix-dev/pixi:0.31.0-jammy AS build

RUN apt-get update && apt-get upgrade -y && apt-get install -y git

# copy source code, pixi.toml and pixi.lock to the container
RUN git clone https://github.com/instanseg/instanseg.git

WORKDIR /instanseg

# last known working state
RUN git checkout b9c9d6b

# run some compilation / build task (if needed)
RUN pixi init --import env.yml
# add InstanSeg as editable install
RUN pixi add --pypi --editable "InstanSeg @ ."

FROM ubuntu:jammy AS production

# copy pixi binary from the build container
COPY --from=build /usr/local/bin/pixi /usr/local/bin/pixi
# copy the production environment into prod container
# please note that the "prefix" (path) needs to stay the same as in the build container
COPY --from=build /instanseg/ /instanseg/
COPY --from=build /instanseg/.pixi/envs/default /instanseg/.pixi/envs/default

WORKDIR /instanseg

# install pip for downstream containers to pip install things
RUN pixi add pip

# set shell to run commands in default pixi environment
SHELL ["pixi", "run", "/bin/bash", "-c"]

# set entrypoint to run pixi commands in default pixi environment
ENTRYPOINT ["pixi", "run", "--no-progress", "--no-lockfile-update"]

# default command runs bash
CMD ["/bin/bash"]
