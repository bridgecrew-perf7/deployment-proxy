import requests

def test_post_versionlock(proxy_url):
    data = {"versionlock": ["","",""], "hostname": "my3.test.unifiedlayer.com", "port": "8003"}
    response = requests.post(proxy_url + '/versionlock', json=data)
    print(response.text)
    assert response.status_code == 201


def test_get_versionlock(proxy_url):
    response = requests.post(proxy_url + '/versionlock')
    print(response.text)
    assert response.status_code == 201