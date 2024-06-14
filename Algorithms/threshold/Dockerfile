# Define an image to start from 
#FROM bethcimini/docker-gradio-demo:latest
FROM gradio-base:latest

# Set the working directory within the container
WORKDIR /workspace

# Install the dependencies for the gradio app
RUN python -m pip install scipy==1.9.1 scikit-image==0.20.0

# Add app.py from the directory where `docker build` was run and add it into the
# workspace directory within the container
ADD /Algorithms /workspace/

# Expose port 8000. You CAN do this from the command line, but it makes it possible to run entirely in the app
EXPOSE 8000

# Run the app. Will be accessible at http://localhost:8000/
CMD [ "python3" , "/workspace/Algorithms/threshold.py" ]