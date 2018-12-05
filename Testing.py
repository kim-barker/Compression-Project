from camzip2 import camzip
from camunzip2 import camunzip
import time

filename = 'hamlet_copy.txt'

start = time.time()
alphabet = camzip('arithmetic', filename, 67)
end = time.time()
print('Zip Time: ', end - start)
print('encoded')

start2 = time.time()
camunzip(filename + '.cza', alphabet)
end2 = time.time()
print('Unzip Time: ', end2 - start2)
print('decoded')

method_names = ['shannon_fano', 'huffman', 'arithmetic']
method = ['s', 'h', 'a']

from filecmp import cmp
from os import stat
from json import load

Nin = stat(filename).st_size
print(f'Length of original file: {Nin} bytes')
Nout = stat(filename + '.cza').st_size
print(f'Length of compressed file: {Nout} bytes')
print(f'Compression rate: {8.0*Nout/Nin} bits/byte')
with open(filename + '.czp', 'r') as fp:
    freq = load(fp)
pf = dict([(a, freq[a]/Nin) for a in freq])
#print(f'Entropy: {H(pf)} bits per symbol')
if cmp(filename,filename+'.cuz'):
    print('The two files are the same')
else:
    print('The files are different')
