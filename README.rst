mir.winenv README
=================

.. image:: https://circleci.com/gh/darkfeline/mir.winenv.svg?style=shield
   :target: https://circleci.com/gh/darkfeline/mir.winenv
   :alt: CircleCI
.. image:: https://codecov.io/gh/darkfeline/mir.winenv/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/darkfeline/mir.winenv
   :alt: Codecov
.. image:: https://badge.fury.io/py/mir.winenv.svg
   :target: https://badge.fury.io/py/mir.winenv
   :alt: PyPI Release


winenv is an environment manager for Wine.

It automates the management of different Wine architectures, locales, and
prefixes.

Dependencies
------------

- Python 3.6

Installation
------------

System-wide or for packaging::

    python setup.py install

For the current user::

    python setup.py install --user

Usage
-----

Adding environments
^^^^^^^^^^^^^^^^^^^

First, you add environments::

    $ winenv add program1 -a win32 -l en_US.UTF-8 -p ~/.local/share/wineprefixes/program1

This adds an environment named ``program1``, with the associated environment
variables ``WINEARCH=win32``, ``LANG=en_US.UTF-8``,
``WINEPREFIX=~/.local/share/wineprefixes/program1``.

The options are optional.  ``-a`` defaults to ``win32``, ``-l`` defaults to
``en_US.UTF-8``, and ``-p`` defaults to ``~/.local/share/wineprefixes/<name of
environment>``.

The default architecture and locale can be configured (see Configuration
section).  In particular, you should configure the default locale to match your
system.

Here are some more examples::

    $ winenv add touhou -a win32 -l ja_JP.UTF-8
    $ winenv add photoshop -a win64
    $ winenv add testing -p ~/temp

Running commands in environments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can run a command within a wine environment::

    $ winenv run touhou wine path/to/executable

You can also start a shell with a wine environment ::

    $ env | egrep -i "lang|wine"
    LANG=en_US.UTF-8

    $ winenv run touhou bash

    bash$ env | egrep -i "lang|wine"
    LANG=ja_JP.UTF-8
    WINEPREFIX=/home/user/.local/share/wineprefixes/touhou
    WINEARCH=win32

    bash$ wine path/to/executable

    bash$ exit

    $ env | egrep -i "lang|wine"
    LANG=en_US.UTF-8

Listing environments
^^^^^^^^^^^^^^^^^^^^

You can list existing environments::

    $ winenv list
    touhou
    photoshop

Verbose listing::

    $ winenv list -v
    touhou
    prefix=/home/user/.local/share/wineprefixes/touhou
    arch=win32
    lang=ja_JP.UTF-8

    photoshop
    prefix=/home/user/.local/share/wineprefixes/photoshop
    arch=win64
    lang=en_US.UTF-8

More help
^^^^^^^^^

Make use of the ``--help`` option as needed.

Configuration and data
----------------------

winenv stores its data in a configuration file.  The default path is
``~/.config/winenv/config.ini``.  You can supply a different file via the
``--config`` option.

The configuration file uses the INI format, as parsed by Python's ``configparser``
module.
