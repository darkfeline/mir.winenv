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

HELP = 'Add an environment.'


def setup_parser(subparsers):
    parser = subparsers.add_parser(
        'add',
        description=HELP,
        help=HELP,
    )
    parser.add_argument('--config',
                        default=configlib.CONFIG_PATH,
                        help='Configuration file to use.')
    parser.add_argument('name', help='Name of environment')
    parser.add_argument('-p', '--prefix', help='Wine prefix path')
    parser.add_argument('-a', '--arch', help='Windows architecture')
    parser.add_argument('-l', '--lang', help='Environment LANG')
    parser.set_defaults(func=main)


def main(args):
    config = configlib.load_config(args.config)
    name = args.name
    if name not in config:
        config.add_section(name)
    if args.prefix is None:
        args.prefix = f'~/.local/share/wineprefixes/{args.name}'
    config[name]['prefix'] = args.prefix
    if args.arch is not None:
        config[name]['arch'] = args.arch
    if args.lang is not None:
        config[name]['lang'] = args.lang
    configlib.save_config(config, args.config)
