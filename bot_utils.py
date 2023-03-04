import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
BOT_ID = os.getenv('BOT_ID')


DB_NAME=os.getenv('DB_NAME')
USER_DB=os.getenv('USER_DB')
PASSWORD_DB=os.getenv('PASSWORD_DB')
HOST_DB=os.getenv('HOST_DB')
PORT_DB=os.getenv('PORT_DB')

def get_product_from_db(text):
    con = psycopg2.connect(database=DB_NAME, user=USER_DB, password=PASSWORD_DB, host=HOST_DB, port=PORT_DB)
    cursor = con.cursor()
    text = text.replace(' ', '%')
    SQL = """select p.barcodes, p."name", p.vendor, ap.price, ap.qty ,
array_to_string(array(select i.url from images i where i.sku = p.sku), ', ') as images,
p.sku::text || p."name"::text as article,
p.sku
from products p 
right outer join active_products ap on p.sku = ap.sku
where LOWER(p.barcodes) like LOWER('%{text}%') or LOWER(p."name") like LOWER('%{text}%') or p.sku::text like '%{text}%'"""
    cursor.execute(SQL.format(text = text))
    row = cursor.fetchall()
    print(row)
    con.close()
    return row

