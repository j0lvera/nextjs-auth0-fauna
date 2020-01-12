"""Users"""

from datetime import timezone, datetime
from itsdangerous import SignatureExpired
from bottle import request, response
from faunadb.client import FaunaClient
from faunadb import query as q
from .app import app, faunadb_client, SECRET
from .app.utils import jsonify, timestamp_verify, timestamp_unsafe_load, logout_user


@app.post("/api/users")
def create_user():
    """Creates user in the database"""
    json = request.json
    print("/api/users json", json)

    utcnow = datetime.now(timezone.utc)
    query = faunadb_client.query(
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

    print("response", query)
    return jsonify(status=201, message=f"User created")


@app.get("/api/users")
def get_profile():
    """Returns profile data from a request cookie"""

    try:
        signed_token = request.get_cookie("token")

        # Verify signature
        token = timestamp_verify(signed_token, SECRET, (60 * 5))

        # Initialize Fauna client
        client = FaunaClient(secret=token)
    except SignatureExpired as e:
        # Remove cookie from headers.
        response.delete_cookie("token", path="/")

        # Attempt to logout the expired ABAC token.
        encoded_payload = e.payload
        if encoded_payload:
            decoded_payload = timestamp_unsafe_load(encoded_payload, SECRET)
            logged_out = logout_user(decoded_payload)
            print("Signature expired. Trying to expire user tokens", logged_out)

        return jsonify(status_code=401, message="Session expired.")
    except Exception as e:  # pylint: disable=broad-except
        print(f"Error ocurred.", e)
        return jsonify(status_code=500)
    else:
        identity = client.query(q.if_(q.has_identity(), q.get(q.identity()), False))
        user = identity["data"]

        return jsonify(status_code=200, message={"user": user["email"]})
