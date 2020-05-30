#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import shutil
import os
import sys
import struct
import array
import tempfile
import codecs
import mmap
import glob

from libs import compression, parser, bmp
from libs.pytable import normal_table

import formats

__title__ = "KHDAYS Image Extractor"
__version__ = "2.0"

def unpackBackground( src, dst, nclr, nscr, ncgr ):    
    with open( os.path.join( src, "NCLR_%03d" % nclr ), "rb" ) as fd:
        palette = formats.NCLRFormat(fd)
                
    with open( os.path.join( src, "NCGR_%03d" % ncgr ), "rb" ) as fd:              
        tile = formats.NCGRFormat(fd)
    
    with open( os.path.join( src, "NSCR_%03d" % nscr ), "rb" ) as fd:
        map = formats.NSCRFormat(fd)   
          
    table = map.scrn_table
    tiles = tile.char_data
    buffer = [[] for y in range(map.chunks["SCRN"]["height"])]

    for i in range(len(table)):
        mapper = table[i]
        
        pal = palette.pltt[mapper.palette]         
        if mapper.number >= 0:
            tile = tiles[mapper.number]
        else:
            tile = [[0 for g in range(8)] for h in range(8)]
        if mapper.h_flip:
            tile = [x[::-1] for x in tile]
        if mapper.v_flip:
            tile = list(reversed(tile))

        for z in range(8):
            for w in range(8):
                pos = i/(map.chunks["SCRN"]["width"]/8)
                buffer[pos*8 + z].append(pal[tile[z][w]])
                
    if not os.path.isdir( dst ):
        os.makedirs( dst )
      
    print os.path.join( dst, 'IMG1_%03d_%03d_%03d.bmp' % ( nclr, nscr , ncgr ) )
    with open( os.path.join( dst, 'IMG1_%03d_%03d_%03d.bmp' % ( nclr, nscr , ncgr ) ), 'wb') as o:
        p = bmp.Writer(map.chunks["SCRN"]["width"],map.chunks["SCRN"]["height"]  ,24)
        p.write(o, buffer)    

if __name__ == "__main__":

    import argparse
    
    os.chdir( sys.path[0] )
    #os.system( 'cls' )

    print "{0:{fill}{align}70}".format( " {0} {1} ".format( __title__, __version__ ) , align = "^" , fill = "=" )

    parser = argparse.ArgumentParser()
    parser.add_argument( '-m', dest = "mode", type = str, required = True )
    parser.add_argument( '-s', dest = "src", type = str, nargs = "?", required = True )
    parser.add_argument( '-d', dest = "dst", type = str, nargs = "?", required = True )
    parser.add_argument( '-nclr', dest = "nu_nclr", type = int )
    parser.add_argument( '-nscr', dest = "nu_nscr", type = int )
    parser.add_argument( '-ncgr', dest = "nu_ncgr", type = int )
    
    args = parser.parse_args()
    
    # dump bg
    if args.mode == "e0":
        print "Unpacking background"           
        unpackBackground( args.src , args.dst , args.nu_nclr, args.nu_nscr, args.nu_ncgr )
    # insert bg
    # elif args.mode == "i0": 
        # print "Packing background"
        # packBackground( args.src , args.dst )
    # # dump ani
    # elif args.mode == "e1": 
        # print "Unpacking animation"
        # unpackSprite( args.src , args.dst )
    # # insert ani
    # elif args.mode == "i1": 
        # print "Packing animation"
        # print args.src1
        # packSprite( args.src , args.dst , args.src1 )
    else:
        sys.exit(1)