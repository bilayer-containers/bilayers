FROM ghcr.io/prefix-dev/pixi:0.70.2-jammy AS build

RUN apt-get update && apt-get upgrade -y && apt-get install -y git

WORKDIR /morphem_inference

# copy pixi.toml, pixi.lock
COPY ./pixi.toml ./pixi.toml
COPY ./pixi.lock ./pixi.lock

RUN --mount=type=cache,target=/root/.cache/rattler pixi install -e cpuenv

# add HF cache dir to the image
ENV HF_HOME=/morphem_inference/hf_cache

# bake the MorphEm weights into the image
# model_cache is not trached in git -> download the weights from the HF model
# repo (https://huggingface.co/CaicedoLab/MorphEm - commit ID: 0e8d58787421f83f975634d72420d85c5dfc9c2c)
# into morphem_inference/model_cache before building
COPY ./model_cache /morphem_inference/model_cache

FROM ubuntu:jammy AS production

# copy pixi binary from the build container
COPY --from=build /usr/local/bin/pixi /usr/local/bin/pixi 
# copy the production environment into prod container
# please note that the "prefix" (path) needs to stay the same as in the build container
COPY --from=build /morphem_inference/ /morphem_inference/
#COPY --from=build /morphem_inference/.pixi/envs/cpuenv /morphem_inference/.pixi/envs/cpuenv

WORKDIR /morphem_inference

COPY ./morphem_inference.py ./morphem_inference.py
# convert all .py files to .pyc files for faster initial startup and run times
RUN pixi run --environment cpuenv python -m compileall -q /morphem_inference/morphem_inference.py

ENV BILAYERS_TOOL_NAME=morphem_inference
ENV BILAYERS_VENV_MANAGER=pixi
ENV BILAYERS_VENV_NAME=cpuenv

# provide python/pip shims that dispatch into the pixi environment
# (replaces reliance on SHELL, which does not survive podman / the UI image)
RUN printf '#!/bin/sh\nexec pixi run --manifest-path /morphem_inference/pixi.toml --environment cpuenv python "$@"\n' > /usr/local/bin/python \
 && chmod +x /usr/local/bin/python

RUN printf '#!/bin/sh\nexec pixi run --manifest-path /morphem_inference/pixi.toml --environment cpuenv python -m pip "$@"\n' > /usr/local/bin/pip \
 && chmod +x /usr/local/bin/pip

# set entrypoint to run pixi commands in pixi environment
ENTRYPOINT ["pixi", "run", "--manifest-path", "/morphem_inference/pixi.toml", "--no-progress", "--frozen", "--environment", "cpuenv"]

# default command runs bash
CMD ["/bin/bash"]