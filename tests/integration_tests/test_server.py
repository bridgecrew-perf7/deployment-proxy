import requests

def test_patch_server(proxy_url, secret_key):
    data = {"hostname": "my3.test.unifiedlayer.com",
            "ip": "3.9.112.22",
            "url": "http://hostname/api/1.0.0",
            "group_id": 1,
            "environment_id": 1,
            "created_by": "twest_client",
            "state": "NEW"}
    valid_header = {"Authorization": secret_key}
    response = requests.patch(proxy_url + '/server', headers=valid_header, json=data)
    print(response.text)
    assert response.status_code == 201



def test_post_server_history(proxy_url, secret_key, server_auth_cookie):
    data = {"server_id": 1,
            "deployment_id": 1,
            "action": "UPDATE",
            "output": "deployment was successful",
            "yum_transaction_id": 1,
            "yum_rollback_id": 1}
    valid_header = {"Authorization": secret_key}
    response = requests.post(proxy_url + '/server/history', headers=valid_header, json=data, cookies=server_auth_cookie)
    print(response.text)
    assert response.status_code == 201
