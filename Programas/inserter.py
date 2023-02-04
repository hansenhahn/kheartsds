#!/usr/bin/env python
# -*- coding: windows-1252 -*-

import re
import shutil
import os
import sys
import struct
import array
import tempfile
import codecs
import glob
import mmap
import binascii
import tl_img

from libs import compression, parser
from libs.pytable import normal_table

__title__ = "KHDAYS Text Processor"
__version__ = "2.0"

languages = ("Ingl\xc3\xaas", "Franc\xc3\xaas", "Alem\xc3\xa3o", "Italiano", "Espanhol")

TAG_MV = r'^\[MV:(.+?)\]$'
TAG_NM = r'^\[(.+?)\]$'
TAG_CH = r'(<.+?>)'
TAG_CH2 = r'^(<.+?>)$'
END = r'^!\D{30}!$'

def scandirs( path ):
    files = []
    for currentFile in glob.glob( os.path.join( path, '*' ) ):
        if os.path.isdir( currentFile ):
            files += scandirs( currentFile )
        else:
            files.append( currentFile )
    return files

def pack_P2(root = 'Arquivos PT-BR/Unpacked P2',
            outdir = 'Arquivos PT-BR/P2',
            extension = '.p2',
            has_fnt = False):

    for dir in os.listdir(root):
        if not dir.endswith(".p2"):
            continue
    
        if not os.path.isdir( os.path.join(root, dir) ):
            continue
        
        try:
            with open(os.path.join(root, dir, 'Makefile'), 'r') as makefile:
                nametable = makefile.readlines()
        except:
            continue
            
        origin = nametable.pop(0)
        entries = len(nametable)
        
        base_address = entries * 6 + 16
        if base_address % 4 != 0: base_address += 2
        
        if has_fnt:
            base_address += entries * 8
        
        while base_address % 0x200 != 0: base_address += 1
        
        extension2 = extension
        head, tail = os.path.split(dir)
        tail = tail.replace("__", "")
        if extension2 == "":
            tail = tail.split('.')[0]
        elif extension2 in tail:
            extension2 = ""

        output = open(os.path.join(outdir, head, tail) + extension2, 'wb')
        output.write('P2')

        if has_fnt:
            output.write(struct.pack('<H', entries | 0x8000))
        else:
            output.write(struct.pack('<H', entries))
        # Se quer FNT??
        output.seek(8, 1)
        output.write(struct.pack('<L', base_address))
        
        names = []
        addresses = [] # (Endereço, Tamanho)
        sizes = []
        
        address = base_address
        for file_name in nametable:
            file_name = file_name.strip('\r\n')
            
            a = re.match(r'^(.+?);(.+?);(.+?)$', file_name)
            name, comp, size = a.groups()
            
            compress = False
            if comp != "None":
                compress = True
        
            print "Adicionando %s em %s." % (name, output.name)
            output.seek(address, 0)
        
            if compress and not name.lower().endswith(".z"):
                name += ".z"
                
            input = open(os.path.join(root, dir, name), 'rb')
            if compress:
                if comp == "lz10":
                    buffer = compression.lzss.compress(input)
                elif comp == "lz11":
                    buffer = compression.onz.compress(input)
            else:
                buffer = array.array('c', input.read())
                
            buffer.tofile(output)   
            input.close()
            
            addresses.append((address - base_address))
            if compress:
                sizes.append(len(buffer) | 0x80000000)
            else:
                sizes.append(len(buffer))           
            address += len(buffer)
            while address % 0x200 != 0:
                address += 1
                output.write("\x00")
            
            names.append(name)
            
        output.seek(0x10, 0)
        for address in addresses:
            output.write(struct.pack('B', ((address & 0x1fe00) >> 9)))
            output.write(struct.pack('B', (address >> 17)))
        if output.tell() % 4 != 0: output.write("\x00\x00")
        for size in sizes:
            output.write(struct.pack('<L', size))
        
        if has_fnt == True:
            for name in names:
                while len(name) != 8 :
                    name += '\x00'
                output.write('%s' % name)


        output.close()

def pack_CAKP(root = '../Textos PT-BR/CAKP', outdir = '../Arquivos PT-BR/Unpacked CAKP'):
    table = normal_table('tabela2.tbl')
    table.fill_with('61=a', '41=A', '30=0')
    table.add_items('0A=\n')
    
    table.set_mode('inverted')
    # Funcionando Perfeitamente

    if os.path.isdir(root):
        files = filter(lambda x: re.match(r'^(.+?)\.txt$', x), scandirs(root))
        #files = filter(lambda x: re.match(r'^(.+?)lbcmn\.txt$', x), scandirs(root))
    else:
        files = [root,]

    for _, fname in enumerate(files):   
        path = fname[len(root):]
        fdirs = outdir + path[:-len(os.path.basename(path))]
        
        with open( fname, 'r') as input:
            filepath = outdir + fname[len(root):].replace(".txt", "")    
            print filepath
            output = open( filepath, "r+b")
            parser.generic_inserter_1(input, output, table)
            output.close()   
            
    for _dir in os.listdir(outdir):        
        if not _dir.startswith("__"):
            continue
            
        #try:
        print os.path.join(outdir, _dir, 'Makefile')
        with open(os.path.join(outdir, _dir, 'Makefile'), 'r') as makefile:
                nametable = makefile.readlines()
        #except:
        #    continue
            
        _, origin = nametable.pop(0).strip('\r\n').split(':')
        entries = len(nametable)
        
        name_info = []
        files = []
        for file_name in nametable:
            file_name = file_name.strip('\r\n')
            
            a = re.match(r'^(.+?);(.+?);(.+?)$', file_name)
            name, comp, size = a.groups()
            name_info.append(name)
            with open(os.path.join(outdir, _dir, name), 'rb') as file:
                print os.path.join(outdir, _dir, name)
                files.append(file.read())
                
        print "Empacotando %s." % origin
        #raw_input()
                
        pst = 0x34
        pst += 4 * (2*len(files) + 1)
        while pst % 0x20 != 0: pst += 1
        
        fat_start = pst
        
        pst += 2 * (len(name_info) + 1)
        names = []
        init = 2 * (len(name_info) + 1)
        for name in name_info:
            names.append(init)
            init += len(name) + 1
            pst += len(name) + 1
                        
        while pst % 0x20 != 0: pst += 1
        
        sizes = []
        addresses = []
        for file in files:
            sizes.append(len(file))
            addresses.append(pst)
            pst += len(file)
            while pst % 0x20 != 0: pst += 1
        
        with open(os.path.join(outdir, origin), 'wb') as f:
            f.write('CAKP')
            f.write('\x00\x00\x00\x00')
            f.write(struct.pack('<L', 0x28))
            f.write(struct.pack('<L', 0x34))
            f.write('\xFF\xFF\xFF\xFF' * 6)
            f.write(struct.pack('<L', 0x01))
            f.write(struct.pack('<L', fat_start))
            
            f.write(struct.pack('<L', init))
            
            f.write(struct.pack('<L', len(files)))
            # Escreve os endereços
            for address in addresses:
                f.write(struct.pack('<L', address))
            # Escreve os tamanhos
            for size in sizes:
                f.write(struct.pack('<L', size))
                
            f.seek(fat_start, 0)
            f.write(struct.pack('<H', len(names)))
            # Escreve os endereços fnt
            for addr in names:
                f.write(struct.pack('<H', addr))
            # Escreve os nomes dos arquivos
            for name in name_info:       
                f.write('%s\x00' % name)
            while f.tell() % 0x20 != 0: f.write("\x00")
            
            # Escreve os arquivos
            for file in files:
                f.write(file)
                while f.tell() % 0x20 != 0: f.write("\x00")
                

def pack_GNRC(root = '../Textos PT-BR/P2',
              outdir = '../Arquivos PT-BR/Unpacked P2',
              first_onz = False):
    table = normal_table('tabela2.tbl')
    table.fill_with('61=a', '41=A', '30=0')
    table.add_items('0A=\n')
    
    table.set_mode('inverted')
    
    if os.path.isdir(root):
        files = filter(lambda x: re.match(r'^(.+?)\.txt$', x), scandirs(root))
    else:
        files = [root,]

    for _, fname in enumerate(files):
        
        path = fname[len(root):]
        fdirs = outdir + path[:-len(os.path.basename(path))]
        
        # if not os.path.isdir(fdirs):
            # os.makedirs(fdirs)    

        with open( fname, 'r') as input:
            filepath = outdir + fname[len(root):].replace(".txt", "")    
            print filepath
            output = open( filepath, "r+b")
            parser.generic_inserter_1(input, output, table)
            output.close()
            
def pack_dat(root, outdir):
    table = normal_table('tabela3.tbl')
    table.fill_with('0061=a', '0041=A', '0030=0')
    table.add_items('000A=\n')
    
    table.set_mode('inverted')
    
    files = [root]
    root = os.path.dirname(root)

    for _, fname in enumerate(files):
        path = fname[len(root):]
        fdirs = outdir + path[:-len(os.path.basename(path))]
        if not os.path.isdir(fdirs):
            os.makedirs(fdirs)    

            
        print "Inserindo %s." % fname

        with open( fname, 'r') as input:
            filepath = outdir + fname[len(root):].replace(".txt", "")
            output = open( filepath, "wb")
            buffer = []
            size = []
            block = array.array('c')
            data = array.array('c')
            header = array.array('c')
            for line in input:
                line = line.strip('\r\n')
                line = line.decode('utf-8').encode('windows-1252')
                if line == '!******************************!':
                    block.pop() # \x0a
                    block.pop() # \x00
                    block.extend('\x00\x00')
                    if (len(block)) % 4 != 0:
                        block.extend('\x00\x00')
                    size.append(len(block))
                    data.extend(struct.pack('<L', len(block)+4))
                    data.extend(block)
                    
                    buffer.append((size, data, header))
                    
                    size = []
                    data = array.array('c')
                    block = array.array('c')
                    header = array.array('c')
                    
                elif line == '!------------------------------!':
                    block.pop() # \x0a
                    block.pop() # \x00
                    block.extend('\x00\x00')
                    if (len(block)) % 4 != 0:
                        block.extend('\x00\x00')

                    size.append(len(block))
                    if len(size) > 1:
                        data.extend(struct.pack('<L', len(block)+4))
                    data.extend(block)
                    block = array.array('c')

                elif line.startswith('[') and line.endswith(']'):
                    header.extend(binascii.unhexlify(line[1:-1]))
                
                else:
                    splited = re.split(TAG_CH, line)
                    for word in splited:
                        tag = re.match(TAG_CH2, word)
                        if tag:
                            tag = tag.groups()[0]
                            if tag in table:
                                block.extend(table[tag][::-1])
                            else:
                                block.extend(struct.pack("<H", int(tag[1:-1],16)))
                        else:
                            for c in word:
                                block.extend(c+"\x00")
                    block.extend('\x0a\x00')
            
            output.write(struct.pack('<L', 0x08))            
            output.write(struct.pack('<L', len(buffer)))
            ptr = 0
            
            for size, block, header in buffer:
                output.write(struct.pack("<L", len(header)+len(block)+12))
                output.write(struct.pack("<L", 12+len(header)))
                output.write(struct.pack("<L", 12+len(header)+size[0]))                
                header.tofile(output)
                block.tofile(output)
            
            output.close()            
            
def pack_rpt(root, outdir):
    table = normal_table('tabela3.tbl')
    table.fill_with('0061=a', '0041=A', '0030=0')
    table.add_items('000A=\n')
    
    table.set_mode('inverted')
    
    files = [root]
    root = os.path.dirname(root)

    for _, fname in enumerate(files):
        path = fname[len(root):]
        fdirs = outdir + path[:-len(os.path.basename(path))]
            
        print "Comprimindo %s." % fname

        with open( fname, 'r') as input:
            filepath = outdir + fname[len(root):].replace(".txt", "")
            output = open( filepath, "wb")
            buffer = []
            size = [0,]
            block = array.array('c')
            header = array.array('c')
            for line in input:
                line = line.strip('\r\n')
                line = line.decode('utf-8').encode('windows-1252')
                if line == '!******************************!':
                    block.pop() # \x0a
                    block.pop() # \x00
                    block.extend('\x00\x00')
                    size.append(len(block)-sum(size))
                    
                    buffer.append((size, block, header))
                    
                    size = [0,]
                    block = array.array('c')
                    header = array.array('c')
                    
                elif line == '!------------------------------!':
                    block.pop() # \x0a
                    block.pop() # \x00
                    block.extend('\x00\x00')                
                    size.append(len(block)-sum(size))

                elif line.startswith('[') and line.endswith(']'):
                    header.extend(binascii.unhexlify(line[1:-1]))
                
                else:
                    splited = re.split(TAG_CH, line)
                    for data in splited:
                        tag = re.match(TAG_CH2, data)
                        if tag:
                            tag = tag.groups()[0]
                            if tag in table:
                                block.extend(table[tag][::-1])
                            else:
                                block.extend(struct.pack("<H", int(tag[1:-1],16)))
                        else:
                            for c in data:
                                block.extend(c+"\x00")
                    block.extend('\x0a\x00')
                    
            output.write(struct.pack('<L', len(buffer)))
            ptr = 0
            
            for size, block, header in buffer:
                header.tofile(output)
                output.write(struct.pack("<H", size[1]/2))
                output.write(struct.pack("<H", size[2]/2))
                output.write(struct.pack("<H", size[3]/2))                
                
                output.write(struct.pack("<L", ptr/2))
                ptr += size[1]
                output.write(struct.pack("<L", ptr/2))
                ptr += size[2]
                output.write(struct.pack("<L", ptr/2))
                ptr += size[3]

            output.seek(4+20*len(buffer))
            for size, block, header in buffer:
                block.tofile(output)
            
            output.close()



def pack_db(root, outdir):
    table = normal_table('tabela3.tbl')
    table.fill_with('0061=a', '0041=A', '0030=0')
    table.add_items('000A=\n')
    
    table.set_mode('inverted')
    
    if os.path.isdir(root):
        files = filter(lambda x: x.__contains__('db_'), scandirs(root))
    else:
        files = [root]
        root = os.path.dirname(root)

    for _, fname in enumerate(scandirs(root)):
        path = fname[len(root):]
        fdirs = outdir + path[:-len(os.path.basename(path))]
        
        if not os.path.basename(path).startswith('db'):
            continue   
        if not os.path.isdir(fdirs):
            os.makedirs(fdirs)  
            
        print "Comprimindo %s." % fname

        with open( fname, 'r') as input:
            filepath = outdir + fname[len(root):].replace(".txt", "")
            output = open( filepath, "wb")
            buffer = []
            block = array.array('c')
            for line in input:
                line = line.strip('\r\n')
                line = line.decode('utf-8').encode('windows-1252')
                if line == '!******************************!':
                    block.pop() # \x0a
                    block.pop() # \x00
                    block.extend('\x00\x00')
                    if (len(block)+2) % 4 != 0:
                        block.extend('\x00\x00')
                    
                    buffer.append(block)
                    block = array.array('c')
               
                else:
                    splited = re.split(TAG_CH, line)
                    for data in splited:
                        tag = re.match(TAG_CH2, data)
                        if tag:
                            tag = tag.groups()[0]
                            if tag in table:
                                block.extend(table[tag][::-1])
                            else:
                                block.extend(struct.pack("<H", int(tag[1:-1],16)))
                        else:
                            for c in data:
                                block.extend(c+"\x00")
                    block.extend('\x0a\x00')
            
            output.write(struct.pack('<L', len(buffer)))
            ptr = 0
            for block in buffer:
                ptr += len(block)
                output.write(struct.pack('<L', ptr))
            for block in buffer:
                block.tofile(output)
            
            output.close()
            
def pack_msi(root, outdir):
    table = normal_table('tabela3.tbl')
    table.fill_with('0061=a', '0041=A', '0030=0')
    table.add_items('000A=\n')
    
    table.set_mode('inverted')
    
    files = [root]
    root = os.path.dirname(root)
    
    for _, fname in enumerate(files):
        path = fname[len(root):]
        fdirs = outdir + path[:-len(os.path.basename(path))]
            
        print "Comprimindo %s." % fname

        with open( fname, 'r') as input:
            filepath = outdir + fname[len(root):].replace(".txt", "")
            output = open( filepath, "wb")
            buffer = []
            block = array.array('c')
            for line in input:
                line = line.strip('\r\n')
                line = line.decode('utf-8').encode('windows-1252')
                if line == '!******************************!':
                    block.pop() # \x0a
                    block.pop() # \x00
                    block.extend('\x00\x00')
                    size = len(block)+2
                    
                    buffer.append((size, block))
                    
                    block = array.array('c')
                    
                elif line == '!------------------------------!':
                    block.pop() # \x0a
                    block.pop() # \x00
                    block.extend('\x00\x00')                

                elif line.startswith('[') and line.endswith(']'):
                    block.extend(binascii.unhexlify(line[1:-1]))
                
                else:
                    splited = re.split(TAG_CH, line)
                    for data in splited:
                        tag = re.match(TAG_CH2, data)
                        if tag:
                            tag = tag.groups()[0]
                            if tag in table:
                                block.extend(table[tag][::-1])
                            else:
                                block.extend(struct.pack("<H", int(tag[1:-1],16)))
                        else:
                            for c in data:
                                block.extend(c+"\x00")
                    block.extend('\x0a\x00')
                    
            output.write(struct.pack('<H', len(buffer)))

            for size, block in buffer:
                output.write(struct.pack("<H", size))
                block.tofile(output)
            
            output.close()                    
                    

def pack_map(root, outdir):

    if os.path.isdir(root):
        files = filter(lambda x: x.__contains__('map_'), scandirs(root))
    else:
        files = [root]
        root = os.path.dirname(root)
                
    for _, fname in enumerate(scandirs(root)):
        path = fname[len(root):]
        fdirs = outdir + path[:-len(os.path.basename(path))]
        
        if not os.path.basename(path).startswith('map'):
            continue   
        if not os.path.isdir(fdirs):
            os.makedirs(fdirs)  
            
        print "Comprimindo %s." % fname

        with open( fname, 'r') as input:
            filepath = outdir + fname[len(root):].replace(".txt", "")
            output = open( filepath, "wb")
            buffer = []
            block = array.array('c')
            for line in input:
                line = line.strip('\r\n')
                line = line.decode('utf-8').encode('windows-1252')
                if line == '!******************************!':
                    block.pop() # \x0a
                    block.pop() # \x00
                    block.extend('\x00\x00')
                    if (len(block)+2) % 4 != 0:
                        block.extend('\x00\x00')
                    
                    buffer.append(block)
                    block = array.array('c')
                elif line.startswith('[') and line.endswith(']'):
                    block.extend(binascii.unhexlify(line[1:-1]))
                
                else:
                    splited = re.split(TAG_CH, line)
                    for data in splited:
                        tag = re.match(TAG_CH2, data)
                        if tag:
                            tag = tag.groups()[0]
                            if tag in table:
                                block.extend(table[tag][::-1])
                            else:
                                block.extend(struct.pack("<H", int(tag[1:-1],16)))
                        else:
                            for c in data:
                                block.extend(c+"\x00")
                    block.extend('\x0a\x00')
                    
            for block in buffer:
                output.write(struct.pack('<L', len(block)+6))
                output.write(struct.pack('<H', 0x18))
                block.tofile(output)
            
            output.write("\xff\xff")
            output.close()

            
                
def pack_Z( root = '../Textos PT-BR/P2',
            outdir = '../Arquivos PT-BR/Unpacked P2'):

    files = filter(lambda x: re.match(r'^(.+?)\.z$', x), scandirs(root))        
    for _, fname in enumerate(files):
        # arquivos .z dentro de pastas com extensão .p2 são comprimidos dentro do próprio empacotador p2
        if ".p2" in fname:
            continue
        
        path = fname[len(root):]
        fdirs = outdir + path[:-len(os.path.basename(path))]
        if not os.path.isdir(fdirs):
            os.makedirs(fdirs)    

        with open( fname, 'r') as input:
            filepath = outdir + fname[len(root):].replace(".txt", "")

            print "Comprimindo %s." % fname
            buffer = compression.onz.compress(input)

            output = open( filepath, "wb")
            buffer.tofile(output)
            output.close()
            
 # *********************** WIP *********************** #
def pack_S(root = '../Textos PT-BR/P2', outdir = '../Arquivos PT-BR/Unpacked P2'):
    table = normal_table('tabela3.tbl')
    table.fill_with('0061=a', '0041=A', '0030=0')
    table.add_items('000A=\n')
    
    table.set_mode('inverted')
    #files = filter(lambda x: re.match(r'^.+?(\.s).*?(\.txt)$', x), scandirs(root))
    
    if os.path.isdir(root):
        files = filter(lambda x: re.match(r'^.+?(\.s).*?(\.txt)$', x), scandirs(root))
    else:
        files = [root]
        root = os.path.dirname(root)   
    
    
    for _, fname in enumerate(files):
        print "Inserindo %s." % fname
        path = fname[len(root):]
        fdirs = outdir + path[:-len(os.path.basename(path))]
        if not os.path.isdir(fdirs):
            os.makedirs(fdirs)    

        with open( fname, 'r') as input:
            filepath = outdir + fname[len(root):].replace(".txt", "")
            output = open( filepath, "wb")
            buffer = []
            block = array.array('c')
            for line in input:
                line = line.strip('\r\n')
                line = line.decode('utf-8').encode('windows-1252')
                if line == '!******************************!':
                    block.pop()
                    block.pop()
                    block.extend('\x00\x00')
                    buffer.append(block)
                    block = array.array('c')
                else:
                    splited = re.split(TAG_CH, line)
                    for data in splited:
                        tag = re.match(TAG_CH2, data)
                        if tag:
                            tag = tag.groups()[0]
                            if tag in table:
                                block.extend(table[tag][::-1])
                            else:
                                block.extend(struct.pack("<H", int(tag[1:-1],16)))
                        else:
                            for c in data:
                                block.extend(c+"\x00")
                    block.extend('\x0a\x00')

                    
            output.write(struct.pack("<L", 8))
            output.write(struct.pack('<L', len(buffer)))
            for block in buffer:
                output.write(struct.pack('<L', len(block)+4))
                block.tofile(output)
            
            output.close()

     
if __name__ == '__main__':
    import argparse
    
    os.chdir( sys.path[0] )
    #os.system( 'cls' )

    print "{0:{fill}{align}70}".format( " {0} {1} ".format( __title__, __version__ ) , align = "^" , fill = "=" )

    aparser = argparse.ArgumentParser()
    aparser.add_argument( '-m', dest = "mode", type = str, required = True )
    aparser.add_argument( '-s', dest = "src", type = str, nargs = "?", required = True )
    aparser.add_argument( '-s1', dest = "src1", type = str, nargs = "?" )
    aparser.add_argument( '-d', dest = "dst", type = str, nargs = "?" )
    aparser.add_argument( '-d1', dest = "dst1", type = str, nargs = "?" )
    aparser.add_argument( '-ext' , dest = "ext", type = str, nargs = "?", required = False, default = "" )
    aparser.add_argument( '-fnt' , dest = "has_fnt", action = "store_true" )
    
    args = aparser.parse_args()
    
    if args.mode == "cakp":
        print "Packing CAKP text"
        pack_CAKP(root = args.src , outdir = args.dst )
        #pack_P2(root = args.src1, outdir = args.dst, extension = args.ext, has_fnt = args.has_fnt)
        
    elif args.mode == ".map":
        print "Packing map text"
        pack_map(args.src , args.dst)  
    elif args.mode == ".db":
        print "Packing db text"
        pack_db(args.src , args.dst)
    elif args.mode == ".rpt.z":
        print "Packing .rpt.z text"        
        pack_rpt(args.src , args.src1)
        pack_Z(root = args.src1 , outdir = args.dst )
    elif args.mode == ".msi.z":
        print "Packing .msi.z text"        
        pack_msi(args.src , args.src1)
        pack_Z(root = args.src1 , outdir = args.dst )        
        
    elif args.mode == ".dat.z":
        print "Packing .dat text"        
        pack_dat(args.src , args.src1)        
        pack_Z(root = args.src1 , outdir = args.dst )
    elif args.mode == "gnrc": 
        print "Packing GNRC text"
        pack_GNRC(root = args.src , outdir = args.src1 )
        pack_P2(root = args.src1, outdir = args.dst, extension = args.ext, has_fnt = args.has_fnt)
    elif args.mode == ".p2": 
        print "Packing .p2 files"
        pack_P2(root = args.src, outdir = args.dst, extension = args.ext, has_fnt = args.has_fnt)
    elif args.mode == ".noext":
        print "Packing .noext text"
        pack_GNRC(root = args.src , outdir = args.dst1 )
        #pack_Z(root = args.src1 , outdir = args.dst )
    elif args.mode == ".s.z":
        print "Packing .s.z text"
        pack_S(root = args.src , outdir = args.src1 )
        pack_Z(root = args.src1 , outdir = args.dst )
    elif args.mode == ".z":
        print "Packing .z"
        pack_Z(root = args.src , outdir = args.dst )
        
    elif args.mode == ".pk2d.z":
        print "Packing .pk2d.z"
        
        tl_img.packBackground(args.src)
        
    else:
        sys.exit(1)
        
    
        
                        


    
    