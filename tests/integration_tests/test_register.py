import requests

def test_post_register_server(proxy_url):
    data = {"hostname": "my3.test.unifiedlayer.com",
            "ip": "3.9.112.22",
            "created_by": "twest_client",
            "state": "NEW",
            "group": "hp_testw",
            "environment": "alpha",
            "location": "test",
            "deployment_proxy": "dep.proxy",
            "url": "http://dep.api:8000/api/1.0.0"}
    response = requests.post(proxy_url + '/register', json=data)
    print(response.text)
    assert response.status_code == 201