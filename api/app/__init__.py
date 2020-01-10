import os
from bottle import Bottle
from faunadb import query as q
from faunadb.client import FaunaClient
from authlib.client import OAuthClient, OAuth2Session

FAUNADB_SERVER_KEY = os.getenv("FAUNADB_SERVER_KEY")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
APP_URL = os.getenv("APP_URL")

# Database
faunadb_client = FaunaClient(secret=FAUNADB_SERVER_KEY)

# OAuth
auth0 = OAuth2Session(
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    scope="openid profile email",
)

app = Bottle()
debug = True
