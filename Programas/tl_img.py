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
import random

from libs import compression, parser, bmp, images
from libs.pytable import normal_table

import formats

__title__ = "KHDAYS Image Extractor"
__version__ = "2.0"

dx = [[8,16,32,64],[16,32,32,64],[8,8,16,32]]
dy = [[8,16,32,64],[8,8,16,32],[16,32,32,64]]

def scandirs( path ):
    files = []
    for currentFile in glob.glob( os.path.join( path, '*' ) ):
        if os.path.isdir( currentFile ):
            files += scandirs( currentFile )
        else:
            files.append( currentFile )
    return files

def unpackAnimation(palette, cell, tile, dst):

    colors_list = list()
    colors = 2**8

    if palette == None:
        # no caso da paleta de cores não ser informada, monta uma pseudo escala de cinza sem cores repetidas
        sumop = [0,0,0]
        color = [0,0,0]
        for x in range(256):
            alpha = 0 if x == 0 else 1
            
            if (x%9) == 0:
                color = (sumop[0], sumop[1], sumop[2]) 
            if (x%9) == 1:
                color = (sumop[0]+1, sumop[1], sumop[2]) 
            if (x%9) == 2:
                color = (sumop[0], sumop[1]+1, sumop[2])              
            if (x%9) == 3:
                color = (sumop[0], sumop[1], sumop[2]+1)  
            if (x%9) == 4:
                color = (sumop[0]+1, sumop[1]+1, sumop[2])                      
            if (x%9) == 5:
                color = (sumop[0]+1, sumop[1], sumop[2]+1)
            if (x%9) == 6:
                color = (sumop[0], sumop[1]+1, sumop[2]+1)
            if (x%9) == 7:
                if (x%3) == 0:
                    color = (sumop[0]+2,sumop[1], sumop[2])
                if (x%3) == 1:
                    color = (sumop[0],sumop[1]+2, sumop[2])
                if (x%3) == 2:
                    color = (sumop[0],sumop[1], sumop[2]+2)
            if (x%9) == 8:
                if (x%3) == 0:
                    color = (sumop[0]+2,sumop[1]+2, sumop[2])
                if (x%3) == 1:
                    color = (sumop[0]+2,sumop[1], sumop[2]+2)
                if (x%3) == 2:
                    color = (sumop[0],sumop[1]+2, sumop[2]+2)
                    
                sumop = (sumop[0]+1, sumop[1]+1, sumop[2]+1)

            r,g,b = color
            colors_list.append((r/31.0, g/31.0, b/31.0, alpha))
    print tile.chunks
    tiles = tile.char_data
    

    for i, sprite in enumerate(cell.cebk_sprite_attr):
        x0, xs = 0x100, -0x100
        y0, ys = 0x80, -0x80

        for j, obj in enumerate(sprite):
            attr0, attr1, attr2 = obj
            if x0 >= attr1.xcoord:
                x0 = attr1.xcoord
            if xs <= attr1.xcoord + dx[attr0.obj_shape][attr1.obj_size]:
                xs = attr1.xcoord + dx[attr0.obj_shape][attr1.obj_size]
                
            if y0 >= attr0.ycoord:
                y0 = attr0.ycoord
            if ys <= attr0.ycoord + dy[attr0.obj_shape][attr1.obj_size]:
                ys = attr0.ycoord + dy[attr0.obj_shape][attr1.obj_size]

        width = abs(x0) + abs(xs)
        height = abs(y0) + abs(ys)

        buffer = array.array('c', '\xFF' * width * height)
        for j, obj in enumerate(sprite):
            attr0, attr1, attr2 = obj          
            print attr0, attr1, attr2

            pal = colors_list#palette.pltt[attr2.palette_number]
            xx = attr1.xcoord - x0
            yy = attr0.ycoord - y0 
            tx = dx[attr0.obj_shape][attr1.obj_size]
            ty = dy[attr0.obj_shape][attr1.obj_size]
            t0 = 0       
            
            for y in range(ty/8):
                for x in range(tx/8):    
                    print len(tiles), attr2.tile_number*2 + t0
                    try:
                        tile = "".join(map(lambda x: struct.pack("8B",*x), tiles[attr2.tile_number/2 + t0]))
                    except:
                        tile = "\x00\x00\x00\x00\x00\x00\x00\x00"
                    t0 += 1
                    
                    buffer[ width*(yy+y*8) + xx*8 + x*64 :
                            width*(yy+y*8) + xx*8 +(x+1)*64 ] = array.array("c", tile)
                            
                    #print width*(yy+y*8) + xx*8 + x*64 , width*(yy+y*8) + xx*8 +(x+1)*64
            

        head, tail = os.path.split(dst)
        if not os.path.isdir( head ):
            os.makedirs( head )
        print len(buffer ), width, height
        with open( dst + "_%d.bmp" % i, 'wb') as o:
            #if tile.chunks["CHAR"]["bitdepth"] == 3:
                w = images.Writer((width, height), colors_list, 8, 1, 0)
                w.write(o, buffer, 8, 'BMP')
                o.close()
        #raw_input()
        #break

                
def unpackBackground( palette, map, tile , dst ):
              
    table = map.scrn_table
    tiles = tile.char_data

    # vamos gerar 16 planos de imagem, cada uma com a sua própria paleta de cores
    buffer = [array.array('c', '\x00'*(map.chunks["SCRN"]["width"]/2*map.chunks["SCRN"]["height"])) for _ in range(16)]
    
    to_dump = []
    
    for i in range(len(table)):
        mapper = table[i]       
        if mapper.palette not in to_dump:
            to_dump.append(mapper.palette)        
        
        if mapper.number >= 0:
            tile = tiles[mapper.number]
        else:
            tile = [[0 for g in range(8)] for h in range(8)]
        if mapper.h_flip:
            tile = [x[::-1] for x in tile]
        if mapper.v_flip:
            tile = list(reversed(tile))

        for z in range(8):
            for w in range(4):
                pos = i
                buffer[mapper.palette][pos*32+z*4+w] = chr( (tile[z][w*2] | (tile[z][w*2+1] << 4)) & 0xff)

    to_dump = sorted(to_dump)
          
    head, tail = os.path.split(dst)
    if not os.path.isdir( head ):
        os.makedirs( head )
      
    for x in to_dump:
        with open( dst + "_p_%d.bmp" % x , 'wb') as o:
            w = images.Writer((map.chunks["SCRN"]["width"],map.chunks["SCRN"]["height"]), palette.pltt[x], 4, 1, 0)
            w.write(o, buffer[x], 4, 'BMP')
            o.close()    

# def unpackBackground( palette, map, tile , dst ):
              
    # table = map.scrn_table
    # tiles = tile.char_data
    # buffer = [[] for y in range(map.chunks["SCRN"]["height"])]

    # for i in range(len(table)):
        # mapper = table[i]
        
        # pal = palette.pltt[mapper.palette]         
        # if mapper.number >= 0:
            # tile = tiles[mapper.number]
        # else:
            # tile = [[0 for g in range(8)] for h in range(8)]
        # if mapper.h_flip:
            # tile = [x[::-1] for x in tile]
        # if mapper.v_flip:
            # tile = list(reversed(tile))

        # for z in range(8):
            # for w in range(8):
                # pos = i/(map.chunks["SCRN"]["width"]/8)
                # buffer[pos*8 + z].append(pal[tile[z][w]])
          
    # head, tail = os.path.split(dst)
    # if not os.path.isdir( head ):
        # os.makedirs( head )
          
    # with open( dst + ".bmp" , 'wb') as o:
        # #if tile.chunks["CHAR"]["bitdepth"] == 3:
            # p = bmp.Writer(map.chunks["SCRN"]["width"],map.chunks["SCRN"]["height"], 24)
            # p.write(o, buffer)    
        # # else:
            # # p = bmp.Writer(map.chunks["SCRN"]["width"],map.chunks["SCRN"]["height"], 24)
            # # p.write(o, buffer)
            
def packBackground(src):
    
    head, tail = os.path.split(src)
    files = filter(lambda x: x.__contains__(tail), scandirs(head))
    
    full_data = []
    full_color = []
    
    # bufferizando os layers e paletas de cores
    for fname in files:
        w = images.Reader(fname)
        data, colormap = w.as_data(mode = 1, bitdepth = 4)
        full_data.append(data)
        full_color.append(colormap)
    
    # vamos montar o tileset e tilemap
    tiles = len(full_data[0])/32
           
    tilelist = [array.array('c', "\x00"*32)]
    tileset = array.array('c')
    tilemap = array.array('c')
    
    for x in range(tiles):
        print x
        for i, data in enumerate(full_data):
            string = data[32*x:32*(x+1)]
            if string.tostring() != "\x00"*32:
                if string in tilelist:
                    mapper = tilelist.index(string)
                    tilemap.extend(struct.pack('<H', mapper|(i<<12) ))
                else:
                    tilelist.append(string)
                    mapper = tilelist.index(string)
                    tileset.extend(string)
                    tilemap.extend(struct.pack('<H', mapper|(i<<12) ))
                    
                break
                
        else:
            raise Exception("Error!")
    
    with open("lala.gba", "wb") as fd:
        tileset.tofile(fd)
        
    with open("lele.gba", "wb") as fd:
        tilemap.tofile(fd)
        
        #head2, tail2 = os.path.split(fname)
        
        
        

        # p = bmp.Reader(src)
        # data = p.read()
        
        # # a imagem foi lida em 24 bits ... criar os tiles
        # width = len(data[0])
        # height = len(data)
        # print width, height


              

# if __name__ == "__main__":

    # import argparse
    
    # os.chdir( sys.path[0] )
    # #os.system( 'cls' )

    # print "{0:{fill}{align}70}".format( " {0} {1} ".format( __title__, __version__ ) , align = "^" , fill = "=" )

    # parser = argparse.ArgumentParser()
    # parser.add_argument( '-m', dest = "mode", type = str, required = True )
    # parser.add_argument( '-s', dest = "src", type = str, nargs = "?", required = True )
    # parser.add_argument( '-d', dest = "dst", type = str, nargs = "?", required = True )
    # parser.add_argument( '-nclr', dest = "nu_nclr", type = int )
    # parser.add_argument( '-nscr', dest = "nu_nscr", type = int )
    # parser.add_argument( '-ncgr', dest = "nu_ncgr", type = int )
    
    # args = parser.parse_args()
    
    # # dump bg
    # if args.mode == "e0":
        # print "Unpacking background"           
        # unpackBackground( args.src , args.dst , args.nu_nclr, args.nu_nscr, args.nu_ncgr )
    # # insert bg
    # # elif args.mode == "i0": 
        # # print "Packing background"
        # # packBackground( args.src , args.dst )
    # # # dump ani
    # # elif args.mode == "e1": 
        # # print "Unpacking animation"
        # # unpackSprite( args.src , args.dst )
    # # # insert ani
    # # elif args.mode == "i1": 
        # # print "Packing animation"
        # # print args.src1
        # # packSprite( args.src , args.dst , args.src1 )
    # else:
        # sys.exit(1)