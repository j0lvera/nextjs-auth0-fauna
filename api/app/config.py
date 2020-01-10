"""General configuration"""
import os

SECRET = os.getenv("SECRET")
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
SALT = os.getenv("SALT")
