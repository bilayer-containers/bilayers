---
title: Getting Started
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

Bilayers provides pre-configured Docker images for widely used bioimage analysis algorithms, each bundled with an interactive web interface (Gradio) or a Jupyter Notebook UI. These images are hosted on DockerHub, enabling researchers and developers to run deep-learning models seamlessly without manual dependency management.

**New to Docker?** Learn the basics in [this introductory blog post on Docker](https://carpenter-singh-lab.broadinstitute.org/docker_for_biologists)

## Prerequisites

1. Install Docker Desktop
    - For Mac: [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
    - For Windows: [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)

2. DockerHub Account
    Bilayers retrieves pre-built images from DockerHub. 
    ![DockerDesktopLook](../images/tool_user/docker_desktop_look.png)

    You’ll need a DockerHub account to pull and run images.  
    Sign up for DockerHub if you don’t have an account.  
    Log in via the command line:
    ```{code}
    docker login
    ```
    You’ll be prompted to enter your DockerHub username and password.

3. Verify Your Docker Installation (Optional but Recommended)
   
    To confirm Docker is installed correctly, run:
    ```{code}
    docker run hello-world
    ```
    If everything is set up properly, you should see a message indicating that Docker is running successfully.


    



