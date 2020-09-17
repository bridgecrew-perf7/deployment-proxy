from dproxy.config import Config

import datetime
from functools import wraps

from flask import request, jsonify
from authlib.jose import jwt


def server_token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """Require server authentication token"""
        server_token = request.headers.get("Authorization")
        if server_token:
            payload = decode_token(server_token)
            if "server" in payload["authorization"]["roles"]:
                return func(*args, **kwargs)
            else:
                response = {
                    "status": "failure",
                    "message": "server token is not valid",
                }
                return jsonify(response), 409
        else:
            response = {
                "status": "failure",
                "message": "please provide a valid server token"
            }
            return jsonify(response), 400
    return wrapper


def encode_server_token(server):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            "sub": server["hostname"],
            "aud": "deployment-api",
            "authorization": {
                "roles": ["server"]
            },
            "server_id": server["id"],
            "hostname": server["hostname"],
            "ip": server["ip"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1000, seconds=5),
            "iat": datetime.datetime.utcnow()
        }
        return jwt.encode({'alg': 'HS256'}, payload, Config.SECRET_KEY)
    except:
        return None


def decode_token(token):
    """
    Decodes the auth_token
    :param token:
    :return: integer|string
    """

    if token.startswith("Bearer "):
        token = token.replace("Bearer ", "")
    try:
        return jwt.decode(token, Config.SECRET_KEY)
    except:
        return None