from flask import Blueprint, render_template, request, redirect, url_for, flash, session

auth = Blueprint('auth', __name__)

# -------------------------------
# 🔐 Authentication Routes
# -------------------------------



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == '123456':
            session['user'] = username
            return redirect(url_for('views.index'))  # views là tên Blueprint khác
        else:
            flash('Invalid username or password.')
            return redirect(url_for('auth.login'))

    return render_template('home.html')  # Trang login

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


