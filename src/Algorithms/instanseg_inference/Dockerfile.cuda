FROM ghcr.io/prefix-dev/pixi:0.31.0-jammy-cuda-12.3.1 AS build

RUN apt-get update && apt-get upgrade -y && apt-get install -y git

# copy source code, pixi.toml and pixi.lock to the container
RUN git clone https://github.com/instanseg/instanseg.git
WORKDIR /instanseg
# run some compilation / build task (if needed)
RUN pixi init --import env.yml
# reinstall packages to use GPU acceleration and CUDA
RUN pixi remove pytorch torchvision monai
ENTRYPOINT [ "/bin/bash" ]
RUN pixi project channel add --priority 3 nvidia/label/cuda-12.3.1
RUN pixi project channel add --priority 2 nvidia
# no way to do this from pixi cli
# this adds "channel-priority = disabled" to the pixi.toml's [project] table
RUN sed -i '/\[project\]/a channel-priority = \"disabled\"' pixi.toml
RUN pixi add "pytorch==2.1.1" "torchvision==0.16.1" "monai=1.3.0" "pytorch-cuda=12.1"
RUN pixi add --pypi "cupy-cuda12x==13.3.0"
# add InstanSeg as editable install
RUN pixi add --pypi --editable "InstanSeg @ ."
# Create the shell-hook bash script to activate the environment
RUN pixi shell-hook > /shell-hook.sh

# extend the shell-hook script to run the command passed to the container
RUN echo 'exec "$@"' >> /shell-hook.sh

FROM nvidia/cuda:12.3.1-base-ubuntu22.04 AS production

# only copy the production environment into prod container
# please note that the "prefix" (path) needs to stay the same as in the build container
COPY --from=build /instanseg/ /instanseg/
COPY --from=build /instanseg/.pixi/envs/default /instanseg/.pixi/envs/default
COPY --from=build /shell-hook.sh /shell-hook.sh
WORKDIR /instanseg

# set the entrypoint to the shell-hook script (activate the environment and run the command)
# no more pixi needed in the prod container
ENTRYPOINT ["/bin/bash", "/shell-hook.sh"]

CMD ["python"]
