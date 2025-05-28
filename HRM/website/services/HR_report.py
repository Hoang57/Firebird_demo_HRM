from flask import Flask, Response, jsonify
from flask_cors import CORS
import datetime
from website.database.database import connect

def get_data_for_report(mapb, start_date, end_date):
    try:
        conn = connect()
        cur = conn.cursor()

        # Nếu mapb là 'all' hoặc None hoặc rỗng, không lọc theo mapb
        if mapb is None or mapb.lower() == 'all' or mapb == '':
            query = """
                SELECT 
                    nv.manv,
                    nv.hoten,
                    nv.mapb,
                    nv.macv,
                    nv.ngayvaolam,
                    c.ngayhieuluc,
                    c.ngayhethan,
                    c.luongcoban
                FROM nhanvien nv
                LEFT JOIN hopdong c ON nv.MANV = c.MANV
                WHERE nv.ngayvaolam BETWEEN ? AND ?
            """
            cur.execute(query, (start_date, end_date))
        else:
            query = """
                SELECT 
                    nv.manv,
                    nv.hoten,
                    nv.mapb,
                    nv.macv,
                    nv.ngayvaolam,
                    c.ngayhieuluc,
                    c.ngayhethan,
                    c.luongcoban
                FROM nhanvien nv
                LEFT JOIN hopdong c ON nv.MANV = c.MANV
                WHERE nv.mapb = ?
                  AND nv.ngayvaolam BETWEEN ? AND ?
            """
            cur.execute(query, (mapb, start_date, end_date))

        columns = [desc[0].lower() for desc in cur.description]
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
        conn.close()
        return result

    except Exception as e:
        print("Error:", e)
        return []

    
def get_section_data():
    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute("SELECT mapb FROM phongban")
        columns = [desc[0].lower() for desc in cur.description]
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
        conn.close()
        return result

    except Exception as e:
        print("Error:", e)
        return []

        