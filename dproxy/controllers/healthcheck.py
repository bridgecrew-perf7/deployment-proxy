def get_healthcheck():
    response = {"status": "success", "message": "proxy is healthy"}
    return response, 200
