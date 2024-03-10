from flask import Blueprint, request, make_response, jsonify
import json
from google_api.google_drive import spread_sheet_operations
from data_conversion.json_converter import format_data


bulk_submissions_app = Blueprint("bulk_submissions", __name__)

@bulk_submissions_app.route("/bulk-submissions/<form_name>", methods=["POST"], strict_slashes=False)
def bulk_submissions(form_name):

    if not request.is_json:
        return make_response(jsonify(error='Invalid JSON'), 400)
    
    data = request.get_json()
    formatted_data = format_data(data, form_name)



    values_list = spread_sheet_operations(formatted_data, form_name)
    response = {
        'message': values_list,
        'status': 200
    }
    
    return json.dumps(response, default=str)
