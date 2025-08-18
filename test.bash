#!/bin/bash

docker build -t svenlatham/svenlatham-beer . && docker run -it -p 8087:8087 -v $(pwd):/app/ svenlatham/svenlatham-beer

