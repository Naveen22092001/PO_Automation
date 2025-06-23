from datetime import datetime
import logging
from flask import jsonify, request
from pymongo import MongoClient

def employee_login(emp_name, emp_password):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Employee_credentials"]
    user = collection.find_one({"Username": emp_name})
    if not user:
        return None

    username = user["Username"]
    password = user["Password"]
    if username == emp_name and password == emp_password:
        if username == "admin":
            return {"Username": username, "message": "Admin login successful"}
        else:
            return {"Username": username, "message": "Login successful"}
    else:
        return None
    

def generate_po_number():
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    po_counter_collection = db["monthly_po_tracker"]
    po_data_collection = db["Purchase_Orders"]
    today = datetime.now()
    full_date = today.strftime("%y%m%d")  # e.g., 250619
    month_key = today.strftime("%y%m")    # e.g., 2506

    # Get current month's record
    record = po_counter_collection.find_one({"month": month_key})

    if record:
        new_count = record["count"] + 1
        po_counter_collection.update_one({"month": month_key}, {"$set": {"count": new_count}})
    else:
        new_count = 1
        po_counter_collection.insert_one({"month": month_key, "count": new_count})

    # Generate PO number with 4-digit padding
    po_number = f"PO-{full_date}-{new_count:04d}" 

    return jsonify({"po_number": po_number})
