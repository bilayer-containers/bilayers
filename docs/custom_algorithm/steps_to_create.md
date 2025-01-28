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
```{code} yaml
git clone https://github.com/your-username/bilayers.git
cd bilayers
```
- Set the original repository as your upstream
```{code} yaml
git remote add upstream https://github.com/bilayer-containers/bilayers.git
```

## 2. Add Your Algorithm Folder
- Open the project in VS Code
- Navigate to `src/algorithms` and create a new folder for your algorithm
- **Naming convention:** Use `algorithm_inference` or `algorithm_training` based on the task 
- Add a `__init__.py` file to your folder
- Add a `config.yaml` file to your folder 

Use the provided skeleton as a starting point
:::{dropdown} config.yaml
:open:
```{code} yaml
parameters:
 
display_only:
  
exec_function:
 name: "generate_cli_command"
 script:
 module:
 cli_command:
 hidden_args:

docker-image:
 org:
 name:
 tag:
 platform: 

algorithm_folder_name:

citations:
 Algorithm:
   - name: ""
     doi: xxxx
     description: ""
```
:::

- Refer to the [Understanding config.yaml](/understanding-config) for usage of each components
- Check the [Choosing a Base Docker Image guide](/right-base-docker-image) for algorithm docker image selection

## 3. Update CI/CD Configuration
- To enable automated interface generation and testing, update the following files:
  `scripts/build_docker.sh`: Edit your algorithm name to `line #7`:
  ```{code}
  ALGORITHM_NAMES=(“your_algorithm”)
  ```
  `scripts/validate.sh`: Edit your algorithm name to `line #6`:
  ```{code}
  ALGORITHM_NAMES=(“your_algorithm”)
  ```

## 4. Test on your end 
- Build and test your Docker images locally. 
  ```{code}
  ./scripts/build_docker.sh
  ```
- Push them to your personal DockerHub repository for validation:
  ```{code}
  docker build -t your-dockerhub-repo/your-algorithm:tag .
  ```
  ```{code}
  docker push your-dockerhub-repo/your-algorithm:tag
  ```
- Share your work with the community by submitting a pull request to Bilayers

## 5. Commit your changes
  ```{code}
  git add .
  ```
  ```{code}
  git commit -m "[Add] new algorithm: algorithm_name"
  ```
  ```{code}
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