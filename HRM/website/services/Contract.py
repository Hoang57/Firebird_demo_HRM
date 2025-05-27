from flask import Flask, Response, jsonify
from flask_cors import CORS
import datetime
from website.database.database import connect

def getContractService(keyword):
    try:
        con = connect()
        cur = con.cursor()

        if keyword:
            query = """
                SELECT * FROM hopdong 
                WHERE MANV LIKE ?
                """
            like_keyword = f"%{keyword}%"
            cur.execute(query, (like_keyword,))
        else:
            cur.execute("SELECT * FROM hopdong")
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

def insert_contract_to_db(contract_data):
    try:
        con = connect()
        cur = con.cursor()

        # Convert date strings to datetime.date objects
        start_date = contract_data.get("NGAYHIEULUC")
        end_date = contract_data.get("NGAYHETHAN")

        if start_date:
            start_date = datetime.date.fromisoformat(start_date)
        if end_date:
            end_date = datetime.date.fromisoformat(end_date)

        # Prepare SQL query with updated order of fields
        query = """
            INSERT INTO hopdong (MANV, LOAIHD, SOHD, MAHD, NGAYHIEULUC, NGAYHETHAN, LUONGCOBAN)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        # Execute the query
        cur.execute(query, (
            contract_data["MANV"],
            contract_data["LOAIHD"],
            contract_data["SOHD"],
            contract_data["MAHD"],
            start_date,
            end_date,
            contract_data["LUONGCOBAN"]
        ))

        con.commit()
        cur.close()
        con.close()

        return True, None
    except Exception as e:
        print("Error:", e)
        return False, str(e)
    
def delete_contract(manv):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM hopdong WHERE MANV = ?", (manv,))
        conn.commit()

        if cursor.rowcount == 0:
            return False, "Contract not found"

        return True, "Contract deleted successfully"

    except Exception as e:
        return False, str(e)

    finally:
        cursor.close()
        conn.close()
        
def get_contract_by_id(manv):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT MANV, LOAIHD, SOHD, MAHD, NGAYHIEULUC, NGAYHETHAN, LUONGCOBAN
            FROM hopdong 
            WHERE MANV = ?
        """, (manv,))
        row = cursor.fetchone()
        if row:
            columns = [desc[0] for desc in cursor.description]
            employee = dict(zip(columns, row))
            return employee
        else:
            return None

    except Exception as e:
        raise e

    
def update_contract(contract_data):
    try:
        conn = connect()
        cur = conn.cursor()
        
        sql = """
            UPDATE hopdong
            SET LOAIHD = ?, SOHD = ?, MAHD = ?, NGAYHIEULUC = ?, NGAYHETHAN = ?, LUONGCOBAN = ?
            WHERE MANV = ?
        """
        params = (
            contract_data.get('LOAIHD'),
            contract_data.get('SOHD'),
            contract_data.get('MAHD'),
            contract_data.get('NGAYHIEULUC'),
            contract_data.get('NGAYHETHAN'),
            contract_data.get('LUONGCOBAN'),
            contract_data.get('MANV')
        )
        cur.execute(sql, params)
        conn.commit()
        if cur.rowcount == 0:
            return False, "Contract not found"
        return True, "Contract updated successfully"
    except Exception as e:
        return False, str(e)
    finally:
        cur.close()
        conn.close()