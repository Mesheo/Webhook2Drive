from flask import Flask, jsonify, make_response, request
from drive_uploader import drive_uploader
from json_converter import json_converter

app = Flask(__name__)

@app.route("/")
def hello_from_root():
    return jsonify(message=f'Hello from root!')

@app.route("/hello")
def hello():
    return jsonify(message='Hello from path!')

@app.route("/webhook", methods=["POST"])
def webhook():
    # Verifica se a requisição contém dados JSON
    if not request.is_json:
        return make_response(jsonify(error='Invalid JSON'), 400)
    
    data = request.get_json()
    json_converter(data)
    drive_uploader()
    
    return jsonify(message=f'Webhook data received successfully. JSON data saved at GoogleDrive')


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)

if __name__ == "__main__":
    app.run(debug=True)
