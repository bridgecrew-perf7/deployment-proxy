Deployment-Proxy

A simple Flask / Celery app that coordinates requests from the deployment-api
to the deployment-clients.

Development Environment
copy the dev environment file from the config directly into .env 
(in the base directory next to start_proxy.sh)

make any edits that you need to make for your environment
(the secret key must match the secret key for the deployment-api)

Install pipenv if needed
(pip install pipenv)

Install Environment
(pipenv install)

Run Deployment-Proxy
(start_proxy.sh)

Run Celery
In another terminal
(start_celery.sh)
