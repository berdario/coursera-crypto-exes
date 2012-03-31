import random
from hashlib import sha256
from time import time
from string import printable
from itertools import product, chain, count, islice, groupby
from multiprocessing import Process, Array, Queue, cpu_count
from math import log

from pymongo import Connection
from bloomfilter import wrapping_bloomify

log2 = lambda x: log(x)/log(2)
bits = lambda x: int(log2(x)+1)

baredb = Connection().hashes.collection

def get_lsbs_str(mystr, l=50):
	result = []
	chars = l / 8
	rem = l % 8
	if rem:
		result += [chr(ord(mystr[-(chars + 1)]) & bits(rem))]
	if chars:
		result += mystr[-chars:]
	return "".join(result)

alphabet = printable[:-5]
def get_rand_block():
	blocks = iter("".join([random.choice(alphabet) for x in range(64)]) for x in count())
	while True:
		yield next(blocks)

def get_proc_block():
	blocks = chain(*[product(*([alphabet]*i)) for i in count()])
	while True:
		yield "".join(next(blocks))

def results(array, ctrlq, resultq, offset, step, slice_size=100000):
	# the bigger the slice_size, the easier that some collisions may slip through
	# but, set it too small, and the IO will slow everything down, 100k should be a good compromise
	db = wrapping_bloomify(baredb, "hash", array)
	t = time()
	elements = {}
	slices = (v for k,v in islice(groupby(enumerate(get_proc_block()), lambda t: t[0]/slice_size), offset, None, step))
	# this will return the strings, paired with an increasing index, and group them by slice size
	# e.g. with slice_size=100000, offset=1 (process "id"), and step=2 (2 processes)
	# it'll return the elements from 100000 to 199999 then from 300000 to 399999 and so on
	
	for s in slices:
		for i, value in s:
			key = get_lsbs_str(sha256(value).digest()).encode("hex")
			el = elements.get(key)
			el = el or db.find_one({"hash": key})
			if el:
				resultq.put([key, value, el['value']])
				return
	
			elements[key]={"hash": key, "value": value}

		ctrlq.put("next process")
		print "from", 1+i-slice_size, "to", i, time()-t
		t = time()
		print "miss rate:", db._bf.get_miss_rate()
		db.insert(elements.values())
		elements = {}
	
if __name__ == "__main__":
	baredb.drop()
	array = Array('c', 87500000)
	control_queue, result_queue = Queue(), Queue()
	procs = cpu_count()
	pool = [Process(target=results, args=(array, control_queue, result_queue, i, procs)) for i in range(procs)]
	for p in pool:
		p.daemon = True
		p.start()
		control_queue.get()
	print result_queue.get()

