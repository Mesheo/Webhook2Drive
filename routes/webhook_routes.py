from flask import Blueprint, request, make_response, jsonify
from google_api.google_drive import drive_uploader
from data_conversion.json_converter import json2csv, format_data

webhook_app = Blueprint("webhook_app", __name__)

@webhook_app.route("/webhook/high_net_worth_individual", methods=["POST"])
def webhook(form_name):
    print("[Routes] - Recebido novas informações no formulário ", form_name)
    if not request.is_json:
        return make_response(jsonify(error='Invalid JSON'), 400)
    
    data = request.get_json()

    print("[Routes] - O que foi recebido na request: ", data)
    formatted_data = format_data(data, form_name)
    csv_file_path = json2csv(formatted_data)
    drive_uploader(form_name, csv_file_path)
    
    return jsonify(message=f'Webhook data received from {form_name} successfully. JSON data saved at GoogleDrive')















@webhook_app.route("/webhook/<form_name>", methods=["POST"])
def webhook(form_name):
    print("[Routes] - Recebido novas informações no formulário ", form_name)
    if not request.is_json:
        return make_response(jsonify(error='Invalid JSON'), 400)
    
    data = request.get_json()

    print("[Routes] - O que foi recebido na request: ", data)
    formatted_data = format_data(data, form_name)
    csv_file_path = json2csv(formatted_data)
    drive_uploader(form_name, csv_file_path)
    
    return jsonify(message=f'Webhook data received from {form_name} successfully. JSON data saved at GoogleDrive')
