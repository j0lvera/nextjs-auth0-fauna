"""Endpoint to logout user"""

from bottle import redirect
from .app import app, APP_URL
from .app.utils import jsonify, delete_cookie


@app.get("/api/logout")
def logout():
    """Logout user"""
    try:
        delete_cookie()
    except Exception as e:  # pylint: disable=broad-except
        print(f"Error ocurred.", e)
        return jsonify(status=500)
    else:
        return redirect(APP_URL)
