from flask import Blueprint, request, redirect, url_for, jsonify, make_response
import json
from website.services.login import LoginService
from website.services.user import GetEmployeeService, insert_employee_to_db, update_employee_in_db, get_employee_by_id, delete_employee_from_db
from website.services.section import get_section_service, insert_section_to_db, delete_section_from_db
from website.services.leave import get_leave_requests, insert_leave_request, delete_leave_request
from website.services.Timkeeping import get_attendance_and_leave_data
from website.services.Contract import getContractService, insert_contract_to_db, delete_contract, update_contract, get_contract_by_id
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

#-----------------------------Employee Routes-------------------------------
@auth.route('/api/employee', methods=['GET'])
def api_employee():
    keyword = request.args.get('query', '').strip()
    employees = GetEmployeeService(keyword)
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

    data['MANV'] = manv  # đảm bảo có MANV

    success, message = update_employee_in_db(data)
    if success:
        return jsonify({"message": message}), 200
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
    
@auth.route('/api/delete_employee/<manv>', methods=['DELETE'])
def api_delete_employee(manv):
    if not manv:
        return jsonify({"error": "No employee ID provided"}), 400

    success, message = delete_employee_from_db(manv)  # Chỉ cần truyền mã nhân viên
    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"error": message}), 400

#-----------------------------Section Routes-------------------------------
@auth.route('/api/get_section', methods=['GET'])
def get_section():
    keyword = request.args.get('query', '').strip()
    sections = get_section_service(keyword)
    return jsonify(sections), 200

@auth.route('/api/insert_section', methods=['POST'])
def api_insert_section():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    success, message = insert_section_to_db(data)
    if success:
        return jsonify({"success": "Section inserted successfully"}), 201
    else:
        return jsonify({"error": message}), 400
    
@auth.route('/api/delete_section/<mapb>', methods=['DELETE'])
def api_delete_section(mapb):
    if not mapb:
        return jsonify({"error": "No section ID provided"}), 400

    success, message = delete_section_from_db(mapb)
    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"error": message}), 400
    
    
  #-----------------------------Leave Requests Routes-------------------------------  
@auth.route('/api/leave_requests', methods=['GET'])
def api_leave_requests():
    keyword = request.args.get('query', '').strip()
    leave_requests = get_leave_requests(keyword)
    return jsonify(leave_requests), 200

@auth.route('/api/insert_leave_request', methods=['POST'])
def api_insert_leave_request():
    data = request.get_json()
    print("Received data:", data)  # Debugging line to check the received data
    if not data:
        return jsonify({"error": "No data provided"}), 400

    success, message = insert_leave_request(data)
    if success:
        return jsonify({"message": "Leave request inserted successfully"}), 201
    else:
        return jsonify({"error": message}), 400
@auth.route('/api/delete_leave_request', methods=['DELETE'])
def api_delete_leave_request():
    data = request.get_json()
    if not data or not all(key in data for key in ('manv', 'startdate', 'enddate')):
        return jsonify({"error": "Invalid data provided"}), 400

    manv = data['manv']
    startdate = data['startdate']
    enddate = data['enddate']

    success, message = delete_leave_request(manv, startdate, enddate)
    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"error": message}), 400
    
#-----------------------------Attendance and Leave Data Routes-------------------------------
@auth.route('/api/attendance_and_leave', methods=['GET'])
def api_attendance_and_leave():
    query_date = request.args.get('date', '').strip() or None
    manv = request.args.get('manv', '').strip() or None

    if not query_date and not manv:
        return jsonify({"error": "Please provide at least one of 'date' or 'manv'."}), 400

    try:
        data = get_attendance_and_leave_data(query_date=query_date, manv=manv)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
#-----------------------------Contract Routes-------------------------------
@auth.route('/api/contract', methods=['GET'])
def api_contract():
    keyword = request.args.get('query', '').strip()
    contracts = getContractService(keyword)
    return jsonify(contracts), 200
@auth.route('/api/insert_contract', methods=['POST'])
def api_insert_contract():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    success, message = insert_contract_to_db(data)
    if success:
        return jsonify({"message": "Contract inserted successfully"}), 201
    else:
        return jsonify({"error": message}), 400
@auth.route('/api/delete_contract/<manv>', methods=['DELETE'])
def api_delete_contract(manv):
    if not manv:
        return jsonify({"error": "No employee ID provided"}), 400

    success, message = delete_contract(manv)
    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"error": message}), 400

@auth.route('/api/update_contract/<manv>', methods=['PUT'])
def api_update_contract(manv):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    data['MANV'] = manv
    success, message = update_contract(data)
    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"error": message}), 400
    

@auth.route('/api/get_contract', methods=['GET'])
def api_get_contract():
    manv = request.args.get("emp_id")  # Lấy tham số từ URL

    if not manv:
        return jsonify({"error": "No employee ID provided"}), 400

    try:
        contract = get_contract_by_id(manv)
        print("Retrieved contract:", contract)  # Debugging line to check the retrieved contract
        if contract:
            return jsonify(contract), 200
        else:
            return jsonify({"error": "Contract not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

