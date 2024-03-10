from flask import Blueprint, request, make_response, jsonify
import json
from google_api.google_drive import spread_sheet_operations
from data_conversion.json_converter import format_data


webhook2sheets_app = Blueprint("webhook2sheets", __name__)

@webhook2sheets_app.route("/webhook/<form_name>", methods=["POST"], strict_slashes=False)
def bulk_submissions(form_name):

    if not request.is_json:
        return make_response(jsonify(error='Invalid JSON'), 400)
    
    data = request.get_json()
    
    formatted_data = format_data(data, form_name)

    worksheet_data = spread_sheet_operations(formatted_data, form_name)
    response = {
        'message': f'Webhook data received from {form_name} successfully. JSON data saved at Google Sheets',
        'data': worksheet_data,
        'status': 200
    }
    
    return json.dumps(response, default=str)
