class Huffman:

	def getTree(self, data):
		def getFrequencies(data):
			f = {}
			for c in data:
				f[c] = 1 if f.get(c) == None else f[c] + 1
			return sorted([(value,key) for (key,value) in f.items()])
		def buildTree(f):
			if len(f) == 1:
				return f
			f = sorted([(f[0][0] + f[1][0], '*', f[0], f[1])] + f[2:])
			return buildTree(f)
		f = getFrequencies(data)
		return buildTree(f)

	def encode(self, data):
		def getNext(t, c):
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
		self.tree = self.getTree(data)
		code = ""
		for c in data:
			code += getNext(self.tree[0], c)
		return code

	def decode(self, code):
		def getNext(t, code):
			if len(t) == 4:
				if code[0] == "0":
					return getNext(t[2], code[1:])
				else:
					return getNext(t[3], code[1:])
			return t[1], code
		data = ""
		stop = False
		while stop == False:
			token, code = getNext(self.tree[0], code)
			if code == "":
				stop = True
			data += token
		return data

def main():
	txt = "this is an example for huffman encoding"
	huffman = Huffman()
	code = huffman.encode(txt)
	print(code)
	value = huffman.decode(code)
	print(value)

if __name__ == "__main__":
	main()
