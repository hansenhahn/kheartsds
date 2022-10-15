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
import array

from libs import compression, parser, bmp, images
from libs.pytable import normal_table

import formats

__title__ = "KHDAYS Image Extractor"
__version__ = "2.0"

dx = [[8,16,32,64],[16,32,32,64],[8,8,16,32]]
dy = [[8,16,32,64],[8,8,16,32],[16,32,32,64]]


def unpackAnimation(palette, cell, tile, dst):

    tiles = tile.char_data

    for i, sprite in enumerate(cell.cebk_sprite_attr):
        width = 0
        height = 0

        for i, obj in enumerate(sprite):
            attr0, attr1, attr2 = obj
            if width <= attr1.xcoord + dx[attr0.obj_shape][attr1.obj_size]:
                width = attr1.xcoord + dx[attr0.obj_shape][attr1.obj_size]
            if height <= attr0.ycoord + dy[attr0.obj_shape][attr1.obj_size]:
                height = attr0.ycoord + dy[attr0.obj_shape][attr1.obj_size]

 
        buffer = array.array('c', '\xFF' * width * height)
        for j, obj in enumerate(sprite):
            attr0, attr1, attr2 = obj        
            print attr1.xcoord , attr0.ycoord
            pal = palette.pltt[attr2.palette_number]
            tx = dx[attr0.obj_shape][attr1.obj_size] / 8
            ty = dy[attr0.obj_shape][attr1.obj_size] / 8
            t0 = 0        

            
            for y in range(ty):
                for x in range(tx):
                    tile = tiles[attr2.tile_number+t0]
                    t0 += 1
                    #print attr0.ycoord + y*8 , attr1.xcoord + 8*x
                    for y8 in range(8):
                        line = struct.pack("8B",*tile[y8])
                        buffer[(width*(attr0.ycoord + y*8 + y8)) + attr1.xcoord + 8*(x):
                               (width*(attr0.ycoord + y*8 + y8)) + attr1.xcoord + 8*(x+1)] = array.array('c',line)
 
            # for yi in range(ty):
                # for xi in range(tx):
                    # for y in range(8):
                        # for x in range(8):
                            # #pos0,0 do sprite
                            # pos0 = attr0.ycoord*witdh + attr0.xcoord
                            # #posX,Y do tile
                            # posT = 8*yi*tx + 8*xi
                            
                            
                            # buffer[attr0.xcoord*width + tx*y + x] = tiles[tx*h + w][8*y + x]
            
            
            
                    # if mapper.number >= 0:
            # tile = tiles[mapper.number]
        # else:
            # tile = [[0 for g in range(8)] for h in range(8)]
        # if mapper.h_flip:
            # tile = [x[::-1] for x in tile]
        # if mapper.v_flip:
            # tile = list(reversed(tile))
            
            
            
            
                        # for obj_param in objs_params:
                            # obj_data = obj_param[6]
                            # for y in range(obj_param[5] / 8):
                                # for w in range(obj_param[4] / 8):
                                    # buffer[(width*(obj_param[3] + y*8)) + obj_param[2]*8 + 64*(w):
                                           # (width*(obj_param[3] + y*8)) + obj_param[2]*8 + 64*(w+1)] = array.array('c',obj_data.pop(0))

        head, tail = os.path.split(dst)
        if not os.path.isdir( head ):
            os.makedirs( head )
        #print buffer 
        with open( dst + "_%d.bmp" % i, 'wb') as o:
            #if tile.chunks["CHAR"]["bitdepth"] == 3:
                # p = bmp.Writer(width,height, 24)
                # p.write(o, buffer)
                print palette.pltt
                w = images.Writer((width, height), palette.pltt[0], 8, 2)
                w.write(o, buffer, 8, 'BMP')
                o.close()
        raw_input()
        #break

                

def unpackBackground( palette, map, tile , dst ):
              
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
          
    head, tail = os.path.split(dst)
    if not os.path.isdir( head ):
        os.makedirs( head )
          
    with open( dst + ".bmp" , 'wb') as o:
        #if tile.chunks["CHAR"]["bitdepth"] == 3:
            p = bmp.Writer(map.chunks["SCRN"]["width"],map.chunks["SCRN"]["height"], 24)
            p.write(o, buffer)    
        # else:
            # p = bmp.Writer(map.chunks["SCRN"]["width"],map.chunks["SCRN"]["height"], 24)
            # p.write(o, buffer) 
              

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