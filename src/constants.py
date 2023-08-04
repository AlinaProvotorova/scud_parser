from pathlib import Path

BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / 'logs'

LOG_FILE = LOG_DIR / 'parser.log'

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'

REGEX_DATE = r"\d{2}\.\d{2}\.\d{4}"

COLUMN_EMPLOYEE = 'Сотрудник'
COLUMN_ARRIVAL = 'Вход'
COLUMN_DEPARTURE = 'Выход'

TIME_FORMAT = r"%H:%M"
DATE_FORMAT = r"%d.%m.%Y"
