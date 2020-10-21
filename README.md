Deployment-Proxy

A simple Flask / Celery app that coordinates requests from the deployment-api
to the deployment-clients, through secure environments.

Development Environment
copy the dev environment file from files
into .env or where ever you want to store your environment file 
(default: /etc/default/dproxy)
export ENV_FILE to load the environment file
(example: export ENV_FILE=".env")

make any edits that you need to make for your environment
(the secret key must match the secret key for the deployment-api)

copy configuration file from files/dproxy.conf to your config location
(default is /etc/deployment/dproxy.conf)
(example: export CONFIG_FILE=files/dproxy.conf)

make and edits that you need to make for your environment
the ENVIRONMENT variables with override the CONFIG variables if both are set.

Install pipenv if needed
(pip install pipenv)

Install Environment
(pipenv install)

Run Deployment-Proxy
(start_proxy.sh)

Run Celery
In another terminal
(start_celery.sh)
