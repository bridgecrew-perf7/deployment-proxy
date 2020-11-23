import requests


def test_get_versionlock(proxy_url):
    response = requests.get(proxy_url + "/versionlock/http/deployment-client.com/8003")
    print(response.text)
    assert response.status_code == 201
