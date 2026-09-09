from flask import Flask, jsonify
import os
import logging

app = Flask(__name__)

APP_VERSION = "1.0.0"
APP_ENV = os.getenv("APP_ENV", "development")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


@app.route("/health")
def health():
    logger.info("Health check requested")
    return jsonify({
        "status": "UP"
    }), 200


@app.route("/version")
def version():
    logger.info("Version endpoint requested")
    return jsonify({
        "version": APP_VERSION
    }), 200


@app.route("/environment")
def environment():
    logger.info("Environment endpoint requested")
    return jsonify({
        "environment": APP_ENV
    }), 200


if __name__ == "__main__":
    logger.info(
        "Starting System Health Dashboard - version=%s environment=%s",
        APP_VERSION,
        APP_ENV
    )
    app.run(host="0.0.0.0", port=5000)









