FROM ghcr.io/prefix-dev/pixi:0.31.0-jammy-cuda-12.3.1 AS build

RUN apt-get update && apt-get upgrade -y && apt-get install -y git

# copy source code, pixi.toml and pixi.lock to the container
RUN git clone https://github.com/instanseg/instanseg.git
WORKDIR /instanseg

# last known working state
RUN git checkout b9c9d6b

# run some compilation / build task (if needed)
RUN pixi init --import env.yml
# reinstall packages to use GPU acceleration and CUDA
RUN pixi remove pytorch torchvision monai
RUN pixi project channel add --priority 3 nvidia/label/cuda-12.3.1
RUN pixi project channel add --priority 2 nvidia
# no way to do this from pixi cli
# this adds "channel-priority = disabled" to the pixi.toml's [project] table
RUN sed -i '/\[project\]/a channel-priority = \"disabled\"' pixi.toml
RUN pixi add "pytorch==2.1.1" "torchvision==0.16.1" "monai==1.3.0" "pytorch-cuda==12.1"
RUN pixi add --pypi "cupy-cuda12x==13.3.0"
# add InstanSeg as editable install
RUN pixi add --pypi --editable "InstanSeg @ ."

FROM nvidia/cuda:12.3.1-base-ubuntu22.04 AS production

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
