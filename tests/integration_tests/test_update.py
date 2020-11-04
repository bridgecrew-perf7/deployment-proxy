import requests


def test_post_update(proxy_url):
    data = {"hostname": "my3.test.unifiedlayer.com", "port": "8003", "api_version": "v1",
            "hosts": ["",""]}
    response = requests.post(proxy_url + '/update', json=data)
    print(response.text)
    assert response.status_code == 202