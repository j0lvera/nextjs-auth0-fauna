"""Endpoint to redirect the user to Auth0 flow"""

from bottle import request, response, redirect
from .app import app, auth0, AUTH0_DOMAIN, APP_URL


@app.get("/api/auth")
def login():
    """Redirects user to Auth0 login/signup"""

    params = dict(request.query.decode())  # pylint: disable=no-member
    mode = params["mode"] if params else "signUp"

    redirect_uri = f"{APP_URL}/api/callback"
    url, state = auth0.create_authorization_url(
        f"{AUTH0_DOMAIN}/authorize", redirect_uri=redirect_uri, mode=mode
    )

    response.set_cookie("auth0:state", state, httponly=True)

    return redirect(url)
