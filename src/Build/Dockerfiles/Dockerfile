# From algorithm image
FROM cellprofiler/runcellpose_no_pretrained:0.1

# Set the working directory within the container
WORKDIR /bilayers

# Install the dependencies for the gradio app
RUN python -m pip install pyyaml gradio==4.36.1 gradio_client==1.0.1 huggingface-hub==0.23.4 pydantic==2.7.4

# Install numpy and opencv-python
RUN python -m pip install numpy==1.23.0 opencv-python-headless==4.5.3.56 matplotlib==3.5.1

# Add app.py file to the container
ADD parse/app.py /bilayers/
# Add __init__.py file for importing the files inside docker-container
ADD __init__.py /bilayers/

# Export the port
EXPOSE 8000

# Define the command to run the app
CMD ["python", "app.py"]