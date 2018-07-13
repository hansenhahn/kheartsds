#!/usr/bin/env python
# -*- coding: utf-8 -*-

# formats/nscr.py

# Copyright 2010/11 Diego Hansen Hahn (aka DiegoHH) <diegohh90 [at] hotmail [dot] com>

# Nitro VieWeR is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License.

# Nitro VieWeR is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Nitro VieWeR. If not, see <http://www.gnu.org/licenses/>.

''' NCLR - Nitro SCreen Resource '''

import array
import exceptions
import struct

__author__ = "Diego Hansen Hahn"
__version__ = "1.0"

class ChunkError(exceptions.Exception):
    def __init__ (self, error):
        setattr(self, "error", error)
    def __str__(self):
        return repr(self.error)

class TileAttr(object):
    def __init__(self, attr):
        attr = struct.unpack('<H', attr)[0]
        self.number = attr & 0x3FF
        self.h_flip = (attr & 0x400) >> 10
        self.v_flip = (attr & 0x800) >> 11
        self.palette = (attr & 0xF000) >> 12

    def __str__(self):
        return '''\
Tile Number: %s
Horizontal Flip: %s
Vertical Flip: %s
Palette Number: %s\
''' % (self.number, self.h_flip, self.v_flip, self.palette)


class NSCRFormat(object):

    def __init__(self, data):
        self.base_addr = data.tell()    
    
        #data.seek(0,0)
        if data.read(4) == "RCSN":
            setattr(self, "data", data)
        else:
            raise TypeError("File not supported.")

        self.read_chunks()
        self.read_scrn_structure()

    def read_chunks(self):
        if not hasattr(self, "data"):
            raise AttributeError()

        chunks = {}
        self.data.seek(self.base_addr)
        # NCLR - Nitro CEll Resource
        stamp = self.data.read(4)
        if stamp == "RCSN":
            chunks.update({"NSCR":{}})
            self.data.read(4) #0100FEFF
            chunks["NSCR"].update({"file_size" : struct.unpack('<L', self.data.read(4))[0]})
            chunks["NSCR"].update({"struct_size" : struct.unpack('<H', self.data.read(2))[0]})
            chunks["NSCR"].update({"total_chunks" : struct.unpack('<H', self.data.read(2))[0]})
        else:
            raise ChunkError("Error with NSCR chunk.")

        chunks_readed = 0

        # SCReeN
        stamp = self.data.read(4)
        if stamp == "NRCS":
            chunks.update({"SCRN":{}})
            chunks["SCRN"].update({"struct_size" : struct.unpack('<L', self.data.read(4))[0]})
            chunks["SCRN"].update({"width" : struct.unpack('<H', self.data.read(2))[0]})
            chunks["SCRN"].update({"height" : struct.unpack('<H', self.data.read(2))[0]})
            self.data.read(4) # Padding
            chunks["SCRN"].update({"data_size" : struct.unpack('<L', self.data.read(4))[0]})
            chunks["SCRN"].update({"data_address" : self.data.tell()})
        else:
            raise ChunkError("Error with SCRN chunk.")

        chunks_readed += 1
        if chunks_readed == chunks["NSCR"]["total_chunks"]:
            setattr(self, "chunks", chunks)
            return chunks
        else:
            raise ChunkError("Missing chunks.")

    def read_scrn_structure(self):
        if not hasattr(self, "chunks"):
            self.read_chunks()

        self.data.seek(self.chunks["SCRN"]["data_address"], 0)

        scrn_table = []
        for x in range(self.chunks["SCRN"]["data_size"]/2):
            scrn_table.append(TileAttr(self.data.read(2)))

        setattr(self, "scrn_table", scrn_table)
        return scrn_table