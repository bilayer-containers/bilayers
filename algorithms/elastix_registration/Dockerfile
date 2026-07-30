FROM superelastix/elastix:5.0.1

# Standalone CPython build (astral-sh/python-build-standalone), already bundles pip
ARG PYTHON_URL=https://github.com/astral-sh/python-build-standalone/releases/download/20260728/cpython-3.10.20%2B20260728-x86_64-unknown-linux-gnu-install_only.tar.gz
ARG PYTHON_SHA256=5b6ae36e239727dd9b9c567023261e8b2fdd716d25dde2b15d68bf105b782856

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && curl -sSL -o /tmp/python.tar.gz "$PYTHON_URL" \
    && echo "$PYTHON_SHA256  /tmp/python.tar.gz" | sha256sum -c - \
    && tar -xzf /tmp/python.tar.gz -C /opt \
    && rm /tmp/python.tar.gz \
    && rm -rf /var/lib/apt/lists/*

# the tarball unpacks to /opt/python -> bin/ holds python, python3, pip, pip3
ENV PATH=/opt/python/bin:$PATH

# smoke test
RUN python --version && python -m pip --version && elastix --version

CMD ["/bin/bash"]
