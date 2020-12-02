from werkzeug.exceptions import InternalServerError
from flask import Flask, request, render_template
from flask.logging import create_logger
from flask_cors import CORS, cross_origin
from schema import SchemaError
import json
from gps_engine.gps_engine import GpsEngine

app = Flask("")
cors = CORS(app)
logger = create_logger(app)


@app.errorhandler(InternalServerError)
@cross_origin()
def handle_500(e):
    original = getattr(e, "original_exception", None)

    if original is not None:
        app.logger.error("Uncaught Exception: %s", original)

    return "Something bad happened", 500


@app.route("/", methods=["POST"])
@cross_origin()
def execute_job():
    try:
        model = GpsEngine((request.get_json()))
        model.validate()
        model.save()
        return model.compute_output()
    except SchemaError as error:
        logger.warning(json.dumps(request.get_json()))
        return error, 400


@app.route("/<model_id>", methods=["GET"])
@cross_origin()
def display_map(model_id=None):
    model = GpsEngine.load(model_id)
    model.plot_map()
    with open("./output.html", "r") as f:
        return "\n".join(f.readlines())


@app.route("/datasets/_health", methods=["GET"])
@cross_origin()
def _health():
    return {"healthy": True}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
