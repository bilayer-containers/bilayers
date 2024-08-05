# from algorithm-image get the docker
FROM threshold-image

# Set the working directory within the container
WORKDIR /bilayers

# Install the dependencies for the gradio app
RUN python -m pip install pyyaml gradio==4.36.1 gradio_client==1.0.1 huggingface-hub==0.23.4 pydantic==2.7.4

# Add app.py file to the container
ADD parse/app.py /bilayers/
# Add __init__.py file for importing the files inside docker-container
ADD __init__.py /bilayers/

# Export the port
EXPOSE 8000

# Define the command to run the app
CMD ["python", "app.py"]