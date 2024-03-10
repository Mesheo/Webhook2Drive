from flask import Flask

from routes.webhook2sheets import webhook2sheets_app
from routes.bulk_submissions import bulk_submissions_app

app = Flask(__name__)

app.register_blueprint(webhook2sheets_app)
app.register_blueprint(bulk_submissions_app)

@app.route("/")
def hello_from_root():
    return 'Hello from root!'

if __name__ == "__main__":
    app.run(debug=True)
