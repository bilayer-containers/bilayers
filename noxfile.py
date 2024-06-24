import nox
import os

@nox.session
def run_parse(session):
    session.install('pyyaml')
    session.cd('src/Build/parse')
    config_path = session.posargs[0]
    session.run("python", "parse.py", config_path)
    session.cd('../../..')
    
@nox.session
def run_generate(session):
    session.install('pyyaml')
    session.cd('src/Build/parse')
    session.run('python', 'generate.py')
    session.cd('../../..')

@nox.session
def build_algorithm(session):
    """Build the Algorithm docker Image"""
    if len(session.posargs) > 0:
        algorithm = session.posargs[0] 
    else:
        algorithm = 'threshold'
    image_name = f'{algorithm}-image'
    dockerfile_path = f'src/Algorithms/{algorithm}/Dockerfile'

    # If Dockerfile doesn't exist for the specified algorithm
    if not os.path.exists(dockerfile_path):
        session.error(f'Dockerfile for {algorithm} not found at {dockerfile_path}')
    session.run('docker', 'build', '-t', image_name, '-f', dockerfile_path, f'src/Algorithms/{algorithm}')

@nox.session
def build_gradio(session):
    """Build the Gradio docker Image"""
    session.run('docker', 'build', '-t', 'gradio-image', '-f', 'src/build/Dockerfiles/Dockerfile', 'src/Build')