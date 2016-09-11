# Copyright (C) 2016  Allen Li

# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import logging
import sys

from mir.winenv import configlib
from mir.winenv import shells

logger = logging.getLogger(__name__)

HELP = 'Load an environment.'


def setup_parser(subparsers):
    parser = subparsers.add_parser(
        'load',
        description=HELP,
        help=HELP,
    )
    parser.add_argument('--config',
                        default=configlib.CONFIG_PATH,
                        help='Configuration file to use.')
    parser.add_argument(
        '--shell',
        choices=shells.SHELLS,
        default=shells.DEFAULT_SHELL,
    )
    parser.add_argument('name', help='Name of environment')
    parser.set_defaults(func=main)


_CONFIG_VAR_MAP = [
    ('WINEPREFIX', 'prefix'),
    ('WINEARCH', 'arch'),
    ('LANG', 'lang'),
]


def load_vars(config_section):
    for var_name, config_name in _CONFIG_VAR_MAP:
        yield var_name, config_section[config_name]


def main(args):
    config = configlib.load_config(args.config)
    name = args.name
    if not config.has_section(name):
        logger.error("%s environment doesn't exist", name)
        sys.exit(1)
    shell = shells.SHELLS[args.shell]
    print(shell.command_separator.join((
        shell.export_variable(var, value)
        for var, value in load_vars(config[name])
    )))
