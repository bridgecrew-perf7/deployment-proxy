from flask import current_app as app


def get_healthcheck():
    app.logger.info("HealthCheck!")
    response = {"status": "success", "message": "proxy is healthy"}
    return response, 200
