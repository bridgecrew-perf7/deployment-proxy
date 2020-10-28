FROM python:3.8.5-buster as base

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-deps

RUN pip install pipenv pytest

RUN apt-get update && apt-get install -y --no-install-recommends gcc python-dev \
    libsasl2-dev libldap2-dev libbz2-dev libffi-dev default-libmysqlclient-dev

COPY Pipfile .
COPY Pipfile.lock .

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base AS runtime

COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"


RUN mkdir -p /var/log/deployment/
RUN useradd --create-home deployment
RUN chown deployment /var/log/deployment/

WORKDIR /home/deployment
USER deployment

ENV PYTHONPATH="/home/deployment/dproxy"

COPY . /home/deployment

CMD ["./start_proxy.sh"]
