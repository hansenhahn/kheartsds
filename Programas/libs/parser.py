#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import os
import sys
import struct
import array
import tempfile

from pytable import normal_table

def write_data(input, output, table):
    data = struct.unpack('B', input.read(1))[0]
    if data == 0:
        return False
    elif (data >= 0xc2) and (data <= 0xd0):
        data = struct.pack('B', data) + input.read(1)
    else:
        data = struct.pack('B', data)
    if data in table:
        output.write(table[data])
    else:
        for x in range(len(data)):
            output.write('<%02X>' % (struct.unpack('B', data[x]))[0])
    return True

def generic_parser_1(file, output, table):

    base_address = struct.unpack('<L', file.read(4))[0]
    while True:
        structs = []
        
        if ( file.tell() == base_address ):
            break
    
        try:
            flag = file.read(2)
            size = struct.unpack('<H', file.read(2))[0] & 0xFF
        except:
            print 
        # if flag == '\x00\x03':
            # break
            
        # \x00 -> Estrutura Header
        if flag == '\x00\x05':
            structs.append(struct.unpack('<L', file.read(4))[0] + base_address)
            file.read(4)            
            
            addrRet = file.tell()

            output.write('&.[HDR].&\n')

            for x in structs:
                file.seek(x, 0)
                data = ""
                while True:
                    byte = struct.unpack('B', file.read(1))[0]
                    data += "%02X" % byte
                    if byte == 0xF:
                        data += "00"
                        break
                output.write("*.%s.*\n" % data)
                output.write('!******************************!\n')              
            file.seek(addrRet, 0)
        
        elif flag == '\x00\x1b':
            file.read(12)
            structs.append(struct.unpack('<L', file.read(4))[0] + base_address)
            
            addrRet = file.tell()

            output.write('&.[HDR].2.&\n')

            for x in structs:
                file.seek(x, 0)
                while True:
                    ret = write_data(file, output, table)
                    if ret == False:
                        break
                output.write('\n!******************************!\n')        
            file.seek(addrRet, 0)           

        
        # \x01 -> Estrutura Diálogo Com Avatar
        elif flag == '\x01\x0a':
            file.read(20)
            structs.append(struct.unpack('<L', file.read(4))[0])
            file.read(16)

            addrRet = file.tell()

            for x in structs:
                if x != 0xFFFFFFFF:
                    output.write('&.[DCA].Arquivo.&\n')
                
                    file.seek(x + base_address, 0)
                    while True:
                        ret = write_data(file, output, table)
                        if ret == False:
                            break
                    output.write('\n!******************************!\n')        
            file.seek(addrRet, 0)               
        
        elif flag == '\x01\x1d':
            fl1 = struct.unpack('<L', file.read(4))[0]
            structs.append(struct.unpack('<L', file.read(4))[0] + base_address)
            file.read(16)
            
            addrRet = file.tell()

            output.write('&.[DCA].Normal.&\n')
            
            for x in structs:
                if fl1 == 0x2:
                    file.seek(x, 0)                     
                    while True:
                        ret = write_data(file, output, table)
                        if ret == False:
                            break
                    output.write('\n!------------------------------!\n')            
                    output.write('!******************************!\n')
                elif fl1 == 0x40:
                    addrDialogs = []            
                    file.seek(x, 0)
                    for y in range(6):
                        pt = struct.unpack('<L', file.read(4))[0]
                        if pt == 0xFFFFFFFF:
                            pt = None
                        else:
                            pt += base_address
                        addrDialogs.append(pt)              
                    for y in addrDialogs:
                        if not y:
                            output.write('*.NULO.*')
                        else:
                            file.seek(y, 0)                         
                            while True:
                                ret = write_data(file, output, table)
                                if ret == False:
                                    break
                        output.write('\n!------------------------------!\n')
                    output.write('!******************************!\n')

            file.seek(addrRet, 0)

        elif flag == '\x01\x1e':
            file.read(12)
            structs.append(struct.unpack('<L', file.read(4))[0] + base_address)
            file.read(40)           

            addrRet = file.tell()

            output.write('&.[DCA].Bip.&\n')
            
            for x in structs:
                file.seek(x, 0)
                while True:
                    ret = write_data(file, output, table)
                    if ret == False:
                        break
                output.write('\n!******************************!\n')        
            file.seek(addrRet, 0)

            
        # \x02 -> Estrutura Diálogos Sem Avatar 
        elif flag == '\x02\x3f':
        
            file.read(4)
            structs.append(struct.unpack('<L', file.read(4))[0] + base_address)
            file.read(16)
            
            addrRet = file.tell()

            output.write('&.[DSA].Normal.&\n')
            
            for x in structs:
                addrDialogs = []            
                file.seek(x, 0)
                for y in range(6):
                    pt = struct.unpack('<L', file.read(4))[0]
                    if pt == 0xFFFFFFFF:
                        pt = None
                    else:
                        pt += base_address
                    addrDialogs.append(pt)              
                for y in addrDialogs:
                    if not y:
                        output.write('*.NULO.*')
                    else:
                        file.seek(y, 0)                         
                        while True:
                            ret = write_data(file, output, table)
                            if ret == False:
                                break
                    output.write('\n!------------------------------!\n')
            output.write('!******************************!\n')              
            file.seek(addrRet, 0)       
        
        # \x02 -> Estruturas Diálogos Condicionais
        elif flag == '\x02\x40':
            file.read(4)
            structs.append(struct.unpack('<L', file.read(4))[0] + base_address)
            file.read(20)
            structs.append(struct.unpack('<L', file.read(4))[0] + base_address)
            file.read(12)
            structs.append(struct.unpack('<L', file.read(4))[0] + base_address)
            if size == 0x13:
                file.read(12)
                structs.append(struct.unpack('<L', file.read(4))[0] + base_address)
            file.read(8)                
                
            addrRet = file.tell()
            
            output.write('&.[DSA].Condicional.&\n')
            
            for x in structs:
                addrDialogs = []            
                file.seek(x, 0)
                for y in range(6):
                    pt = struct.unpack('<L', file.read(4))[0]
                    if pt == 0xFFFFFFFF:
                        pt = None
                    else:
                        pt += base_address
                    addrDialogs.append(pt)              
                for y in addrDialogs:
                    if not y:
                        output.write('*.NULO.*')
                    else:
                        file.seek(y, 0)                         
                        while True:
                            ret = write_data(file, output, table)
                            if ret == False:
                                break
                    output.write('\n!------------------------------!\n')
                output.write('!++++++++++++++++++++++++++++++!\n')
            output.write('!******************************!\n')              
            file.seek(addrRet, 0)
                
        # \x03 -> Estrutura Vídeo - Legenda
        elif flag == '\x03\x01':
            structs = []
            file.read(4)
            structs.append(struct.unpack('<L', file.read(4))[0] + base_address)
            addrRet = file.tell()
            
            output.write('&.[VID].Legenda.&\n')
            
            for x in structs:
                file.seek(x, 0)
                while True:
                    ret = write_data(file, output, table)
                    if ret == False:
                        break
                output.write('\n!******************************!\n')
            file.seek(addrRet, 0)
        
    # \x03 -> Estrutura Vídeo - Nome
        elif flag == '\x03\x02':
            structs = []
            for x in range(3):
                file.read(4)
                pt = struct.unpack('<L', file.read(4))[0]
                if pt == 0xFFFFFFFF:
                    pt = None
                else:
                    pt += base_address
                structs.append(pt)
            addrRet = file.tell()
            
            output.write('&.[VID].Título.&\n')
        
            for x in structs:
                if not x:
                    output.write('*.NULO.*')
                else:
                    file.seek(x, 0)     
                    while True:
                        ret = write_data(file, output, table)
                        if ret == False:
                            break
                output.write('\n!++++++++++++++++++++++++++++++!\n')
            output.write('!******************************!\n')
        
            file.seek(addrRet, 0)
            
        # \x03 -> Estrutura Vídeo - Tempo?
        elif flag == '\x03\x03':
            file.read(4)
            
            output.write('&.[VID].Tempo.&\n')
            output.write('*.%08X.*\n' % struct.unpack('<L', file.read(4))[0])
            output.write('!******************************!\n')
            
        # \x13 -> Estrutura Evento?
        elif flag == '\x13\x00':
            structs = []
            file.read(4)
            structs.append(struct.unpack('<L', file.read(4))[0] + base_address)
            file.read(16)
            addrRet = file.tell()
            
            output.write('&.[EVT].&\n')
                    
            for x in structs:
                addrDialog = []
                file.seek(x, 0)
                for y in range(6):
                    addrDialog.append(struct.unpack('<L', file.read(4))[0] + base_address)
                for y in addrDialog:
                    file.seek(y, 0)                         
                    while True:
                        ret = write_data(file, output, table)
                        if ret == False:
                            break
                    output.write('\n!------------------------------!\n')
                output.write('!******************************!\n')
            
            file.seek(addrRet, 0)
            
        else:
            file.read(4 * (size-1))
            
TAG_MV = r'^\[MV:(.+?)\]$'
TAG_NM = r'^\[(.+?)\]$'
TAG_CH = r'(<.+?>)'
TAG_CH2 = r'^<(.+?)>$'
END = r'^!\D{30}!$'

#MARK1 = r'^&\.(.+?)\.&$' - Errei num dos scripts
MARK1 = r'^&\.(.+?)&$'      # Compatibilidade
MARK2 = r'^\*\.(.+?)\.\*$'

SEP1 = r'^!\*{30}!$'
SEP2 = r'^!-{30}!$'
SEP3 = r'^!+{30}!$'

def read_line(line, table):
    splited = re.split(TAG_CH, line)
    string = ""
    for data in splited:
        tag = re.match(TAG_CH2, data)
        if not tag:
            for c in data:
                try:
                    string += table[c]
                except:
                    print line
                    raise TypeError
        else:
            tag = tag.groups()[0]
            string += chr(int(tag, 16))
    return string
            
def generic_inserter_1(input, output, table):

    _dict = {
            '\x00\x05': [], '\x00\x1b': [],
            '\x01\x0a': [], '\x01\x1d': [], '\x01\x1e': [],
            '\x02\x3f': [], '\x02\x40': [],
            '\x03\x01': [], '\x03\x02': [], '\x03\x03': [],
            '\x13\x00': []
            }
            
    print "Recriando %s..." % input.name

    c = input.readlines()
    
    while True:
        if not c:
            break
        line = c.pop(0)
        line = line.strip('\r\n')
        a = re.match(MARK1, line)
        if a and a.group() == '&.[DSA].Normal.&':
            block = []
            for x in range(6):
                buffer = array.array('c')
                while True:
                    line = c.pop(0)
                    line = line.strip('\r\n')
                    if re.match(SEP2, line):
                        buffer.pop()
                        break
                    elif re.match(MARK2, line):
                        buffer.extend("\n")
                    else:
                        string = read_line(line, table)
                        buffer.extend("%s\n" % string)
                block.append(buffer)
            _dict['\x02\x3f'].append(block)
            
        elif a and a.group() == '&.[DSA].Condicional.&':    
            block = [[],[],[],[]]
            for y in range(4):
                for x in range(6):
                    buffer = array.array('c')
                    while True:
                        line = c.pop(0)
                        line = line.strip('\r\n')
                        if re.match(SEP2, line):
                            buffer.pop()
                            break
                        elif re.match(SEP1, line):
                            break
                        elif re.match(MARK2, line):
                            line = c.pop(0)
                            break
                        else:
                            string = read_line(line, table)
                            buffer.extend("%s\n" % string)
                    if re.match(SEP1, line):
                        break
                    block[y].append(buffer)
                if re.match(SEP1, line):
                    c.insert(0, '\n!******************************!\n')
                    break
                c.pop(0) #!++..++!
            _dict['\x02\x40'].append(block)

        elif a and a.group() == '&.[VID].Legenda.&':
            line = c.pop(0)
            line = line.strip('\r\n')
            _dict['\x03\x01'].append(read_line(line, table))
            
        elif a and a.group() == '&.[VID].Título.&':
            block = []      
            for x in range(3):
                line = c.pop(0)
                line = line.strip('\r\n')
                if re.match(MARK2, line):
                    block.append(None)
                else:
                    block.append(read_line(line, table))
                c.pop(0)
            _dict['\x03\x02'].append(block)
            
        elif a and a.group() == '&.[VID].Tempo.&':
            line = c.pop(0)
            line = line.strip('\r\n')
            
            string = ""
            
            d = re.match(MARK2, line)
            for x in range(len(d.groups()[0])/2):
                string += chr(int(d.groups()[0][2*x:(2*x)+2], 16))

            _dict['\x03\x03'].append(string)
            
        elif a and a.group() == '&.[HDR].&':
            line = c.pop(0)
            line = line.strip('\r\n')   
            string = ""
            
            d = re.match(MARK2, line)
            for x in range(len(d.groups()[0])/2):
                string += chr(int(d.groups()[0][2*x:(2*x)+2], 16))

            _dict['\x00\x05'].append(string)

        elif a and a.group() in ('&.[HDR].2&', '&.[HDR].2.&'):
            line = c.pop(0)
            line = line.strip('\r\n')
            _dict['\x00\x1b'].append(read_line(line, table))
            
        elif a and a.group() == '&.[EVT].&':
            block = []
            for x in range(6):
                buffer = array.array('c')
                while True:
                    line = c.pop(0)
                    line = line.strip('\r\n')
                    if re.match(SEP2, line):
                        buffer.pop()
                        break
                    elif re.match(MARK2, line):
                        pass
                    else:
                        string = read_line(line, table)
                        buffer.extend("%s\n" % string)
                block.append(buffer)
            _dict['\x13\x00'].append(block)     
        
        elif a and a.group() in ('&.[DCA].Arquivo.&', '&.[DCA].Arquivo&'):
            line = c.pop(0)
            line = line.strip('\r\n')
            _dict['\x01\x0a'].append(read_line(line, table))
            
        elif a and a.group() == '&.[DCA].Bip.&':
            line = c.pop(0)
            line = line.strip('\r\n')
            _dict['\x01\x1e'].append(read_line(line, table))
            
        elif a and a.group() == '&.[DCA].Normal.&':
            block = []
            for x in range(6):
                buffer = array.array('c')
                while True:
                    line = c.pop(0)
                    line = line.strip('\r\n')
                    if re.match(SEP2, line):
                        buffer.pop()
                        break
                    elif re.match(SEP1, line):
                        break
                    elif re.match(MARK2, line):
                        buffer.extend("\n")
                    else:
                        string = read_line(line, table)
                        buffer.extend("%s\n" % string)
                if re.match(SEP1, line):
                    c.insert(0, '\n!******************************!\n')
                    break
                block.append(buffer)
            _dict['\x01\x1d'].append(block)             
    
        c.pop(0) # !**..**! 
    
    base_address = struct.unpack('<L',output.read(4))[0]
   
    
    #data_ptr = base_address
    # POCOTO POCOTO POCOTO --- VAI CAVALO!!!
    if os.path.isfile( input.name + "size" ):
        print input.name + "size"
        g = open( input.name + "size" , "rb" )
        data_ptr = struct.unpack("<L", g.read(4))[0]
        g.close()
    else:
        data_ptr = os.path.getsize( output.name )
        g = open( input.name + "size" , "wb" )
        g.write( struct.pack("<L", data_ptr) )
        g.close()        

    while True:        
        
        pointers = []
    
        flag = output.read(2)
        size = struct.unpack('<H', output.read(2))[0] & 0xFF

        #print hex(struct.unpack("<H", flag)[0])
        
        if flag == '\x01\x0A':
            addrRet = output.tell() 
            
            output.seek(20, 1)
            if output.read(4) == '\xff\xff\xff\xff':
                output.seek(16, 1)  
            else:       
                data = _dict['\x01\x0A'].pop(0)
            
                output.seek(data_ptr, 0)
                output.write(data)
                output.write('\x00')
                pointers.append(data_ptr - base_address)
                while output.tell() % 4 != 0:
                    output.write('\x00')
                data_ptr = output.tell()
                
                output.seek(addrRet, 0)
                output.seek(20, 1)
                output.write(struct.pack('<L', pointers[0]))
                output.seek(16, 1)          
        
        elif flag == '\x01\x1E':
            data = _dict['\x01\x1E'].pop(0)
        
            addrRet = output.tell()         
            output.seek(data_ptr, 0)
            output.write(data)
            output.write('\x00')
            pointers.append(data_ptr - base_address)
            while output.tell() % 4 != 0:
                output.write('\x00')
            data_ptr = output.tell()
            
            output.seek(addrRet, 0)
            output.seek(12, 1)
            output.write(struct.pack('<L', pointers[0]))
            output.seek(40, 1)
        
        # [DCA] Normal
        elif flag == '\x01\x1D':
            data = _dict['\x01\x1D'].pop(0)
            
            addrRet = output.tell()
            fl1 = struct.unpack('<L', output.read(4))[0]
            
            output.seek(data_ptr, 0)

            if fl1 == 0x40:
                ptr = []
                for y in range(6):
                    string = data.pop(0)
                    if string:
                        output.write(string)
                        output.write('\x00')
                        ptr.append(data_ptr - base_address)
                        while output.tell() % 4 != 0:
                            output.write('\x00')
                        data_ptr = output.tell()
                    else:
                        ptr.append(0xFFFFFFFF)
                        data_ptr = output.tell()
                pointers.append(output.tell() - base_address)
                for y in ptr:
                    output.write(struct.pack('<L', y))
                output.write(struct.pack('<L', 0xFFFFFFFF))
                data_ptr = output.tell()
            else:
                pointers.append(data_ptr - base_address)
                string = data.pop(0)
                output.write(string)
                output.write('\x00')
                data_ptr = output.tell()

            output.seek(addrRet, 0)
            output.seek(4, 1)
            output.write(struct.pack('<L', pointers[0]))
            output.seek(16, 1)
        # [DSA] Normal
        elif flag == '\x02\x3F':        
            data = _dict['\x02\x3F'].pop(0)
            
            addrRet = output.tell()
            
            output.seek(data_ptr, 0)

            ptr = []
            for y in range(6):
                string = data.pop(0)
                if string:
                    output.write(string)
                    output.write('\x00')
                    ptr.append(data_ptr - base_address)
                    while output.tell() % 4 != 0:
                        output.write('\x00')
                    data_ptr = output.tell()
                else:
                    ptr.append(0xFFFFFFFF)
                    data_ptr = output.tell()
            pointers.append(output.tell() - base_address)
            for y in ptr:
                output.write(struct.pack('<L', y))
            output.write(struct.pack('<L', 0xFFFFFFFF))
            data_ptr = output.tell()
                    
            output.seek(addrRet, 0)
            output.seek(4, 1)
            output.write(struct.pack('<L', pointers[0]))
            output.seek(16, 1)
        # [DSA] Condicional
        elif flag == '\x02\x40':
            data = _dict['\x02\x40'].pop(0)
            if data[3]:
                l = 4
            else:
                l = 3
        
            addrRet = output.tell()
            
            output.seek(data_ptr, 0)
            for x in range(l):
                ptr = []
                for y in range(6):
                    string = data[x].pop(0)
                    if string:
                        output.write(string)
                        output.write('\x00')
                        ptr.append(data_ptr - base_address)
                        while output.tell() % 4 != 0:
                            output.write('\x00')
                        data_ptr = output.tell()
                    else:
                        ptr.append(0xFFFFFFFF)
                        data_ptr = output.tell()
                pointers.append(output.tell() - base_address)
                for y in ptr:
                    output.write(struct.pack('<L', y))
                output.write(struct.pack('<L', 0xFFFFFFFF))
                data_ptr = output.tell()
                    
            output.seek(addrRet, 0)
            output.seek(4, 1)
            output.write(struct.pack('<L', pointers[0]))
            output.seek(20, 1)
            output.write(struct.pack('<L', pointers[1]))
            output.seek(12, 1)
            output.write(struct.pack('<L', pointers[2]))
            if l == 4:
                output.seek(12, 1)
                output.write(struct.pack('<L', pointers[3]))
            output.seek(8, 1)
        
        # [VID].Legenda        
        elif flag == '\x03\x01':
            data = _dict['\x03\x01'].pop(0)
        
            addrRet = output.tell()         
            output.seek(data_ptr, 0)
            output.write(data)
            output.write('\x00')
            pointers.append(data_ptr - base_address)
            while output.tell() % 4 != 0:
                output.write('\x00')
            data_ptr = output.tell()
            
            output.seek(addrRet, 0)
            output.seek(4, 1)
            output.write(struct.pack('<L', pointers[0]))

        elif flag == '\x03\x02':
            data = _dict['\x03\x02'].pop(0)
        
            addrRet = output.tell()             
            output.seek(data_ptr, 0)
            for x in range(3):
                string = data.pop(0)
                if string:
                    output.write(string)
                    output.write('\x00')
                    pointers.append(data_ptr - base_address)
                    while output.tell() % 4 != 0:
                        output.write('\x00')
                    data_ptr = output.tell()
                else:
                    pointers.append(0xFFFFFFFF)
                    data_ptr = output.tell()
                    
            output.seek(addrRet, 0)
            output.seek(4, 1)
            output.write(struct.pack('<L', pointers[0]))
            output.seek(4, 1)
            output.write(struct.pack('<L', pointers[1]))
            output.seek(4, 1)
            output.write(struct.pack('<L', pointers[2]))
            
            #
            
        elif flag == '\x03\x03':
            data = _dict['\x03\x03'].pop(0)
            output.seek(4, 1)
            output.write(data[::-1])
            
        elif flag == '\x00\x05':
            data = _dict['\x00\x05'].pop(0)
        
            addrRet = output.tell()
            
            output.seek(data_ptr, 0)            
            pointers.append(output.tell() - base_address)
            output.write(data)
            output.write('\x00')
            while output.tell() % 4 != 0:
                output.write('\x00')
            data_ptr = output.tell()
            
            output.seek(addrRet, 0)
            output.write(struct.pack('<L', pointers[0]))    
            output.seek(4, 1)
            
            
        elif flag == '\x00\x1b':
            data = _dict['\x00\x1b'].pop(0)
            
            addrRet = output.tell()
            
            output.seek(data_ptr, 0)            
            pointers.append(output.tell() - base_address)
            output.write(data)
            output.write('\x00')
            while output.tell() % 4 != 0:
                output.write('\x00')
            data_ptr = output.tell()
            
            output.seek(addrRet, 0)
            output.seek(12, 1)
            output.write(struct.pack('<L', pointers[0]))                
                
        elif flag == '\x13\x00':
            data = _dict['\x13\x00'].pop(0)
            
            addrRet = output.tell()
            
            output.seek(data_ptr, 0)

            ptr = []
            for y in range(6):
                string = data[x].pop(0)
                if string:
                    output.write(string)
                    output.write('\x00')
                    ptr.append(data_ptr - base_address)
                    while output.tell() % 4 != 0:
                        output.write('\x00')
                    data_ptr = output.tell()
                else:
                    ptr.append(0xFFFFFFFF)
                    data_ptr = output.tell()
            pointers.append(output.tell() - base_address)
            for y in ptr:
                output.write(struct.pack('<L', y))
            output.write(struct.pack('<L', 0xFFFFFFFF))
            data_ptr = output.tell()
                    
            output.seek(addrRet, 0)
            output.seek(4, 1)
            output.write(struct.pack('<L', pointers[0]))
            output.seek(16, 1)          
                
        # elif flag == '\x00\x03':
            # break           
            
        else:
            output.seek(4 * (size-1), 1)
            
        if output.tell() >= base_address:
            break
            
        output.flush()

    return True
