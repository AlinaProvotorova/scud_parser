import yaml
import logging

with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

logging.basicConfig(
    filename='app.log', level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
