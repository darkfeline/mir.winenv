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

from mir.winenv import configlib
from mir.winenv import shells

HELP = 'Reset environment.'


def setup_parser(subparsers):
    parser = subparsers.add_parser(
        'reset',
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
    parser.set_defaults(func=main)


def main(args):
    config = configlib.load_config(args.config)
    shell = shells.SHELLS[args.shell]
    print(shell.command_separator.join((
        shell.unset_variable('WINEPREFIX'),
        shell.unset_variable('WINEARCH'),
        shell.export_variable('LANG', config['DEFAULT']['lang']),
    )))
