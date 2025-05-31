import json
from datetime import date, datetime, timedelta, timezone
from website.database.database import connect
import jwt
import secrets
from website.config import SECRET_KEY, ALGORITHM
import bcrypt


def convert_values(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    return obj


from datetime import datetime, timedelta, timezone

def create_jwt_token(data, expires_in_minutes=30):
    # Đặt timezone Việt Nam là UTC+7
    VN_TIMEZONE = timezone(timedelta(hours=7))

    payload = data.copy()
    # Thời gian hiện tại ở múi giờ Việt Nam
    now_vn = datetime.now(VN_TIMEZONE)

    # Thời gian hết hạn token tính theo múi giờ Việt Nam
    payload['exp'] = now_vn + timedelta(minutes=expires_in_minutes)

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token



def LoginService(username, password):
    con = connect()
    if con is None:
        raise ConnectionError("Failed to connect to the database. Please kiểm tra lại kết nối.")

    cur = con.cursor()
    
    # Truy vấn chỉ theo username
    cur.execute("SELECT * FROM ACCOUNT WHERE USER_NAME = ?", (username,))
    row = cur.fetchone()

    if not row:
        con.close()
        return json.dumps({"error": "Invalid username or password."}, ensure_ascii=False)

    # Lấy các cột
    columns = [desc[0] for desc in cur.description]
    user_data = dict(zip(columns, [convert_values(value) for value in row]))
    con.close()

    # Lấy hashed password từ cơ sở dữ liệu
    hashed_password = user_data.get("PASSWORD")

    # So sánh mật khẩu nhập vào với mật khẩu đã băm
    if not bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
        return json.dumps({"error": "Invalid username or password."}, ensure_ascii=False)

    # Tạo JWT token nếu đúng mật khẩu
    token = create_jwt_token({
        "user_id": user_data.get("ID"),
        "username": user_data.get("USER_NAME"),
        "role": user_data.get("ACC_ROLE"),
        "section": user_data.get("ACC_SECTION")
    })

    return json.dumps({
        "token": token,
        "username": user_data.get("USER_NAME"),
        "role": user_data.get("ACC_ROLE"),
        "section": user_data.get("ACC_SECTION")
    }, ensure_ascii=False)
