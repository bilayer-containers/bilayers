# Argument that takes Algorithm-Image-Name as input
ARG BASE_IMAGE

# From algorithm image
FROM $BASE_IMAGE

ARG FOLDER_NAME

# Install the dependencies for the gradio app
RUN python -m pip install --no-cache-dir pyyaml gradio==4.44.1 huggingface-hub==0.34.3

# Set the working directory within the container
WORKDIR /bilayers

# Add app.py file to the container
COPY generated_folders/$FOLDER_NAME/app.py /bilayers/

# Add __init__.py file for importing the files inside docker-container
RUN touch /bilayers/__init__.py

# Export the port
EXPOSE 7878

# Define the command to run the app
CMD ["python", "-u", "app.py"]
