import os


class Config(object):
    POINT_API_URL = os.environ.get("POINT_API_URL") or "http://localhost:3002/v1"
    RATELIMIT_HEADERS_ENABLED = True
    RATELIMIT_STORAGE_URL = os.environ.get("REDIS_URL") or "memory://"
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    THING_API_URL = os.environ.get("THING_API_URL") or "http://localhost:3001/v1"
    TIMEOUT = int(os.environ.get("TIMEOUT")) or 5
