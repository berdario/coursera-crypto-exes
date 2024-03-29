from itertools import combinations, starmap, product, izip, permutations, groupby
from collections import defaultdict

def xor_str(c1,c2):
	return " ".join([str(ord(a)^ord(b)) for a,b in zip(c1,c2)])

def xor(c1,c2):
	return [chr(ord(a)^ord(b)) for a,b in zip(c1,c2)]


cyp = ["315c4eeaa8b5f8aaf9174145bf43e1784b8fa00dc71d885a804e5ee9fa40b16349c146fb778cdf2d3aff021dfff5b403b510d0d0455468aeb98622b137dae857553ccd8883a7bc37520e06e515d22c954eba5025b8cc57ee59418ce7dc6bc41556bdb36bbca3e8774301fbcaa3b83b220809560987815f65286764703de0f3d524400a19b159610b11ef3e"
,"234c02ecbbfbafa3ed18510abd11fa724fcda2018a1a8342cf064bbde548b12b07df44ba7191d9606ef4081ffde5ad46a5069d9f7f543bedb9c861bf29c7e205132eda9382b0bc2c5c4b45f919cf3a9f1cb74151f6d551f4480c82b2cb24cc5b028aa76eb7b4ab24171ab3cdadb8356f"
,"32510ba9a7b2bba9b8005d43a304b5714cc0bb0c8a34884dd91304b8ad40b62b07df44ba6e9d8a2368e51d04e0e7b207b70b9b8261112bacb6c866a232dfe257527dc29398f5f3251a0d47e503c66e935de81230b59b7afb5f41afa8d661cb"
,"32510ba9aab2a8a4fd06414fb517b5605cc0aa0dc91a8908c2064ba8ad5ea06a029056f47a8ad3306ef5021eafe1ac01a81197847a5c68a1b78769a37bc8f4575432c198ccb4ef63590256e305cd3a9544ee4160ead45aef520489e7da7d835402bca670bda8eb775200b8dabbba246b130f040d8ec6447e2c767f3d30ed81ea2e4c1404e1315a1010e7229be6636aaa"
,"3f561ba9adb4b6ebec54424ba317b564418fac0dd35f8c08d31a1fe9e24fe56808c213f17c81d9607cee021dafe1e001b21ade877a5e68bea88d61b93ac5ee0d562e8e9582f5ef375f0a4ae20ed86e935de81230b59b73fb4302cd95d770c65b40aaa065f2a5e33a5a0bb5dcaba43722130f042f8ec85b7c2070"
,"32510bfbacfbb9befd54415da243e1695ecabd58c519cd4bd2061bbde24eb76a19d84aba34d8de287be84d07e7e9a30ee714979c7e1123a8bd9822a33ecaf512472e8e8f8db3f9635c1949e640c621854eba0d79eccf52ff111284b4cc61d11902aebc66f2b2e436434eacc0aba938220b084800c2ca4e693522643573b2c4ce35050b0cf774201f0fe52ac9f26d71b6cf61a711cc229f77ace7aa88a2f19983122b11be87a59c355d25f8e4"
,"32510bfbacfbb9befd54415da243e1695ecabd58c519cd4bd90f1fa6ea5ba47b01c909ba7696cf606ef40c04afe1ac0aa8148dd066592ded9f8774b529c7ea125d298e8883f5e9305f4b44f915cb2bd05af51373fd9b4af511039fa2d96f83414aaaf261bda2e97b170fb5cce2a53e675c154c0d9681596934777e2275b381ce2e40582afe67650b13e72287ff2270abcf73bb028932836fbdecfecee0a3b894473c1bbeb6b4913a536ce4f9b13f1efff71ea313c8661dd9a4ce"
,"315c4eeaa8b5f8bffd11155ea506b56041c6a00c8a08854dd21a4bbde54ce56801d943ba708b8a3574f40c00fff9e00fa1439fd0654327a3bfc860b92f89ee04132ecb9298f5fd2d5e4b45e40ecc3b9d59e9417df7c95bba410e9aa2ca24c5474da2f276baa3ac325918b2daada43d6712150441c2e04f6565517f317da9d3"
,"271946f9bbb2aeadec111841a81abc300ecaa01bd8069d5cc91005e9fe4aad6e04d513e96d99de2569bc5e50eeeca709b50a8a987f4264edb6896fb537d0a716132ddc938fb0f836480e06ed0fcd6e9759f40462f9cf57f4564186a2c1778f1543efa270bda5e933421cbe88a4a52222190f471e9bd15f652b653b7071aec59a2705081ffe72651d08f822c9ed6d76e48b63ab15d0208573a7eef027"
,"466d06ece998b7a2fb1d464fed2ced7641ddaa3cc31c9941cf110abbf409ed39598005b3399ccfafb61d0315fca0a314be138a9f32503bedac8067f03adbf3575c3b8edc9ba7f537530541ab0f9f3cd04ff50d66f1d559ba520e89a2cb2a83"
,"32510ba9babebbbefd001547a810e67149caee11d945cd7fc81a05e9f85aac650e9052ba6a8cd8257bf14d13e6f0a803b54fde9e77472dbff89d71b57bddef121336cb85ccb8f3315f4b52e301d16e9f52f904"]
dcyp=[x.decode("hex") for x in cyp]
l =  len(dcyp)
xors = starmap(xor, combinations(dcyp,2))
indexes = combinations(range(l),2)
xors = dict(izip(indexes, xors))


is_alnum = lambda x: x==32 or 64<x<91 or 96<x<123 or 47<x<58
is_al = lambda x: x==32 or 64<x<91 or 96<x<123
al = defaultdict(lambda :[])
al.update({chr(i):[] for i in range(128)})
[al[chr(i^j)].append((chr(i),chr(j))) for i,j in product(range(128),range(128)) if is_al(i) and is_al(j)]
# to bootstrap I ignore the numbers


candidates = dict()
for k,this_xor in xors.iteritems():
	first = dcyp[k[0]]
	second = dcyp[k[1]]
	#candidates[k]=[(x, first[i], second[i]) for i,x in enumerate(this_xor) if len(al[x])==2]
	candidates[k]=[i for i,x in enumerate(this_xor) if len(al[x])==2]

# Check that candidates are only those that contain the space character
all_candidates = [k for k,v in al.iteritems() if len(v)==2]
assert not [al[k] for k in all_candidates if all([" " not in t for t in al[k]])]

intersection = lambda x,y: [val for val in x if val in y]
get_candidate = lambda key: candidates.get(tuple(sorted(key)))

spaces = dict()
hid_key = dict()
for n,keys in groupby(permutations(range(l),2), lambda x:x[0]):
	spaces[n] = reduce(intersection, map(get_candidate, keys))
	cmsg = list(dcyp[n])
	hid_key.update({s:ord(cmsg[s])^ord(" ") for s in spaces[n]})

def decrypt(msg):
	keys = hid_key
	codes = map(ord, list(msg))
	"".join(map(chr, [c^keys.get(i,0) for i,c in enumerate(codes)]))

	d = []
	for i,c in enumerate(codes):
		try:
			d.append(c^keys[i])
		except KeyError:
			d.append(63) # 63 == "?"
	return "".join(map(chr,d))

def _update_keys(cmsg, idx, char):
	hid_key[idx]=ord(dcyp[cmsg][idx])^ord(char)

def update_keys(cmsg, idx, char):
	_update_keys(cmsg, idx, char)
	if all(is_alnum(hid_key[idx]^ord(m[idx])) for m in dcyp):
		print "Success!"
	else:
		print "Failure (maybe)"
	print_messages(idx)

def reset_key(idx):
	del hid_key[idx]
	
def print_messages(idx=None):
	if not idx:
		s = slice(None)
	elif idx<5:
		s = slice(idx+5)
	else:
		s = slice(idx-5, idx+5)

	print "\n".join("%2d %s" % (i, decrypt(c)[s]) for i,c in enumerate(dcyp))

final_key = {0: 102, 1: 57, 2: 110, 3: 137, 4: 201, 5: 219, 6: 216, 7: 204, 8: 152, 9: 116, 10: 53, 11: 42, 12: 205, 13: 99, 14: 149, 15: 16, 16: 46, 17: 175, 18: 206, 19: 120, 20: 170, 21: 127, 22: 237, 23: 40, 24: 160, 25: 127, 26: 107, 27: 201, 28: 141, 29: 41, 30: 197, 31: 11, 32: 105, 33: 176, 34: 51, 35: 154, 36: 25, 37: 248, 38: 170, 39: 64, 40: 26, 41: 156, 42: 109, 43: 112, 44: 143, 45: 128, 46: 192, 47: 102, 48: 199, 49: 99, 50: 254, 51: 240, 52: 18, 53: 49, 54: 72, 55: 205, 56: 216, 57: 232, 58: 2, 59: 208, 60: 91, 61: 169, 62: 135, 63: 119, 64: 51, 65: 93, 66: 174, 67: 252, 68: 236, 69: 213, 70: 156, 71: 67, 72: 58, 73: 107, 74: 38, 75: 139, 76: 96, 77: 191, 78: 78, 79: 240, 80: 60, 81: 154, 82: 97}

