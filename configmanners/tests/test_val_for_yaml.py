# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import unittest
import os
import yaml
import tempfile
import contextlib
from io import StringIO

from configmanners.namespace import Namespace
from configmanners.config_manager import ConfigurationManager
from configmanners.datetime_util import datetime_from_ISO_string
from configmanners.value_sources import for_yaml
from configmanners.value_sources.for_yaml import ValueSource
from configmanners.dotdict import DotDict, DotDictWithAcquisition
from configmanners.converters import str_to_list_of_ints


# ------------------------------------------------------------------------------
def stringIO_context_wrapper(a_stringIO_instance):
    @contextlib.contextmanager
    def stringIO_context_manager():
        yield a_stringIO_instance

    return stringIO_context_manager


# ------------------------------------------------------------------------------
def bbb_minus_one(config, local_config, args):
    return config.bbb - 1


# ==============================================================================
class TestCase(unittest.TestCase):

    # --------------------------------------------------------------------------
    def test_for_yaml_basics(self):
        tmp_filename = os.path.join(tempfile.gettempdir(), "test.yml")
        j = {
            "fred": "wilma",
            "number": 23,
        }
        with open(tmp_filename, "w") as f:
            yaml.dump(j, f)
        try:
            jvs = ValueSource(tmp_filename)
            vals = jvs.get_values(None, True)
            self.assertEqual(vals["fred"], "wilma")
            self.assertEqual(vals["number"], 23)
        finally:
            if os.path.isfile(tmp_filename):
                os.remove(tmp_filename)

    # --------------------------------------------------------------------------
    def test_write_yaml_single_level(self):
        n = Namespace(doc="top")
        n.add_option(
            "aaa",
            "2011-05-04T15:10:00",
            "the a",
            short_form="a",
            from_string_converter=datetime_from_ISO_string,
        )

        c = ConfigurationManager(
            [n], use_admin_controls=True, use_auto_help=False, argv_source=[]
        )

        out = StringIO()
        c.write_conf(for_yaml, opener=stringIO_context_wrapper(out))
        received = out.getvalue()
        out.close()

        expect_to_find = {
            # "aaa": datetime_from_ISO_string("2011-05-04T15:10:00"),
            "aaa": "2011-05-04T15:10:00"
        }
        jrec = yaml.load(received, Loader=yaml.Loader)
        self.assertEqual(jrec, expect_to_find)

    # --------------------------------------------------------------------------
    def test_write_yaml_multi_level(self):
        n = Namespace(doc="top")
        n.add_option(
            "aaa",
            "2011-05-04T15:10:00",
            "the a",
            short_form="a",
            from_string_converter=datetime_from_ISO_string,
        )
        n.namespace('level2')
        n.level2.add_option(
            "bbb",
            True,
            "the bbb",
        )
        n.level2.add_option(
            "ccc",
            [1, 2, 3, 4],
            "ccc numbers",
            from_string_converter=str_to_list_of_ints,
        )

        c = ConfigurationManager(
            [n], use_admin_controls=True, use_auto_help=False, argv_source=[]
        )

        out = StringIO()
        c.write_conf(for_yaml, opener=stringIO_context_wrapper(out))
        received = out.getvalue()
        out.close()
        jrec = yaml.load(received, Loader=yaml.Loader)

        expect_to_find = {
            "aaa": "2011-05-04T15:10:00",
            "level2": {"bbb": True, "ccc": "1, 2, 3, 4"},
        }
        self.assertEqual(jrec, expect_to_find)

    def test_write_yaml_round_trip(self):
        n = Namespace(doc="top")
        n.add_option(
            "aaa",
            "2011-05-04T15:10:00",
            "the a",
            short_form="a",
            from_string_converter=datetime_from_ISO_string,
        )
        n.namespace('level2')
        n.level2.add_option(
            "bbb",
            True,
            "the bbb",
        )
        n.level2.add_option(
            "ccc",
            [1, 2, 3, 4],
            "ccc numbers",
            from_string_converter=str_to_list_of_ints,
        )

        c = ConfigurationManager(
            [n], use_admin_controls=True, use_auto_help=False, argv_source=[]
        )

        out = StringIO()
        c.write_conf(for_yaml, opener=stringIO_context_wrapper(out))
        received = out.getvalue()
        out.close()

        jrec = yaml.load(received, Loader=yaml.Loader)

        c2 = ConfigurationManager([n], [jrec], use_admin_controls=False)
        config = c2.get_config(dict)

        expect_to_find = {
            "aaa": datetime_from_ISO_string("2011-05-04T15:10:00"),
            "level2": {"bbb": True, "ccc": [1, 2, 3, 4]},
        }
        self.assertEqual(config, expect_to_find)

    def test_get_values(self):
        j = {"a": "1", "b": 2, "c": {"d": "x", "e": "y"}, "d": {"d": "X"}}
        tmp_filename = os.path.join(tempfile.gettempdir(), "test.yml")
        with open(tmp_filename, "w") as f:
            yaml.dump(j, f)
        try:
            jvs = ValueSource(tmp_filename)
            vals = jvs.get_values(None, True, DotDict)
            self.assertTrue(isinstance(vals, DotDict))
            vals = jvs.get_values(None, True, DotDictWithAcquisition)
            self.assertTrue(isinstance(vals, DotDictWithAcquisition))
            self.assertEqual(vals.d.b, 2)
        finally:
            if os.path.isfile(tmp_filename):
                os.remove(tmp_filename)
