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

from winenv import configlib

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
    parser.set_defaults(func=main)


def main(args):
    config = configlib.load_config(args.config)
    print('unset WINEPREFIX')
    print('unset WINEARCH')
    print('export LANG={}'.format(config['DEFAULT']['lang']))
