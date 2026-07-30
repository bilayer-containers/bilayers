FROM superelastix/elastix:5.0.1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    python3.9 python3.9-dev python3.9-distutils curl \
    && curl -sS https://bootstrap.pypa.io/pip/3.9/get-pip.py | python3.9 \
    && rm -rf /var/lib/apt/lists/*


RUN ln -sf /usr/bin/python3.9 /usr/local/bin/python3 && \
    ln -sf /usr/bin/python3.9 /usr/local/bin/python

RUN python --version && python -m pip --version && elastix --version

CMD ["/bin/bash"]
