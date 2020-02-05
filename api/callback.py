"""Auth0 callback URL"""

from bottle import request, response, redirect
from faunadb.errors import NotFound
from .app import app, auth0, AUTH0_DOMAIN, APP_URL, SECRET
from .app.utils import (
    timestamp_sign,
    jsonify,
    user_login_or_signup,
)


@app.get("/api/callback")
def callback():
    """Add docstring later"""

    try:
        # Fetch Auth0 JWT token from Auth0's API
        token = auth0.fetch_access_token(
            f"{AUTH0_DOMAIN}/oauth/token",
            authorization_response=request.url,
            redirect_uri=f"{APP_URL}/api/callback",
        )

        # Generate a Fauna ABAC token from a given Auth0 JWT
        id_token = token["id_token"]
        secret = user_login_or_signup(id_token)
        print("secret from exchange", secret)

        # Timestamp the Fauna ABAC token
        signed_token = timestamp_sign(secret, SECRET)
        print("timestamped signed token", signed_token)
    except NotFound as e:
        print("User not found in FaunaDB.")
        return jsonify(status=404, message="User not found.")
    except Exception as e:
        print("something went wrong", e)
    else:
        response.set_cookie("token", signed_token, httponly=True, path="/")
        return redirect("/dashboard")
