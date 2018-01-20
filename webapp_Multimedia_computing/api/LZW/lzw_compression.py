#!/usr/bin/env python
# encoding: utf-8

import os, chardet
import sys, re, math, unicodedata, codecs, pickle
import numpy as np
from scipy import misc
from math import log


class LZW:

	file_input = ''
	file_output = ''
	compression_raito = 0.0
	is_image = False


	def initialize_table(self, file_extension):

		# get sorted list of unique element

		if file_extension in ['.jpeg', '.jpg', '.png', '.bmp']:
			self.is_image = True
			element = [str(x) for x in range(0, 256)]
		else:
			# using ASCII table
			self.is_image = False
			element = [chr(x) for x in range(0,128)]

		encode_table = dict(zip(element, list(range(1, len(element) + 1))))
		decode_table = dict(zip(list(range(1, len(element) + 1)), element))

		return encode_table, decode_table

	def encode(self, list_input, file_extension):
		"""
			Compress list_input 
		"""

		result = []

		# initial dictionary
		# at the begining the dict is emplty. Add new single value if reaches it
		# keys = '123-123' using '-' to concate elements
		encode_table, decode_table = self.initialize_table(file_extension)

		pre_element = list_input[0]

		# loop each element in list_input except the first element
		for element in list_input[1:]:
			cur_element = '-' + element

			"""
			# check new singhle element and add to dictionary
			temp_pre_element = list(filter(None, pre_element.split('-'))) 
			if len(temp_pre_element)==1 and pre_element not in encode_table:
				encode_table[temp_pre_element[0]] = len(encode_table)+1

				# for streamming 
				# if reach the new element put the 0 before the real element
				result.append(0)
				result.append(temp_pre_element[0])
				encode_table[pre_element+cur_element] = len(encode_table)+1
				pre_element = cur_element[1:]
				continue
			"""

			# check sequence is already in dictionary or not
			if (pre_element + cur_element) in encode_table:
				pre_element = pre_element + cur_element
			else:
				result.append(encode_table[pre_element])
				encode_table[pre_element+cur_element] = len(encode_table)+1
				pre_element = cur_element[1:] # remove the '-' before of the cur_element

		# output for the last element
		result.append(encode_table[pre_element])

		return result, decode_table

	def decode(self, list_input, decode_table):
		"""
		Decompress list_input
		"""
		result = []

		if self.is_image:
			separate_symbol = '-'
		else:
			separate_symbol = ''

		# initialize decode_table dictionary
		decode_table = decode_table

		pre_entry = None

		for element in list_input:
			cur_element = element

			try:
				entry = decode_table[cur_element]
			except KeyError as e:
				# handle if code (cur_element) hasn't been in decode_table yet
				temp_pre_entry = list(filter(None, pre_entry.split(separate_symbol)))
				entry = pre_entry + separate_symbol + temp_pre_entry[0]

			# add entry to result
			# format entry to add to result list
			# entry format: 'abc-adc' -> ['abc', 'abc']
			if self.is_image:
				temp_entry = list(filter(None, entry.split(separate_symbol)))
				result = result + temp_entry # list + list mean concatenating
			else:
				temp_entry = list(entry)
				result = result + temp_entry

			if pre_entry is not None:
				decode_table[len(decode_table)+1] = pre_entry + separate_symbol + temp_entry[0]
			pre_entry = entry

			#print(result)
			#print(decode_table)

		return result, decode_table

	def preprocess(self, filename):
		"""
		Preprocess input file:
			with image: convert to 1-dimension array
			with text: get string
		"""

		# check file extension: text file (txt) and image file (.jpeg, .jpg, .png, .bmp) 
		file_name, file_extension = os.path.splitext(filename)
		additionInformation = {'extension': file_extension}

		if file_extension == '.txt':
			pass
			# detect file encoding
			#encode = chardet.detect(open(filename, 'r').read())

			file_input = codecs.open(filename, mode='r', encoding='utf8', errors='ignore')
			string_input = file_input.read()

			return string_input, additionInformation

		# with image file 
		# convert pixel matrix to 1 dimension array
		elif file_extension in ['.jpeg', '.jpg', '.png', '.bmp']:
			image = misc.imread(filename)
			# save the resolution information
			additionInformation['resolution'] = image.shape

			# convert image to 1-dimension array
			image_array = image.reshape(-1)
			image_array = [str(x) for x in image_array]

			return image_array, additionInformation

	def int_to_bits(self, list_input):
		"""
		Convert list integer to bits string
		"""
		maxCode = max(list_input)
		bits_needed = len(bin(maxCode)[2:])
		result = [bin(x)[2:].zfill(bits_needed) for x in list_input]

		# join to one string
		result = ''.join(result)

		return result, bits_needed

	def save_to(self, encode_result, file_path, additionInformation=None):
		"""
		Save encode results to file
		::encode_result : (encode_list, initial_table)
		"""
		encode_list, initial_table = encode_result



		# first of all write intial_table
		with open(file_path, 'wb') as file:

			# write addition information of file:
			# 	- file extension
			# 	- image resolution if file is image

			"""
			for key in additionInformation:
				file.write(bytes('%s-%s'%(key,additionInformation[key]), 'UTF-8'))
			"""



			str_bits, bits_needed = self.int_to_bits(encode_list)
			file.write(bytes([bits_needed]))
			#print("Bitneeded: ", bits_needed)
			#print("IN bytes: ", int.from_bytes(bytes([bits_needed]), byteorder='little'))

			list_bits = re.findall(r'\d{1,8}', str_bits)

			#count = 1
			# write list code
			for code in list_bits:
				#print(bytes([code]))
				file.write(int(code,2).to_bytes(1, byteorder='little'))
				#count += 1

		return (0, 'success')

	def read_file(self, file_path):
		"""
		Read file to decode
		File structre: 
			between $x-y$ is key-value of initial_table
		Return: 
			list_code, initial_table (using for decoding process)
		"""

		with open(file_path, 'rb') as file:

			initial_table = self.initialize_table('.txt')[1]

			# get #bit to unpack
			bits_needed = file.read(1)
			bits_needed = int.from_bytes(bits_needed, byteorder='little')

			bytes_remain = file.read()
			list_of_bytes = [bytes([i]) for i in bytes_remain]

			# convert bytes to bits
			list_bits = [bin(int.from_bytes(x, byteorder='little'))[2:].zfill(8) for x in list_of_bytes]

			# join to one string
			string_bits = ''.join(list_bits)

			#print(list_bits[-5:])
			#print(string_bits[-50:])

			codes = []
			index = 0
			while(index < len(string_bits)):

				codes.append(int(string_bits[index:index+bits_needed], 2))
				index += bits_needed
				"""
				if len(string_bits) - index < 2*bits_needed:
					codes.append(int(list_bits[-1]))
					break
				"""
			#print("Index: ", index)
			#print("len: ", len(string_bits))
			if index > len(string_bits):
				codes[-2] += codes[-1]
				del codes[-1]

			#codes = [int(x) for x in list_bits]

			#print("Done readfile")

			return codes, initial_table

	def lzw_compression(self, filename, save_file_name):
		"""
		Appyl LZW compression on file
		"""

		self.file_input = filename

		# get list input from preprocess
		list_input, additionInformation = self.preprocess(filename)

		#print("List: ", list_input)

		# Encoding
		encode_list, decode_table = self.encode(list_input, additionInformation['extension'])

		#print("Encode: ", encode_list)

		# save to file 
		self.file_output = save_file_name

		# if file is image then store information of resolution (using in decode)
		status = self.save_to((encode_list, decode_table), self.file_output, additionInformation)
		# return

		# calculate comporession raito
		# get size of file input/output
		size_input = os.path.getsize(self.file_input)
		size_output = os.path.getsize(self.file_output)

		self.compression_raito = float(size_input)/size_output

		print("Compression Raito: ", self.compression_raito)

		return self.compression_raito

	def lzw_decompression(self, filename, save_file_name):
		"""
		Apply LZW decompression on file
		"""

		# read file 
		list_input, initial_table = self.read_file(filename)

		# decode 
		result, decode_table = self.decode(list_input, initial_table)

		file_decode_output = save_file_name

		with open(file_decode_output, 'w') as file:
			for char in result:
				file.write(char)


		return (0, 'File save to %s'%(file_decode_output))


def print_dict(dictionary):

	for key in dictionary:
		print("%s : %s"%(key, dictionary[key]))

def main():

	test = LZW()
	a = test.lzw_compression('test.txt', 'encode.thuyngao')
	print(a)

	# decompression 
	a = test.lzw_decompression('encode.thuyngao', 'decode.txt')
	print(a)
	

if __name__ == '__main__':
	main()



