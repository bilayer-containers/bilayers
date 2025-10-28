# Fiji Headless Dockerfile with system Python available for downstream layers

# Use Python base image (faster build in your location)
FROM python:3.11-slim-bookworm

# Define maintainer
LABEL maintainer="https://gitter.im/fiji/fiji"

# Install wget and unzip first (needed for Fiji download)
RUN apt-get update && \
    apt-get install -y wget unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a user for Fiji early
RUN useradd -ms /bin/bash fiji && \
    mkdir /opt/imagej && chown fiji:fiji /opt/imagej

USER fiji
WORKDIR /opt/imagej

# Install Fiji (portable no-Java version) - do this before JDK/X11 packages
RUN wget --progress=bar:force https://downloads.imagej.net/fiji/latest/fiji-latest-portable-nojava.zip \
 && unzip -q fiji-latest-portable-nojava.zip \
 && mv Fiji/* Fiji/.* . 2>/dev/null || true \
 && rm -rf Fiji \
 && rm fiji-latest-portable-nojava.zip

# Switch back to root to install remaining system packages
USER root

# Install JDK 21 from Adoptium repository, X11 libs and xvfb (required by Fiji headless)
RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates curl gnupg && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://packages.adoptium.net/artifactory/api/gpg/key/public | gpg --dearmor -o /etc/apt/keyrings/adoptium.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/adoptium.gpg] https://packages.adoptium.net/artifactory/deb bookworm main" > /etc/apt/sources.list.d/adoptium.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        temurin-21-jdk xvfb xauth \
        libx11-6 libxext6 libxrender1 libxtst6 libxi6 \
        libxau6 libxdmcp6 libxcb1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Switch back to fiji user
USER fiji

# Add ImageJ to the PATH
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/imagej"

# Set working directory for macros
WORKDIR /app

# Copy the ImageJ macro script
COPY --chown=fiji:fiji threshold.ijm /app/threshold.ijm
