import nox
import os
import yaml

@nox.session
def run_parse(session):
    session.install('pyyaml')
    session.cd('src/build/parse')
    config_path = session.posargs[0]
    session.run("python", "parse.py", config_path)
    session.cd('../../..')
    
@nox.session
def run_generate(session):
    session.install('pyyaml','jinja2', 'nbformat', 'ipython', 'ipywidgets')
    session.cd('src/build/parse')
    config_path = session.posargs[0]
    session.run('python', 'generate.py', config_path)
    session.cd('../../..')

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
            org = config.get('docker_image', {}).get('org')
            name = config.get('docker_image', {}).get('name')
            tag = config.get('docker_image', {}).get('tag')
            docker_image_name = f'{org}/{name}:{tag}' if org and name and tag else None
            algorithm_folder_name = config.get('algorithm_folder_name', None)

            # Save the Docker image name in a file
            with open('/tmp/docker_image_name.txt', 'w') as file:
                file.write(docker_image_name)

            with open('/tmp/algorithm_folder_name.txt', 'w') as file:
                file.write(algorithm_folder_name)
                
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

    dockerfile_path = f'src/build/Dockerfiles/{interface.capitalize()}.Dockerfile'
    print("Dockerfile Path: ", dockerfile_path)

    # Read the Docker image name from the file
    with open('/tmp/docker_image_name.txt', 'r') as file:
        base_image = file.read().strip()

    with open('/tmp/algorithm_folder_name.txt', 'r') as file:
        algorithm_folder_name = file.read().strip()
        
    if interface == 'gradio':
        session.run('docker', 'build', '-f', 'Gradio.Dockerfile', '--build-arg',  f'BASE_IMAGE={base_image}', '--build-arg',  f'FOLDER_NAME={algorithm_folder_name}', '-t', image_name, '-f', dockerfile_path, 'src/build')
    elif interface == 'jupyter':
        session.run('docker', 'build', '-f', 'Jupyter.Dockerfile', '--build-arg',  f'BASE_IMAGE={base_image}', '--build-arg',  f'FOLDER_NAME={algorithm_folder_name}', '-t', image_name, '-f', dockerfile_path, 'src/build')

@nox.session
def install_gradio(session):
    """Install Gradio"""
    session.install('gradio')