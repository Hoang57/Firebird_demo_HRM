import json
from datetime import date, datetime, timedelta
from website.database.database import connect
import jwt
import secrets
from website.config import SECRET_KEY, ALGORITHM


def convert_values(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    return obj

def create_jwt_token(data, expires_in_minutes=5):
    payload = data.copy()
    payload['exp'] = datetime.utcnow() + timedelta(minutes=expires_in_minutes)
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def LoginService(username, password):
    con = connect()
    if con is None:
        raise ConnectionError("Failed to connect to the database. Please kiểm tra lại kết nối.")

    cur = con.cursor()
    cur.execute("SELECT * FROM ACCOUNT a WHERE user_name = ? AND password = ?", (username, password))

    columns = [desc[0] for desc in cur.description]
    rows = [dict(zip(columns, [convert_values(value) for value in row])) for row in cur.fetchall()]
    
    con.close()

    if not rows:
        # Trả JSON thông báo lỗi
        return json.dumps({"error": "Invalid username or password."}, ensure_ascii=False)

    user_data = rows[0]

    # Tạo JWT
    token = create_jwt_token({
        "user_id": user_data.get("id"),
        "username": user_data.get("user_name"),
        "role": user_data.get("role")
    })

    # Trả JSON chứa token
    return json.dumps({"token": token}, ensure_ascii=False)
