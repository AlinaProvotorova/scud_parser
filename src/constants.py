from pathlib import Path

BASE_DIR = Path(__file__).parent

LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'parser.log'
LOG_DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'

EXCEL_REGEX_DATE = r"\d{2}\.\d{2}\.\d{4}"
EXCEL_COLUMN_EMPLOYEE = 'Сотрудник'
EXCEL_COLUMN_ARRIVAL = 'Вход'
EXCEL_COLUMN_DEPARTURE = 'Выход'
EXCEL_REGEX_TIME = r"%H:%M"
EXEL_REGEX_DATE = r"%d.%m.%Y"
