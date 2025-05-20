from flask import Flask, Response, jsonify
from flask_cors import CORS
import datetime
from website.database.database import connect

def GetEmpolyeeService(keyword):
    try:
        con = connect()
        cur = con.cursor()

        if keyword:
            query = """
                SELECT * FROM nhanvien 
                WHERE HOTEN LIKE ? OR MANV LIKE ?
            """
            like_keyword = f"%{keyword}%"
            cur.execute(query, (like_keyword, like_keyword))
        else:
            cur.execute("SELECT * FROM nhanvien")

        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()

        result = []
        for row in rows:
            row_dict = {}
            for col, val in zip(columns, row):
                if isinstance(val, (datetime.date, datetime.datetime)):
                    row_dict[col] = val.isoformat()
                else:
                    row_dict[col] = val
            result.append(row_dict)

        cur.close()
        con.close()

        return result
    except Exception as e:
        print("Error:", e)
        return []

def insert_employee_to_db(employee_data):
    try:
        ngaysinh = employee_data.get("NGAYSINH")
        if ngaysinh:
            try:
                ngaysinh = datetime.date.fromisoformat(ngaysinh)
            except ValueError:
                return False, "NGAYSINH phải theo định dạng ISO (YYYY-MM-DD)"
        else:
            ngaysinh = None

        Start_date = datetime.date.today()

        con = connect()
        cur = con.cursor()

        query = """
            INSERT INTO nhanvien (HOTEN, NGAYSINH, GIOITINH, DIACHI, SODT, EMAIL, NGAYVAOLAM, MAPB, MACV)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        values = (
            employee_data.get("HOTEN"),
            employee_data.get("NGAYSINH"),
            employee_data.get("GIOITINH"),
            employee_data.get("DIACHI"),
            employee_data.get("SODT"),
            employee_data.get("EMAIL"),
            Start_date,
            employee_data.get("MAPB"),
            employee_data.get("MACV"),
        )

        cur.execute(query, values)
        con.commit()

        cur.close()
        con.close()
        return True, None

    except Exception as e:
        return False, str(e)
    
def update_employee_in_db(employee_data):
    try:
        conn = connect()
        cur = conn.cursor()
        
        sql = """
            UPDATE NHANVIEN
            SET HOTEN = ?, NGAYSINH = ?, GIOITINH = ?, DIACHI = ?, SODT = ?, EMAIL = ?, MAPB = ?, MACV = ?
            WHERE MANV = ?
        """
        
        params = (
            employee_data.get('HOTEN'),
            employee_data.get('NGAYSINH'),
            employee_data.get('GIOITINH'),
            employee_data.get('DIACHI'),
            employee_data.get('SODT'),
            employee_data.get('EMAIL'),
            employee_data.get('MAPB'),
            employee_data.get('MACV'),
            
        )
        cur.execute(sql, params)
        conn.commit()
        if cur.rowcount == 0:
                jsonify({"error": "Employee not found"}), 404

        return jsonify({"message": "updae employee successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()
    
    
def get_employee_by_id(employee_id):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM NHANVIEN WHERE MANV = ?", (employee_id,))
        row = cursor.fetchone()

        if row:
            columns = ["MANV", "HOTEN", "NGAYSINH", "GIOITINH", "DIACHI", "SODT", "EMAIL", "NGAYVAOLAM", "MAPB", "MACV", "ANHDAIDIEN", "TRANGTHAI"]
            employee = dict(zip(columns, row))
            return employee  # ✅ chỉ trả về dict
        else:
            return None
    except Exception as e:
        raise e

