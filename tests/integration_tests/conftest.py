import pytest
import datetime
from dproxy.app import app as application

@pytest.fixture
def app():
    ctx = application.app_context()
    ctx.push()
    return application


@pytest.fixture
def app_context():
    return application.app_context()


@pytest.fixture(scope="module")
def proxy_url():
    url = 'http://localhost.localdomain:8002/api/1.0.0'
    return url


@pytest.fixture(scope="module")
def secret_key():
    secret_key = "EnzHRohtbOd2KN3Z5VssLbG45FmlVQPLQAmJj7eFBHEPqwoHvX"
    return secret_key