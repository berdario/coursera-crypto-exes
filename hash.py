import random
#from Crypto.Hash import SHA256
from hashlib import sha256
from collections import defaultdict
from time import time
from string import printable
from itertools import product, chain, count
from array import array

def get_lsbs_str(mystr):
	chrlist = list(mystr)
	result1 = [chr(ord(chrlist[-7])&(3))]
	result2 = chrlist[-6:]
	return array("c", result1 + result2)

alphabet = printable[:-5]
def get_rand_block():
	blocks = iter("".join([random.choice(alphabet) for x in range(64)]) for x in count())
	while True:
		yield next(blocks)

def get_proc_block():
	blocks = chain(*[product(*([alphabet]*i)) for i in range(60)])
	while True:
		yield array("c", (next(blocks)))

def results():
	d = dict()
	t = time()
	iterator = get_rand_block()
	for i in range(2**25):
		if not (i % 100000):
			print i, time()-t
			t = time()
		block = next(iterator)
		key = get_lsbs_str(sha256(block).digest())
		if key in d:
			print d[key]
			print block
		d[key] = block
	
	#res = filter(lambda t:len(t[1])>1, d.iteritems())
	#return res
	
# blocks = (("%0128x" % i).decode("base64") for i in xrange(2**512))
# 
# def res():
# 	d = defaultdict(lambda :[])
# 	for block in blocks:
# 		d[get_lsbs_str(sha256(block).digest())].append(block)
# 
# 	res = filter(lambda t:len(t[1])>1, d.iteritems())
# 	return res

if __name__ == "__main__": 
	pass
