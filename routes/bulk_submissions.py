from flask import Blueprint, request, make_response, jsonify
import json
from google_api.google_drive import spread_sheet_operations
from data_conversion.json_converter import format_bulk_data


bulk_submissions_app = Blueprint("bulk_submissions", __name__)

@bulk_submissions_app.route("/bulk_submissions/<form_name>", methods=["POST"], strict_slashes=False)
def bulk_submissions(form_name):
    if not request.is_json:
        return make_response(jsonify(error='Invalid JSON'), 400)
    
    bulk_submissions = request.get_json()
    print("\n[BULK_SUBMISSIONS] - Olha como chegou: ", bulk_submissions)
    formatted_bulk_submissions = format_bulk_data(bulk_submissions, form_name)
    print("\n[BULK_SUBMISSIONS] - Olha como ficou: ", formatted_bulk_submissions)

    for formatted_submission in formatted_bulk_submissions:
        worksheet_data = spread_sheet_operations(formatted_submission, form_name)
        response = {
            'message': f'Bulk data received from {form_name} successfully. JSON data saved at Google Sheets',
            'data': worksheet_data,
            'status': 200
        }
    
    return json.dumps(response, default=str)
