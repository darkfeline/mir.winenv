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

import configparser
import os
from pathlib import Path


CONFIG_PATH = (Path.home() / '.config' / 'winenv' / 'config.ini')


def make_config():
    """Make default configuration."""
    config = configparser.ConfigParser()
    config['DEFAULT']['arch'] = 'win32'
    config['DEFAULT']['lang'] = 'en_US.UTF-8'
    return config


def load_config(path: 'PathLike'):
    """Safely read config file."""
    path = Path(path)
    config = make_config()
    if path.is_file():
        config.read(path)
    return config


def save_config(config, path: 'PathLike'):
    """Safely save config file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w') as file:
        config.write(file)


def get_env_vars(config, env_name):
    """Return a dict of environment variables for the named environment."""
    if not config.has_section(env_name):
        raise ValueError(f"{env_name} environment doesn't exist")
    config_section = config[env_name]
    return {
        'WINEPREFIX': os.path.expanduser(config_section['prefix']),
        'WINEARCH': config_section['arch'],
        'LANG': config_section['lang'],
    }
