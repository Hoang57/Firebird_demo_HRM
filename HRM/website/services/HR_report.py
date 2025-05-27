from flask import Flask, Response, jsonify
from flask_cors import CORS
import datetime
from website.database.database import connect

def get_data_for_report(mapb):
    try:
        conn = connect()
        cur = conn.cursor()
        
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
            where nv.mapb = ?
        """
        like_keyword = f"%{mapb}%"
        cur.execute(query, (like_keyword,))  # ✅ Đóng gói tuple có 1 phần tử

        
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
        conn.close()    
        return result
    except Exception as e:
        print("Error:", e)
        return []
        
        