import logging
import os

from bcolors import bcolors

from little_conf import LittleConfig


class Config(LittleConfig):
    LOG_LEVEL: str = 'DEBUG'
    var1: int  # get from config file
    var2: str = ''

    class Config:
        yaml_conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '')
        extra = 'ignore'
        env_nested_delimiter = '__'


def on_conf_init(config):
    print(f'{bcolors.OKGREEN}###INIT CONFIG###{bcolors.ENDC}')
    print(f'set Log level {config.LOG_LEVEL}')

    logging.basicConfig(level=config.LOG_LEVEL, force=True)

    print(
        f'{bcolors.OKGREEN}Try kill -s HUP {os.getpid()} to reload config{bcolors.ENDC}'
    )


config = Config(on_init=on_conf_init)
