#! /usr/bin/env python3

import logging
from time import sleep

logger = logging.getLogger(__name__)


def run():
    while True:

        logger.debug('debug log')
        sleep(1)
        logger.info('info log')

        print('-----------------------------')
        sleep(1)


if __name__ == '__main__':
    run()
