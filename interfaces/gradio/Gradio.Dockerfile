# Argument that takes Algorithm-Image-Name as input
ARG BASE_IMAGE

# From algorithm image
FROM $BASE_IMAGE

ARG FOLDER_NAME

# Install the dependencies for the gradio app
# Note:
# - Gradio depends on pydantic. However, as of 04/03/2025, pydantic version 2.11 introduces a bug that breaks the Gradio app.
# - As a workaround, we pin pydantic to version 2.10.6.
# - huggingface-hub > 0.26 removed HfFolder, causing import errors. Pin to 0.26.2.
# For more details, refer to:
#   - https://github.com/gradio-app/gradio/issues/10662
#   - https://github.com/gradio-app/gradio/pull/10908
RUN python -m pip install --user --no-cache-dir pyyaml gradio gradio_client huggingface-hub==0.26.2 pydantic==2.10.6

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
