"""Users"""

from datetime import timezone, datetime
from bottle import request
from faunadb.client import FaunaClient
from faunadb import query as q
from .app import app, faunadb_client
from .app.utils import jsonify


@app.post("/api/users")
def create_user():
    """Creates user in the database"""
    json = request.json
    print("/api/users json", json)

    utcnow = datetime.now(timezone.utc)
    response = faunadb_client.query(
        q.create(
            q.collection("users"),
            {
                "data": {
                    "email": json["email"],
                    "auth0UserId": json["auth0UserId"],
                    "auth0Tenant": json["auth0Tenant"],
                    "createdBy": utcnow,
                    "updatedBy": utcnow,
                }
            },
        )
    )

    print("response", response)
    return jsonify(status=201, message=f"User created")


@app.get("/api/users")
def get_profile():
    """Returns profile data from a request cookie"""

    token = request.get_cookie("token")
    client = FaunaClient(secret=token)

    identity = client.query(q.if_(q.has_identity(), q.get(q.identity()), False))
    user = identity["data"]

    return jsonify(status_code=200, message={"user": user["email"]})
