#!/usr/bin/env python
# -*- coding: windows-1252 -*-

import os
import sys
import struct
import array
import tempfile
import glob
import mmap
import shutil
import re
import binascii
import tl_img

#from pytable import normal_table
from libs import compression, parser, normal_table

__title__ = "KHDAYS Text Processor"
__version__ = "2.0"

languages = ("Ingl\xc3\xaas", "Franc\xc3\xaas", "Alem\xc3\xa3o", "Italiano", "Espanhol")

def scandirs( path ):
    files = []
    for currentFile in glob.glob( os.path.join( path, '*' ) ):
        if os.path.isdir( currentFile ):
            files += scandirs( currentFile )
        else:
            files.append( currentFile )
    return files
# unpack_P2 - 100%
# 
def unpack_P2(root = 'Arquivos/P2', outdir = 'Arquivos/Unpacked P2'):

    files = scandirs(root)
    
    for _, fname in enumerate(files):
        with open( fname, 'rb') as packed_file:
            # Leitura do Header do Arquivo
            if packed_file.read(2) != 'P2':
                print 'Arquivo lido n�o � do tipo P2'
                
            else:
                print 'Desempacotando arquivo P2 - %s.' %fname
                path = fname[len(root):]
                head, tail  = os.path.split(fname)        
                
                unpacked_dir = outdir + path[:-len(os.path.basename(path))] + "__" + tail
                if not unpacked_dir.endswith(".p2"):
                    unpacked_dir += ".p2"

                if not os.path.isdir(unpacked_dir):
                    os.makedirs(unpacked_dir)                   
            
                entries = struct.unpack('<H', packed_file.read(2))[0]
                if entries & 0x8000: 
                    entries = entries ^ 0x8000
                    fnt = True
                else:
                    fnt = False
                packed_file.read(8)
                base_address = struct.unpack('<L', packed_file.read(4))[0]
                
                # Leitura da Tabela de Endere�os e Tamanhos
                names = []
                addresses = []
                sizes = []
                sizes_unc = []
                compress = []
                for x in range(entries):
                    address = (struct.unpack('B', packed_file.read(1))[0]<<9|struct.unpack('B', packed_file.read(1))[0]<<17)
                    addresses.append(address + base_address)
                if packed_file.tell() % 4 != 0:
                    packed_file.read(2) # Salta o dummy
                for x in range(entries):
                    size = struct.unpack('<L', packed_file.read(4))[0]
                    if size & 0x80000000:
                        size = size & 0x7fffffff
                        compress.append(True)
                    else:
                        compress.append(False)
                    sizes.append(size)
                    sizes_unc.append(size)
                if fnt == True:
                    for x in range(entries):
                        name = packed_file.read(8).replace('\x00', '')
                        names.append(name)
                                        
                # Desempacotamento dos Arquivos
                for x in range(entries):
                    # N�o descomprime os arquivos extra�dos
                    if compress[x] == False:
                        compress[x] = "None"                         
                        
                        if fnt == True:
                            output = open(os.path.join(unpacked_dir, '%s' %(names[x])), 'wb')               
                        else:   
                            output = open(os.path.join(unpacked_dir, '%s_%03d' %(tail.replace(".p2",""), x)), 'wb')
                            names.append('%s_%03d' %(tail.replace(".p2",""), x))
                        packed_file.seek(addresses[x],0)
                        output.write(packed_file.read(sizes[x]))
                        output.close()

                    else:

                        packed_file.seek(addresses[x], 0)
                        flag = packed_file.read(1)
                        sizes_unc[x] = struct.unpack("<L", packed_file.read(3)+"\x00")[0]
                        
                        if flag == '\x10':
                            compress[x] = "lz10"
                            buffer = compression.lzss.uncompress(packed_file, addresses[x])         
                        elif flag == '\x11':            
                            compress[x] = "lz11"
                            buffer = compression.onz.uncompress(packed_file, addresses[x]) 

                        if fnt == True:
                            output = open(os.path.join(unpacked_dir, '%s' %(names[x])), 'wb')               
                        else:
                            # for�a para que tenha a extens�o .z/.Z para ser descomprimido posteriormente
                            if flag == '\x10':
                                output = open(os.path.join(unpacked_dir, '%s_%03d.Z' %(tail.replace(".p2",""), x)), 'wb')
                            elif flag == '\x11':
                                output = open(os.path.join(unpacked_dir, '%s_%03d.z' %(tail.replace(".p2",""), x)), 'wb')
                            else:
                                raise Exception()
                            names.append('%s_%03d' %(tail.replace(".p2",""), x))
                            
                        buffer.tofile(output)                       
                        output.close()
                    
                with open(os.path.join(unpacked_dir, 'Makefile'), 'w') as c:
                    c.write("Origin: %s\n" % tail)
                    for x, name in enumerate(names):
                        c.write("%s;%s;%d\n" % (name, compress[x], sizes_unc[x]))                                

def extract_S(root = "Arquivos/S"):
    table = normal_table('kh.tbl')

    for file_name in os.listdir(root):
        head, tail  = os.path.split(file_name)

        output = open(os.path.join('Textos/S', '%s.txt' %tail), 'w')    
        
        with open(os.path.join(root, file_name), 'rb') as onzfile:  
        
            print "Extraindo %s." %file_name
        
            buffer = compression.onz.uncompress(onzfile, 0)
            
            file = tempfile.NamedTemporaryFile()
            buffer.tofile(file.file)
            
            file.seek(0, 0)     
        
            stamp = struct.unpack('<L', file.read(4))[0] # Deve ser 8??
            entries = struct.unpack('<L', file.read(4))[0]
            
            for x in range(entries):            
                lenght = struct.unpack('<L', file.read(4))[0]
                
                data = struct.unpack('<H', file.read(2))[0]
                if data > 0 and data < 0x20:
                    header_size = data
                    file.read(2)
                    
                    str_lenght = struct.unpack('<L', file.read(4))[0] - header_size
                    #Imprime alguns bytes do header
                    for y in range((header_size - 12)/4):
                        output.write("[%08X]" % struct.unpack('<L', file.read(4))[0])               
                    output.write('\n')
                    total_lenght = header_size
                    
                    while True:
                        for z in range((str_lenght/2)):
                            data = file.read(2)
                            if data == '\x00\x00': #Padding
                                pass
                            elif data[::-1] in table:   # Tags
                                output.write(table[data[::-1]])
                            else:               
                                cc = unichr(struct.unpack('<H', data)[0])
                                output.write(cc.encode('utf-8'))
                        total_lenght += str_lenght
                        if total_lenght < lenght:
                            str_lenght = struct.unpack('<L', file.read(4))[0] - 4 # Menos ele mesmo
                            total_lenght += 4
                            output.write('\n!------------------------------!\n')
                        else:
                            break
                    output.write('\n!******************************!\n')
                                        
                else:
                    cc = unichr(data)
                    output.write(cc.encode('utf-8'))

                    for z in range((lenght/2) - 3):
                        data = file.read(2)
                        if data == '\x00\x00': #Padding
                            pass
                        elif data[::-1] in table:   # Tags
                            output.write(table[data[::-1]])
                        else:               
                            cc = unichr(struct.unpack('<H', data)[0])
                            output.write(cc.encode('utf-8'))
                    
                    output.write('\n!******************************!\n')
            file.close()
        output.close()
        
                        
def unpack_CAKP(root, outdir):
    if os.path.isdir(root):
        files = scandirs(root)
    else:
        files = [root]
        root = os.path.dirname(root)

    table = normal_table('tabela2.tbl')
    table.fill_with('61=a', '41=A', '30=0')
    table.add_items('0A=\n')
        
    for _, fname in enumerate(files):
        if "Makefile" in fname:
            continue
            
        path = fname[len(root):]
        fdirs = outdir + path[:-len(os.path.basename(path))]
        if not os.path.isdir(fdirs):
            os.makedirs(fdirs)    
    
        with open( fname, 'rb') as file:
            # Leitura do Header do Arquivo
            if file.read(4) != 'CAKP':
                print 'Arquivo %s n�o � do tipo CAKP. Extraindo normalmente...' % fname
               
                if 'em0' not in fname:
                    file.seek(0, 0) 
                    output = open("%s.txt" % (outdir+fname[len(root):]), 'w')
                    parser.generic_parser_1(file, output, table)
                    output.close()                
            else: 
                head,tail = os.path.split(fdirs + fname[len(root):])
                fdirs = os.path.join(head, "__"+tail)
                if not os.path.isdir(fdirs):
                    os.makedirs(fdirs)  
                    
                print 'Desempacotando arquivo CAKP - %s.' % fname
                
                head, tail  = os.path.split(fname)
                ftmp = os.path.join(head, "__"+tail)
                if not os.path.isdir(ftmp):
                    os.makedirs(ftmp)                  
                
                file.seek(40, 1) # S�o valores constantes - Ler documenta��o
                
                fnt_base_address = struct.unpack('<L', file.read(4))[0]
                fnt_size = struct.unpack('<L', file.read(4))[0]
                entries = struct.unpack('<L', file.read(4))[0]
                
                addresses = []
                for x in range(entries):
                    addresses.append(struct.unpack('<L', file.read(4))[0])
                sizes = []
                for x in range(entries):
                    sizes.append(struct.unpack('<L', file.read(4))[0])
                
                file.seek(fnt_base_address, 0)
                fnt_entries = struct.unpack('<H', file.read(2))[0]
                fnt_addresses = []
                for x in range(fnt_entries):
                    fnt_addresses.append(struct.unpack('<H', file.read(2))[0])

                fnt_names = []
                for x in fnt_addresses:
                    file.seek(fnt_base_address + x, 0)
                    name = ''
                    while True:
                        data = file.read(1)
                        if data == '\x00': break
                        else: name += data
                    fnt_names.append(name)
                    
                # Extraindo conte�do:
                make = open(os.path.join(ftmp, 'Makefile'), 'w')
                make.write("Origin:%s\n" % tail)
                for x in range(entries):
                    make.write("%s;None;%d\n" % (fnt_names[x],sizes[x]) )
                                    
                    output = open(os.path.join(ftmp, fnt_names[x]), 'wb')
                        
                    file.seek(addresses[x], 0)
                    output.write(file.read(sizes[x]))
                        
                    output.close()  
                    h,t = os.path.split(fnt_names[x])
                    #print h,t
                    #if t not in ('_i', '_e', 'chara', 'shop', 'stmi'):
                        
                    output = open(os.path.join(fdirs, fnt_names[x]) + '.txt', 'w')                                                                               
                    input = open(os.path.join(ftmp, fnt_names[x]), 'rb')
                    
                    parser.generic_parser_1(input, output, table)                           
                    
                    input.close()
                    output.close()
                        
                make.close()                                                      
                        
def unpack_Z( root, outdir ):
    if os.path.isdir(root):
        files = filter(lambda x: re.match(r'^(.+?)\.z$', x), scandirs(root)) 
    else:
        files = [root]
        root = os.path.dirname(root)
          
    for _, fname in enumerate(files):
        
        path = fname[len(root):]
        fdirs = outdir + path[:-len(os.path.basename(path))]
        if not os.path.isdir(fdirs):
            os.makedirs(fdirs)    

        with open( fname, 'rb') as input:
            filepath = outdir + fname[len(root):]
            print "Descomprimindo %s." %filepath 
            flag = input.read(1)    

            if flag == "\x10":
                buffer = compression.lzss.uncompress(input, 0)
            elif flag == "\x11":
                buffer = compression.onz.uncompress(input, 0)
            
            output = open( filepath, "wb")
            buffer.tofile(output)            
            output.close()
            
def unpack_no_ext(root, outdir, ignore_p2=False):
    if os.path.isdir(root):
        files = scandirs(root)
    else:
        files = [root]
        root = os.path.dirname(root)
        
    for _, fname in enumerate(files): 
        if ignore_p2 and ".p2" in fname:
            continue            
    
        path = fname[len(root):]
        fdirs = outdir + path[:-len(os.path.basename(path))]
        if not os.path.isdir(fdirs):
            os.makedirs(fdirs)    

        with open( fname, 'rb') as input:
            filepath = outdir + fname[len(root):]
            
            if "Makefile" in fname:
                print "Copiando Makefile"  
                shutil.copy(fname, fdirs+"Makefile")
            else:
                print "Extraindo %s" %filepath 

                table = normal_table('tabela2.tbl')
                table.fill_with('61=a', '41=A', '30=0')
                table.add_items('0A=\n')

                output = open(fdirs + os.path.basename(path) + '.txt', 'wb')
                
                parser.generic_parser_1(input, output, table)
                
                output.close()

def unpack_S( root, outdir ):
    if os.path.isdir(root):
        files = filter(lambda x: x.__contains__('.s'), scandirs(root))
    else:
        files = [root]
        root = os.path.dirname(root)
        
    for _, fname in enumerate(files):
        
        path = fname[len(root):]
        fdirs = outdir + path[:-len(os.path.basename(path))]
        if not os.path.isdir(fdirs):
            os.makedirs(fdirs)    

        with open(fname, 'rb') as fd:          
            print "Extraindo %s." %fname                

            table = normal_table('tabela3.tbl')
            table.fill_with('0061=a', '0041=A', '0030=0')
            table.add_items('000A=\n')

            output = open(fdirs + os.path.basename(path) + '.txt', 'w')                  

            pointer = struct.unpack("<L", fd.read(4))[0]
            entries = struct.unpack("<L", fd.read(4))[0]

            for _ in range(entries):
                size = struct.unpack("<L", fd.read(4))[0] - 4
                for _ in range(size/2):
                    d = struct.unpack("<H", fd.read(2))[0]
                    c = struct.pack(">H",d)
                    if c in table:
                        output.write(table[c])
                    elif d > 0:
                        output.write("<%04X>" % d)      
                
                output.write('\n!******************************!\n')

            output.close()
            
def unpack_dat( root, outdir ):
    if os.path.isdir(root):
        files = filter(lambda x: x.__contains__('.dat'), scandirs(root))
    else:
        files = [root]
        root = os.path.dirname(root)
        
    for _, fname in enumerate(files):
        
        path = fname[len(root):]
        fdirs = outdir + path[:-len(os.path.basename(path))]
        if not os.path.isdir(fdirs):
            os.makedirs(fdirs)    

        with open(fname, 'rb') as fd:          
            print "Extraindo %s." %fname                

            table = normal_table('tabela3.tbl')
            table.fill_with('0061=a', '0041=A', '0030=0')
            table.add_items('000A=\n')

            output = open(fdirs + os.path.basename(path) + '.txt', 'w')                  

            pointer = struct.unpack("<L", fd.read(4))[0]
            entries = struct.unpack("<L", fd.read(4))[0]

            for _ in range(entries):
                link = fd.tell()
                size = struct.unpack("<L", fd.read(4))[0]
                title_ptr = struct.unpack("<L", fd.read(4))[0]
                content_ptr = struct.unpack("<L", fd.read(4))[0]
                
                output.write("[" + binascii.hexlify(fd.read(link+title_ptr - fd.tell())).upper() + "]\n")
                
                fd.seek(link + title_ptr)
                while True:
                    d = struct.unpack("<H", fd.read(2))[0]
                    c = struct.pack(">H",d)
                    if c in table:
                        output.write(table[c])
                    elif d > 0:
                        output.write("<%04X>" % d)
                    if d == 0:
                        output.write('\n!------------------------------!\n')
                        break
                        
                fd.seek(link + content_ptr)
                while fd.tell() < (link + size):
                    block_link = fd.tell()
                    block_size = struct.unpack("<L", fd.read(4))[0]
                    
                    while True:
                        d = struct.unpack("<H", fd.read(2))[0]
                        c = struct.pack(">H",d)
                        if c in table:
                            output.write(table[c])
                        elif d > 0:
                            output.write("<%04X>" % d)
                        if d == 0:
                            # tamanho ou tamanho com padding
                            if (fd.tell()-link) in (size, size-2):
                                output.write('\n!******************************!\n')
                            else:
                                output.write('\n!------------------------------!\n')
                            break
                            
                    fd.seek(block_link+block_size)
                
                fd.seek(link+size)

            output.close()
        
def unpack_rpt(root,outdir):
    files = [root]
    root = os.path.dirname(root)
        
    for _, fname in enumerate(files):
        
        path = fname[len(root):]
        fdirs = outdir + path[:-len(os.path.basename(path))]
        if not os.path.isdir(fdirs):
            os.makedirs(fdirs)   

        with open(fname, 'rb') as fd:          
            print "Extraindo %s." %fname   

            table = normal_table('tabela3.tbl')
            table.fill_with('0061=a', '0041=A', '0030=0')
            table.add_items('000A=\n')

            output = open(fdirs + os.path.basename(path) + '.txt', 'w')
            
            fd.seek(0,0)
            
            entries = struct.unpack("<L", fd.read(4))[0]
            ptr = 4+20*entries
            
            for _ in range(entries):
                output.write("[" + binascii.hexlify(fd.read(2)).upper() + "]\n")
                _ = fd.read(6)
                pointer = []
                pointer = struct.unpack("<LLL", fd.read(12))
                link = fd.tell()
                
                for i, rptr in enumerate(pointer):      
                    fd.seek(ptr + rptr*2)
                    while True:
                        d = struct.unpack("<H", fd.read(2))[0]
                        if d == 0: break
                        c = struct.pack(">H",d)
                        if c in table:
                            output.write(table[c])
                        elif d > 0:
                            output.write("<%04x>" % d)
                            
                    if i in (0,1):       
                        output.write('\n!------------------------------!\n')
                    else:
                        output.write('\n!******************************!\n')              
                fd.seek(link)
                
            output.close()     

def unpack_msi(root,outdir):
    files = [root]
    root = os.path.dirname(root)
        
    for _, fname in enumerate(files):
        
        path = fname[len(root):]
        fdirs = outdir + path[:-len(os.path.basename(path))]
        if not os.path.isdir(fdirs):
            os.makedirs(fdirs)   

        with open(fname, 'rb') as fd:          
            print "Extraindo %s." %fname   

            table = normal_table('tabela3.tbl')
            table.fill_with('0061=a', '0041=A', '0030=0')
            table.add_items('000A=\n')

            output = open(fdirs + os.path.basename(path) + '.txt', 'w')
            
            fd.seek(0,0)
            
            # ??
            entries = struct.unpack("<H", fd.read(2))[0]

            for _ in range(entries):
                size = struct.unpack("<H", fd.read(2))[0]
                count = 2
                    
                output.write("[" + binascii.hexlify(fd.read(46)).upper() + "]\n")
                count += 46
                
                while count != size:
                    d = struct.unpack("<H", fd.read(2))[0]
                    count += 2
                    if d == 0: 
                        output.write('\n!------------------------------!\n')
                        continue
                    
                    c = struct.pack(">H",d)
                    if c in table:
                        output.write(table[c])
                    elif d > 0:
                        output.write("<%04x>" % d)
                            
                output.write('\n!******************************!\n')
                
            output.close()              

def unpack_map( src, dst ):

    for _, fname in enumerate(scandirs(src)):
        path = fname[len(src):]
        fdirs = dst + path[:-len(os.path.basename(path))]
        
        if not os.path.basename(path).startswith('map'):
            continue        
        
        if not os.path.isdir(fdirs):
            os.makedirs(fdirs)    

        with open(fname, 'rb') as fd:          
            if "Makefile" in fname:
                continue
                
            if fd.read(4) == "D2KP":
                continue
        
            print "Extraindo %s." %fname       

            table = normal_table('tabela3.tbl')
            table.fill_with('0061=a', '0041=A', '0030=0')
            table.add_items('000A=\n')

            output = open(fdirs + os.path.basename(path) + '.txt', 'w')
            
            fd.seek(0,0)
            
            while True:
                size = struct.unpack("<L", fd.read(4))[0]
                if size == 0xffffffff: break
                
                hdr_size = struct.unpack("<H", fd.read(2))[0]
                
                output.write("[" + binascii.hexlify(fd.read(hdr_size-6)).upper() + "]\n")
                size = size - hdr_size
                for _ in range(size/2):
                    d = struct.unpack("<H", fd.read(2))[0]
                    c = struct.pack(">H",d)
                    if c in table:
                        output.write(table[c])
                    elif d > 0:
                        output.write("<%04x>" % d)      
                
                output.write('\n!******************************!\n')            
            
            output.close()            

def unpack_db( src, dst ):

    for _, fname in enumerate(scandirs(src)):
        path = fname[len(src):]
        fdirs = dst + path[:-len(os.path.basename(path))]
        
        if not os.path.basename(path).startswith('db'):
            continue        
        
        if not os.path.isdir(fdirs):
            os.makedirs(fdirs)    

        with open(fname, 'rb') as fd:          
            print "Extraindo %s." %fname       

            table = normal_table('tabela3.tbl')
            table.fill_with('0061=a', '0041=A', '0030=0')
            table.add_items('000A=\n')

            output = open(fdirs + os.path.basename(path) + '.txt', 'w')
            
            entries = struct.unpack("<L", fd.read(4))[0]
            buffer_ptr = [struct.unpack("<L", fd.read(4))[0] for _ in range(entries)]
            
            last = 0
            for curr in buffer_ptr:
                size = curr - last
                for _ in range(size/2):
                    d = struct.unpack("<H", fd.read(2))[0]
                    c = struct.pack(">H",d)
                    if c in table:
                        output.write(table[c])
                    elif d > 0:
                        output.write("<%04x>" % d)      
                
                output.write('\n!******************************!\n')
                last = curr
            
            output.close()

import formats
def unpack_D2KP( root, outdir, img, img_args ):
    
    if os.path.isdir(root):
        files = scandirs(root)
    else:
        files = [root]
        root = os.path.dirname(root)    
    
    for _, fname in enumerate(files):
        
        with open(fname, 'rb') as f:
            print ">> Extracting PK2D"
            
            f.seek( 0 )
            assert f.read(4) == "D2KP"
            
            f.read(4) # Dummy
            ptrs = struct.unpack( "<8L", f.read( 8 * 4 ) ) # L� a tabela de ponteiros
            
            assets = {  "NCLR":[],
                        "NCGR":[],
                        "NSCR":[],
                        "NCER":[],
                        "NANR":[]        
            }            

            for k, p in enumerate(ptrs):
                if p == 0xffffffff: # -1
                    continue
                    
                f.seek(p)
                entries = struct.unpack( "<L", f.read(4) )[0]
                ptrs2 = struct.unpack( "<%dL" % entries, f.read( entries * 4 ) ) # L� a tabela de ponteiros
                sizes = struct.unpack( "<%dL" % entries, f.read( entries * 4 ) ) # L� a tabela de ponteiros
                

                
                for i, p2 in enumerate(ptrs2):
                    f.seek(p2)
                    data = f.read(sizes[i])
                    stamp = data[0:4]
                    f.seek(p2)

                    if stamp == "RLCN": # Paleta de cores
                        print ">> Extracting NCLR"
                        assets["NCLR"].append(formats.NCLRFormat(f))

                    elif stamp == "RGCN": # Tileset
                        print ">> Extracting NCGR"
                        assets["NCGR"].append(formats.NCGRFormat(f))                
                        
                    elif stamp == "RCSN": # Tilemap
                        print ">> Extracting NSCR"
                        assets["NSCR"].append(formats.NSCRFormat(f))   
                            
                    elif stamp == "RECN":
                        print ">> Extracting NCER"
                        assets["NCER"].append(formats.NCERFormat(f)) 
                            
                    elif stamp == "RNAN":
                        print ">> Extracting NANR"
                        assets["NANR"].append(data)  
                            
                    else:
                        print ">> Missing " + stamp
                
            print assets
            if img == "bg":
                tl_img.unpackBackground(assets["NCLR"][img_args[0]], assets["NSCR"][img_args[1]], assets["NCGR"][img_args[2]], outdir)
            elif img == "ani":
                #tl_img.unpackAnimation(assets["NCLR"][img_args[0]], assets["NCER"][img_args[1]], assets["NCGR"][img_args[2]], outdir)
                tl_img.unpackAnimation(None, assets["NCER"][img_args[1]], assets["NCGR"][img_args[2]], outdir)
            
if __name__ == '__main__':
    import argparse
    
    os.chdir( sys.path[0] )


    print "{0:{fill}{align}70}".format( " {0} {1} ".format( __title__, __version__ ) , align = "^" , fill = "=" )

    aparser = argparse.ArgumentParser()
    aparser.add_argument( '-m', dest = "mode", type = str, required = True )
    aparser.add_argument( '-s', dest = "src", type = str, nargs = "?", default= "" )
    aparser.add_argument( '-s1', dest = "src1", type = str, nargs = "?", default= "" )
    aparser.add_argument( '-d', dest = "dst", type = str, nargs = "?", required = True )
    aparser.add_argument( '-ext' , dest = "ext", type = str, nargs = "?", required = False, default = "" )
    aparser.add_argument( '-fnt' , dest = "has_fnt", action = "store_true" )
    aparser.add_argument( '-img' , dest = "img", type=str, required = False )
    aparser.add_argument( '-img-args' , dest = "img_args", type=int, nargs= "+", required = False )
    
    args = aparser.parse_args()
    
    if args.mode == "cakp":
        print "Unpacking cakp container"
        unpack_CAKP(root = args.src1 , outdir = args.dst )
        
    elif args.mode == ".p2": 
        print "Unpacking .p2 container"
        unpack_P2(root = args.src , outdir = args.dst)
        
    elif args.mode == ".z": 
        print "Unpacking .z container"
        unpack_Z(root = args.src , outdir = args.dst)
        
    elif args.mode == ".noext.z":
        print "Unpacking .noext.z text"
        if args.src:
            unpack_Z(root = args.src , outdir = args.src1 )
            
        unpack_no_ext(root = args.src1 , outdir = args.dst , ignore_p2 = args.ignore_p2 )
        
    elif args.mode == ".s.z":
        print "Unpacking .s.z text"
        if args.src:
            unpack_Z(root = args.src , outdir = args.src1 )
        unpack_S(root = args.src1 , outdir = args.dst )
        
    elif args.mode == ".pk2d.z":
        print "Unpacking .pk2d.z text"
        if args.src:
            unpack_Z(root = args.src , outdir = args.src1 )
        unpack_D2KP(args.src1 , args.dst, args.img, args.img_args)
        
    elif args.mode == ".rpt":
        print "Unpacking rpt text"
        unpack_rpt(root = args.src , outdir = args.dst)
                
        
    elif args.mode == ".db":
        print "Unpacking db text"
        unpack_db(src = args.src , dst = args.dst)
        
    elif args.mode == ".map":
        print "Unpacking map text"
        unpack_map(src = args.src , dst = args.dst)    
        
    elif args.mode == ".dat.z":
        print "Unpacking dat text"
        unpack_dat(root = args.src , outdir = args.dst) 
                        
    elif args.mode == ".msi.z":
        print "Unpacking msi text"
        unpack_msi(root = args.src , outdir = args.dst) 
