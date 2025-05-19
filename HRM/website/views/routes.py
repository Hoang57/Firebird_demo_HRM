from flask import Blueprint, render_template, session, redirect, url_for, flash, make_response, request

import jwt

SECRET_KEY = '123456'
ALGORITHM = 'HS256'

def verify_jwt_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')  
@views.route('/login')
def login():
    return render_template('login.html') 

@views.route('/index')
def index():
    token = request.cookies.get('jwt_token')
    if not token:
        return redirect(url_for('views.login'))

    user_data = verify_jwt_token(token)
    if not user_data:
        return redirect(url_for('views.login'))

    response = make_response(render_template('index.html', user=user_data))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


# -------------------------------
# 📊 HR Management Routes
# -------------------------------

@views.route('/index/employee')
def employee():
    return render_template('viewemployee.html')

@views.route('/index/department')
def department():
    return render_template('view_section.html')

@views.route('/index/timekeeping')
def timekeeping():
    return render_template('timekeeping.html')

@views.route('/index/contract')
def contract():
    return render_template('labor_contract.html')

@views.route('/index/employee_evaluation')
def employee_evaluation():
    return render_template('employee_evaluation.html')

@views.route('/index/HR_statistics')
def HR_statistics():
    return render_template('HR_statistics.html')




