FROM ghcr.io/prefix-dev/pixi:0.31.0-jammy AS build

RUN apt-get update && apt-get upgrade -y && apt-get install -y git

# copy source code, pixi.toml and pixi.lock to the container
RUN git clone https://github.com/instanseg/instanseg.git
WORKDIR /instanseg
# run some compilation / build task (if needed)
RUN pixi init --import env.yml
# add InstanSeg as editable install
RUN pixi add --pypi --editable "InstanSeg @ ."
# Create the shell-hook bash script to activate the environment
RUN pixi shell-hook > /shell-hook.sh

# extend the shell-hook script to run the command passed to the container
RUN echo 'exec "$@"' >> /shell-hook.sh

FROM ubuntu:jammy AS production

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
