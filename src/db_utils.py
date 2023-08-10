import os

import mysql.connector
from tqdm import tqdm

from configs import logging, config_db
from script_parser import process_single_excel

CLOSE_DATABASE_LOG = "Соединение с базой данных закрыто."
ERROR_LOG = "Ошибка: {}"
ERROR_NO_DATABASE = "Ошибка: Базы данных {} не существует"
DEBUG_NOT_EXEL_FILE = "Файл {} пропущен, т.к. не является Exel файлом"
DATABASE_EXECUTE = "База данных и таблицы успешно созданы."
DATABASE_DELETE = "База данных и таблицы удаленны."


def get_employee_id_by_full_name(full_name, cursor):
    sql_query = "SELECT id FROM employee WHERE full_name = %s"
    cursor.execute(sql_query, (full_name,))
    result = cursor.fetchone()
    if result:
        employee_id = result[0]
        return employee_id


def execute_sql_script():
    try:
        conn = mysql.connector.connect(
            host=config_db.host,
            user=config_db.user,
            password=config_db.password
        )
        cursor = conn.cursor()
        with open('../database/schema.sql', 'r', encoding='utf-8') as sql_file:
            sql_script = sql_file.read()
        for statement in sql_script.split(';'):
            if statement.strip():
                cursor.execute(statement)
        conn.commit()
        logging.info(DATABASE_EXECUTE)
    except mysql.connector.Error as err:
        logging.error(ERROR_LOG.format(err))
    finally:
        cursor.close()
        conn.close()
        logging.info(CLOSE_DATABASE_LOG)


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
        logging.info(DATABASE_DELETE)
    except mysql.connector.Error as err:
        logging.error(ERROR_LOG.format(err))
    finally:
        cursor.close()
        conn.close()
        logging.info(CLOSE_DATABASE_LOG)


def process_excel_files(excel_directory):
    sql_set_employee = """
                    INSERT IGNORE INTO employee (full_name)
                    VALUES (%s)
                    """
    sql_set_attendance = """
                    INSERT IGNORE INTO attendance 
                    (employee_id, work_date, arrival_time, 
                    departure_time, comment)
                    VALUES (%s, %s, %s, %s, %s)
                    """
    sql_set_unique_number = "INSERT  INTO unique_file (number) VALUES (%s)"
    try:
        conn = mysql.connector.connect(
            host=config_db.host,
            user=config_db.user,
            password=config_db.password,
            database=config_db.database
        )
        cursor = conn.cursor()

        for filename in tqdm(os.listdir(excel_directory)):
            file_path = os.path.join(excel_directory, filename)
            if '.~lock.' not in filename and os.path.isfile(file_path):
                if not filename.endswith(('.xlsx', '.xls')):
                    logging.debug(DEBUG_NOT_EXEL_FILE.format(filename))
                    continue

                try:
                    dataset = process_single_excel(file_path, cursor)
                except ValueError as err:
                    logging.debug(err)
                    continue

                if dataset:
                    dataset, number = dataset
                    cursor.execute(sql_set_unique_number, (number,))
                    conn.commit()

                    for employee, data in dataset.items():
                        cursor.execute(sql_set_employee, (employee,))
                        conn.commit()

                        employee_id = cursor.lastrowid
                        if employee_id == 0:
                            employee_id = get_employee_id_by_full_name(
                                employee, cursor
                            )

                        for d in data:
                            cursor.execute(
                                sql_set_attendance, (employee_id, *d)
                            )
                            conn.commit()
    except mysql.connector.ProgrammingError as err:
        if err.errno == mysql.connector.errorcode.ER_SYNTAX_ERROR:
            logging.error(ERROR_LOG.format(err))
        else:
            logging.error(ERROR_NO_DATABASE.format(config_db.database))
    except mysql.connector.Error as err:
        logging.error(ERROR_LOG.format(err))
    finally:
        cursor.close()
        conn.close()
        logging.info(CLOSE_DATABASE_LOG)
