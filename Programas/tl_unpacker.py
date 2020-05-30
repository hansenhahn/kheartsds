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

__title__ = "KHDAYS Unpacker"
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
                print 'Unpacking P2 - %s.' % src
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

def unpackD2KP( f, dst2 ):
        
    print ">> Extracting PK2D"
    
    f.seek( 0 )
    assert f.read(4) == "D2KP"
    
    f.read(4) # Dummy
    ptrs = struct.unpack( "<8L", f.read( 8 * 4 ) ) # Lê a tabela de ponteiros
    
    palettes = []
    tiles = []
    maps = []
    
    for k, p in enumerate(ptrs):
        if p == 0xffffffff: # -1
            continue
            
        f.seek(p)
        entries = struct.unpack( "<L", f.read(4) )[0]
        ptrs2 = struct.unpack( "<%dL" % entries, f.read( entries * 4 ) ) # Lê a tabela de ponteiros
        sizes = struct.unpack( "<%dL" % entries, f.read( entries * 4 ) ) # Lê a tabela de ponteiros
        for i, p2 in enumerate(ptrs2):
            f.seek(p2)
            data = f.read(sizes[i])
            stamp = data[0:4]

            if stamp == "RLCN": # Paleta de cores
                print ">> Extracting NCLR"
                with open( os.path.join( dst2, "NCLR_%03d" % i ), "wb" ) as fd:
                    fd.write( data)
                
            elif stamp == "RGCN": # Tileset
                print ">> Extracting NCGR"
                with open( os.path.join( dst2, "NCGR_%03d" % i ), "wb" ) as fd:
                    fd.write( data)                
                
            elif stamp == "RCSN": # Tilemap
                print ">> Extracting NSCR"
                with open( os.path.join( dst2, "NSCR_%03d" % i ), "wb" ) as fd:
                    fd.write( data)   
                    
            elif stamp == "RECN":
                print ">> Extracting NCER"
                with open( os.path.join( dst2, "NCER_%03d" % i ), "wb" ) as fd:
                    fd.write( data)   
                    
            elif stamp == "RNAN":
                print ">> Extracting NANR"
                with open( os.path.join( dst2, "NANR_%03d" % i ), "wb" ) as fd:
                    fd.write( data)  
                    
            else:
                print ">> Missing " + stamp

        
def unpack( src, dst ):    
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
            
        for i, f in enumerate(ret):
            with open( os.path.join(path, "P2_%03d" % i), "wb" ) as fd:
                f.seek(0)
                fd.write(f.read())        
        
            f.seek(0)
            stamp = f.read(4)
            if stamp == "D2KP":
                dst2 = os.path.join( path, "PK2D_%03d" % i  )
                if not os.path.isdir( dst2 ):
                    os.makedirs( dst2 )            
                unpackD2KP( f, dst2 )
        
            f.close()
 
    
    
    
                            
if __name__ == "__main__":

    import argparse
    
    os.chdir( sys.path[0] )
    #os.system( 'cls' )

    print "{0:{fill}{align}70}".format( " {0} {1} ".format( __title__, __version__ ) , align = "^" , fill = "=" )

    parser = argparse.ArgumentParser()
    parser.add_argument( '-s', dest = "src", type = str, nargs = "?", required = True )
    parser.add_argument( '-d', dest = "dst", type = str, nargs = "?", required = True )
    
    args = parser.parse_args()
    
    print "Unpacking ..."        
    unpack( args.src , args.dst )
    sys.exit(1)                            