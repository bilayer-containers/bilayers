import nox
import os
import yaml

@nox.session
def run_parse(session):
    session.install('pyyaml')
    session.cd('src/Build/parse')
    config_path = session.posargs[0]
    session.run("python", "parse.py", config_path)
    session.cd('../../..')
    
@nox.session
def run_generate(session):
    session.install('pyyaml', 'jinja2')
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

    # Take the input from build_docker.sh file pass it whilst building the image
    algorithm_name = session.posargs[1] 

    session.run('docker', 'build', '--build-arg',  f'ALGORITHM_NAME={algorithm_name}', '-t', image_name, '-f', dockerfile_path, 'src/Build')

@nox.session
def install_gradio(session):
    """Install Gradio"""
    session.install('gradio')