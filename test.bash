#!/bin/bash

# if podman is installed, use that, otherwise use docker
if command -v podman &> /dev/null
then
    echo "Using podman"
    # resisting aliases here in case we have variation in the config
    podman build -t svenlatham-beer . && podman run -it -p 8087:8087 -v .:/app/ localhost/svenlatham-beer
else
    echo "Using docker"
    docker build -t svenlatham/svenlatham-beer . && docker run -it -p 8087:8087 -v $(pwd):/app/ svenlatham/svenlatham-beer
fi
