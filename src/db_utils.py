import mysql.connector
import os
from configs import config, logging
from script_parser import process_single_excel


def execute_sql_script():
    try:
        conn = mysql.connector.connect(
            host=config['database']['host'],
            user=config['database']['username'],
            password=config['database']['password'],
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
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            logging.info("Соединение с базой данных закрыто.")


def process_excel_files(excel_directory):
    conn = mysql.connector.connect(
        host=config['database']['host'],
        user=config['database']['username'],
        password=config['database']['password'],
        database=config['database']['database_name']
    )
    cursor = conn.cursor()

    for filename in os.listdir(excel_directory):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(excel_directory, filename)
            process_single_excel(file_path, cursor)

    conn.commit()
    cursor.close()
    conn.close()
