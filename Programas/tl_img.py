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

def scandirs(path):
    files = []
    for currentFile in glob.glob( os.path.join(path, '*') ):
        if os.path.isdir(currentFile):
            files += scandirs(currentFile)
        else:
            files.append(currentFile)
    return files

def unpack_P2( src ):
        ret = []

        with open(src, 'rb') as packed_file:
        # Leitura do Header do Arquivo
            if packed_file.read(2) != 'P2':
                print 'Arquivo lido não é do tipo P2'
            else:
                print 'Desempacotando arquivo P2 - %s.' % src
                entries = struct.unpack('<H', packed_file.read(2))[0]
                if entries & 0x8000: 
                    entries = entries ^ 0x8000
                    fnt = True
                else:
                    fnt = False
                packed_file.read(8)
                base_address = struct.unpack('<L', packed_file.read(4))[0]
        # Leitura da Tabela de Endereços e Tamanhos
                names = []
                addresses = []
                sizes = []
                compress = []
                for x in range(entries):
                    address = (struct.unpack('B', packed_file.read(1))[0]<<9|struct.unpack('B', packed_file.read(1))[0]<<17)
                    addresses.append(address + base_address)
                if packed_file.tell() % 4 != 0:
                    packed_file.read(2) # Salta o dummy
                for x in range(entries):
                    size = struct.unpack('<L', packed_file.read(4))[0]
                    if size & 0x80000000:
                        size ^ 0x80000000
                        compress.append(True)
                    else:
                        compress.append(False)
                    sizes.append(size)
                if fnt == True:
                    for x in range(entries):
                        name = packed_file.read(8).replace('\x00', '')
                        names.append(name)
                                        
        # Desempacotamento dos Arquivos        
                for x in range(entries):
                
                    # Não descomprime os arquivos extraídos
                    if compress[x] == False:
                        compress[x] = "None"
                        # if fnt == True:
                            # output = open(os.path.join(unpacked_dir, '%s' %(names[x])), 'wb')               
                        # else:   
                            # output = open(os.path.join(unpacked_dir, '%s_%03d' %(f, x)), 'wb')
                            # names.append('%s_%03d' %(f, x))
                        packed_file.seek(addresses[x],0)
                        output = mmap.mmap( -1, sizes[x] )
                        output.write( packed_file.read(sizes[x]) )
                        output.seek(0)
                        ret.append( output )
                        
                        #output.write(packed_file.read(sizes[x]))
                        #output.close()
                    else:
                        # if fnt == True:
                            # output = open(os.path.join(unpacked_dir, '%s' %(names[x])), 'wb')               
                        # else:
                            # output = open(os.path.join(unpacked_dir, '%s_%03d' %(f, x)), 'wb')
                            # names.append('%s_%03d' %(f, x))
                        packed_file.seek(addresses[x], 0)
                        flag = packed_file.read(1)
                        if flag == '\x10':
                            compress[x] = "LZSS"
                            buffer = compression.lzss.uncompress(packed_file, addresses[x])         
                        elif flag == '\x11':            
                            compress[x] = "ONZ"
                            buffer = compression.onz.uncompress(packed_file, addresses[x])          
                            
                        output = mmap.mmap( -1, len(buffer) )
                        output.write( buffer.tostring() )
                        output.seek(0)
                        ret.append( output )                            
                        #buffer.tofile(output)
                        #output.close()
                    
                # with open(os.path.join(unpacked_dir, 'make.txt'), 'w') as c:
                    # for x, name in enumerate(names):
                        # c.write("%s %s\n" % (name, compress[x]))
                        
        return ret

def unpackD2KP( f ):
    
    f.seek( 0 )
    assert f.read(4) == "D2KP"
    
    f.read(4) # Dummy
    ptrs = struct.unpack( "<8L", f.read( 8 * 4 ) ) # Lê a tabela de ponteiros
    
    palettes = []
    tiles = []
    maps = []
    
    for p in ptrs:
        if p == 0xffffffff: # -1
            continue
            
        f.seek( p )
        entries = struct.unpack( "<L", f.read(4) )[0]
        ptrs2 = struct.unpack( "<%dL" % entries, f.read( entries * 4 ) ) # Lê a tabela de ponteiros
        for p2 in ptrs2:
            f.seek( p2 )
            base_address = f.tell()
            stamp = f.read(4)
            f.seek( base_address )
            
            if stamp == "RLCN": # Paleta de cores
                print ">> Extracting NCLR"
                palettes.append(formats.NCLRFormat(f))
                
            elif stamp == "RGCN": # Tileset
                print ">> Extracting NCGR"
                tiles.append(formats.NCGRFormat(f))
                
            elif stamp == "RCSN": # Tilemap
                print ">> Extracting NSCR"
                maps.append(formats.NSCRFormat(f))
    
    a = maps[0]
    b = tiles[0]
    c = palettes[0]
    table = a.scrn_table
    tiles = b.char_data
    buffer = [[] for y in range(a.chunks["SCRN"]["height"])]

    print a.chunks["SCRN"]["height"]
    print a.chunks["SCRN"]["width"]

    for i in range(len(table)):
        mapper = table[i]
        
        palette = c.pltt[mapper.palette]
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
                pos = i/(a.chunks["SCRN"]["width"]/8)
                buffer[pos*8 + z].append(palette[tile[z][w]])

    with open('nscr.bmp' , 'wb') as o:
        p = bmp.Writer(256,192,24)
        p.write(o, buffer)        
    raw_input()
        
def unpackImage( src, dst, mode ):    
    #bg_path = os.path.join(src, 'bg')
    files = filter(lambda x: x.__contains__('.p2'), scandirs(src))
        
    for _, fname in enumerate(files):
        # Retorna uma lista de memory maps com os arquivos desempacotados
        ret = unpack_P2( fname )
        print ">> Total files: ", len(ret)
        
        head, tail = os.path.split(fname)        
        path = os.path.join( dst , tail.split('.')[0] )
        if not os.path.isdir( path ):
            os.makedirs( path )
            
        for f in ret:
            stamp = f.read(4)
            if stamp == "D2KP":
                unpackD2KP( f )
        
            f.close()
 
    
    
    
                            
if __name__ == "__main__":

    import argparse
    
    os.chdir( sys.path[0] )
    #os.system( 'cls' )

    print "{0:{fill}{align}70}".format( " {0} {1} ".format( __title__, __version__ ) , align = "^" , fill = "=" )

    parser = argparse.ArgumentParser()
    parser.add_argument( '-m', dest = "mode", type = str, required = True )
    parser.add_argument( '-s', dest = "src", type = str, nargs = "?", required = True )
    parser.add_argument( '-s1', dest = "src1", type = str, nargs = "?" )
    parser.add_argument( '-d', dest = "dst", type = str, nargs = "?", required = True )
    
    args = parser.parse_args()
    
    # dump bg
    if args.mode == "e0":
        print "Unpacking background"           
        unpackImage( args.src , args.dst , args.mode )
    # insert bg
    elif args.mode == "i0": 
        print "Packing background"
        packBackground( args.src , args.dst )
    # dump ani
    elif args.mode == "e1": 
        print "Unpacking animation"
        unpackSprite( args.src , args.dst )
    # insert ani
    elif args.mode == "i1": 
        print "Packing animation"
        print args.src1
        packSprite( args.src , args.dst , args.src1 )
    else:
        sys.exit(1)                            