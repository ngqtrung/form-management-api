from flask import Flask, request
from flask_cors import CORS

from app.bases.api.factory import install_resources
from app.bases.api.openapi import register_docs
from app.common.utils import log
from app.errors import register_error_handlers
from app.extensions import db


def create_app(config_object="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    CORS(app, origins=app.config["CORS_ORIGINS"])

    register_error_handlers(app)
    install_resources(app)
    register_docs(app)

    @app.after_request
    def log_request(response):
        log.info(f"{request.method} {request.path} -> {response.status_code}")
        return response

    return app
