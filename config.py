import os


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "your_secret_key_goes_here"
    RATELIMIT_STORAGE_URL = os.environ.get("REDIS_URL") or "memory://"
    RATELIMIT_HEADERS_ENABLED = True
