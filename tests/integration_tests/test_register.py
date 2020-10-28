import requests

def test_post_register_server(proxy_url):
    data = {"hostname": "my3.test.unifiedlayer.com",
            "ip": "3.9.112.22",
            "created_by": "twest_client",
            "state": "NEW",
            "group": "hp_testw",
            "environment": "alpha",
            "location": "test",
            "deployment_proxy": "deployment-proxy.unifiedlayer.com",
            "url": "http://deploument-api.unifiedlayer.com/api/1.0.0"}
    response = requests.post(proxy_url + '/register', json=data)
    print(response.text)
    assert response.status_code == 201