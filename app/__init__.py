import logging

from flask import Flask
from flask_assets import Bundle, Environment
from flask_compress import Compress
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect

from config import Config

assets = Environment()
compress = Compress()
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address, default_limits=["2 per second", "60 per minute"])
talisman = Talisman()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True

    # Set content security policy
    csp = {
        "default-src": "'self'",
        "style-src": ["https://cdn.jsdelivr.net", "https://unpkg.com", "'self'"],
        "script-src": ["https://cdn.jsdelivr.net", "https://unpkg.com", "'self'"],
        "font-src": "https://cdn.jsdelivr.net",
        "img-src": [
            "https://cdn.jsdelivr.net",
            "https://*.tile.openstreetmap.org",
            "data:",
            "'self'",
        ],
    }

    # Initialise app extensions
    assets.init_app(app)
    compress.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    talisman.init_app(
        app,
        content_security_policy=csp,
        content_security_policy_nonce_in=["script-src"],
    )

    # Create static asset bundles
    css = Bundle("src/css/*.css", filters="cssmin", output="dist/css/custom-%(version)s.min.css")
    js = Bundle("src/js/*.js", filters="jsmin", output="dist/js/custom-%(version)s.min.js")
    if "css" not in assets:
        assets.register("css", css)
    if "js" not in assets:
        assets.register("js", js)

    # Register blueprints
    from app.main import bp as main_bp
    from app.point import bp as point_bp
    from app.thing import bp as thing_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(point_bp, url_prefix="/points")
    app.register_blueprint(thing_bp, url_prefix="/things")

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Startup")

    return app
