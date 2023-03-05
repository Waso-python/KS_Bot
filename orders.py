import fdb, os
import datetime

FDB_HOST_DB=os.getenv('FDB_HOST_DB')
FDB_HOST_DB_NAME=os.getenv('FDB_HOST_DB_NAME')
FDB_USER_DB=os.getenv('FDB_USER_DB')
FDB_PASSWORD_DB=os.getenv('FDB_PASSWORD_DB')


def main_choice(text):
    text = text.replace('/', '')
    print(text)
    if text == 'за день':
        return find_orders_by_day()
    elif text.isdigit():
        print('запрос цифровой')
        res = find_orders_by_number(text)
        if res:
            print('Запрос по номеру заказа')
            return res
        else:
            print('Запрос по номеру телефона')
            return find_orders_by_phone(text)
    else:
        return find_orders_by_client_name(text)

def find_orders_by_client_name(name):
    con = fdb.connect(
        host=FDB_HOST_DB, database=FDB_HOST_DB_NAME,
        user=FDB_USER_DB, password=FDB_PASSWORD_DB, charset='utf-8'
      )

    cur = con.cursor()

    # Execute the SELECT statement:
    cur.execute(f"select \
    zakaz_view.cod_zakaz,\
    zakaz_view.date_zakaz,\
    zakaz_view.type_name,\
    zakaz_view.isp_fio,\
    zakaz_view.price,\
    zakaz_view.name,\
    zakaz_view.fio_name,\
    zakaz_view.client_telefon\
    from zakaz_view \
    where lower(zakaz_view.fio_name) like '%{name.lower()}%' and zakaz_view.zakaz_status not in (4,6)\
    order by zakaz_view.date_zakaz DESC")

    # Retrieve all rows as a sequence and print that sequence:
    result = cur.fetchall()
    result = list(map(lambda x: ['/' + str(x[0]),*x], result))
    con.close()
    if len(result) == 1:
        return get_detailed_order(result[0][1])
    else:
        if len(result) < 15:
            return f"Найдено {len(result)} заказов:\n" + "\n".join([str(order) for order in result])
        else:
            return f"Найдено {len(result)} заказов:\n" + "\nУточните запрос"

def find_orders_by_phone(phone):
    con = fdb.connect(
        host=FDB_HOST_DB, database=FDB_HOST_DB_NAME,
        user=FDB_USER_DB, password=FDB_PASSWORD_DB, charset='utf-8'
      )

    cur = con.cursor()

    # Execute the SELECT statement:
    cur.execute(f"select \
    zakaz_view.cod_zakaz,\
    zakaz_view.date_zakaz,\
    zakaz_view.type_name,\
    zakaz_view.isp_fio,\
    zakaz_view.price,\
    zakaz_view.name,\
    zakaz_view.fio_name,\
    zakaz_view.client_telefon\
	from zakaz_view \
    where zakaz_view.client_telefon like '%{phone}%'\
    order by zakaz_view.date_zakaz DESC")

    # Retrieve all rows as a sequence and print that sequence:
    result = cur.fetchall()
    con.close()
    if len(result) < 10:
        return f"Найдено {len(result)} заказов:\n" + "\n".join([str(order) for order in result])
    else:
        return f"Найдено {len(result)} заказов:\n" + "\nУточните запрос"

def find_orders_by_number(text):
    con = fdb.connect(
        host=FDB_HOST_DB, database=FDB_HOST_DB_NAME,
        user=FDB_USER_DB, password=FDB_PASSWORD_DB, charset='utf-8'
      )

    cur = con.cursor()

    # Execute the SELECT statement:
    cur.execute(f"select \
    zakaz_view.cod_zakaz,\
    zakaz_view.date_zakaz,\
    zakaz_view.type_name,\
    zakaz_view.isp_fio,\
    zakaz_view.price,\
    zakaz_view.name\
	from zakaz_view \
    where zakaz_view.cod_zakaz = {int(text)}")

    # Retrieve all rows as a sequence and print that sequence:
    result = cur.fetchall()
    con.close()
    if len(result) > 1:
        return f"Найдено {len(result)} заказов:\n" + "\n".join([str(order) for order in result])
    elif len(result) == 1:
        return get_detailed_order(text)
    else:
        return None

def get_detailed_order(text):
    con = fdb.connect(
        host=FDB_HOST_DB, database=FDB_HOST_DB_NAME,
        user=FDB_USER_DB, password=FDB_PASSWORD_DB, charset='utf-8'
      )

    cur = con.cursor()

    # Execute the SELECT statement:
    cur.execute(f"select \
    zakaz_view.cod_zakaz,\
    zakaz_view.date_zakaz,\
    zakaz_view.type_name,\
    zakaz_view.opisanie_zakaz,\
    zakaz_view.comment_isp_zakaz,\
    zakaz_view.isp_fio,\
    zakaz_view.price,\
    zakaz_view.name,\
    zakaz_view.fio_name,\
    zakaz_view.client_telefon\
	from zakaz_view \
    where zakaz_view.cod_zakaz = {int(text)}")
    

    # Retrieve all rows as a sequence and print that sequence:
    result = cur.fetchone()
    con.close()
    cod_zakaz = result[0]
    date_zakaz = result[1] 
    type_name = result[2] 
    opisanie_zakaz = result[3] 
    comment_isp_zakaz = result[4] 
    isp_fio = result[5] 
    price = result[6] 
    status = result[7]
    fio_name = result[8]
    client_telefon = result[9]
    
    if len(result) > 0:
        return f"Заказ №<b>{text}</b> :\n" + "\n".join([str(order) for order in result])

def find_orders_by_day():
    con = fdb.connect(
        host=FDB_HOST_DB, database=FDB_HOST_DB_NAME,
        user=FDB_USER_DB, password=FDB_PASSWORD_DB, charset='utf-8'
      )

    cur = con.cursor()
    today = datetime.date.today()
    formatted_date = today.strftime('%d.%m.%Y')
    # Execute the SELECT statement:
    cur.execute(f"select \
    zakaz_view.cod_zakaz,\
    zakaz_view.date_zakaz,\
    zakaz_view.type_name,\
    zakaz_view.isp_fio,\
    zakaz_view.price,\
    zakaz_view.name\
	from zakaz_view \
    where zakaz_view.date_zakaz = '{formatted_date}'")

    # Retrieve all rows as a sequence and print that sequence:
    result = cur.fetchall()
    result = list(map(lambda x: ['/' + str(x[0]),*x], result))
    con.close()
    return f"Найдено {len(result)} заказов:\n" + "\n".join([str(order) for order in result])

def find_unsend_sms():
    con = fdb.connect(
        host=FDB_HOST_DB, database=FDB_HOST_DB_NAME,
        user=FDB_USER_DB, password=FDB_PASSWORD_DB, charset='utf-8'
      )

    cur = con.cursor()

    # Execute the SELECT statement:
    cur.execute("select sms_call.sc_result, sms_call.sc_complete, zakaz.client_telefon, sms_call.sc_cod from sms_call inner join zakaz on (sms_call.sc_zakaz = zakaz.cod_zakaz) where sms_call.sc_complete = 1 and sms_call.sc_vid = 2")

    # Retrieve all rows as a sequence and print that sequence:
    result = cur.fetchall()
    con.close()
    return result