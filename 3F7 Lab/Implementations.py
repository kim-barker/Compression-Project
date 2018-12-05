# 3F7 Coding

# 2. Trees
from trees import xtree2newick, code2xtree
t = [-1, 0, 0, 1, 1, 3, 3, 4, 2]
#print(tree2newick(t,['root','child 0', 'grandchild 0','g','a']))
#print(code2tree(tree2code([3,3,4,4,-1])))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  :?OP))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))                             
#print(tree2newick(t))

# 3. Shannon Coding

##from random import random
##p = [random() for k in range(10)]
##p = dict([(chr(k+ord('a')),p[k]/sum(p)) for k in range(len(p))])
##print(f'Probability distribution: {p}\n')
##c = shannon_fano(p)
##print(f'Codebook: {c}\n')
##xt = code2xtree(c)
##print(f'Cut and paste for phylo.io: {xtree2newick(xt)}')


# 4. Compressing a File

from vl_codes import shannon_fano
f = open('hamlet.txt', 'r')
hamlet = f.read()
f.close()

from itertools import groupby
frequencies = dict([(key, len(list(group))) for key, group in groupby(sorted(hamlet))])
Nin = sum([frequencies[a] for a in frequencies])
p = dict([(a,frequencies[a]/Nin) for a in frequencies])
print(f'File length: {Nin}')

c = shannon_fano(p)
##print(len(code2xtree(c)))
##print(c)
#print(xtree2newick(code2xtree(c)))

from vl_codes import vl_encode
hamlet_sf = vl_encode(hamlet,c);
#print(f'Length of binary sequence: {len(hamlet_sf)}')

from vl_codes import bytes2bits, bits2bytes
x = bits2bytes([0,1,1,0,1,1,0,0,0])
print(x)
print([format(a, '08b') for a in x])
#y = bytes2bits(x)
#print(f'The original bits are: {y}')

##hamlet_zipped = bits2bytes(hamlet_sf)
##Nout = len(hamlet_zipped)
##print(f'Length of compressed string: {Nout}')
##
from math import log2
H = lambda pr: -sum([pr[a]*log2(pr[a]) for a in pr])
#print(f'Entropy: {H(p)}')

##from vl_codes import vl_decode
##xt = code2xtree(c)
##hamlet_unzipped = vl_decode(hamlet_sf,xt)
##print(f'Length of the unzipped file: {len(hamlet_unzipped)}')
##print(''.join(hamlet_unzipped[:294]))

from camzip2 import camzip
from camunzip2 import camunzip

import time

start = time.time()
camzip('huffman', 'hamlet.txt')
end = time.time()
print('Zip Time: ', end - start)
start2 = time.time()
camunzip('hamlet.txt.cza')
end2 = time.time()
print('Unzip Time: ', end2 - start2)

method_names = ['shannon_fano', 'huffman', 'arithmetic']
method = ['s', 'h', 'a']

from filecmp import cmp
from os import stat
from json import load
filename = 'hamlet.txt'
Nin = stat(filename).st_size
print(f'Length of original file: {Nin} bytes')
Nout = stat(filename + '.cz' + method[2]).st_size
print(f'Length of compressed file: {Nout} bytes')
print(f'Compression rate: {8.0*Nout/Nin} bits/byte')
with open(filename + '.czp', 'r') as fp:
    freq = load(fp)
pf = dict([(a, freq[a]/Nin) for a in freq])
print(f'Entropy: {H(pf)} bits per symbol')
if cmp(filename,filename+'.cuz'):
    print('The two files are the same')
else:
    print('The files are different')

# 5. Huffman Algorithm
from vl_codes import huffman
##xt = huffman(p)
##print(xtree2newick(xt))

# 6. Arithmetic Coding
##import arithmetic as arith
##arith_encoded = arith.encode(hamlet, p)
##arith_decoded = arith.decode(arith_encoded, p, Nin)
##print('\n'+''.join(arith_decoded[:294]))
