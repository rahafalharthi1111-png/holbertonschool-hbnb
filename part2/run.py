from flask import Flask
from app.api import api

app = Flask(__name__)
api.init_app(app)  # ربط الـNamespace مع Flask

if __name__ == "__main__":
    app.run(debug=True)
