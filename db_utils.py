import mysql.connector

from utils import config, logging


def execute_sql_script():
    try:
        conn = mysql.connector.connect(
            host=config['database']['host'],
            user=config['database']['username'],
            password=config['database']['password'],
        )

        cursor = conn.cursor()

        with open('schema.sql', 'r') as sql_file:
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


if __name__ == "__main__":

    execute_sql_script()
