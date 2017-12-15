#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import struct
import array
import tempfile

#from pytable import normal_table
from libs import compression, parser, normal_table

languages = ("Ingl\xc3\xaas", "Franc\xc3\xaas", "Alem\xc3\xa3o", "Italiano", "Espanhol")

# unpack_P2 - 100%
# 
#
#
#



def unpack_P2(dir = 'Arquivos/P2', outdir = 'Arquivos/Unpacked P2'):
	for file_name in os.listdir(dir):
		if not os.path.isdir(os.path.join(dir, file_name)):
			head, tail  = os.path.split(file_name)
			try:
				f, ext = tail.split('.')		
			except:
				f = tail
			unpacked_dir = os.path.join(outdir, f)
			
			if not os.path.isdir(unpacked_dir):
				os.mkdir(unpacked_dir)
							
			with open(os.path.join(dir, file_name), 'rb') as packed_file:
			# Leitura do Header do Arquivo
				if packed_file.read(2) != 'P2':
					print 'Arquivo lido não é do tipo P2'
				else:
					print 'Desempacotando arquivo P2 - %s.' %f
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
							if fnt == True:
								output = open(os.path.join(unpacked_dir, '%s' %(names[x])), 'wb')				
							else:	
								output = open(os.path.join(unpacked_dir, '%s_%03d' %(f, x)), 'wb')
								names.append('%s_%03d' %(f, x))
							packed_file.seek(addresses[x],0)
							output.write(packed_file.read(sizes[x]))
							output.close()
						else:
							if fnt == True:
								output = open(os.path.join(unpacked_dir, '%s' %(names[x])), 'wb')				
							else:
								output = open(os.path.join(unpacked_dir, '%s_%03d' %(f, x)), 'wb')
								names.append('%s_%03d' %(f, x))
							packed_file.seek(addresses[x], 0)
							flag = packed_file.read(1)
							if flag == '\x10':
								compress[x] = "LZSS"
								buffer = compression.lzss.uncompress(packed_file, addresses[x])			
							elif flag == '\x11':			
								compress[x] = "ONZ"
								buffer = compression.onz.uncompress(packed_file, addresses[x])			
							buffer.tofile(output)
							output.close()
						
					with open(os.path.join(unpacked_dir, 'make.txt'), 'w') as c:
						for x, name in enumerate(names):
							c.write("%s %s\n" % (name, compress[x]))								
	
def extract_P2(root = 'Arquivos/Unpacked P2'):
	table = normal_table('kh.tbl')

	for _dir in os.listdir(root):

		out = os.path.join('Textos/P2', _dir)
		dir = os.path.join(root, _dir)
		
		if not os.path.isdir(out):
			os.mkdir(out)
		
		for file_name in os.listdir(dir):
			head, tail  = os.path.split(file_name)
			# table = normal_table('kh.tbl')
			output = open(os.path.join(out, '%s.txt' %tail), 'w')
			# output = open('out.txt', 'w')
			
			print "Extraindo %s." %file_name

			with open(os.path.join(dir, file_name), 'rb') as file:
				# Tipo 1 de arquivos
				if _dir in ('db_en',):
					fat_entries = struct.unpack('<L', file.read(4))[0]
					base_address = 4 + fat_entries * 4
					lenght = []
					previous_lenght = 0
					for x in range(fat_entries):
						current_lenght = struct.unpack('<L', file.read(4))[0]
						lenght.append(current_lenght - previous_lenght)
						previous_lenght = current_lenght
					file.seek(base_address, 0)
					
					for x in range(fat_entries):
						for y in range(lenght[x]/2):
							data = file.read(2)
							if data[::-1] in table:
								output.write(table[data[::-1]])
							else:				
								cc = unichr(struct.unpack('<H', data)[0])
								output.write(cc.encode('utf-8'))
						output.write('\n!------------------------------!\n')
				# Tipo 2 de arquivos
				elif _dir in ('m','EV_AL','EV_AW','EV_BB','EV_DP','EV_HE','EV_NM','EV_PP','EV_S','EV_TT'):
					table = normal_table('tabela2.tbl')
					table.fill_with('61=a', '41=A', '30=0')
					table.add_items('0A=\n')
					
					if "make.txt" not in file.name:
						parser.generic_parser_1(file, output, table)		
										
			output.close()

def extract_S(root = "Arquivos/S"):
	table = normal_table('kh.tbl')

	for file_name in os.listdir(root):
		head, tail  = os.path.split(file_name)

		output = open(os.path.join('Textos/S', '%s.txt' %tail), 'w')	
		
		with open(os.path.join(root, file_name), 'rb') as onzfile:		
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
							elif data[::-1] in table:	# Tags
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
						elif data[::-1] in table:	# Tags
							output.write(table[data[::-1]])
						else:				
							cc = unichr(struct.unpack('<H', data)[0])
							output.write(cc.encode('utf-8'))
					
					output.write('\n!******************************!\n')
			file.close()
		output.close()
		
		
def extract_CAKP(root = "Arquivos/Unpacked CAKP"):
	table = normal_table('tabela2.tbl')
	table.fill_with('61=a', '41=A', '30=0')
	table.add_items('0A=\n')

	for _dir in os.listdir(root):

		_out = os.path.join('Textos/CAKP', _dir)
		dir = os.path.join(root, _dir)
		
		if not os.path.isdir(_out):
			os.mkdir(_out)
			
		for file_name in os.listdir(dir):
			if file_name != "make.txt":
				out = os.path.join(_out, file_name)
				
				if not os.path.isdir(out):
					try:	os.mkdir(out)			
					except: pass
			
				with open(os.path.join(dir, file_name), 'rb') as file:
					# Lê o header, fat e fnt, e cria um make.txt
					if file.read(4) != 'CAKP':
						try:	os.rmdir(out)
						except: pass
						print 'Arquivo %s não é do tipo CAKP. Extraindo normalmente...' % file_name
						file.seek(0,0)						
						output = open(out, 'wb')
						output.write(file.read())						
						output.close()	
						
						if file_name not in ('em0', 'em0m'):
							file.seek(0, 0)
							output = open("%s.txt" % out, 'w')
							parser.generic_parser_1(file, output, table)
							output.close()
						
					else:
						print 'Desempacotando arquivo CAKP - %s.' % file_name
						file.seek(40, 1) # São valores constantes - Ler documentação
						
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
							
						# Extraindo conteúdo:
						make = open(os.path.join(out, 'make.txt'), 'w')
						for x in range(entries):
							make.write(fnt_names[x] + '\n')
											
							output = open(os.path.join(out, fnt_names[x]), 'wb')
								
							file.seek(addresses[x], 0)
							output.write(file.read(sizes[x]))
								
							output.close()	
						
							if fnt_names[x] not in ('_i', '_e', 'chara', 'shop', 'stmi'):
								
								output = open(os.path.join(out, fnt_names[x]) + '.txt', 'w')
								
								file.seek(addresses[x], 0)
																						
								input = tempfile.NamedTemporaryFile()
								input.write(file.read(sizes[x]))
								input.seek(0, 0)
								
								parser.generic_parser_1(input, output, table)							
								
								input.close()
								output.close()
								
						make.close()
						
						
			
			
import psyco
psyco.full()		
		

if __name__ == '__main__':
# Extrair os diálogos com avatar
	unpack_P2('Arquivos/P2', 'Arquivos/Unpacked P2')
	extract_P2()
	
#
	#unpack_P2('Arquivos/CAKP','Arquivos/Unpacked CAKP')
	#extract_CAKP()
	#extract_P2()
	
	
	
	
	#unpack_P2(dir = 'Arquivos/CAKP', outdir = 'Arquivos/Unpacked CAKP')
	#extract_S()
