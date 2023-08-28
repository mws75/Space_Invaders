# Use an Ubuntu base image
FROM ubuntu:latest

# Install required dependencies for Pygame
RUN apt-get update \
    && apt-get install -y python3-pip python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev

# Install Pygame
RUN pip3 install pygame

# Set the working directory
WORKDIR /app

# Copy your Pygame application files to the container
COPY . /app

# Set the display environment variable (required for GUI applications)
ENV DISPLAY=:0

# Run your Pygame application
CMD ["python3", "your_pygame_app.py"]
