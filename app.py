from flask import Flask, jsonify
import os

from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

APP_VERSION = "1.0.0"
APP_ENV = os.getenv("APP_ENV", "development")

REQUEST_COUNT = Counter(
    "system_health_requests_total",
    "Total number of requests handled by the System Health Dashboard"
)


@app.route("/health")
def health():
    REQUEST_COUNT.inc()

    return jsonify({
        "status": "UP"
    }), 200


@app.route("/version")
def version():
    REQUEST_COUNT.inc()

    return jsonify({
        "version": APP_VERSION
    }), 200


@app.route("/environment")
def environment():
    REQUEST_COUNT.inc()

    return jsonify({
        "environment": APP_ENV
    }), 200


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
