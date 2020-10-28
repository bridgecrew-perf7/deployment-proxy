import requests


def test_post_rollback(proxy_url):
    data = {"server_id": 1,
            "deployment_id": 1,
            "action": "UPDATE",
            "output": "deployment was successful",
            "hosts": ["my1.test.unifiedlayer.com", "my2.test.unifiedlayer.com","my3.test.unifiedlayer.com"],
            "yum_transaction_id": 1,
            "yum_rollback_id": 1}
    response = requests.post(proxy_url + '/rollback', json=data)
    print(response.text)
    assert response.status_code == 202