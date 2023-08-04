from pathlib import Path

BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / 'logs'

LOG_FILE = LOG_DIR / 'parser.log'

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'

