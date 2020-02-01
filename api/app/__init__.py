"""
Module with everything related to the Bottle instance, configuration
and client instances.
"""

import os
from bottle import Bottle
from faunadb.client import FaunaClient
from authlib.client import OAuthClient, OAuth2Session

# Config

SECRET = os.getenv("SECRET")
SALT = os.getenv("SALT")
DEBUG = os.getenv("DEBUG")
APP_URL = os.getenv("APP_URL")

FAUNADB_SERVER_KEY = os.getenv("FAUNADB_SERVER_KEY")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")

# Database

faunadb_client = FaunaClient(secret=FAUNADB_SERVER_KEY)

# OAuth

auth0 = OAuth2Session(
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    scope="openid profile email",
)

app = Bottle()
debug = DEBUG
