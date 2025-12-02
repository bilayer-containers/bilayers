# Argument that takes Algorithm-Image-Name as input
ARG BASE_IMAGE

# From algorithm image
FROM $BASE_IMAGE

ARG FOLDER_NAME

# Install the dependencies for the streamlit app
# Note:

RUN python -m pip install pyyaml streamlit pydantic

# Set the working directory within the container
WORKDIR /bilayers

# Add app.py file to the container
ADD parse/generated_folders/$FOLDER_NAME/streamlit_app.py /bilayers/

# Add __init__.py file for importing the files inside docker-container
ADD __init__.py /bilayers/

# Export the port
EXPOSE 8501

# Define the command to run the app
CMD ["streamlit", "run", "streamlit_app.py"]