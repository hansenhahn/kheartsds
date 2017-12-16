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

from pytable import normal_table
from libs import compression, parser

languages = ("Ingl\xc3\xaas", "Franc\xc3\xaas", "Alem\xc3\xa3o", "Italiano", "Espanhol")


TAG_MV = r'^\[MV:(.+?)\]$'
TAG_NM = r'^\[(.+?)\]$'
TAG_CH = r'(<.+?>)'
TAG_CH2 = r'^<(.+?)>$'
END = r'^!\D{30}!$'

def pack_P2(root = 'Arquivos PT-BR/Unpacked P2',
			outdir = 'Arquivos PT-BR/P2',
			extension = '.p2',
			has_fnt = False):

	for dir in os.listdir(root):
		#output = open(os.path.join('Arquivos PT-BR/P2', dir) + '.p2', 'wb')
		output = open(os.path.join(outdir, dir) + extension, 'wb')
		#entries = len(os.listdir(os.path.join(root, dir)))
		
		with open(os.path.join(root, dir, 'make.txt'), 'r') as makefile:
			nametable = makefile.readlines()
			
		entries = len(nametable)
		
		base_address = entries * 6 + 16
		if base_address % 4 != 0: base_address += 2
		
		if has_fnt:
			base_address += entries * 8
		
		while base_address % 0x200 != 0: base_address += 1
		
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
			
			a = re.match(r'^(.+?) (.+?)$', file_name)
			name, comp = a.groups()
			
			compress = False
			if comp != "None":
				compress = True
		
			print "Adicionando %s em %s." % (name, output.name)
			output.seek(address, 0)
		
			input = open(os.path.join(root, dir, name), 'rb')
			if compress:
				if comp == "LZSS":
					buffer = compression.lzss.compress(input)
				elif comp == "ONZ":
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
				output.write(name)
				while output.tell() % 8 != 0: output.seek(1,1)

		output.close()

def pack_CAKP(root = "Textos PT-BR/CAKP"):
	table = normal_table('tabela2.tbl')
	table.fill_with('61=a', '41=A', '30=0')
	table.add_items('0A=\n')
	
	table.set_mode('inverted')
	# Funcionando Perfeitamente

	for _dir in os.listdir(root):
	
		_out = os.path.join('Arquivos PT-BR/Unpacked CAKP', _dir)
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
				with open(os.path.join(folder, 'make.txt'), 'r') as makefile:
					for file in makefile.readlines():
						nametable.append(file.strip('\r\n'))
				
				files = []
				for name in nametable:
					with open(os.path.join(folder, name), 'rb') as file:
						files.append(file.read())

				print "Empacotando %s." % folder
						
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
				
def pack_GNRC(root = "Textos PT-BR/P2"):
	table = normal_table('tabela2.tbl')
	table.fill_with('61=a', '41=A', '30=0')
	table.add_items('0A=\n')
	
	table.set_mode('inverted')
	for _dir in os.listdir(root):
	
		_out = os.path.join('Arquivos PT-BR/Unpacked P2', _dir)
		dir = os.path.join(root, _dir)
		
		if not os.path.isdir(_out):
			os.mkdir(_out)
			
		for f in os.listdir(dir):
			a = re.match(r'^(.+?)\.z\.txt$', f)
			if a:
				with open(os.path.join(dir, f), 'r') as input:
					output = open(os.path.join(_out, a.groups()[0]), 'r+b')
					parser.generic_inserter_1(input, output, table)
					output.close()
			else:
				pass 				

 # *********************** WIP *********************** #
				
# def insert_S(root = 'Textos PT-BR/S'):

	# table = normal_table('kh.tbl')
	
	# table.set_mode('inverted')

	# for file_name in os.listdir(root):
		# print file_name
	
		# input = open(os.path.join(root, file_name), 'r')

		# buffer = []
		
		# block = array.array('c')
		# for line in input:
			# line = line.strip('\r\n')		
			# if line == '!******************************!':
				# block.pop()
				# block.pop()
				# block.extend('\x00\x00')
				# buffer.append(block)
				# block = array.array('c')
			# else:
				# splited = re.split(TAG_CH, line)
				# for data in splited:
					# tag = re.match(TAG_CH2, data)
					# if tag:
						# tag = tag.groups()[0]
						# block.extend(table[tag][::-1])
					# else:
						# for c in data:
							# block.extend(c + '\x00')
				# block.extend('\x0a\x00')
				
		# output = open('teste.raw', 'wb')
		# output.write('\x08\x00\x00\x00')
		# output.write(struct.pack('<L', len(buffer)))
		# for block in buffer:
			# output.write(struct.pack('<L', len(block)+4))
			# block.tofile(output)
		
		# output.close()
		
		# output = open('teste.raw', 'rb')
		# with open('out.bin', 'wb') as f:
				# buffer = compression.onz.compress(output)
				# buffer.tofile(f)
				
		# output.close()
		# input.close()
		
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
				
				
						
import psyco
psyco.full()
	
if __name__ == '__main__':
	# insert_P2()
	# pack_P2()
	#insert_S()
	
# Para gerar os arquivos dos diálogos sem avatar
	# pack_CAKP()
	# pack_P2(root = 'Arquivos PT-BR/Unpacked CAKP', outdir = 'Arquivos PT-BR/CAKP', extension = '', has_fnt = True)
	
# Para gerar os arquivos dos diálogos com avatar
	pack_GNRC()
	pack_P2(root = 'Arquivos PT-BR/Unpacked P2', outdir = 'Arquivos PT-BR/P2', extension = '.p2', has_fnt = False)
	
	