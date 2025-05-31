from flask import Flask, Response, jsonify
from flask_cors import CORS
import datetime
from website.database.database import connect


def get_data_evaluation_by_user(keyword, section_id):
    try:
        con = connect()
        cur = con.cursor()
        
        if keyword:
            query = """
                SELECT d.manv, d.nguoidanhgia, d.ngaydanhgia, d.xeploai, d.nhanxet
                FROM danhgia d
                LEFT JOIN nhanvien n ON d.manv = n.manv
                WHERE (d.manv LIKE ? OR d.nguoidanhgia LIKE ?)
                AND n.mapb = ?
            """
            like_keyword = f"%{keyword}%"
            cur.execute(query, (like_keyword, like_keyword, section_id))
        else:
            query = """
                SELECT d.manv, d.nguoidanhgia, d.ngaydanhgia, d.xeploai, d.nhanxet
                FROM danhgia d
                LEFT JOIN nhanvien n ON d.manv = n.manv
                WHERE n.mapb = ?
            """
            cur.execute(query, (section_id,))
        
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
        return result  # ✅ KHÔNG ĐƯỢC THIẾU
    except Exception as e:
        print("Error:", e)
        return []
    
def get_data_evaluation_by_admin(keyword):
    try:
        con = connect()
        cur = con.cursor()
        
        if keyword:
            query = """
                SELECT d.manv, d.nguoidanhgia, d.ngaydanhgia, d.xeploai, d.nhanxet
                FROM danhgia d

                WHERE manv LIKE ? OR nguoidanhgia LIKE ?
            
            """
            like_keyword = f"%{keyword}%"
            cur.execute(query, (like_keyword, like_keyword))
        else:
            cur.execute("SELECT d.manv, d.nguoidanhgia, d.ngaydanhgia, d.xeploai, d.nhanxet FROM danhgia d")
        
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
        return result  # ✅ KHÔNG ĐƯỢC THIẾU
    except Exception as e:
        print("Error:", e)
        return []

def insert_evaluation(data):
    employee_id = data.get("MANV")
    reviewer_id = data.get("NGUOIDANHGIA")

    if not check_section(reviewer_id, employee_id):
        return False, "Người đánh giá và người được đánh giá phải thuộc cùng phòng ban."

    try:
        conn = connect()
        cur = conn.cursor()
        query = """INSERT INTO danhgia (MANV, NGUOIDANHGIA, NGAYDANHGIA, XEPLOAI, NHANXET)
                    VALUES (?, ?, ?, ?, ?)"""
        values = (
            employee_id,
            reviewer_id,
            data.get("NGAYDANHGIA"),
            data.get("XEPLOAI"),
            data.get("NHANXET"),
        )
        cur.execute(query, values)
        conn.commit()
        cur.close()
        conn.close()
        return True, None

    except Exception as e:
        return False, str(e)

    
def check_section(employee_id, reviewer_id):
    conn = connect()
    cur = conn.cursor()
    try:
        query = """
            SELECT a.ACC_SECTION, b.MAPB
            FROM ACCOUNT a
            JOIN nhanvien b ON 1=1
            WHERE a.user_name = ? AND b.manv = ?
        """
        cur.execute(query, (employee_id, reviewer_id))
        row = cur.fetchone()
        if row and row[0] == row[1]:
            return True
        return False
    finally:
        cur.close()
        conn.close()

        
    


