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
        "style-src": "https://cdn.jsdelivr.net",
        "script-src": "https://cdn.jsdelivr.net",
        "img-src": ["data:", "'self'"],
    }
    talisman.init_app(app, content_security_policy=csp, content_security_policy_nonce_in=['style-src', 'script-src'])

    js = Bundle('src/js/*.js', filters='jsmin', output='dist/js/main-%(version)s.js')
    css = Bundle('src/css/*.css', filters='cssmin', output='dist/css/main-%(version)s.css')
    assets.register('js', js)
    assets.register('css', css)
    
    # Register blueprints
    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Startup")

    return app
