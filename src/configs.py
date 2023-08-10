import argparse
import logging
from logging.handlers import RotatingFileHandler

import yaml

from constants import LOG_DIR, LOG_FILE, LOG_DATETIME_FORMAT, LOG_FORMAT


def get_config():
    with open("../etc/config.yaml", "r", encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file)
    return config


class ConfigDatabase:
    host: str = None
    user: str = None
    password: str = None
    database: str = None

    def __init__(self, config):
        self.host = config['database']['host']
        self.user = config['database']['username']
        self.password = config['database']['password']
        self.database = config['database']['database_name']


config_database = get_config()
config_db = ConfigDatabase(config_database)


def configure_argument_parser():
    parser = argparse.ArgumentParser(
        description=(
            'Скрипт для импорта данных о дисциплинах '
            'труда из файлов Excel в базу данных MySQL'
        )
    )
    subparsers = parser.add_subparsers(title='commands', dest='command')
    import_parser = subparsers.add_parser(
        'import', help='Импортировать данные из Excel'
    )
    import_parser.add_argument(
        'excel_directory',
        help='Путь к директории содержащей Excel файлы'
    )
    subparsers.add_parser('execute_db', help='Создание базы данных')
    subparsers.add_parser('delete_db', help='Удаление базы данных')
    return parser


def configure_logging():
    LOG_DIR.mkdir(exist_ok=True)
    rotating_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=10 ** 6, backupCount=5, encoding='utf-8'
    )
    logging.basicConfig(
        datefmt=LOG_DATETIME_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )
