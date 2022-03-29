import argparse
import json

import conlo

from ._config import Config
from ._creator import Creator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type=str, help='config file path')
    parser.add_argument('-d', '--debug', action='store_true', help='debug output')
    args = parser.parse_args()

    print(f'===========> loading config: {args.config}')
    config = Config()
    if args.config:
        config.load(args.config)
    else:
        config.input()
    print('loaded:')
    print(json.dumps(config.config, skipkeys=True, indent=4))

    print(f'===========> running creator')
    creator = Creator(config)
    creator.run()