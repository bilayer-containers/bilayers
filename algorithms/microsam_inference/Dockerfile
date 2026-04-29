FROM mambaorg/micromamba:1.5.8

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libegl1 libopengl0 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /bilayers

RUN micromamba install -y -n base -c conda-forge \
    python=3.11 \
    pip \
    micro_sam \
    && micromamba clean --all --yes

SHELL ["micromamba", "run", "-n", "base", "/bin/bash", "-c"]

CMD ["python"]