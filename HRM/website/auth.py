from flask import Blueprint
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash, session
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Kiểm tra thông tin đăng nhập
        if username == 'admin' and password == '123456':
            session['user'] = username
            # Lưu thông tin người dùng vào session
            return redirect(url_for('views.index'))  # Chuyển hướng đến index.html
        else:
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

    return render_template('home.html')  # Hiển thị trang login
    
@auth.route('/logout')
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