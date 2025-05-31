from flask import Flask, Response, jsonify
from flask_cors import CORS
import datetime
from website.database.database import connect
import bcrypt

def insert_account(account):
    try:
        conn = connect()
        cur = conn.cursor()
        
        raw_password = account.get("PASSWORD")
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
        
        query = """INSERT INTO ACCOUNT(USER_NAME, PASSWORD, ACC_ROLE, ACC_SECTION)
                    VALUES(?,?,?,?)"""
                    
        values =(
            account.get("USER_NAME"),
            hashed_password.decode('utf-8'),
            account.get("ACC_ROLE"),
            account.get("ACC_SECTION")
        )
        
        cur.execute(query, values)
        conn.commit()
        
        cur.close()
        conn.close()
        return True, None
    
    except Exception as e:
        return False, str(e)
