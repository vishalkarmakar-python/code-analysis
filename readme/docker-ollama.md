# Ollama Docker Setup and Usage Guide

This guide covers Ollama Docker image setup, container configuration, and essential commands for managing and interacting with language models locally using Ollama on Docker.

## Table of Contents

- [Ollama Docker Setup](#ollama-docker-setup)
  - [System Prerequisites](#system-prerequisites)
  - [Downloading the Ollama Docker Image](#downloading-the-ollama-docker-image)
  - [Initial Container Configuration and Launch](#initial-container-configuration-and-launch)
    - [Understanding the `docker run` Parameters](#understanding-the-docker-run-parameters)
- [Ollama Model Interaction & Management](#ollama-model-interaction--management)
  - [Running and Interacting with a Model](#running-and-interacting-with-a-model)
  - [Core Ollama and Docker Operations](#core-ollama-and-docker-operations)
- [Advanced Topics & Workflow](#advanced-topics--workflow)
  - [Accessing the Ollama API](#accessing-the-ollama-api)
  - [Running Ollama on CPU (Without GPU)](#running-ollama-on-cpu-without-gpu)
  - [Understanding Data Persistence (Volumes)](#understanding-data-persistence-volumes)
  - [Updating Ollama and Models](#updating-ollama-and-models)
- [Troubleshooting Common Issues](#troubleshooting-common-issues)
- [Further Information & Best Practices](#further-information--best-practices)

## Ollama Docker Setup

This section details the prerequisites and steps to get the Ollama server running in a Docker container.

### System Prerequisites

Before you begin, ensure you have the following:

1.  **Docker Installed:**
    - Docker must be installed and running on your system.
    - Download from the [official Docker website](https://docs.docker.com/get-docker/).
2.  **GPU for Acceleration (Recommended):**
    - An **NVIDIA GPU** is highly recommended for optimal performance with larger models.
    - Ensure **up-to-date NVIDIA drivers** are installed on your host system.
    - **NVIDIA Container Toolkit** (for Linux users): This must be installed to enable GPU access for Docker containers.
    - **Docker Desktop (Windows/macOS):** GPU support can usually be enabled through Docker Desktop's settings.
3.  **Sufficient System Resources:**
    - Adequate free **disk space** for the Ollama Docker image and downloaded language models (which can be several gigabytes each).
    - Sufficient **RAM** and **GPU VRAM** (especially for larger models).
4.  **Internet Connection:**
    - An active internet connection is required to download the Ollama Docker image and the language models.

### Downloading the Ollama Docker Image

This is the first step to get the necessary Ollama software.

1.  **Pull the Image**
    - Open your terminal or command prompt.
    - Execute the following command:
      ```bash
      docker pull ollama/ollama
      ```
    - **Explanation:** This command fetches the latest official `ollama/ollama` image from Docker Hub. This image contains the Ollama server application and command-line interface. You typically only need to do this once or when you want to update to a newer version of the Ollama image.

### Initial Container Configuration and Launch

Once the image is downloaded, you need to run it as a container with the appropriate configuration.

1.  **Run the Ollama Container**
    - Execute the following command in your terminal:
      ```bash
      docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
      ```
    - This command starts the Ollama server in a detached Docker container.

#### Understanding the `docker run` Parameters

Each flag in the `docker run` command plays a crucial role:

- **`-d` (Detached Mode):**
  - Runs the container in the background, allowing you to continue using your terminal.
  - The Ollama server will run as a background service.
- **`--gpus=all` (GPU Acceleration):**
  - Makes all available NVIDIA GPUs on your host system accessible to the container. This significantly speeds up model inference.
  - If you do not have an NVIDIA GPU or do not wish to use it, you can omit this flag (see [Running Ollama on CPU](#running-ollama-on-cpu-without-gpu)).
- **`-v ollama:/root/.ollama` (Volume Mounting for Persistence):**
  - Mounts a Docker named volume called `ollama` to the `/root/.ollama` directory inside the container.
  - **Importance:** Ollama stores downloaded models and its configuration in `/root/.ollama`. Using a named volume ensures that this data persists even if the container is stopped, removed, and recreated. Without this, you would lose all downloaded models when the container is removed.
- **`-p 11434:11434` (Port Mapping):**
  - Publishes port `11434` of the container to port `11434` on your host machine.
  - Ollama's API server listens on port `11434` by default. This mapping allows you (and other applications on your host) to communicate with the Ollama API.
- **`--name ollama` (Container Naming):**
  - Assigns a user-friendly name (`ollama`) to your container.
  - This makes it easier to refer to the container in subsequent Docker commands (e.g., `docker stop ollama`, `docker logs ollama`).
- **`ollama/ollama` (Image Name):**
  - Specifies the Docker image to use for creating the container (the one you pulled in the previous step). By default, this image is configured to start the `ollama serve` command.

## Ollama Model Interaction & Management

This section covers essential commands for interacting with models via Ollama and managing your Ollama Docker environment.

### Running and Interacting with a Model

After the Ollama server container is running, you can interact with language models.

1.  **Execute `ollama run` inside the container:**

    - Use the following command:
      ```bash
      docker exec -it ollama ollama run llama3.2:3b
      ```
    - **Note on Model Name:** The model tag `llama3.2:3b` is used here as per your specific request. Please verify that this exact model tag is available in the [Ollama Library](https://ollama.com/library). Common Llama 3 tags include `llama3:8b`, `llama3:70b`, and their instruct versions (e.g., `llama3:8b-instruct`). If `llama3.2:3b` is not found, you will need to replace it with a valid model tag.

2.  **Command Breakdown:**

    - `docker exec`: Executes a command inside an already **running container**.
    - `-it`: Allocates a **pseudo-TTY** (`-t`) and keeps **stdin open** (`-i`). This is crucial for an interactive session with the model.
    - `ollama`: The name of the running container (as specified by `--name ollama` in the `docker run` command).
    - `ollama run llama3.2:3b`: This is the Ollama CLI command to run the specified model.
      - If the model (`llama3.2:3b` in this case) is not already present in the `ollama` volume, Ollama will automatically download it first.
      - After the model is available, it will be loaded, and you'll enter an interactive chat session in your terminal.

3.  **Interacting:**
    - Once the model loads, you can type your prompts and press `Enter` to get responses.
    - To exit the interactive session, type `/bye` and press `Enter`, or use `Ctrl+D`.

### Core Ollama and Docker Operations

Here's a table of common commands for managing your Ollama setup:

| Category              | Operation                          | Command                                           | Description                                                                                                                                                                   |
| --------------------- | ---------------------------------- | ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Model Management**  | List downloaded models             | `docker exec ollama ollama list`                  | Shows all language models currently downloaded and available in your Ollama instance.                                                                                         |
|                       | Pull a new model                   | `docker exec ollama ollama pull <model_name:tag>` | Downloads a new model from the Ollama library (e.g., `docker exec ollama ollama pull mistral:latest`).                                                                        |
|                       | Remove a model                     | `docker exec ollama ollama rm <model_name:tag>`   | Deletes a downloaded model from your Ollama instance to free up space.                                                                                                        |
| **Container Ops**     | View container logs                | `docker logs ollama`                              | Displays the logs generated by the Ollama server running inside the container. Useful for troubleshooting.                                                                    |
|                       | Stop the container                 | `docker stop ollama`                              | Gracefully stops the running `ollama` container. The server will no longer be accessible.                                                                                     |
|                       | Start the container                | `docker start ollama`                             | Restarts a previously stopped `ollama` container.                                                                                                                             |
|                       | Remove the container               | `docker rm ollama`                                | Deletes the `ollama` container. **Note:** If you used the `-v ollama:/root/.ollama` volume, your models will NOT be deleted. If you didn't, container removal deletes models. |
|                       | View running containers            | `docker ps`                                       | Lists all currently running Docker containers.                                                                                                                                |
|                       | View all containers (inc. stopped) | `docker ps -a`                                    | Lists all Docker containers, including those that are stopped.                                                                                                                |
| **Volume Management** | Inspect volume                     | `docker volume inspect ollama`                    | Shows details about the `ollama` named volume, including its mount point on the host.                                                                                         |
|                       | List volumes                       | `docker volume ls`                                | Lists all Docker volumes on your system.                                                                                                                                      |
|                       | Remove volume (USE CAUTION!)       | `docker volume rm ollama`                         | **Deletes the `ollama` volume and all models stored within it.** Use only if you intend to remove all Ollama data. Ensure the container is stopped and removed first.         |

## Advanced Topics & Workflow

This section delves into more advanced usage patterns and configurations.

### Accessing the Ollama API

With the Ollama server running and port `11434` published, you can interact with its REST API directly from your host machine or other applications.

- **Example: List models using `curl`** (if `curl` is installed on your host):
  ```bash
  curl http://localhost:11434/api/tags
  ```
- **Example: Generate text with a model via API:**
  ```bash
  curl http://localhost:11434/api/generate -d '{
    "model": "llama3.2:3b", # Ensure this model is available
    "prompt": "Why is the sky blue?",
    "stream": false
  }'
  ```
  (Remember to replace `llama3.2:3b` with an available model if needed).
- The API can be used to integrate Ollama into your own applications, scripts, or custom frontends. Refer to the [Ollama API documentation](https://github.com/ollama/ollama/blob/main/docs/api.md) for more details.

### Running Ollama on CPU (Without GPU)

If you don't have an NVIDIA GPU or prefer to run on CPU, modify the `docker run` command by omitting the `--gpus=all` flag:

```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```
