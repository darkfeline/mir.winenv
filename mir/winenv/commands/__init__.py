# Copyright (C) 2016, 2017  Allen Li

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

import importlib


def setup_parser(parser):
    """Setup ArgumentParser with commands."""
    subparsers = parser.add_subparsers(title='Commands')
    for command in COMMANDS:
        command.setup_parser(subparsers)


COMMANDS = []


def _add_command_module(module_name: str):
    """Add a submodule as a command."""
    mod = importlib.import_module(f'mir.winenv.commands.{module_name}')
    COMMANDS.append(mod)


_add_command_module('add')
_add_command_module('list')
_add_command_module('run')
