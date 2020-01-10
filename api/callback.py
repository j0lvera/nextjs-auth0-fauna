"""Auth0 callback URL"""

from bottle import request, response, redirect
from .app import app, auth0, AUTH0_DOMAIN, APP_URL
from .app.utils import (
    # decode_token,
    exchange_jwt_for_secret,
    # generate_timed_signed_token,
)


@app.get("/api/callback")
def callback():
    """Add docstring later"""
    # params = dict(request.query.decode())
    # print("params", params)

    # Fetch token from Auth0 API
    token = auth0.fetch_access_token(
        f"{AUTH0_DOMAIN}/oauth/token",
        authorization_response=request.url,
        redirect_uri=f"{APP_URL}/api/callback",
    )

    id_token = token["id_token"]

    secret = exchange_jwt_for_secret(id_token)
    print("secret from exchange", secret)
    # timed_signed_token = generate_timed_signed_token(secret)
    # print("timed signed token", timed_signed_token)

    response.set_cookie("token", secret, httponly=True, path="/")
    # response.set_cookie("token", id_token, httponly=True, path="/")
    # response.set_cookie("token", timed_signed_token, httponly=True, path="/")
    return redirect("/dashboard")
