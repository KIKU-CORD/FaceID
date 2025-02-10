import psycopg2
from psycopg2.extensions import connection
from psycopg2.extras import DictCursor

def get_connection() -> connection:

    # 172.20.0.2 = Database Server

    url = "host=172.20.0.2 dbname=JEC-23CC user=ccuser password=Cnetuser"

    return psycopg2.connect(url)

def getAllValue(table: str):

    table = '"' + table + '"'

    with get_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur: # 結果を辞書型で取得
            cur.execute('select * from ' + table)
            data = cur.fetchall()
            return data

def getValue(target: str, table: str, check: str, checkid: str):

    table = '"' + table + '"'

    checkid = "'" + checkid + "'"

    with get_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur: # 結果を辞書型で取得
            cur.execute('select ' + target + ' from ' +  + table + ' where ' + check + ' = ' + checkid)
            data = cur.fetchall()
            return data
        
def addValue(table: str, add: str, addv: str, allv: str): #allv and allv format: test1,test2,test3,...

    table = '"' + table + '"'

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('insert into ' + table + ' (' + allv + ') values (' + addv + ')')
            conn.commit() # 値の追加を決定する
        
def updateValue(table: str, update: str, updatev: str, check: str, checkid: str):

    table = '"' + table + '"'

    checkid = "'" + checkid + "'"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('update ' + table + ' set ' + update + ' = ' + updatev + ' where ' + check + ' = ' + checkid)
            conn.commit() # 値の更新を決定する