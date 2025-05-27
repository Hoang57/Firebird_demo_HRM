from flask import jsonify, request, Response, Flask
import datetime
from website.database.database import connect

def get_section_service(keyword):
    try:
        conn = connect()
        cur = conn.cursor()
        
        if(keyword):
            query = query = """
                SELECT MAPB, TENPB FROM phongban 
                WHERE MAPB LIKE ? 
            """
            like_keyword = f"%{keyword}%"
            cur.execute(query, (like_keyword))
        else:
            cur.execute("SELECT * FROM phongban")
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
    
def insert_section_to_db(section_data):
    try:
        conn = connect()
        cur = conn.cursor()
        
        query = """
            INSERT INTO phongban
            VALUES (?, ?, ?)
        """
        values = (
            section_data.get("MAPB"),
            section_data.get("TENPB"),
            section_data.get("MOTA")
        )
        
        cur.execute(query, values)
        conn.commit()
        
        cur.close()
        conn.close()
        return True, None
        
    except Exception as e:
        print("Error:", e)
        return False, str(e)
    
def delete_section_from_db(mapb):
    try: 
        conn = connect()
        cur = conn.cursor()
        
        cur.execute("DELETE FROM phongban WHERE MAPB = ?", (mapb,))
        conn.commit()
        
        if cur.rowcount == 0:
            return False, "Section not found"
        
        return True, "Section deleted successfully"
    except Exception as e:
        return False, str(e)
    finally:
        cur.close()
        conn.close()