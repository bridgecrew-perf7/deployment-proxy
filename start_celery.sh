#!/usr/bin/env bash

export PYTHONPATH="$PWD/dproxy"
pipenv run celery -A dproxy.app:runner worker -l DEBUG
