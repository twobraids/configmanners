#!/usr/bin/env python

import configmanners
parser = configmanners.ArgumentParser()
parser.add_argument("echo")
args = parser.parse_args()
print(args.echo)
