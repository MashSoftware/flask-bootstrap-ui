from config import Config
from flask import Flask
from flask_compress import Compress
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address, default_limits=["2 per second", "60 per minute"])
compress = Compress()
talisman = Talisman()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    csrf.init_app(app)
    limiter.init_app(app)
    compress.init_app(app)
    csp = {
        "default-src": "'self'",
        "style-src": "cdn.jsdelivr.net",
        "script-src": "cdn.jsdelivr.net",
    }
    talisman.init_app(app, content_security_policy=csp)

    # Register blueprints
    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    return app
