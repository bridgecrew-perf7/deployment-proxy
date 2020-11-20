import requests


def test_post_register_server(proxy_url, proxy_hostname):
    data = {
        "hostname": "my3.test.unifiedlayer.com",
        "ip": "3.9.112.22",
        "port": "8003",
        "version": "v1",
        "protocol": "http",
        "created_by": "test_client",
        "state": "NEW",
        "group": "hp_test",
        "environment": "alpha",
        "location": "test",
        "deployment_proxy": proxy_hostname,
    }
    response = requests.post(proxy_url + "/register", json=data)
    print(response.text)
    assert response.status_code == 201
