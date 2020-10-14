#!/usr/bin/env bash

pipenv run gunicorn -b 0.0.0.0:8002 --log-level=DEBUG --workers=1 --timeout=90 'dproxy.app:app'
