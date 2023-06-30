#!/bin/bash
# We're going to use this to build a local output in _build/
docker build -t svenlatham-beer . && docker run -p 8087:8087 -v .:/app/ localhost/svenlatham-beer
wget -r -nH -P "./_site/" "http://localhost:8087"
