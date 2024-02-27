from flask import Flask

from routes.bulk_submissions_upload import bulk_submissions_app
from routes.webhook_routes import webhook_app

app = Flask(__name__)

app.register_blueprint(bulk_submissions_app)
app.register_blueprint(webhook_app)

@app.route("/")
def hello_from_root():
    return 'Hello from root!'

if __name__ == "__main__":
    app.run(debug=True)
