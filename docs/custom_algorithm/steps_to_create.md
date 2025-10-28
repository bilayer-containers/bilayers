---
title: Steps to create your custom algorithm's interface
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---


## 1. Fork bilayers repository
Go to [Bilayers GitHub Repo](https://github.com/bilayer-containers/bilayers/tree/main)
- Click the Fork button on top-right corner
- Clone your forked repository to your local system
```{code} bash
git clone https://github.com/your-username/bilayers.git
cd bilayers
```
- Set the original repository as your upstream
```{code} bash
git remote add upstream https://github.com/bilayer-containers/bilayers.git
```

### Install Pixi and start the dev environment

- Install Pixi (if not already installed). Example using pip:
```{code} bash
curl -fsSL https://pixi.sh/install.sh | sh
# wget if you don't have curl
wget -qO- https://pixi.sh/install.sh | sh
```

- Start the development shell:
```{code} bash
pixi shell -e dev
```

## 2. Add Your Algorithm Folder
- Open the project in VS Code
- Navigate to `src/bilayers/algorithms` and create a new folder for your algorithm
- **Naming convention:** Use `algorithm_inference` or `algorithm_training` based on the task 
- Add a `__init__.py` file to your folder
- Add a `config.yaml` file to your folder 

Use the provided skeleton as a starting point
:::{dropdown} config.yaml
:open:
```{code} yaml
citations:
  - name: ""
    doi: ""
    license: ""
    description: ""

docker_image:
  org:
  name:
  tag:
  platform:

algorithm_folder_name:

exec_function:
  name: "generate_cli_command"
  cli_command:
  hidden_args:

inputs:

outputs:

parameters:

display_only:
```
:::

- Refer to the [Understanding config.yaml](/understanding-config) for usage of each components
- Check the [Choosing a Base Docker Image guide](/right-base-docker-image) for algorithm docker image selection

## 3. Update CI/CD Configuration
- To enable automated interface generation and testing, update the following files:
  `scripts/build_docker.sh`: Edit your algorithm name to `line #7`:
  ```{code} bash
  ALGORITHM_NAMES=(“your_algorithm”)
  ```
  `scripts/validate.sh`: Edit your algorithm name to `line #6`:
  ```{code} bash
  ALGORITHM_NAMES=(“your_algorithm”)
  ```

## 4. Test on your end 
- Build and test your Docker images locally. 
  ```{code} bash
  ./scripts/build_docker.sh
  ```
- Push them to your personal DockerHub repository for validation:
  ```{code} bash
  docker build -t your-dockerhub-repo/your-algorithm:tag .
  ```
  ```{code} bash
  docker push your-dockerhub-repo/your-algorithm:tag
  ```
- Share your work with the community by submitting a pull request to Bilayers

## 5. Commit your changes
  ```{code} bash
  git add .
  ```
  ```{code} bash
  git commit -m "[Add] new algorithm: algorithm_name"
  ```
  ```{code} bash
  git push origin main
  ```

## 6. Submit a Pull request
- Open a PR to the main Bilayers repository. Provide a clear description of your algorithm and its usage

## 7. Review and Approval
- The Bilayers team will review your PR
- Upon approval:
    Your algorithm will be added to the main repository.
    Docker images will be published to the Bilayers DockerHub for community use
<!-- 
## Next Steps
For more details, check the Bilayers Contribution Guide or use the issue tracker for support -->