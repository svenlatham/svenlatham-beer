#!/bin/bash
echo "Generating thumbs"
python generate-thumbs.py
export FLASK_APP=www
export FLASK_DEBUG=1
echo "Running Flask app"
flask run --host=0.0.0.0 --port=8087