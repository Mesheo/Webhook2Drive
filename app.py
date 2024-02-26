from flask import Flask, jsonify, make_response

from routes.bulk_submissions_upload import bulk_submissions_app
from routes.webhook_routes import webhook_app


app = Flask(__name__)

app.register_blueprint(bulk_submissions_app)
app.register_blueprint(webhook_app)

@app.route("/")
def hello_from_root():
    return jsonify(message=f'Hello from root!')

@app.route("/hello")
def hello():
    return jsonify(message='Hello from path!')

@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)

if __name__ == "__main__":
    app.run(debug=True)
