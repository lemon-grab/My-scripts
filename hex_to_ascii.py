#!/usr/bin/env python3

import sys

string = sys.argv[1]
object = bytes.fromhex(string)
ascii = object.decode("ASCII")
print(ascii)
