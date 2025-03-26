FROM python:3.9-slim

# Set working directory
WORKDIR /bilayers

# Copy the inference script into the container
COPY stardist_inference.py /bilayers

# Install system dependencies required for StarDist and OpenMP
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    g++ \
    libomp-dev \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, and wheel
RUN pip install --upgrade pip setuptools wheel

# Install required Python dependencies
RUN pip install "numpy<2.0" scikit-image tensorflow csbdeep stardist

# Precompile the Python module (optional)
RUN python -m compileall /bilayers/stardist_inference.py

CMD ["/bin/bash"]
