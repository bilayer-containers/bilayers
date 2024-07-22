import nox
import os
<<<<<<< HEAD
<<<<<<< HEAD
import yaml
=======
>>>>>>> f18e05f ([Add] Github Actions workflow and the bash script to dynamically pull up Interfaces)
=======
import yaml
>>>>>>> d7feedb ([Add] Cellpose's Gradio generation via CLI Usage)

@nox.session
def run_parse(session):
    session.install('pyyaml')
    session.cd('src/Build/parse')
    config_path = session.posargs[0]
    session.run("python", "parse.py", config_path)
    session.cd('../../..')
    
@nox.session
def run_generate(session):
<<<<<<< HEAD
    session.install('pyyaml', 'jinja2')
=======
    session.install('pyyaml')
>>>>>>> f18e05f ([Add] Github Actions workflow and the bash script to dynamically pull up Interfaces)
    session.cd('src/Build/parse')
    session.run('python', 'generate.py')
    session.cd('../../..')

# Prevoiusly, we had more basic nox-session for building the Algorithm docker image
# @nox.session
# def build_algorithm(session):
#     """Build the Algorithm docker Image"""
#     if len(session.posargs) > 0:
#         algorithm = session.posargs[0] 
#     else:
#         algorithm = 'threshold'
#     print("Building Algorithm Nox-File: ", algorithm)
#     image_name = f'{algorithm}-image'
#     print("Image Name: ", image_name)
#     dockerfile_path = f'src/Algorithms/{algorithm}/Dockerfile'
#     print("Dockerfile Path: ", dockerfile_path)

#     # If Dockerfile doesn't exist for the specified algorithm
#     if not os.path.exists(dockerfile_path):
#         print(f'Dockerfile for {algorithm} not found at {dockerfile_path}')
#         session.error(f'Dockerfile for {algorithm} not found at {dockerfile_path}')
#     session.run('docker', 'build', '-t', image_name, '-f', dockerfile_path, f'src/Algorithms/{algorithm}')


@nox.session
def build_algorithm(session):
    """Build the Algorithm docker Image"""
    if len(session.posargs) > 0:
        algorithm = session.posargs[0] 
<<<<<<< HEAD
<<<<<<< HEAD
        print("Algorithm Name in build_algorithm session: ", algorithm)
    else:
        algorithm = 'threshold'
    
    print("Building Algorithm Nox-File: ", algorithm)
    image_name = f'{algorithm}'
    print("Image Name: ", image_name)
    dockerfile_path = f'src/Algorithms/{algorithm}/Dockerfile'
    config_file_path = f'src/Algorithms/{algorithm}/config.yaml'

    print("Dockerfile Path: ", dockerfile_path)

    if os.path.exists(dockerfile_path):
        # If Dockerfile exists, build the image
        session.run('docker', 'build', '-t', image_name, '-f', dockerfile_path, f'src/Algorithms/{algorithm}')
    else:
        # If Dockerfile doesn't exist, look into the config.yaml file
        print(f'Dockerfile for {algorithm} not found at {dockerfile_path}')
        
        if os.path.exists(config_file_path):
            print(f'Checking config file at {config_file_path}')
            with open(config_file_path, 'r') as file:
                config = yaml.safe_load(file)
            
            # Extract the Docker image name from the config
            org = config.get('docker-image', {}).get('org')
            name = config.get('docker-image', {}).get('name')
            tag = config.get('docker-image', {}).get('tag')
            docker_image_name = f'{org}/{name}:{tag}' if org and name and tag else None

            # Save the Docker image name in a file
            with open('/tmp/docker_image_name.txt', 'w') as file:
                file.write(docker_image_name)
                
<<<<<<< HEAD
            if docker_image_name:
                print(f'Found Docker image name in config: {docker_image_name}')
                # Pull the Docker image from DockerHub
                session.run('docker', 'pull', docker_image_name)
            else:
                session.error(f'Docker image name not found in {config_file_path}')
        else:
            session.error(f'Config file not found at {config_file_path}')

@nox.session
def build_interface(session):
    """Build the Gradio docker Image"""
    if len(session.posargs) > 0:
        interface = session.posargs[0] 
    else:
        interface = 'gradio'
    print("Building Interface Nox-File: ", interface)

    image_name = f'{interface}-image'
    print("Image Name: ", image_name)

    dockerfile_path = f'src/Build/Dockerfiles/Dockerfile'
    print("Dockerfile Path: ", dockerfile_path)

    # Read the Docker image name from the file
    with open('/tmp/docker_image_name.txt', 'r') as file:
        base_image = file.read().strip()

    session.run('docker', 'build', '--build-arg',  f'BASE_IMAGE={base_image}', '-t', image_name, '-f', dockerfile_path, 'src/Build')

@nox.session
def install_gradio(session):
    """Install Gradio"""
    session.install('gradio')
=======
=======
        print("Algorithm Name in build_algorithm session: ", algorithm)
>>>>>>> d7feedb ([Add] Cellpose's Gradio generation via CLI Usage)
    else:
        algorithm = 'threshold'
    
    print("Building Algorithm Nox-File: ", algorithm)
    image_name = f'{algorithm}'
    print("Image Name: ", image_name)
    dockerfile_path = f'src/Algorithms/{algorithm}/Dockerfile'
    config_file_path = f'src/Algorithms/{algorithm}/config.yaml'

    print("Dockerfile Path: ", dockerfile_path)

    if os.path.exists(dockerfile_path):
        # If Dockerfile exists, build the image
        session.run('docker', 'build', '-t', image_name, '-f', dockerfile_path, f'src/Algorithms/{algorithm}')
    else:
        # If Dockerfile doesn't exist, look into the config.yaml file
        print(f'Dockerfile for {algorithm} not found at {dockerfile_path}')
        
        if os.path.exists(config_file_path):
            print(f'Checking config file at {config_file_path}')
            with open(config_file_path, 'r') as file:
                config = yaml.safe_load(file)
            
            # Extract the Docker image name from the config
            org = config.get('docker-image', {}).get('org')
            name = config.get('docker-image', {}).get('name')
            tag = config.get('docker-image', {}).get('tag')
            docker_image_name = f'{org}/{name}:{tag}' if org and name and tag else None
            
=======
>>>>>>> 0763482 ([Update] Noxfile to dynamically set Base-Image to dockerfile)
            if docker_image_name:
                print(f'Found Docker image name in config: {docker_image_name}')
                # Pull the Docker image from DockerHub
                session.run('docker', 'pull', docker_image_name)
            else:
                session.error(f'Docker image name not found in {config_file_path}')
        else:
            session.error(f'Config file not found at {config_file_path}')

@nox.session
def build_interface(session):
    """Build the Gradio docker Image"""
<<<<<<< HEAD
    session.run('docker', 'build', '-t', 'gradio-image', '-f', 'src/build/Dockerfiles/Dockerfile', 'src/Build')
>>>>>>> f18e05f ([Add] Github Actions workflow and the bash script to dynamically pull up Interfaces)
=======
    if len(session.posargs) > 0:
        interface = session.posargs[0] 
    else:
        interface = 'gradio'
    print("Building Interface Nox-File: ", interface)

    image_name = f'{interface}-image'
    print("Image Name: ", image_name)

    dockerfile_path = f'src/Build/Dockerfiles/Dockerfile'
    print("Dockerfile Path: ", dockerfile_path)

<<<<<<< HEAD
<<<<<<< HEAD
    session.run('docker', 'build', '-t', image_name, '-f', dockerfile_path, 'src/Build')
>>>>>>> 2fbe84b ([mod] noxfile for building interface-image)
=======
    # Take the input from build_docker.sh file pass it whilst building the image
    algorithm_name = session.posargs[1] 
=======
    # Read the Docker image name from the file
    with open('/tmp/docker_image_name.txt', 'r') as file:
        base_image = file.read().strip()
>>>>>>> 0763482 ([Update] Noxfile to dynamically set Base-Image to dockerfile)

    session.run('docker', 'build', '--build-arg',  f'BASE_IMAGE={base_image}', '-t', image_name, '-f', dockerfile_path, 'src/Build')

@nox.session
def install_gradio(session):
    """Install Gradio"""
    session.install('gradio')
>>>>>>> d7feedb ([Add] Cellpose's Gradio generation via CLI Usage)
