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
def proxy_hostname():
    proxy = 'deployment-proxy.unifiedlayer.com'
    return proxy

@pytest.fixture(scope="module")
def proxy_url(proxy_hostname):
    url = f"http://{proxy_hostname}:8002/api/v1"
    return url

@pytest.fixture(scope="module")
def secret_key():
    secret_key = "EnzHRohtbOd2KN3Z5VssLbG45FmlVQPLQAmJj7eFBHEPqwoHvX"
    return secret_key
