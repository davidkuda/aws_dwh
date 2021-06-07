import os
import configparser


def parse_configs(config_file: str) -> dict:
    config = configparser.ConfigParser()
    config.read_file(open(config_file))
    sections = config.sections()
    configs = {}
    for section in sections:
        for item in config[section].items():
            k = item[0].upper()
            v = item[1]
            configs.update({k: v})
    return configs


def get_secrets():
    key = os.environ.get('CREDS__AWS_UDACITY__KEY')
    secret = os.environ.get('CREDS__AWS_UDACITY__SECRET')
    return {'KEY': key, 'SECRET': secret}