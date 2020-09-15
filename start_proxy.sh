#!/usr/bin/env bash

pipenv run gunicorn -b 127.0.0.1:8002 --log-level=DEBUG --workers=2 --timeout=90 'dproxy.app:app'
