#!/usr/bin/env python
from __future__ import absolute_import, division, print_function
import configmanners
parser = configmanners.ArgumentParser()
parser.add_argument("--verbosity", help="increase output verbosity")
args = parser.parse_args()
if args.verbosity:
    print("verbosity turned on")
