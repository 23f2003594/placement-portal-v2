from flask import Flask
from database import init_db
from config import DB_PATH
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Placement portal is running DB at {}".format(DB_PATH)

if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        init_db()
    else:
        print("Database already exists at {}".format(DB_PATH))
    app.run(debug=True)
