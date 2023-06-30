#!/bin/bash

podman build -t svenlatham-beer . && podman run -it -p 8087:8087 -v .:/app/ localhost/svenlatham-beer