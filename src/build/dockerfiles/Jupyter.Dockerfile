# Argument that takes Algorithm-Image-Name as input
ARG BASE_IMAGE

# From algorithm image
FROM $BASE_IMAGE

ARG FOLDER_NAME

# Install the dependencies for the gradio app
RUN python -m pip install pyyaml jupyter huggingface-hub==0.23.4 pydantic==2.7.4

# Set the working directory within the container
WORKDIR /bilayers

# # Install numpy and opencv-python
# RUN python -m pip install numpy==1.23.0 opencv-python-headless==4.5.3.56 matplotlib==3.5.1

# Add app.py file to the container
ADD parse/generated_folders/$FOLDER_NAME/generated_notebook.ipynb /bilayers/

# Add __init__.py file for importing the files inside docker-container
ADD __init__.py /bilayers/

# Export the port
EXPOSE 7878

# Define the command to run the app
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root", "--port=7878"]