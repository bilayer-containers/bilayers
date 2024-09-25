FROM mambaorg/micromamba:1-focal-cuda-12.1.1

USER root

#SETUP
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y git

USER $MAMBA_USER

#INSTANSEG
RUN git clone https://github.com/instanseg/instanseg.git
WORKDIR instanseg

RUN micromamba create --file env.yml && micromamba clean --all --yes

ENV ENV_NAME=instanseg
