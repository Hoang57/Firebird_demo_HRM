from flask import Blueprint, render_template, session, redirect, url_for, flash, make_response



views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')  # Hiển thị trang home.html

@views.route('/login')
def login():
    return render_template('login.html')  # Hiển thị trang login.html

@views.route('/index')
def index():
    if 'user' not in session:
        flash('You need to log in first.')
        return redirect(url_for('views.login'))
    
    response = make_response(render_template('index.html'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
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




