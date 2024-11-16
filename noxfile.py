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
        algorithm = 'threshold_inference'
    
    print("Building Algorithm Nox-File: ", algorithm)
    image_name = f'{algorithm}'
    print("Image Name: ", image_name)
    dockerfile_path = f'src/algorithms/{algorithm}/Dockerfile'
    config_file_path = f'src/algorithms/{algorithm}/config.yaml'

    # Start by checking the config file for DockerHub image details
    if os.path.exists(config_file_path):
        print(f'Checking config file at {config_file_path}')
        with open(config_file_path, 'r') as file:
            config = yaml.safe_load(file)
        
        org = config.get('docker_image', {}).get('org')
        name = config.get('docker_image', {}).get('name')
        tag = config.get('docker_image', {}).get('tag')
        docker_image_name = f'{org}/{name}:{tag}' if org and name and tag else None
        algorithm_folder_name = config.get('algorithm_folder_name', None)

        # Save the algorithm folder name in a file
        with open('/tmp/algorithm_folder_name.txt', 'w') as file:
            file.write(algorithm_folder_name)

        # Attempt to pull the image from DockerHub
        try:
            print(f'Trying to pull the Docker image: {docker_image_name}')
            session.run('docker', 'pull', "--platform", "linux/amd64", "bilayer/instanseg:1.0.2")
            print(f'Successfully pulled Docker image from DockerHub: {docker_image_name}')
            # Save the Docker image name in a file
            with open('/tmp/docker_image_name.txt', 'w') as file:
                file.write(docker_image_name)
        except Exception as e:
            print(f'Failed to pull Docker image from DockerHub. Error: {e}')
            # Proceed to build from Dockerfile if pull fails
            if os.path.exists(dockerfile_path):
                print("Pull failed; attempting to build locally from Dockerfile.")
                # session.run('docker', 'build', '-t', image_name, '-f', dockerfile_path, f'src/algorithms/{algorithm}')
                session.run('docker', 'buildx', "build", "--platform", "linux/amd64", '-t', image_name, '-f', dockerfile_path, f'src/algorithms/{algorithm}')
                # Save the locally built Docker image name in a file
                with open('/tmp/docker_image_name.txt', 'w') as file:
                    file.write(image_name)
            else:
                session.error(f'Neither Docker image on DockerHub nor Dockerfile found for {algorithm}')

    else:
        # If the config file does not exist, report an error
        session.error(f'Config file not found at {config_file_path}')

@nox.session
def build_interface(session):
    """Build the Gradio docker Image"""
    if len(session.posargs) > 0:
        interface = session.posargs[0]
        algorithm = session.posargs[1]
    else:
        interface = 'gradio'
    print("Building Interface Nox-File: ", interface)

    image_name = f'{algorithm}_{interface}_image'
    print("Image Name: ", image_name)

    dockerfile_path = f'src/build/dockerfiles/{interface.capitalize()}.Dockerfile'
    print("Dockerfile Path: ", dockerfile_path)

    # Read the Docker image name from the file
    with open('/tmp/docker_image_name.txt', 'r') as file:
        base_image = file.read().strip()

    with open('/tmp/algorithm_folder_name.txt', 'r') as file:
        algorithm_folder_name = file.read().strip()
        
    if interface == 'gradio':
        session.run('docker', 'buildx', 'build', '--platform', 'linux/amd64', '-f', 'Gradio.Dockerfile', '--build-arg',  f'BASE_IMAGE={base_image}', '--build-arg',  f'FOLDER_NAME={algorithm_folder_name}', '-t', image_name, '-f', dockerfile_path, 'src/build')
    elif interface == 'jupyter':
        session.run('docker', 'buildx', 'build', '--platform', 'linux/amd64', '-f', 'Jupyter.Dockerfile', '--build-arg',  f'BASE_IMAGE={base_image}', '--build-arg',  f'FOLDER_NAME={algorithm_folder_name}', '-t', image_name, '-f', dockerfile_path, 'src/build')

@nox.session
def install_gradio(session):
    """Install Gradio"""
    session.install('gradio')