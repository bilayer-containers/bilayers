# Argument that takes Algorithm-Image-Name as input
ARG BASE_IMAGE

# From algorithm image
FROM $BASE_IMAGE

ARG FOLDER_NAME

# Set the working directory within the container
WORKDIR /bilayers

# Install the dependencies for the gradio app
RUN python -m pip install pyyaml gradio==4.36.1 gradio_client==1.0.1 huggingface-hub==0.23.4 pydantic==2.7.4

# Install numpy and opencv-python
RUN python -m pip install numpy==1.23.0 opencv-python-headless==4.5.3.56 matplotlib==3.5.1

# Add app.py file to the container
ADD parse/generated_folders/$FOLDER_NAME/app.py /bilayers/

# Add __init__.py file for importing the files inside docker-container
ADD __init__.py /bilayers/

# Export the port
EXPOSE 8000

# Define the command to run the app
CMD ["python", "-u", "app.py"]