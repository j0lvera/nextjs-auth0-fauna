"""Utils"""

import json

# from functools import wraps
import time
from datetime import datetime, timezone
from bottle import response
from faunadb import query as q
from faunadb.client import FaunaClient

from itsdangerous import URLSafeTimedSerializer
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
from authlib.oidc.core import CodeIDToken
from authlib.jose import jwt

from urllib.request import urlopen
from bottle import request
from . import AUTH0_DOMAIN
from . import faunadb_client


# Misc


def jsonify(*args, **kwargs):
    """Response helper"""
    if args and kwargs:
        raise TypeError("jsonify() behavior undefined when passed both args and kwargs")
    if len(args) == 1:
        data = args[0]
    else:
        data = args or kwargs

    if "status" in data:
        response.status = data["status"]
        # Remove element from response
        del data["status"]

    response.content_type = "application/json"
    return json.dumps(data)


# Auth


def get_pubkey(auth0_domain):
    """Get public key from a given Auth0 domain"""

    jsonurl = urlopen(f"{auth0_domain}/.well-known/jwks.json")
    print("jsonurl", jsonurl)
    jwks = json.loads(jsonurl.read())
    x5c = jwks["keys"][0]["x5c"][0]
    cert_str = f"-----BEGIN CERTIFICATE-----\n{x5c}\n-----END CERTIFICATE-----\n"
    cert_obj = load_pem_x509_certificate(cert_str.encode("utf-8"), default_backend())
    return cert_obj.public_key()


def decode_token(token):
    """Decodes and validates an auth0 token"""

    if token is None:
        raise Exception("Token is missing")

    public_key = get_pubkey(AUTH0_DOMAIN)
    claims_options = {
        "iss": {"essential": True, "values": [f"{AUTH0_DOMAIN}/"]},
        "sub": {"essential": False},
    }
    decoded = jwt.decode(
        token, public_key, claims_cls=CodeIDToken, claims_options=claims_options
    )
    decoded.validate()
    return decoded


# def requires_auth(func):
#     """Auth decorator"""

#     @wraps(func)
#     def decorated(*args, **kwargs):
#         # 1. get token from the header
#         token = request.get_cookie("token")

#         # 2. decode token
#         try:
#             decode_token(token)
#         # 3. catch exceptions
#         except InvalidClaimError as error:
#             print("Invalid claim error", error)
#             return jsonify(
#                 status_code=401,
#                 message={
#                     "code": "invalid_claims",
#                     "description": "Incorrect claims, please check the issuer",
#                 },
#             )
#         return func(*args, **kwargs)

#     return decorated


def get_token():
    """Get token from the cookie headers"""
    token = request.get_cookie("token")
    return decode_token(token)


def timestamp_sign(token: str, secret: str) -> str:
    """Signs token with a timestamp."""

    s = URLSafeTimedSerializer(secret)
    return s.dumps(token)


def timestamp_verify(signed_token: str, secret: str, max_age: int) -> str:
    """Validates signed token."""

    s = URLSafeTimedSerializer(secret)
    return s.loads(signed_token, max_age=max_age)


# https://pythonhosted.org/itsdangerous/#responding-to-failure
def timestamp_unsafe_load(payload: str, secret: str):
    """Loads unsafe decoded payload."""
    s = URLSafeTimedSerializer(secret)
    return s.load_payload(payload)


def delete_cookie(cookie_id="token"):
    """Destroy user's cookie."""
    response.set_cookie(
        cookie_id,
        "",
        httponly=True,
        path="/",
        expires=time.time() - (2 * 3600 * 24 * 365),
    )


# FaunaDB


def logout_user(token: str) -> bool:
    """Logs out user tokens."""

    client = FaunaClient(secret=token)
    return client.query(q.logout(True))


def find_ref(index: str, match_values: str) -> object:
    """Find user reference"""
    return q.select(["ref"], q.get(q.match(q.index(index), match_values)))


def faunadb_login(ref):
    """
    Creates an ABAC token from a given Auth0 user id or Faunadb reference object

    :param ref: FaunaDB ref object
    :return: FaunaDB query's result
    """

    return q.let(
        {
            "userToken": q.let(
                {"userRef": ref},
                q.do(q.create(q.tokens(), {"instance": q.var("userRef")})),
            )
        },
        q.do(q.select(["secret"], q.var("userToken"))),
    )


def faunadb_create_user(email: str, auth0_user_id: str) -> object:
    utc_now = datetime.now(timezone.utc)

    user_data = {
        "email": email,
        "auth0UserId": auth0_user_id,
        "createdBy": utc_now,
        "updatedBy": utc_now,
    }

    return q.create(q.collection("users"), {"data": user_data})


def user_login_or_signup(auth0_jwt: str) -> str:
    """
    Should use this function when the user has successfully logged in or signed
    up in Auth0.

    It will search for the user and return an ABAC token if its found, otherwise
    it will create a new user and then return an ABAC token.

    :param auth0_jwt: Auth0 JWT
    :return: An ABAC FaunaDB token
    """

    decoded = decode_token(auth0_jwt)
    email = decoded["email"]
    auth0_user_id = decoded["sub"].replace("auth0|", "")

    return faunadb_client.query(
        q.if_expr(
            # Conditional expression
            q.is_empty(q.match(q.index("users_by_auth0_id"), auth0_user_id)),
            # True
            q.let(
                {
                    "userRef": q.select(
                        ["ref"], faunadb_create_user(email, auth0_user_id)
                    )
                },
                q.do(faunadb_login(q.var("userRef"))),
            ),
            # False
            q.let(
                {"userRef": find_ref("users_by_auth0_id", auth0_user_id)},
                q.do(faunadb_login(q.var("userRef"))),
            ),
        )
    )
