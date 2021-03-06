# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
from environs import Env
import os

env = Env()
env.read_env()

ENV = env.str("FLASK_ENV", default="production")
DEBUG = ENV == "development"
SQLALCHEMY_DATABASE_URI = env.str("DATABASE_LOCAL_URL")
SQLALCHEMY_BINDS = {
    "localserver": env.str("DATABASE_LOCAL_URL"),
    "userserver": env.str("DATABASE_SERVER_URL")
}
SECRET_KEY = env.str("SECRET_KEY")
SEND_FILE_MAX_AGE_DEFAULT = env.int("SEND_FILE_MAX_AGE_DEFAULT")
BCRYPT_LOG_ROUNDS = env.int("BCRYPT_LOG_ROUNDS", default=13)
DEBUG_TB_ENABLED = DEBUG
DEBUG_TB_INTERCEPT_REDIRECTS = False
CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.
SQLALCHEMY_TRACK_MODIFICATIONS = False

CARRENT_URL = "http://127.0.0.1:5001"

REQUEST_HEADER = {
    "contentType": "application/json",
    "dataType": "json",
    "Connection": "keep-alive",
    "Accept": "*/*"
}