# Argument that takes Algorithm-Image-Name as input
ARG BASE_IMAGE

# From algorithm image
FROM $BASE_IMAGE

ARG FOLDER_NAME

# USER root

# RUN apt-get update && apt-get install -y python3 python3-pip

# Set the working directory within the container
WORKDIR /bilayers

# ARG install_str="python -m pip install pyyaml gradio gradio_client huggingface-hub pydantic"
# Install the dependencies for the gradio app
RUN python -m pip install pyyaml gradio gradio_client huggingface-hub pydantic

# Check if /shell-hook.sh exists and execute it if it does
# RUN if [ -f /shell-hook.sh ]; then /bin/bash /shell-hook.sh echo install_str; else echo install_str; fi


# Install numpy and opencv-python
# RUN python -m pip install numpy==1.23.0 opencv-python-headless==4.5.3.56 matplotlib==3.5.1

# Add app.py file to the container
ADD parse/generated_folders/$FOLDER_NAME/app.py /bilayers/

# Add __init__.py file for importing the files inside docker-container
ADD __init__.py /bilayers/

# Export the port
EXPOSE 7878

# RUN if [ -f /shell-hook.sh ]; then command_str='["/bin/bash", "/shell-hook.sh", "python", "-u", "app.py"]'; else command_str='["python", "-u", "app.py"]'; fi
# RUN "/bin/bash "/shell-hook.sh"

# Define the command to run the app
CMD ["python", "-u", "app.py"]