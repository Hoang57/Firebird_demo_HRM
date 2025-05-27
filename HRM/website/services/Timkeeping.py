from flask import Flask, Response, jsonify
from flask_cors import CORS
import datetime
from website.database.database import connect

def get_attendance_and_leave_data(query_date=None, manv=None):
    try:
        con = connect()
        cur = con.cursor()

        conditions_chamcong = []
        conditions_nghiphep = []
        params = []

        # Xây dựng điều kiện cho bảng CHAMCONG
        if query_date:
            conditions_chamcong.append("NGAYCHAMCONG = ?")
            params.append(query_date)
        if manv:
            conditions_chamcong.append("MANV = ?")
            params.append(manv)

        chamcong_condition = " AND ".join(conditions_chamcong) if conditions_chamcong else "1=1"

        # Xây dựng điều kiện cho bảng NGHIPHEP
        if query_date:
            conditions_nghiphep.append("? >= NGAYBATDAU AND ? <= NGAYKETTHUC")
            params.extend([query_date, query_date])
        if manv:
            conditions_nghiphep.append("MANV = ?")
            params.append(manv)

        nghiphep_condition = " AND ".join(conditions_nghiphep) if conditions_nghiphep else "1=1"

        # Câu SQL tổng
        sql = f"""
            SELECT MANV, NGAYCHAMCONG, GIOVAO, GIORA, NULL AS STATUS, NULL AS NOTES
            FROM CHAMCONG
            WHERE {chamcong_condition}

            UNION

            SELECT MANV, NULL AS NGAYCHAMCONG, NULL AS GIOVAO, NULL AS GIORA, LOAINGHIPHEP AS STATUS, LYDO AS NOTES
            FROM NGHIPHEP
            WHERE {nghiphep_condition}
        """

        cur.execute(sql, tuple(params))

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
