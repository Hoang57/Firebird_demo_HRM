import datetime
from website.database.database import connect

def get_leave_requests(keyword):
    try:
        con = connect()
        cur = con.cursor()
        
        if keyword:
            query = "SELECT * FROM nghiphep WHERE MANV LIKE ? OR MANP LIKE ?"
            like_keyword = f"%{keyword}%"
            cur.execute(query, (like_keyword, like_keyword))
        else:
            cur.execute("SELECT * FROM nghiphep")
            
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
            
def insert_leave_request(data):
    try:
        con = connect()
        cur = con.cursor()
        query = """INSERT INTO NGHIPHEP (MANV, LOAINGHIPHEP, NGAYBATDAU, NGAYKETTHUC, LYDO, NGAYGUIDON, NGUOIDUYET) 
                VALUES (?, ?, ?, ?, ?, ?, ?)"""
        
        values = (
            data.get("manv"),
            data.get("loainghiphep"),
            data.get("ngaybatdau"),
            data.get("ngayketthuc"),
            data.get("lydo"),
            data.get("ngayguidon"),
            data.get("nguoiduyet")
        )
        
        cur.execute(query, values)
        con.commit()
        cur.close()
        con.close()
        
        return True, None
    
    except Exception as e:
        print("Error:", e)
        return False, str(e)
    
def delete_leave_request(manv, startdate, enddate):
    try:
        con = connect()
        cur = con.cursor()
        
        query = "DELETE FROM NGHIPHEP WHERE MANV = ? AND NGAYBATDAU = ? AND NGAYKETTHUC = ?"
        cur.execute(query, (manv, startdate, enddate))
        con.commit()
        
        if cur. rowcount == 0:
            return False, "No leave request found with the provided details"
        
        
        return True, "Leave request deleted successfully"
    
    except Exception as e:
        print("Error:", e)
        return False, str(e)
    finally:
        cur.close()
        con.close()