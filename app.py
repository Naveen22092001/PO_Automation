from datetime import datetime
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from users import employee_login, generate_and_save_po_number, get_preview_po_number
import logging
application = Flask(__name__)
CORS(application)
client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
db = client["Timesheet"]
current_po_collection = db["Current_PO_Number"]

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

# @application.route('/api/preview_po_number', methods=['GET'])
# def preview_po_number():
#     preview_po = preview_po_number()
#     return jsonify({"po_number": preview_po})

# @application.route('/api/preview_po_number', methods=['GET', 'OPTIONS'])
# def preview_po_number():
#     if request.method == 'OPTIONS':
#         return '', 200  # Handle CORS preflight

#     try:
#         po_number = generate_po_number()
#         return jsonify({"po_number": po_number}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

##################################################################################
# @application.route("/api/preview_po_number", methods=["GET"])

# def preview_po_number():
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]
#     current_po_collection = db["Current_PO_Number"]
#     # Find the latest PO number document, exclude _id
#     try:
#         # Try to get the latest PO number document (no _id)
#         po_doc = current_po_collection.find_one({}, {"_id": 0})
#         if po_doc and "po_number" in po_doc:
#             return jsonify({"po_number": po_doc["po_number"]})
#         else:
#             return jsonify({"error": "Unable to generate PO number"}), 404
#     except Exception as e:
#         return jsonify({"error": "Unable to generate PO number"}), 500

# ###################################################################################################################################

# @application.route('/api/submit_po', methods=['POST'])
# def call_submit_po():
#     return submit_po()

####################################################################################################################################

# @application.route("/api/preview_po_number", methods=["GET"])
# def preview_po_number():
#     po_doc = current_po_collection.find_one()
#     if po_doc and "po_number" in po_doc:
#         return jsonify({"po_number": po_doc["po_number"]})
#     else:
#         return jsonify({"error": "Unable to generate PO number"}), 404


# @application.route("/api/submit_po", methods=["POST"])
# def submit_po():
#     try:
#         data = request.json
#         po_number = generate_po_number()
#         save_po_document(data, po_number)

#         return jsonify({
#             "message": "PO submitted successfully",
#             "po_number": po_number
#         })
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


############################################################################################################################

# @application.route("/api/preview_po_number", methods=["GET"])
# def preview_po_number():
#     po_doc = current_po_collection.find_one()
#     if po_doc and "po_number" in po_doc:
#         return jsonify({"po_number": po_doc["po_number"]})
#     else:
#         try:
#             new_po = generate_po_number()
#             return jsonify({"po_number": new_po})
#         except Exception as e:
#             return jsonify({"error": "Unable to generate PO number"}), 500


# @application.route("/api/submit_po", methods=["POST"])
# def submit_po():
#     data = request.json

#     # Get the currently generated PO number
#     po_doc = current_po_collection.find_one()
#     if not po_doc or "po_number" not in po_doc:
#         return jsonify({"error": "No PO number available"}), 400

#     current_po = po_doc["po_number"]

#     # Save the PO document
#     try:
#         save_po_document(data, current_po)
#         # Generate the next PO number for future preview
#         generate_po_number()
#         return jsonify({"message": "PO submitted successfully", "po_number": current_po})
#     except Exception as e:
#         return jsonify({"error": "Failed to submit PO"}), 500

###################################################################################################################################
@application.route("/api/preview_po_number", methods=["GET"])
def preview_po_number():
    try:
        po_number = get_preview_po_number()
        return jsonify({"po_number": po_number})
    except Exception as e:
        return jsonify({"error": "Unable to generate PO number"}), 500

@application.route("/api/submit_po", methods=["POST"])
def submit_po():
    try:
        data = request.json
        po_number = generate_and_save_po_number(data)
        return jsonify({"message": "PO submitted successfully", "po_number": po_number})
    except Exception as e:
        return jsonify({"error": "PO submission failed"}), 500