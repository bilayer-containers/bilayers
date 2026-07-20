FROM ubuntu:22.04 AS build

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential \
        git \
        openjdk-11-jdk-headless \
        python3-dev \
        python3-venv \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/venv

RUN --mount=type=cache,target=/root/.cache/pip \
    /opt/venv/bin/python    -m pip install --upgrade pip \
    && /opt/venv/bin/python -m pip install numpy numcodecs \
    && /opt/venv/bin/python -m pip install git+https://github.com/labsyspharm/ashlar.git@v1.20.0


FROM ubuntu:22.04 AS production

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        openjdk-11-jdk-headless \
        python3-tk \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build /opt/venv /opt/venv

RUN printf '#!/bin/sh\nexec /opt/venv/bin/python "$@"\n' > /usr/local/bin/python \
    && chmod +x /usr/local/bin/python

RUN printf '#!/bin/sh\nexec /opt/venv/bin/python -m pip "$@"\n' > /usr/local/bin/pip \
    && chmod +x /usr/local/bin/pip

RUN printf '#!/bin/sh\nexec /opt/venv/bin/ashlar "$@"\n' > /usr/local/bin/ashlar \
    && chmod +x /usr/local/bin/ashlar

# Utilize a single CPU core
ENV OMP_NUM_THREADS=1

VOLUME /data

WORKDIR /data

CMD ["/bin/bash"]
