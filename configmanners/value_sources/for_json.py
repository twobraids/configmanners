# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import json
import collections
import sys

from configmanners.converters import to_string_converters, to_str
from configmanners.namespace import Namespace
from configmanners.option import Option, Aggregation

from configmanners.value_sources.source_exceptions import (
    ValueException,
    NotEnoughInformationException,
    CantHandleTypeException,
)

from configmanners.dotdict import DotDict
from configmanners.memoize import memoize

can_handle = (bytes, str, json)

file_name_extension = "json"

types_not_needing_string_conversion = (int, float, str, bool)


# ==============================================================================
class LoadingJsonFileFailsException(ValueException):
    pass


# ==============================================================================
class ValueSource(object):

    # --------------------------------------------------------------------------
    def __init__(self, source, the_config_manager=None):
        self.values = None
        if source is json:
            try:
                app = the_config_manager._get_option("admin.application")
                source = "%s.%s" % (app.value.app_name, file_name_extension)
            except (AttributeError, KeyError):
                raise NotEnoughInformationException(
                    "Can't setup an json file without knowing the file name"
                )
        if isinstance(source, (bytes, str)):
            source = to_str(source)
        if isinstance(source, str) and source.endswith(file_name_extension):
            try:
                with open(source) as fp:
                    self.values = json.load(fp)
            except IOError as x:
                # The file doesn't exist.  That's ok, we'll give warning
                # but this isn't a fatal error
                import warnings

                warnings.warn("%s doesn't exist" % source)
                self.values = {}
            except ValueError as x:
                raise LoadingJsonFileFailsException("Cannot load json: %s" % str(x))
        else:
            raise CantHandleTypeException()

        self.identity = source

    # --------------------------------------------------------------------------
    @memoize()
    def get_values(self, config_manager, ignore_mismatches, obj_hook=DotDict):
        if isinstance(self.values, obj_hook):
            return self.values
        return obj_hook(self.values)

    # --------------------------------------------------------------------------
    @staticmethod
    def namespace_to_value_dict(a_mapping):
        result_dict = dict()
        for a_key, a_value in a_mapping.items():
            if isinstance(a_value, (Namespace, collections.abc.Mapping)):
                result_dict[a_key] = ValueSource.namespace_to_value_dict(a_value)
            elif isinstance(a_value, Aggregation):
                continue
            elif isinstance(a_value, Option):
                if isinstance(a_value.value, types_not_needing_string_conversion):
                    result_dict[a_key] = a_value.value
                else:
                    try:
                        result_dict[a_key] = a_value.to_string_converter(a_value.value)
                    except TypeError:
                        result_dict[a_key] = to_str(a_value.value)

            elif isinstance(a_value, types_not_needing_string_conversion):
                result_dict[a_key] = a_value
            else:
                result_dict[a_key] = to_str(a_value)
        return result_dict

    @staticmethod
    def write(source_dict, output_stream=sys.stdout):
        json_dict = ValueSource.namespace_to_value_dict(source_dict)
        json.dump(json_dict, output_stream)
