from flask import Blueprint
import json

bulk_submissions_app = Blueprint("bulk_submissions", __name__)

@bulk_submissions_app.route("/bulk-submissions", methods=["GET"], strict_slashes=False)
def bulk_submissions():
    response = {
        'message': 'Voce tentou uploadr um monte!!',
        'status': 200
    }
    
    return json.dumps(response, default=str)
