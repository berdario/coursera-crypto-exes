import random
#from Crypto.Hash import SHA256
from hashlib import sha256
from collections import defaultdict
from time import time
from string import printable
from itertools import product, chain, count
from array import array

from pymongo import Connection

db = Connection().hashes.collection

def get_lsbs_str(mystr):
	chrlist = list(mystr)
	result1 = [chr(ord(chrlist[-7])&(3))]
	result2 = chrlist[-6:]
	return "".join(result1 + result2).encode("base64")

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
	t = time()
	elements = {}
	iterator = get_proc_block()
	for i in xrange(2**33):
		if not (i % 100000):
			print i, time()-t
			t = time()
		if not (i % 1000000) and i>1:
			db.insert(elements.values())
			elements = []
		block = next(iterator)
		key = get_lsbs_str(sha256(block).digest())
		el = elements.get(key)
		el = el or db.find_one({"hash": key})
		if el:
			print key, block, el['value']
			break
		elements[key]={"hash": key, "value": block}
	
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
	db.drop()
	results()
