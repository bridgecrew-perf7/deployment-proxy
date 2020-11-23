import requests


def test_patch_server(proxy_url, secret_key):
    data = {
        "protocol": "http",
        "hostname": "my3.test.unifiedlayer.com",
        "ip": "3.9.112.22",
        "port": "8003",
        "version": "v1",
        "group_id": 1,
        "environment_id": 1,
        "created_by": "test_client",
        "state": "NEW",
    }
    valid_header = {"Authorization": secret_key}
    response = requests.patch(proxy_url + "/server", headers=valid_header, json=data)
    print(response.text)
    assert response.status_code == 201
