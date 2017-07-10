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

import subprocess
import sys
from unittest import mock

import pytest

from mir.winenv.__main__ import main


@pytest.fixture
def config_file(tmpdir):
    """Temporary global config file default path."""
    config_file = tmpdir / 'config'
    with mock.patch('mir.winenv.configlib.CONFIG_PATH', str(config_file)):
        yield config_file


def test_add_explicit(config_file):
    exit = main(['add', 'touhou',
                 '-p', '/tmp/prefix',
                 '-a', 'win32',
                 '-l', 'ja_JP.UTF-8'])
    assert exit == 0
    assert config_file.read_text().strip() == '''\
[DEFAULT]
arch = win32
lang = en_US.UTF-8

[touhou]
prefix = /tmp/prefix
arch = win32
lang = ja_JP.UTF-8
'''.strip()


def test_invalid_command(config_file):
    exit = main(['foobar'])
    assert exit != 0


def test_add_defaults(config_file):
    exit = main(['add', 'touhou'])
    assert exit == 0
    assert config_file.read_text().strip() == '''\
[DEFAULT]
arch = win32
lang = en_US.UTF-8

[touhou]
prefix = ~/.local/share/wineprefixes/touhou
'''.strip()


def test_add_should_overwrite_existing(config_file):
    config_file.write_text('''\
[DEFAULT]
arch = win32
lang = en_US.UTF-8

[touhou]
prefix = /tmp/eggs
''')
    exit = main(['add', 'touhou', '-p', '/tmp/spam'])
    assert exit == 0
    assert config_file.read_text().strip() == '''\
[DEFAULT]
arch = win32
lang = en_US.UTF-8

[touhou]
prefix = /tmp/spam
'''.strip()


def test_add_should_ignore_unspecified(config_file):
    config_file.write_text('''\
[DEFAULT]
arch = win32
lang = en_US.UTF-8

[touhou]
prefix = /tmp/eggs
lang = ja_JP.UTF-8
''')
    exit = main(['add', 'touhou', '-p', '/tmp/spam'])
    assert exit == 0
    assert config_file.read_text().strip() == '''\
[DEFAULT]
arch = win32
lang = en_US.UTF-8

[touhou]
prefix = /tmp/spam
lang = ja_JP.UTF-8
'''.strip()


def test_list(config_file, capsys):
    config_file.write_text('''\
[DEFAULT]
arch = win32
lang = en_US.UTF-8

[touhou]
prefix = ~/.local/share/wineprefixes/touhou
arch = win32
lang = ja_JP.UTF-8

[other]
prefix = ~/.local/share/wineprefixes/other
''')
    exit = main(['list'])
    assert exit == 0
    out, err = capsys.readouterr()
    assert out == '''\
touhou
other
'''


def test_list_verbose(config_file, capsys):
    config_file.write_text('''\
[DEFAULT]
arch = win32
lang = en_US.UTF-8

[touhou]
prefix = ~/.local/share/wineprefixes/touhou
arch = win32
lang = ja_JP.UTF-8

[other]
prefix = ~/.local/share/wineprefixes/other
''')
    exit = main(['list', '-v'])
    assert exit == 0
    out, err = capsys.readouterr()
    assert out == '''\
touhou
prefix=~/.local/share/wineprefixes/touhou
arch=win32
lang=ja_JP.UTF-8

other
prefix=~/.local/share/wineprefixes/other
arch=win32
lang=en_US.UTF-8
'''


def test_run(config_file):
    config_file.write_text('''\
[touhou]
prefix = /tmp/touhou
arch = win32
lang = ja_JP.UTF-8
''')
    with mock.patch('os.execvpe') as e:
        exit = main(['run', 'touhou', 'wine', '-some', 'args'])
    assert exit == 0
    assert e.call_args[0][0] == 'wine'
    assert e.call_args[0][1] == ['wine', '-some', 'args']
    assert e.call_args[0][2]['WINEPREFIX'] == '/tmp/touhou'
    assert e.call_args[0][2]['WINEARCH'] == 'win32'
    assert e.call_args[0][2]['LANG'] == 'ja_JP.UTF-8'


def test_run_missing_section_should_return_1(config_file):
    with mock.patch('os.execvpe') as e:
        exit = main(['run', 'touhou', 'wine', '-some', 'args'])
    assert exit == 1
    e.assert_not_called()
