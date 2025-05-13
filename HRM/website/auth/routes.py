from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
import json
from website.services.login import LoginService

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
        return jsonify(result_data), 200
    else:
        return jsonify(result_data), 401

@auth.route('/auth/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))

@auth.route('/register')
def register():
    return "<p>Register Page</p>"

@auth.route('/profile')
def profile():
    return "<p>Profile Page</p>"

@auth.route('/settings')
def settings():
    return "<p>Settings Page</p>"


