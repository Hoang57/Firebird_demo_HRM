from flask import Blueprint, render_template, session, redirect, url_for, flash, make_response



views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')  # Hiển thị trang home.html

@views.route('/index')
def index():
    if 'user' not in session:
        flash('You need to log in first.')
        return redirect(url_for('auth.login'))
    
    response = make_response(render_template('index.html'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response




