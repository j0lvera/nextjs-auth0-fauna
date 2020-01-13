"""Users"""

from datetime import timezone, datetime
from itsdangerous import SignatureExpired
from bottle import request
from faunadb.client import FaunaClient
from faunadb import query as q
from faunadb.errors import Unauthorized
from .app import app, faunadb_client, SECRET
from .app.utils import (
    jsonify,
    timestamp_verify,
    timestamp_unsafe_load,
    logout_user,
    delete_cookie,
)


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
    return jsonify(status=201, message="User created.")


@app.get("/api/users")
def get_profile():
    """Returns profile data from a request cookie"""

    try:
        signed_token = request.get_cookie("token")
        print("signed token in /api/users", signed_token)

        # Verify signature
        token = timestamp_verify(signed_token, SECRET, 300)  # (60*5) five minutes
        print("timestamp verified token in /api/users", token)

        # Initialize Fauna client
        client = FaunaClient(secret=token)
    except SignatureExpired as e:
        try:
            # Remove cookie from headers.
            delete_cookie()

            # Attempt to logout the expired ABAC token.
            encoded_payload = e.payload
            # if encoded_payload:
            decoded_payload = timestamp_unsafe_load(encoded_payload, SECRET)
            logged_out = logout_user(decoded_payload)
            print("Signature expired. Trying to expire user tokens", logged_out)
        except Unauthorized as e:
            print(
                "Could not logout ABAC token. Most likely the token is already invalid.",
                e,
            )
        except Exception as e:  # pylint: disable=broad-except
            print("Something went wrong.", e)
        return jsonify(status=401, message="Session expired.")
    except Exception as e:  # pylint: disable=broad-except
        print(f"Error ocurred.", e)
        return jsonify(status=500)
    else:
        identity = client.query(q.if_(q.has_identity(), q.get(q.identity()), False))
        user = identity["data"]

        return jsonify(status=200, user=user["email"])
