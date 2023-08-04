import mysql.connector
import os
from configs import logging, config_db
from script_parser import process_single_excel
from tqdm import tqdm


def get_employee_id_by_full_name(full_name, cursor):
    sql_query = "SELECT id FROM employee WHERE full_name = %s"
    cursor.execute(sql_query, (full_name,))
    result = cursor.fetchone()
    if result:
        employee_id = result[0]
        return employee_id
    else:
        return None


def execute_sql_script():
    try:
        conn = mysql.connector.connect(
            host=config_db.host,
            user=config_db.user,
            password=config_db.password
        )
        cursor = conn.cursor()
        with open('../schema.sql', 'r') as sql_file:
            sql_script = sql_file.read()
        for statement in sql_script.split(';'):
            if statement.strip():
                cursor.execute(statement)
        conn.commit()
        logging.info("База данных и таблицы успешно созданы.")
    except mysql.connector.Error as err:
        logging.error(f"Ошибка: {err}")
    finally:
        cursor.close()
        conn.close()
        logging.info("Соединение с базой данных закрыто.")


def delete_database_script():
    try:
        conn = mysql.connector.connect(
            host=config_db.host,
            user=config_db.user,
            password=config_db.password,
        )
        cursor = conn.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS {config_db.database}")
        conn.commit()
        logging.info("База данных и таблицы удаленны.")
    except mysql.connector.Error as err:
        logging.error(f"Ошибка: {err}")
    finally:
        cursor.close()
        conn.close()


def process_excel_files(excel_directory):
    sql_employee = """
                    INSERT IGNORE INTO employee (full_name)
                    VALUES (%s)
                    """
    sql_attendance = """
                    INSERT IGNORE INTO attendance 
                    (employee_id, work_date, arrival_time, departure_time, comment)
                    VALUES (%s, %s, %s, %s, %s)
                    """
    try:
        conn = mysql.connector.connect(
            host=config_db.host,
            user=config_db.user,
            password=config_db.password,
            database=config_db.database
        )
        cursor = conn.cursor()
        for filename in tqdm(os.listdir(excel_directory)):
            f = os.path.join(excel_directory, filename)
            if '.~lock.' in filename:
                continue
            if os.path.isfile(f):
                if not filename.endswith('.xlsx') and not filename.endswith('.xls'):
                    logging.debug(f"Файл {filename} пропущен, т.к. не является Exel файлом")
                    continue
            file_path = os.path.join(excel_directory, filename)

            datas = process_single_excel(file_path, cursor)
            if datas is None:
                continue
            datas, number = datas
            sql_query = "INSERT  INTO unique_file (number) VALUES (%s)"
            cursor.execute(sql_query, (number,))
            conn.commit()
            for employee, data in datas.items():
                cursor.execute(sql_employee, (employee,))
                conn.commit()
                employee_id = cursor.lastrowid
                if employee_id == 0:
                    employee_id = get_employee_id_by_full_name(employee, cursor)
                for work_date, arrival_time, departure_time, comment in data:
                    cursor.execute(
                        sql_attendance,
                        (
                            employee_id, work_date, arrival_time,
                            departure_time, comment
                        )
                    )
                    conn.commit()
    except mysql.connector.ProgrammingError as err:
        if err.errno == mysql.connector.errorcode.ER_SYNTAX_ERROR:
            logging.error(f"Ошибка: {err}")
        else:
            logging.error(f"Ошибка: Базы данных {config_db.database} не существует")
    except mysql.connector.Error as err:
        logging.error(f"Ошибка: {err}")
    finally:
        cursor.close()
        conn.close()
