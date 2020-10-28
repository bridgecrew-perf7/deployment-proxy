import requests


def test_get_healthcheck(proxy_url):
    response = requests.get(proxy_url + '/')
    print(response.text)
    assert response.status_code == 200
