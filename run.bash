#!/bin/bash
python generate-thumbs.py
export FLASK_APP=www
export FLASK_DEBUG=1
flask run --host=0.0.0.0 --port=8087