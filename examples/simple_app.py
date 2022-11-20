#! /usr/bin/env python3

import os

from bcolors import bcolors
from config import config


def run():
    print(f'{bcolors.OKGREEN}Config for local{bcolors.ENDC}')
    print(config)

    os.environ['service_env'] = 'prod'  # set prod environment
    config.reload()
    print(f'{bcolors.OKGREEN}Config for prod{bcolors.ENDC}')
    print(config)


if __name__ == '__main__':
    run()
