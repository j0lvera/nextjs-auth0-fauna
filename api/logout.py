"""Endpoint to logout user"""

import time
from bottle import response, redirect
from .app import app
from .app.utils import jsonify


@app.get("/api/logout")
def logout():
    """Logout user"""
    try:
        response.set_cookie(
            "token",
            "",
            httponly=True,
            path="/",
            expires=time.time() - (2 * 3600 * 24 * 365),
        )
    except Exception as e:  # pylint: disable=broad-except
        print(f"Error ocurred.", e)
        return jsonify(status_code=500)
    else:
        return redirect("/")
