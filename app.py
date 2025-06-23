from datetime import datetime
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from users import employee_login, submit_po
import logging
application = Flask(__name__)
CORS(application)


@application.route("/")
def home():
    return jsonify({"message": "Backend is running successfully!"})


###########################################################################
# Route to fetch all available API routes
@application.route("/api/routes", methods=["GET"])
def get_routes():
    return jsonify([str(rule) for rule in application.url_map.iter_rules()])
logging.basicConfig(level=logging.DEBUG)


#############################################################################################
#API Endpoint for the login post request 
@application.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("email")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user_data = employee_login(username, password)  # Check credentials

    if user_data:
        if username =="admin":
            return jsonify({"user": user_data, "message": "Admin login successful"}), 200
        else:
            return jsonify({"user": user_data, "message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

##################################################################################################################################

@application.route('/api/po_number', methods=['GET'])
def preview_po_number():
    preview_po = preview_po_number()
    return jsonify({"po_number": preview_po})

###################################################################################################################################

@application.route('/api/submit_po', methods=['POST'])
def call_submit_po():
    return submit_po()

####################################################################################################################################