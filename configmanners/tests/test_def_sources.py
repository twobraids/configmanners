# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import unittest
import collections

from configmanners.namespace import Namespace

from configmanners.dotdict import DotDict
import configmanners.def_sources as defsrc


# ==============================================================================
class TestCase(unittest.TestCase):

    # --------------------------------------------------------------------------
    def test_setup_definitions_1(self):
        d = DotDict()

        def fake_mapping_func(source, destination):
            self.assertTrue(isinstance(source, collections.abc.Mapping))
            self.assertEqual(d, destination)

        saved_original = defsrc.definition_dispatch.copy()
        try:
            defsrc.definition_dispatch[collections.abc.Mapping] = fake_mapping_func
            s = {}
            defsrc.setup_definitions(s, d)
            s = DotDict()
            defsrc.setup_definitions(s, d)
            s = Namespace()
            defsrc.setup_definitions(s, d)
        finally:
            defsrc.definition_dispatch = saved_original

    # --------------------------------------------------------------------------
    def test_setup_definitions_2(self):
        d = DotDict()

        def fake_mapping_func(source, destination):
            self.assertTrue(source is collections)
            self.assertEqual(d, destination)

        saved_original = defsrc.definition_dispatch.copy()
        try:
            defsrc.definition_dispatch[type(collections)] = fake_mapping_func
            s = collections
            defsrc.setup_definitions(s, d)
        finally:
            defsrc.definition_dispatch = saved_original

    # --------------------------------------------------------------------------
    def test_setup_definitions_3(self):
        d = DotDict()

        def fake_mapping_func(source, destination):
            self.assertTrue(isinstance(source, str))
            self.assertEqual(d, destination)

        saved_original = defsrc.definition_dispatch.copy()
        try:
            defsrc.definition_dispatch[str] = fake_mapping_func
            s = "{}"
            defsrc.setup_definitions(s, d)
        finally:
            defsrc.definition_dispatch = saved_original
