#!/usr/bin/env python

import configmanners
parser = configmanners.ArgumentParser()
parser.add_argument("square", help="display a square of a given number")
args = parser.parse_args()
print(int(args.square)**2)

