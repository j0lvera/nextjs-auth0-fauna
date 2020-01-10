from .app import app


@app.get("/api")
def index():
    return "Hello, world"
