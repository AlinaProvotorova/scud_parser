import logging

from configs import configure_argument_parser, configure_logging
from db_utils import (
    process_excel_files, execute_sql_script, delete_database_script
)

START_LOG = 'Парсер запущен!'
ARGS_LOG = 'Аргументы командной строки: {}'
FINISH_LOG = 'Парсер завершил работу.'


def main():
    # try:
        configure_logging()
        logging.info(START_LOG)
        arg_parser = configure_argument_parser()
        args = arg_parser.parse_args()
        logging.info(ARGS_LOG.format(args))
        if args.command == 'execute_db':
            execute_sql_script()
        elif args.command == 'import':
            excel_directory = args.excel_directory
            process_excel_files(excel_directory)
        elif args.command == 'delete_db':
            delete_database_script()
        logging.info(FINISH_LOG)
    # except Exception as err:
    #     logging.error(f'Ошибка: {err}')


if __name__ == "__main__":
    main()
