from flask import Blueprint, render_template, session, redirect, url_for, flash, make_response, request, send_file
import pandas as pd
import io
from datetime import datetime
from website.services.HR_report import get_data_for_report  # nếu anh tách ra riêng
import secrets
import jwt
from website.config import SECRET_KEY, ALGORITHM

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
    return render_template('home.html')  # Hiển thị trang home.html

@views.route('/login')
def login():
    return render_template('login.html')  # Hiển thị trang login.html

@views.route('/index')
def index():
    token = request.cookies.get('jwt_token')

    if not token:
        return redirect(url_for('views.login'))

    user_data = verify_jwt_token(token)
    if not user_data:
        # Nếu token không hợp lệ thì xóa cookie
        response = redirect(url_for('views.login'))
        response.set_cookie('jwt_token', '', expires=0)
        return response

    # Token hợp lệ → render trang
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

@views.route('/index/leave_request')
def leave_request():
    return render_template('leave_request.html')

#Generate HR Report-------------------------------

@views.route('/generate_report', methods=['POST'])
def generate_report():
    department = request.form.get('department')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    report_type = request.form.get('report_type', 'both')

    # 🔽 Lấy dữ liệu từ database theo phòng ban
    data = get_data_for_report(department)
    print(f"Data retrieved for department {department}: {data}")
    # Chuyển sang DataFrame
    df = pd.DataFrame(data)
    df['ngayvaolam'] = pd.to_datetime(df['ngayvaolam'])

    # 🔽 Lọc theo thời gian vào làm
    df_filtered = df[
        (df['ngayvaolam'] >= pd.to_datetime(start_date)) &
        (df['ngayvaolam'] <= pd.to_datetime(end_date))
    ]

    # Summary: chỉ thông tin chính
    df_summary = df_filtered[['manv', 'hoten', 'mapb', 'macv']]
    
    # Detailed: đầy đủ thông tin hợp đồng
    df_detailed = df_filtered[[
        'manv', 'hoten', 'mapb', 'macv', 'ngayvaolam',
        'ngayhieuluc', 'ngayhethan', 'luongcoban'
    ]]

    # Ghi vào file Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        if report_type == 'summary':
            df_summary.to_excel(writer, sheet_name='Summary Report', index=False)
        elif report_type == 'detailed':
            df_detailed.to_excel(writer, sheet_name='Detailed Report', index=False)
        else:
            df_summary.to_excel(writer, sheet_name='Summary Report', index=False)
            df_detailed.to_excel(writer, sheet_name='Detailed Report', index=False)

    output.seek(0)

    filename = f"HR_Report_{department}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    return send_file(
        output,
        download_name=filename,
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
