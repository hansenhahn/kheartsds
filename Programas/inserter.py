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
        
        head, tail = os.path.split(dir)
        tail = tail.replace("__", "")
        
        output = open(os.path.join(outdir, head, tail) + extension, 'wb')
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
            while address % 0x200 != 0: address += 1
            
            names.append(name)
            
        output.seek(0x10, 0)
        for address in addresses:
            output.write(struct.pack('B', ((address & 0x1fe00) >> 9)))
            output.write(struct.pack('B', (address >> 17)))
        if output.tell() % 4 != 0: output.seek(2,1)
        for size in sizes:
            output.write(struct.pack('<L', size))
        
        if has_fnt == True:
            for name in names:
                output.write('%s\x00' % name)
                while output.tell() % 8 != 0: output.seek(1,1)

        output.close()

def pack_CAKP(root = '../Textos PT-BR/CAKP', outdir = '../Arquivos PT-BR/Unpacked CAKP'):
    table = normal_table('tabela2.tbl')
    table.fill_with('61=a', '41=A', '30=0')
    table.add_items('0A=\n')
    
    table.set_mode('inverted')
    # Funcionando Perfeitamente

    for _dir in os.listdir(root):
    
        _out = os.path.join( outdir, _dir)
        dir = os.path.join(root, _dir)
        
        if not os.path.isdir(_out):
            os.mkdir(_out)
        
        for _folder in os.listdir(dir):
            folder = os.path.join(dir, _folder)
            
            if os.path.isdir(folder):
                
                for f in os.listdir(folder):
                    if f != 'make.txt':
                        a = re.match(r'^(.+?)\.txt$', f)
                        if a:
                            with open(os.path.join(folder, f), 'r') as input:
                                output = open(os.path.join(folder, a.groups()[0]), 'r+b')
                                parser.generic_inserter_1(input, output, table)
                                output.close()
                        else:
                            pass
            
                nametable = []
                
                if not os.path.isdir( folder ):
                    continue
                
                with open(os.path.join(folder, 'make.txt'), 'r') as makefile:
                    for file in makefile.readlines():
                        nametable.append(file.strip('\r\n'))
                
                files = []
                for name in nametable:
                    with open(os.path.join(folder, name), 'rb') as file:
                        print os.path.join(folder, name)
                        
                        files.append(file.read())
                
                print "Empacotando %s." % folder
                #raw_input()
                        
                pst = 0x34
                pst += 4 * (2*len(files) + 1)
                while pst % 0x20 != 0: pst += 1
                
                fat_start = pst
                
                pst += 2 * (len(nametable) + 1)
                names = []
                init = 2 * (len(nametable) + 1)
                for name in nametable:
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
                
                with open(os.path.join(_out, _folder), 'wb') as f:
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
                    for name in nametable:
                        f.write('%s\x00' % name)
                    while f.tell() % 0x20 != 0: f.seek(1, 1)
                    
                    # Escreve os arquivos
                    for file in files:
                        f.write(file)
                        while f.tell() % 0x20 != 0: f.seek(1, 1)

            else:
                print "Copiando %s" % folder
                shutil.copy(folder, os.path.join(_out, _folder))
                
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
    print root
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
    
    
    
    
    # for _dir in os.listdir(root):
        # out = os.path.join( outdir, _dir)
        # dir = os.path.join(root, _dir)
        
        # if not os.path.isdir(out):
            # os.makedirs(out)
            
        # for f in os.listdir(dir):
            # a = re.match(r'^(.+?)\.txt$', f)
            # if a:
                # with open(os.path.join(dir, f), 'r') as input:
                    # output = open(os.path.join(out, a.groups()[0]), 'r+b')
                    # parser.generic_inserter_1(input, output, table)
                    # output.close()
            # else:
                # pass                
                
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
    files = filter(lambda x: re.match(r'^.+?(\.s).*?(\.txt)$', x), scandirs(root))       
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

        
# def insert_P2(root = 'Textos PT-BR/P2'):

    # for _dir in os.listdir(root):
    
        # base = os.path.join('Arquivos/Unpacked P2', _dir)
        # out = os.path.join('Arquivos PT-BR/Unpacked P2', _dir)
        # dir = os.path.join(root, _dir)        
        
        # if not os.path.isdir(out):
            # os.mkdir(out)
        
        # for file_name in os.listdir(dir):
            # input = open(os.path.join(dir, file_name), 'r')
    
            # texts = []
            # files = []
            # structs = []
            
            # for line in input:
                # line = line.strip('\r\n')
                # line = line.replace('\xef\xbb\xbf','')
                # if re.match(END, line):
                    # pass
                # elif re.match(TAG_MV, line):
                    # a = re.match(TAG_MV, line)
                    # files.append(a.groups()[0]+'\x00')
                # elif re.match(TAG_NM, line):
                    # a = re.match(TAG_NM, line)
                    # string = ""
                    # for x in range(len(a.groups()[0])/2):
                        # string += chr(int(a.groups()[0][2*x:(2*x)+2], 16))
                    # string += '\x0f'
                    # structs.append(string)
                # else:
                    # splited = re.split(TAG_CH, line)
                    # string = ""
                    # for data in splited:
                        # tag = re.match(TAG_CH2, data)
                        # if not tag:
                            # string += data
                        # else:
                            # tag = tag.groups()[0]
                            # string += chr(int(tag, 16))
                    # string += '\x00'
                    # texts.append(string)

            # input.close()
                        
            # pointers_files = []
            # pointers_texts = []
            # pointers_structs = []
            
            # Arquivo de saída
            # name = file_name.split('.')[0]
            
            # file = open(os.path.join(out, name), 'wb')
            # input = open(os.path.join(base, name), 'rb')
    
            # base_address = struct.unpack('<L', input.read(4))[0]

            # file.seek(base_address, 0)
            # for x in range(len(files)):
                # pointers_files.append(file.tell() - base_address)
                # file.write(files[x])
                # while file.tell() % 4 != 0: file.write('\x00')
                
            # for x in range(len(texts)):
                # pointers_texts.append(file.tell() - base_address)
                # file.write(texts[x])
                # while file.tell() % 4 != 0: file.write('\x00')
            
            # for x in range(len(structs)):
                # pointers_structs.append(file.tell() - base_address)
                # file.write(structs[x])
                # while file.tell() % 4 != 0: file.write('\x00')
            
            # file.seek(0,0)
            # file.write(struct.pack('<L', base_address))
            
            # while True:
                # flag = input.read(2)
                # size = struct.unpack('<H', input.read(2))[0] & 0xFF
                # if flag == '\x00\x03':
                    # file.write(flag)
                    # file.write(struct.pack('<H', size))
                    # break
                # elif flag == '\x03\x02':
                    # file.write(flag)
                    # file.write(struct.pack('<H', size))
                    # for x in range(3):
                        # file.write(input.read(4))
                        # input.read(4)         
                        # file.write(struct.pack('<L', pointers_files.pop(0)))
                # elif flag == '\x03\x01':
                    # file.write(flag)
                    # file.write(struct.pack('<H', size))   
                    # file.write(input.read(4))
                    # file.write(struct.pack('<L', pointers_texts.pop(0)))
                    # input.read(4)
                # elif flag == '\x00\x05':
                    # file.write(flag)
                    # file.write(struct.pack('<H', size))

                    # file.write(struct.pack('<L', pointers_structs.pop(0)))
                    # input.read(4)
                    # file.write(input.read(4))                 
                # else:
                    # file.write(flag)
                    # file.write(struct.pack('<H', size))

                    # for x in range(size-1):
                        # file.write(input.read(4))


            # input.close()
            # file.close()
    
    # file = open('m_000.bin', 'rb')    
    
    
    # with open('out.bin', 'wb') as f:
        # buffer = compression.onz.compress(file)
        # buffer.tofile(f)
    
    # file.close()
                
     
# if __name__ == '__main__':
    # # insert_P2()
    # # pack_P2()
    # #insert_S()
    
# # Para gerar os arquivos dos diálogos sem avatar
    # pack_CAKP(root = "../Textos Traduzidos/mi/mi")
    # pack_P2(root = '../Arquivos PT-BR/Unpacked CAKP', outdir = '../Arquivos PT-BR/CAKP', extension = '', has_fnt = True)
    
# # # Para gerar os arquivos dos diálogos com avatar
    # pack_GNRC(root = "../Textos Traduzidos/ev")
    # # # Os arquivos m tem fnt
    # #pack_P2(root = '../Arquivos PT-BR/Unpacked P2', outdir = 'Arquivos PT-BR/P2', extension = '.p2', has_fnt = True)
    # # # OS demais arquivos não
    # pack_P2(root = '../Arquivos PT-BR/Unpacked P2', outdir = '../Arquivos PT-BR/P2', extension = '.p2', has_fnt = False)
    # sys.exit(0)
     
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
        pack_CAKP(root = args.src , outdir = args.src1 )
        pack_P2(root = args.src1, outdir = args.dst, extension = args.ext, has_fnt = args.has_fnt)
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
    else:
        sys.exit(1)
        
    
        
                        


    
    