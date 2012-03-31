import math
from pymongo import Connection, collection


class BitMap(object):
    BITS_IN_CHR = 8

    def __init__(self, M):
        self.bmap = [chr(0)] * int(math.ceil(M/8.0))

    def __getitem__(self, ind):
        #compute which byte (chr) the ind belongs to
        byte_ind = ind/self.BITS_IN_CHR
        bit_ind  = ind%self.BITS_IN_CHR
        return (ord(self.bmap[byte_ind]) & 1<<bit_ind)!=0

    def __setitem__(self, ind, val):
        #compute which byte (chr) the ind belongs to
        assert(val == True or val == False)
        byte_ind = ind/self.BITS_IN_CHR
        bit_ind  = ind%self.BITS_IN_CHR
        if val:
            self.bmap[byte_ind] = chr(ord(self.bmap[byte_ind]) | 1<<bit_ind)
        else:
            self.bmap[byte_ind] = chr(ord(self.bmap[byte_ind]) ^ 1<<bit_ind)

#DEFAULT HASH FUNCTIONS
def h1(key, max_out):
    return (key.__hash__())%max_out

def h2(key, max_out):
    return (key[::-1].__hash__())%max_out


class BloomFilter(object):
    
    def __init__(self, M=1000, filters=[h1,h2], keys=None):
        #self._bmap = [0]*M #<- depricated
        self._total_accs = 0
        self._total_misses = 0
        self._bmap = BitMap(M)
        self._M = M;
        self._filters = filters
        if(keys):
            self.add_keys(keys)

    def add_keys(self, keys):
        for key in keys:
            self.add_key(key)

    def add_key(self, key):
        #apply filters
        for bit_ind in map(lambda f: f(key, self._M), self._filters):
            self._bmap[bit_ind] = 1

    def contains(self,key):
        self.inc_accs()
        for bit_ind in map(lambda f: f(key, self._M), self._filters):
            if not(self._bmap[bit_ind]):
                return False
        return True

    def get_bmap(self):
        return self._bmap
    
    def inc_accs(self):
        self._total_accs += 1

    def inc_misses(self):
        self._total_misses += 1

    def get_miss_rate(self):
        #return error rate (e.g., #misses / #total access)
        return self._total_misses / float(self._total_accs)

def bloomify(coll_obj, coll_key, M=None):
    """
    Modifies a pymongo.collection.Collection object's find() calls to access
    a bloom filter. This will reduce the number of database queries.
    Input:
        coll_obj       - instance of pymongo.collection.Collection
        coll_key (str) - given a document in the collection, the key will
                         be used to extract out elements to use in the 
                         bloomfilter.
        M (int)        - number of bits to use in the bloomfilter 
                         (defaults to 2x docs in coll_obj)
    """
    assert( type(coll_obj) is collection.Collection )
    #1. construct bloom filter
    coll_itr = coll_obj.find()
    M = 10*coll_itr.count() if not(M) else M
    bf = BloomFilter(M)
    #2. add items to bloom filter
    for doc in coll_itr:
        #determine if the document contains the key
        if coll_key in doc:
            bf.add_key(doc[coll_key])
    #3. construct new find_one function
    orig_find_one = coll_obj.find_one
    def new_find_one(spec_or_id=None, *args, **kwargs):
        """
        find_one function to overwrite.
        note: it does not require a "self" argument
        """
        if spec_or_id and (type(spec_or_id) is dict):
            if (coll_key in spec_or_id) and not(bf.contains(spec_or_id[coll_key])):
                    return None
        result = orig_find_one(spec_or_id, *args, **kwargs)
        if not(result): #false-positive occured (a miss)
            bf.inc_misses()
        return result
    #4. construct new insert function
    orig_insert = coll_obj.insert
    def new_insert(doc_or_docs, *args, **kwargs):
    	if isinstance(doc_or_docs, dict):
    		try:
    			bf.add_key(doc_or_docs[coll_key])
    		except KeyError:
    			pass
    	else:
    		bf.add_keys((doc[coll_key] for doc in doc_or_docs if coll_key in doc))
    	orig_insert(doc_or_docs, *args, **kwargs)
    #5. re-assign find_one and insert
    coll_obj._bf = bf
    coll_obj.find_one = new_find_one
    coll_obj.insert = new_insert
    return coll_obj



