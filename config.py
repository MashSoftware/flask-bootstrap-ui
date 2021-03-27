import os


class Config(object):
    RATELIMIT_HEADERS_ENABLED = True
    RATELIMIT_STORAGE_URL = os.environ.get("REDIS_URL") or "memory://"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "your_secret_key_goes_here"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
