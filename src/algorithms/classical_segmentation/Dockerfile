# Define an image to start from 
FROM python:3.9-slim

# Set the working directory within the container
WORKDIR /bilayers

COPY classical_segmentation.py /bilayers

# Install the dependencies for the specific algorithm
RUN python -m pip install scipy==1.9.1 scikit-image==0.20.0

# Precompile Python module
RUN python -m compileall /bilayers/classical_segmentation.py

CMD ["python"]
