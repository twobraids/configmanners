# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from configmanners.def_sources.for_mappings import (
    setup_definitions as setup_definitions_for_mappings,
)


def setup_definitions(source, destination):
    module_dict = source.__dict__.copy()
    del module_dict["__builtins__"]
    setup_definitions_for_mappings(module_dict, destination)
