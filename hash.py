import random
#from Crypto.Hash import SHA256
from hashlib import sha256
from collections import defaultdict
from time import time
from string import printable
from itertools import product, chain, count
from array import array
from math import log

log2 = lambda x: log(x)/log(2)
bits = lambda x: int(log2(x)+1)

def get_lsbs_str(mystr, l=50):
	result = []
	chars = l / 8
	rem = l % 8
	if rem:
		result += [chr(ord(mystr[-(chars + 1)]) & (2**bits(rem))-1)]
	if chars:
		result += mystr[-chars:]
	return "".join(result)

alphabet = printable[:-5]
def get_rand_block():
	blocks = iter("".join([random.choice(alphabet) for x in range(64)]) for x in count())
	while True:
		yield next(blocks)

def get_proc_block():
	blocks = chain(*[product(*([alphabet]*i)) for i in range(60)])
	while True:
		yield "".join(next(blocks))

def results():
	d = {}
	t = time()
	iterator = get_proc_block()
	for i in xrange(2**25):
		if not (i % 100000):
			print i, time()-t
			t = time()
		block = next(iterator)
		key = get_lsbs_str(sha256(block).digest(), 50)
		if key in d:
			print i
			print block
			break
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
	results()
