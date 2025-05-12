
import json
from datetime import date, datetime
from website.database.database import connect
# Hàm hỗ trợ chuyển đổi kiểu dữ liệu
def convert_values(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    return obj

def LoginService(username, password):
    con = connect()
    if con is None:
        raise ConnectionError("Failed to connect to the database. Please check the 'connect' function.")
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM ACCOUNT a WHERE user_name  = ? AND password = ?", (username, password))

    # Lấy tên cột
    columns = [desc[0] for desc in cur.description]

    # Lấy dữ liệu và chuyển đổi thành dict
    rows = [dict(zip(columns, [convert_values(value) for value in row])) for row in cur.fetchall()]

    # Chuyển sang JSON
    result_json = json.dumps(rows, ensure_ascii=False, indent=4)
    con.close()
    #print(result_json)
    return result_json

