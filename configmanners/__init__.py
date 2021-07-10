# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

__version__ = "3.0"

# Having these here makes it possible to easily import once configmanners is
# installed.
# For example::
#
#    from configmanners import Namespace, ConfigurationManager
#

from configmanners.config_manager import ConfigurationManager
from configmanners.required_config import RequiredConfig
from configmanners.namespace import Namespace
from configmanners.config_file_future_proxy import ConfigFileFutureProxy
from configmanners.converters import (
    class_converter,
    regex_converter,
    timedelta_converter
)

from configmanners.environment import environment
# this next line brings in command_line and, if argparse is available,
# a definition of the configmanners version of ArgumentParser.  Why is it done
# with "import *" ? Because we don't know what symbols to import, the decision
# about what is symbols exist within the module.  To make the import specific
# here, it would be necessary to reproduce the same logic that is already
# in the commandline module.
from configmanners.commandline import *


# ------------------------------------------------------------------------------
def configuration(*args, **kwargs):
    """this function just instantiates a ConfigurationManager and returns
    the configuration dictionary.  It accepts all the same parameters as the
    constructor for the ConfigurationManager class."""
    try:
        config_kwargs = {'mapping_class': kwargs.pop('mapping_class')}
    except KeyError:
        config_kwargs = {}
    cm = ConfigurationManager(*args, **kwargs)
    return cm.get_config(**config_kwargs)
