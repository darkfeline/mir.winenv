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

import argparse
import logging

from . import commands


def main():
    """Entry point."""
    logging.basicConfig(level='INFO')
    parser = argparse.ArgumentParser()
    commands.setup_parser(parser)

    args = parser.parse_args()

    try:
        func = args.func
    except AttributeError:
        parser.print_help()
    else:
        func(args)


if __name__ == '__main__':
    main()
