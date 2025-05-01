import firebirdsql
import json
from datetime import date, datetime

# Hàm hỗ trợ chuyển đổi kiểu dữ liệu
def convert_values(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    return obj

# Kết nối đến CSDL
con = firebirdsql.connect(
    host='127.0.0.1',
    port=3050,
    database='/Users/nguyenviethoang/temp/HRM.fdb',
    user='SYSDBA',
    password='masterkey'
)

cur = con.cursor()
cur.execute("SELECT * FROM nhanvien")

# Lấy tên cột
columns = [desc[0] for desc in cur.description]

# Lấy dữ liệu và chuyển đổi thành dict
rows = [dict(zip(columns, [convert_values(value) for value in row])) for row in cur.fetchall()]

# Chuyển sang JSON
result_json = json.dumps(rows, ensure_ascii=False, indent=4)
print(result_json)

con.close()