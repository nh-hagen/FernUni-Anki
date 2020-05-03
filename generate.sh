#!/bin/sh

set -e

sudo docker run --rm -ti -v "$PWD:/anki" -u $UID python:3-alpine sh -c "pip install --prefix /tmp genanki && cd /anki && PYTHONUSERBASE=/tmp python generate.py"
