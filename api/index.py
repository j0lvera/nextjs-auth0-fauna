"""Main endpoint"""

from .app import app


@app.get("/api")
def index():  # pylint: disable=missing-function-docstring

    return "Hello, world"
