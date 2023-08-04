import argparse
import yaml
import logging
from logging.handlers import RotatingFileHandler

from constants import LOG_DIR, LOG_FILE, DATETIME_FORMAT, LOG_FORMAT


def configure_argument_parser():
    parser = argparse.ArgumentParser(
        description=(
            'Скрипт для импорта данных о дисциплинах '
            'труда из файлов Excel в базу данных MySQL'
        )
    )
    subparsers = parser.add_subparsers(title='commands', dest='command')
    import_parser = subparsers.add_parser('import', help='Импортировать данные из Excel')
    import_parser.add_argument(
        'excel_directory',
        help='Путь к директории содержащей Excel файлы'
    )
    subparsers.add_parser('execute_db', help='Создание базы данных')
    return parser


def get_config():
    with open("../config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)
    return config


config = get_config()


def configure_logging():
    LOG_DIR.mkdir(exist_ok=True)
    rotating_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=10 ** 6, backupCount=5, encoding='utf-8'
    )
    logging.basicConfig(
        datefmt=DATETIME_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )
