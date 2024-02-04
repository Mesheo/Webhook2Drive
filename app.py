from flask import Flask, jsonify, make_response, request
from google_api.google_drive import drive_uploader
from data_conversion.json_converter import json2csv

app = Flask(__name__)

@app.route("/")
def hello_from_root():
    return jsonify(message=f'Hello from root!')

@app.route("/hello")
def hello():
    return jsonify(message='Hello from path!')

@app.route("/webhook/<form_name>", methods=["POST"])
def webhook(form_name):
    # Verifica se a requisição contém dados JSON
    if not request.is_json:
        return make_response(jsonify(error='Invalid JSON'), 400)
    
    data = request.get_json()
    csv_file_path = json2csv(data)
    drive_uploader(form_name, csv_file_path)
    
    return jsonify(message=f'Webhook data received from {form_name} successfully. JSON data saved at GoogleDrive')


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)

if __name__ == "__main__":
    app.run(debug=True)
