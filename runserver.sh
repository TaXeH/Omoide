#!/bin/bash
source ./venv/bin/activate
gunicorn --workers=4 --bind :8080 omoide.application.app:app
