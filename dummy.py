#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import struct

import psyco
psyco.full()

def DummyIt(filename):
	with open(filename, "r+b") as f:
		f.seek(0x14, 0)		
		chip_size = 131072 * (2 ** ord(f.read(1)))
		f.seek(0x80, 0)
		used_size = struct.unpack('<L', f.read(4))[0]	
		
		diff = chip_size - used_size
		
		f.seek(0x0, 2)
		f.write("\xFF" * diff)

if __name__ == "__main__":
	DummyIt(sys.argv[1])

