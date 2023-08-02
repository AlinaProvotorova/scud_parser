import mysql.connector
import yaml
import logging

logging.basicConfig(
    filename='app.log', level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def read_config():
    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)
    return config


def execute_sql_script(config):
    try:
        conn = mysql.connector.connect(
            host=config['host'],
            user=config['username'],
            password=config['password'],
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
    config = read_config()

    execute_sql_script(config['database'])
