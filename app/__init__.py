import logging

from config import Config
from flask import Flask
from flask_assets import Bundle, Environment
from flask_compress import Compress
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address, default_limits=["2 per second", "60 per minute"])
compress = Compress()
talisman = Talisman()
assets = Environment()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    assets.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    compress.init_app(app)
    csp = {
        "default-src": "'self'",
        "style-src": ["https://cdn.jsdelivr.net", "'self'"],
        "script-src": ["https://cdn.jsdelivr.net", "'self'"],
        "font-src": "https://cdn.jsdelivr.net",
        "img-src": [
            "https://cdn.jsdelivr.net",
            "https://*.tile.openstreetmap.org",
            "data:",
            "'self'",
        ],
    }
    talisman.init_app(
        app,
        content_security_policy=csp,
        content_security_policy_nonce_in=["script-src"],
    )

    js = Bundle("src/js/*.js", filters="jsmin", output="dist/js/custom-%(version)s.js")
    css = Bundle("src/css/*.css", filters="cssmin", output="dist/css/custom-%(version)s.css")
    if "js" not in assets:
        assets.register("js", js)
    if "css" not in assets:
        assets.register("css", css)

    # Register blueprints
    from app.main import bp as main_bp
    from app.thing import bp as thing_bp
    from app.point import bp as point_bp
    from app.line import bp as line_bp
    from app.polygon import bp as polygon_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(thing_bp, url_prefix="/things")
    app.register_blueprint(point_bp, url_prefix="/points")
    app.register_blueprint(line_bp, url_prefix="/lines")
    app.register_blueprint(polygon_bp, url_prefix="/polygons")

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Startup")

    return app
