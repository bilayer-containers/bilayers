# Define an image to start from 
FROM python:3.10.0-slim

# Set the working directory within the container
WORKDIR /bilayers

# Install the dependencies for the specific algorithm
RUN python -m pip install scipy==1.9.1 scikit-image==0.20.0

# Add algorithm_name.py from the directory where `docker build` was run and add it into the
# workspace directory within the container
<<<<<<< Updated upstream
ADD config.yaml /bilayers/
<<<<<<< HEAD
=======
ADD threshold.py /bilayers/
>>>>>>> f18e05f ([Add] Github Actions workflow and the bash script to dynamically pull up Interfaces)
=======
ADD threshold.py /bilayers/
>>>>>>> Stashed changes
