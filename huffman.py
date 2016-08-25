class Huffman:
	"""
	This is the definition of a class of objects that represent the Huffman
	data compression algorithm
	"""

	def encode(self, data):
		"""
		This function receives plain text and returns the same data encoded (compressed)
		"""		
		def getTree():
			"""
			This function constructs (and returns) a tree structure that holds individual characters of the input
			message along with their frequencies. This tree can then be used for encoding and decoding the message.
			"""		
			def getFrequencies():
				"""
				This function returns a sorted list of character frequencies in the input message.
				"""		
				from collections import defaultdict
				f = defaultdict(int)
				for c in data:
					f[c] += 1
				return sorted([(value,key) for (key,value) in f.items()])
			def buildTree(f):
				"""
				This function constructs the tree that holds individual characters and their frequencies
				in the form of a list
				"""		
				if len(f) == 1:
					return f
				f = sorted([(f[0][0] + f[1][0], '*', f[0], f[1])] + f[2:])
				return buildTree(f)
			#traverse the text and compute the frequency of occurence for each character
			f = getFrequencies()
			#use the frequencies to create the tree and return it 
			return buildTree(f)

		def getNext(t, c):
			"""
			This function traverses the tree and gradually (recursively) develops the code
			for the particular character given as input
			"""			
			def find(t, c):
				if len(t) == 4:
					return find(t[2], c) or find(t[3], c)
				return t[1] == c
			if len(t) == 4:
				if find(t[2], c):
					return "0" + getNext(t[2], c)
				if find(t[3], c):
					return "1" + getNext(t[3], c)
				return ""
			return ""
		#create a tree for the particular message given as a parameter and store it in the object
		self.tree = getTree()
		#utilise the tree to encode the message character by character and return the code
		code = ""
		for c in data:
			code += getNext(self.tree[0], c)
		return code

	def decode(self, code):
		"""
		This function receives an encoded (compressed) message and returns the same 
		data as readable text (decompressed) 
		"""		
		def getNext(t, code):
			"""
			This function traverses recursively the tree using the binary digits in the code
			and returns the character the corresponds to the particular code given as parameter
			"""			
			if len(t) == 4:
				if code[0] == "0":
					return getNext(t[2], code[1:])
				else:
					return getNext(t[3], code[1:])
			return t[1], code
		#use the existing tree in the object to decode the message given as a parameter, code by code
		data = ""
		stop = False
		while stop == False:
			token, code = getNext(self.tree[0], code)
			if code == "":
				stop = True
			data += token
		return data

import unittest

class TestUM(unittest.TestCase):
 
	def setUp(self):
		self.huffman = Huffman()
	
	def test_encoding(self):
		input_text = "this is an example for huffman encoding"
		output_code = "0010000111111100010111111000101110001110111011001011000100000100000111011011110010100011101001100101111011100100110001110111010111001100101100111111101100000"
		self.assertEqual(self.huffman.encode(input_text), output_code)

	def test_decoding(self):
		self.huffman.tree = [(39, '*', (16, '*', (8, '*', (4, '*', (2, '*', (1, 'g'), (1, 'l')), (2, '*', (1, 'p'), (1, 'r'))), (4, '*', (2, '*', (1, 't'), (1, 'u')), (2, 'h'))), (8, '*', (4, '*', (2, 'm'), (2, 'o')), (4, 'n'))), (23, '*', (11, '*', (5, '*', (2, 's'), (3, '*', (1, 'x'), (2, '*', (1, 'c'), (1, 'd')))), (6, ' ')), (12, '*', (6, '*', (3, 'a'), (3, 'e')), (6, '*', (3, 'f'), (3, 'i')))))]
		input_code = "0010000111111100010111111000101110001110111011001011000100000100000111011011110010100011101001100101111011100100110001110111010111001100101100111111101100000"
		output_text = "this is an example for huffman encoding"
		self.assertEqual(self.huffman.decode(input_code), output_text)

if __name__ == "__main__":
	unittest.main()
