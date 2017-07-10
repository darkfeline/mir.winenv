# Copyright (C) 2017 Allen Li
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import configparser
import os
from unittest import mock

import pytest

from mir.winenv import configlib


def test_make_config():
    config = configlib.make_config()
    assert isinstance(config, configparser.ConfigParser)
    assert config['DEFAULT']['arch'] == 'win32'
    assert config['DEFAULT']['lang'] == 'en_US.UTF-8'


def test_load_config(tmpdir):
    config_path = tmpdir / 'config'
    config_path.write_text('''\
[touhou]
prefix = ~/.local/share/wineprefixes/touhou
arch = win32
lang = ja_JP.UTF-8
''')
    config = configlib.load_config(config_path)
    assert isinstance(config, configparser.ConfigParser)
    assert config['touhou']['prefix'] == '~/.local/share/wineprefixes/touhou'
    assert config['touhou']['arch'] == 'win32'
    assert config['touhou']['lang'] == 'ja_JP.UTF-8'


def test_load_config_with_missing_file_should_be_empty(tmpdir):
    config_path = tmpdir / 'config'
    config = configlib.load_config(config_path)
    assert isinstance(config, configparser.ConfigParser)
    assert not config.sections()


def test_save_config(tmpdir):
    config_path = tmpdir / 'config'
    config = configlib.make_config()
    configlib.save_config(config, config_path)
    assert config_path.read_text().strip() == '''\
[DEFAULT]
arch = win32
lang = en_US.UTF-8
'''.strip()


def test_get_env_vars():
    config = configparser.ConfigParser()
    config.add_section('touhou')
    config['touhou']['prefix'] = '~/.local/share/wineprefixes/touhou'
    config['touhou']['arch'] = 'win32'
    config['touhou']['arch'] = 'win32'
    config['touhou']['lang'] = 'ja_JP.UTF-8'
    with mock.patch.dict(os.environ, {'HOME': '/home/alice'}):
        got = configlib.get_env_vars(config, 'touhou')
    assert got == {
        'WINEPREFIX': '/home/alice/.local/share/wineprefixes/touhou',
        'WINEARCH': 'win32',
        'LANG': 'ja_JP.UTF-8',
    }


def test_get_env_vars_missing_section_should_raise():
    config = configparser.ConfigParser()
    with pytest.raises(ValueError):
        got = configlib.get_env_vars(config, 'touhou')
