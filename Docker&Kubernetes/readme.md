### Section 1: Core Concepts

## Q1.1

What is a docker container and how is different from a virtual machine?

A docker container is an isolated environment that can be used on a virtual machine. The app that runs in the container has it's own dependencies different from what would normally be on a virtual machine. Is like spliting a virtual machines in more slices (each slice is a container), each slice is isolated from the others. 

## Q1.2

Match the Docker command to its function:

A. docker build -> build image from dockerfile
B. docker ps -> show running containers
C. docker run -> run a container

## Q1.3

Name three reasons why Docker is useful in modern DevOps pipelines.

1. Docker is used in modern CI/CD pipelies to guarantee that the same code runs everywhere (own machine, development environment, production, etc). So it makes bugs reproductible and deployments predictible.
2. Dokcer images are versioned, immutable unit of deployments which means that 


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

Explain how Docker layer caching works and how it helps with CI/CD pipelines.


### Section 3: Docker Networking, Volumes, and Compose

## Q3.1

Write a docker-compose.yml file for a Python web app and a Redis container.

![q31](Section3/images/q31.png)