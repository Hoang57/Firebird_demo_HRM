from flask import Flask, Response, jsonify
from flask_cors import CORS
import datetime
from website.database.database import connect


def get_data_evaluation(keyword):
    try:
        con = connect()
        cur = con.cursor()
        
        if keyword:
            query = """
                SELECT manv, nguoidanhgia, ngaydanhgia, xeploai, nhanxet
                FROM danhgia
                WHERE manv LIKE ? OR nguoidanhgia LIKE ?
            """
            like_keyword = f"%{keyword}%"
            cur.execute(query, (like_keyword, like_keyword))
        else:
            cur.execute("SELECT manv, nguoidanhgia, ngaydanhgia, xeploai, nhanxet FROM danhgia")
        
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

