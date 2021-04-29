import os


class Config(object):
    RATELIMIT_HEADERS_ENABLED = True
    RATELIMIT_STORAGE_URL = os.environ.get("REDIS_URL") or "memory://"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "your_secret_key_goes_here"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    THING_API_URL = os.environ.get("THING_API_URL") or "http://localhost:3000"
    THING_API_VERSION = os.environ.get("THING_API_VERSION") or "v1"
    TIMEOUT = os.environ.get("TIMEOUT") or 5
