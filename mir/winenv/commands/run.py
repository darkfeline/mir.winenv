# Copyright (C) 2017  Allen Li

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

import argparse
import logging
import os
import sys

from mir.winenv import configlib

logger = logging.getLogger(__name__)

HELP = 'Run a command in a wine environment.'


def setup_parser(subparsers):
    parser = subparsers.add_parser(
        'run',
        description=HELP,
        help=HELP,
    )
    parser.add_argument('--config',
                        default=configlib.CONFIG_PATH,
                        help='Configuration file to use.')
    parser.add_argument('name', help='Name of environment')
    parser.add_argument('command', help='Command to run')
    parser.add_argument('command_args',
                        nargs=argparse.REMAINDER,
                        help='Arguments to pass to command')
    parser.set_defaults(func=main)


def main(args):
    config = configlib.load_config(args.config)
    if not config.has_section(args.name):
        logger.error("%s environment doesn't exist", args.name)
        sys.exit(1)
    os.execvpe(
        args.command,
        [args.command, *args.command_args],
        _get_environment(config, args.name))


def _get_environment(config, env_name):
    env = os.environ.copy()
    env.update(configlib.get_env_vars(config, env_name))
    return env
