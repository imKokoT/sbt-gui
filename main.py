from .properties import *
from logger import logger     # type: ignore
from runtime_data import rtd  # type: ignore


def start_gui():
    logger.info(f'plugin "{PLUGIN_NAME}" {VERSION=}')
    if not RUN_WITH_ANY and rtd['version'] not in SUPPORTS_VERSIONS:
        logger.error(f'unsupported tool version {rtd['version']}; supports versions: {SUPPORTS_VERSIONS}')
        exit(1)
    if RUN_WITH_ANY:
        logger.warning(f'{RUN_WITH_ANY=}')


if __name__ == '__main__':
    print(f'{PLUGIN_NAME=}\n'
          f'{AUTHOR=}\n'
          f'{VERSION=}\n'
          f'{f'{DEBUG=}\n' if DEBUG else ''}'
          f'{f'{RUN_WITH_ANY=}\n' if RUN_WITH_ANY else ''}')
