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

HELP = 'List environments.'


def setup_parser(subparsers):
    parser = subparsers.add_parser(
        'list',
        description=HELP,
        help=HELP,
    )
    parser.add_argument('--config',
                        default=configlib.CONFIG_PATH,
                        help='Configuration file to use.')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='List environment settings.')
    parser.set_defaults(func=main)

_KEYS = ['prefix', 'arch', 'lang']


def main(args):
    config = configlib.load_config(args.config)
    if args.verbose:
        sections = []
        for section in config.sections():
            lines = []
            lines.append(section)
            for key in _KEYS:
                lines.append('{}={}'.format(key, config[section][key]))
            sections.append('\n'.join(lines))
        print('\n\n'.join(sections))
    else:
        for section in config.sections():
            print(section)
