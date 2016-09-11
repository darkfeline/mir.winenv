winenv README
=============

winenv is an environment manager for Wine.

It automates the management of different Wine architectures, locales, and
prefixes.

Dependendies
------------

- Python 3

Installation
------------

System-wide or for packaging::

    python setup.py install

For the current user::

    python setup.py install --user

You will have to add ``~/.local/bin`` to your shell's ``PATH`` if it isn't
present already; this is where Python installs scripts for users.

Shell setup
-----------

You need to set up your shell as well.  winenv works with POSIX ``sh`` or any
compatible shell (Bash, ZSH, etc.).

Put the following in your configuration file::

    wenv() {
        eval "$(winenv load $1)"
    }

    wenvoff() {
        eval "$(winenv reset)"
    }

fish shell is also supported::

    function wenv -a env_name
      eval (winenv load --shell fish $env_name)
    end

    function wenvoff
      eval (winenv reset --shell fish)
    end

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

Loading environments
^^^^^^^^^^^^^^^^^^^^

You can load an environment using the shell function defined previously::

    $ env | egrep -i "lang|wine"
    LANG=en_US.UTF-8

    $ wenv touhou
    $ env | egrep -i "lang|wine"
    LANG=ja_JP.UTF-8
    WINEPREFIX=/home/user/.local/share/wineprefixes/touhou
    WINEARCH=win32

    $ wenv photoshop
    $ env | egrep -i "lang|wine"
    LANG=en_US.UTF-8
    WINEPREFIX=/home/user/.local/share/wineprefixes/photoshop
    WINEARCH=win64

After loading an environment, you can use ``wine`` and ``winecfg`` freely
without worrying about your Wine environment.

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

Resetting environments
^^^^^^^^^^^^^^^^^^^^^^

You can reset Wine environment settings using the shell function defined
previously::

    $ env | egrep -i "lang|wine"
    LANG=en_US.UTF-8

    $ wenv touhou
    $ env | egrep -i "lang|wine"
    LANG=ja_JP.UTF-8
    WINEPREFIX=/home/user/.local/share/wineprefixes/touhou
    WINEARCH=win32

    $ wenvoff
    $ env | egrep -i "lang|wine"
    LANG=en_US.UTF-8

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
