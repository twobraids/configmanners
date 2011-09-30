import re
import os
import datetime
import tempfile
from contextlib import contextmanager
import ConfigParser
import io
from cStringIO import StringIO
import json
import functools

import configman.config_manager as config_manager
from configman.dotdict import DotDict

import unittest
class TestCase(unittest.TestCase):

    def test_OptionsByIniFile_basics(self):
        tmp_filename = os.path.join(tempfile.gettempdir(), 'test.conf')
        open(tmp_filename, 'w').write("""
; comment
[top_level]
name=Peter
awesome:
; comment
[othersection]
foo=bar  ; other comment
        """)

        try:
            o = config_manager.OptionsByIniFile(tmp_filename)
            c = config_manager.ConfigurationManager([],
                                        manager_controls=False,
                                        use_config_files=False,
                                        auto_help=False,
                                        argv_source=[])

            self.assertEqual(o.get_values(c, False),
                             {'othersection.foo': 'bar',
                              'name': 'Peter',
                              'awesome': ''})
            self.assertEqual(o.get_values(c, True),
                             {'othersection.foo': 'bar',
                              'name': 'Peter',
                              'awesome': ''})
            # XXX (peterbe): commented out because I'm not sure if
            # OptionsByIniFile get_values() should depend on the configuration
            # manager it is given as first argument or not.
            #self.assertEqual(o.get_values(c, True), {})
            #self.assertRaises(config_manager.NotAnOptionError,
            #                  o.get_values, c, False)

            #c.option_definitions.option('limit', default=0)
            #self.assertEqual(o.get_values(c, False), {'limit': '20'})
            #self.assertEqual(o.get_values(c, True), {'limit': '20'})
        finally:
            if os.path.isfile(tmp_filename):
                os.remove(tmp_filename)
