#!/bin/bash
# 1. Update package index
sudo apt-get update -y

# 2. Install Docker
sudo apt-get install -y docker.io

# 3. Start and Enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# 4. Allow the 'ubuntu' user to run docker commands without sudo
sudo usermod -aG docker ubuntu

# 5. (Optional) Run your container
# docker run -d -p 80:8080 your-image:latest