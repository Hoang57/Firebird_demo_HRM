from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, make_response
import json
from website.services.login import LoginService
from website.services.user import GetEmpolyeeService, insert_employee_to_db, update_employee_in_db, get_employee_by_id
auth = Blueprint('auth', __name__)

# -------------------------------
# 🔐 Authentication Routes
# -------------------------------

@auth.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    result = LoginService(username, password)

    try:
        result_data = json.loads(result)
    except json.JSONDecodeError:
        return jsonify({"error": "Server error."}), 500

    if 'token' in result_data:
        token = result_data['token']
        response = make_response(jsonify(result_data), 200)
        response.set_cookie('jwt_token', token, httponly=True, max_age=3600)
        return response
    else:
        return jsonify(result_data), 401

@auth.route('/auth/logout')
def logout():
    response = make_response(redirect(url_for('views.login')))
    # Delete the jwt_token cookie by setting it with an immediate expiration time
    response.set_cookie('jwt_token', '', expires=0)
    return response

@auth.route('/register')
def register():
    return "<p>Register Page</p>"

@auth.route('/profile')
def profile():
    return "<p>Profile Page</p>"

@auth.route('/settings')
def settings():
    return "<p>Settings Page</p>"

@auth.route('/api/employee', methods=['GET'])
def api_employee():
    keyword = request.args.get('query', '').strip()
    employees = GetEmpolyeeService(keyword)
    return jsonify(employees), 200

@auth.route('/api/insert_employee', methods=['POST'])
def api_insert_employee():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    success, message = insert_employee_to_db(data)
    if success:
        return jsonify({"message": "Employee inserted successfully"}), 201
    else:
        return jsonify({"error": message}), 400
    
    
@auth.route('/api/update_employee/<manv>', methods=['PUT'])
def api_update_employee(manv):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    data['MANV'] = manv  # đảm bảo MANV được set vào data

    success, message = update_employee_in_db(data)
    if success:
        return jsonify({"message": "Employee updated successfully"}), 200
    else:
        return jsonify({"error": message}), 400

@auth.route('/api/get_emp', methods=['GET'])
def api_get_emp():
    emp_id = request.args.get('emp_id')
    if not emp_id:
        return jsonify({"error": "No employee ID provided"}), 400

    try:
        employee = get_employee_by_id(emp_id)
        if employee:
            return jsonify(employee), 200
        else:
            return jsonify({"error": "Employee not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
