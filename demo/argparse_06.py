#!/usr/bin/env python

import configmanners
parser = configmanners.ArgumentParser()
parser.add_argument("--verbose", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()
if args.verbose:
   print("verbosity turned on")

