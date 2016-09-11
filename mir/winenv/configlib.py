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

import configparser
import os
import tempfile

CONFIG_PATH = os.path.join(os.environ['HOME'], '.config',
                           'winenv', 'config.ini')


def make_config():
    """Make default configuration."""
    config = configparser.ConfigParser()
    config['DEFAULT']['arch'] = 'win32'
    config['DEFAULT']['lang'] = 'en_US.UTF-8'
    return config


def load_config(path):
    """Safely read config file."""
    config = make_config()
    if os.path.isfile(path):
        config.read(path)
    return config


def save_config(config, path):
    """Safely save config file."""
    dirpath = os.path.dirname(path)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    temp_fd, temp_path = tempfile.mkstemp(dir=dirpath)
    with os.fdopen(temp_fd, 'w') as file:
        config.write(file)
    os.rename(temp_path, path)
