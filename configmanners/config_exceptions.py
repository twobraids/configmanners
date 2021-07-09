# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import absolute_import, division, print_function


class configmannersException(Exception):
    pass


class ConfigFileMissingError(IOError, configmannersException):
    pass


class ConfigFileOptionNameMissingError(configmannersException):
    pass


class NotAnOptionError(configmannersException):
    pass


class OptionError(configmannersException):
    pass


class CannotConvertError(configmannersException):
    pass
