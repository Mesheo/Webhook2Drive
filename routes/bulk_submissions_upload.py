from flask import Blueprint
import json
from google_api.google_drive import spread_sheet_operations


bulk_submissions_app = Blueprint("bulk_submissions", __name__)

@bulk_submissions_app.route("/bulk-submissions", methods=["GET"], strict_slashes=False)
def bulk_submissions():
    values_list = spread_sheet_operations()
    response = {
        'message': values_list,
        'status': 200
    }
    
    return json.dumps(response, default=str)
