import firebirdsql
# --------------Connect to the database-----------------
def connect():
    con = firebirdsql.connect(
        host='127.0.0.1',
        port=3050,
        database='/Users/nguyenviethoang/temp/HRM.fdb',
        user='SYSDBA',
        password='masterkey'
    )
    return con

#------------------------------------------------------

