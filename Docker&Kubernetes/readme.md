### Section 1: Core Concepts

## Q1.1

# What is a docker container and how is different from a virtual machine?

A docker container is a lightweight, isolated runtime environment that packages an application togheter with its dependancies, libraries and configuration so it can run accross different systems. Containers share the host operationg system's kernel but remain isolated from each other using Linux kernel features such as namespaces (network, process, filesystem) and cgroups (resources like CPU, memory, etc).

Unlike virtual machines, containers do not include a full operating system. Multiple containers share the host OS hernel while remaining isolated from each other. A VM is also requiring more resources and are much slower than containers.

As an annalogy: VMs are like different buildings, each with its own foundation, and containers are like apartments in the same building, they share the same foundation but are isolated units.


## Q1.2

# Match the Docker command to its function:

A. docker build -> build image from dockerfile
B. docker ps -> show running containers
C. docker run -> run a container

## Q1.3

# Name three reasons why Docker is useful in modern DevOps pipelines.

1. Docker is used in modern CI/CD pipelies to guarantee that the same code runs everywhere (own machine, development environment, production, etc). So it makes bugs reproductible and deployments predictible.
2. Docker images are versioned, immutable unit of deployments which means that the content of them does not change, it can be tagged, stored and deployed across environments and makes rollbacks simple and reliable
3. Docker enables fast automation and scalability because containers are lightweight, start in seconds and can be created or destroyed programatically with minimal overhead. this fast startup and teardown allows pipelines to execute stages in parallel and on demand, significantly reducing feedback time. Containers can be horizontally scaled easily by running multiple instances (very useful when using orchestration tools like Kubernetes). The CI/CD Pipelines become faster and easier to automate ent-to-end.

### Section 2: Dockerfile and Image building

## Q2.1 Coding

Given a Python app with app.py and requirements.txt, write a basic Dockerfile to build and 
run it.

![q21](Section2/images/q21.png)

docker run -p 8080:5000 --name container1 my-app:latest

Access in browser http://127.0.0.1:8080/

## Q2.2 Coding

Modify the above Dockerfile to use a multi-stage build with no pip/build tools in final image.

![q22](Section2/images/q22.png)

docker run -p 8080:5000 --name multi-stage multi-stage:latest

Access in browser http://127.0.0.1:8080/

## Q2.3 

# Explain how Docker layer caching works and how it helps with CI/CD pipelines.

Docker layer caching works by breaking the image build process into multiple steps, called layers and saving the result of each step. When CI/CD pipeline runs, Docker checks whether a layer can be reused or needs to be rebuild based on what has changes. If only the application code changes, Docker reuses each earliers layers such as the base image and installed dependancies and rebuilds only the final layers. This avoids repeating steps like downloading packages ot installing dependancies. As a result, image builds are much faster, fewer resources are used and CI/CD pipeline are more efficent and reliable.

In a Dockerfile each instruction creates a read-only layer. The order is very important for the building logic.


### Section 3: Docker Networking, Volumes, and Compose

## Q3.1

Write a docker-compose.yml file for a Python web app and a Redis container.

![q31](Section3/images/q31.png)

![q31](Section3/images/q31-containers.png)

## Q3.2

In what scenario would you use Docker Compose instead of running containers manually?

Docker Compose is ideal for defining and running multi-container applications. Instead of running services manually with complex `docker run` commands, you define the entire stack (containers, networks, volumes) in a single `docker-compose.yml` file. This ensures reproducibility across environments, simplifies orchestration (starting/stopping the whole stack with one command), and automatically handles networking between services.

## Q3.3 - Multiple Choice

Which of the following are benefits of using volumes in Docker?

A. Data persists after container deletion
B. Can be backed up
C. Consume less memory
D. Can be shared between containers

**Correct Answers: A, B, D**


### Section 4: Challenge

You are given a Node.js app that connects to PostgreSQL. Write a docker-compose.yaml and explain how to use .env for DB_USER, DB_PASS and DB_NAME. Add suggestive comments to understand the role of each component used in docker-compose.yaml.

# Note: View Docker compose file and .env file in Section4 folder
