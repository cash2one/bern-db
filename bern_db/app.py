from flask import Flask, jsonify

from .users import user_datastore
from .api import v0
from .extensions import db, admin, limiter, security

DEFAULT_BLUEPRINTS = [
    v0,
]

def create_app(blueprints=None):
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(__name__)
    configure_app(app)
    configure_hooks(app)
    configure_blueprints(app, blueprints)
    configure_extensions(app)
    configure_error_handlers(app)

    return app

def configure_app(app):
    app.config.from_object("bern_db.config")

def configure_hooks(app):
    pass

def configure_blueprints(app, blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

def configure_extensions(app):
    db.init_app(app)

    limiter.init_app(app)

    admin.init_app(app)

    security.init_app(app, user_datastore)

    # Remove rate-limit from admin views
    for view in admin._views:
        limiter.exempt(view.blueprint)

def configure_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not Found"}), 404

    @app.errorhandler(429)
    def not_found(error):
        return jsonify({
            "error": "Too Many Requests",
            "description": error.description
        }), 429
