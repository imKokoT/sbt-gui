from .properties import *
from .menu_gui import MenuGUI
from logger import logger     # type: ignore
from runtime_data import rtd  # type: ignore
import re


def start_gui():
    logger.info(f'plugin "{PLUGIN_NAME}" {VERSION=}')
    if not RUN_WITH_ANY:
        p = [re.compile('^' + re.escape(v).replace('\\*', '.*') + '$') for v in SUPPORTS_VERSIONS]
        if not any(p.match(rtd['version']) for p in p): # type: ignore
            logger.error(f'unsupported tool version {rtd['version']}; supports versions: {SUPPORTS_VERSIONS}')
            exit(1)
    else:
        logger.warning(f'{RUN_WITH_ANY=}')

    app = MenuGUI()
    app.mainloop()


if __name__ == '__main__':
    print(f'{PLUGIN_NAME=}\n'
          f'{AUTHOR=}\n'
          f'{VERSION=}\n'
          f'{f'{DEBUG=}\n' if DEBUG else ''}'
          f'{f'{RUN_WITH_ANY=}\n' if RUN_WITH_ANY else ''}')
