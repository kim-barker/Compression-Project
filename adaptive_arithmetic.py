from math import floor, ceil
from sys import stdout as so
from bisect import bisect
import collections

# Set up integer arithmetic coding
precision = 32
one = int(2**precision - 1)
quarter = int(ceil(one/4))
half = 2*quarter
threequarters = 3*quarter
print('0.25, 0.5, 0.75, 1', (quarter, half, threequarters, one))

def adaptive_arithmetic_encode(x, alphabet):

        #Set initial variables
        interval = (0, one)
        straddle = 0 # initialise the straddle counter to 0

        f = collections.OrderedDict()
        for char in alphabet:
                f[char] = 1
        
        encoded = []
        length = len(x)

        for k in range(len(x)):
                a = x[k]                   
                interval, y, straddle = encode_symbol(a, f, k, interval, length, straddle)
                f[a] += 1  
                encoded += y

        # termination bits
        lo, hi = interval[0], interval[1]
        straddle += 1 # adding 1 to straddle for "good measure" (ensures prefix-freeness)
        if lo < quarter:
                encoded.append(0)
                for i in range(straddle): encoded.append(1)
        else:
                encoded.append(1)
                for i in range(straddle):encoded.append(0)
        
        return encoded


def encode_symbol(b, f, i, interval, length, straddle):
    'Encode single input symbol and calculate running probability'
    # b = single symbol
    # f = dictionary storing symbol frequencies
    # i = ith symbol in input being coded
    # interval = current hi, lo value
    
    # Update probability estimates
    total_freq = len(f) + i
    
    p = {} #dictionary to store running probabilities
    for a in f: # for every frequency in f
        p[a] = f[a]/(total_freq)

    # Compute cumulative probability
    cp = [0.0]
    for a in p: # for every probability in p
        cp.append(cp[-1]+p[a])
    cp.pop()

##    print('Test for 1:', cp[-1]+p[b])
            
    cp = dict([(a,mf) for a,mf in zip(p,cp)])
    
    y = [] # initialise encoded list
    lo,hi = interval[0], interval[1] # initialise lo and hi

##    print('f', f)
##    print('p', p)
##    print('cp',cp)
    if i % 100 == 0:
        so.write('Arithmetic encoded %d%%    \r' % int(floor(i/length*100)))
        so.flush()

##    print('starting lohi', (lo, hi))
##    print('cp,p', cp[b], p[b])
    lohi_range = hi-lo+1
    lo = lo + int(ceil(cp[b]*lohi_range))
    hi = lo + int(floor(p[b]*lohi_range))
    if hi >= one:
            hi -= 1
##    print(int(ceil(cp[b]*lohi_range)))
##    print((p[b]*lohi_range))
##    print(floor(p[b]*lohi_range))
##    print(int(floor(p[b]*lohi_range)))
##    print('adj lohi', (lo, hi))

    if (lo == hi):
            raise NameError('Zero interval!')

    while True:
            if hi < half: # if lo < hi < 1/2
                y.append(0)
                for i in range(straddle): y.append(1)
                straddle = 0 # zero the straddle counter
                lo *= 2
                hi = (2*hi) +1
##                print('here, lohi', (lo, hi))
            elif lo >= half: # if hi > lo >= 1/2
                y.append(1)
                
                for i in range(straddle):
                        y.append(0)
        
                straddle = 0 # reset the straddle counter
##                print('here start, lohi', (lo, hi))
                lo -= half
                hi -= half
##                print('here half lohi', (lo, hi))
                lo *= 2
                hi = 2*hi +1
##                print('here2, lohi', (lo, hi))
			
            elif lo >= quarter and hi < threequarters: # if 1/4 < lo < hi < 3/4

                straddle += 1
                
                lo -= quarter
                hi -= quarter

                lo *= 2
                hi = 2*hi +1
##                print('here3, lohi', (lo, hi))
                
            else:
##                print('break else')
                break
        
    interval = (lo, hi)

    return interval, y, straddle

def adaptive_arithmetic_decode(encoded, alphabet):

        #Set initial variables
        interval = (0, one)
        char_count = '0'
        eof = False

        f = collections.OrderedDict()
        for char in alphabet:
                f[char] = 1
        
        length = len(encoded)

        encoded.extend((precision)*[0]) # dummy zeros to prevent index out of bound errors
        x = length*[0] # initialise all zeros

        # initialise by taking first 'precision' bits from y and converting to a number
        value = int(''.join(str(a) for a in encoded[0:precision]), 2)
        position = precision # position where currently reading y
        
        for k in range(length):
                interval, value, position, x, eof = decode_symbol(encoded, f, k, x, interval, value, position)
##                print('symbol', x[k])
                if eof == True:
##                        print('eof')
##                        print('eof f', f)
                        x = x[:k]
                        break

                f[x[k]] += 1
                
        return x

def decode_symbol(y, f, k, x, interval, value, position):

    # y = single received symbol
    # f = dictionary storing symbol frequencies
    # i = ith symbol in input being coded
    # interval = current hi, lo value

    eof = False # for termination step
    
    # Update probability estimates
    total_freq = len(f) + k
    p = {} #dictionary to store running probabilities
    for a in f: # for every frequency in f
        p[a] = f[a]/(total_freq)

    # Compute cumulative probability
    cp = [0.0]
    for a in p: # for every probability in p
        cp.append(cp[-1]+p[a])
    cp.pop()
    
    alphabet = list(p)

    p = list(p.values())

    lo, hi = interval[0], interval[1]
    lohi_range = hi - lo + 1

    a = bisect(cp, (value-lo)/lohi_range) - 1
    x[k] = alphabet[a] # encoded alphabet[a]

    lo = lo + int(ceil(cp[a]*lohi_range))
    hi = lo + int(floor(p[a]*lohi_range))
    if hi >= one:
            hi -= 1    
    if (lo == hi):
            raise NameError('Zero interval!')
    while True:
        if position == len(y):
                eof= True
                print('eof raised here')
                break
        if hi < half:
                
                lo = 2*lo
                hi = 2*hi + 1
                value = 2*value + y[position]
                position += 1
                
                # do nothing
##                pass
        elif lo >= half:
                lo = lo - half
                hi = hi - half
                value = value - half
                
                lo = 2*lo
                hi = 2*hi + 1
                value = 2*value + y[position]
                position += 1
                
        elif lo >= quarter and hi < threequarters:
                lo = lo - quarter
                hi = hi - quarter
                value = value - quarter
                
                lo = 2*lo
                hi = 2*hi + 1
                value = 2*value + y[position]
                position += 1
                
        else:
                break

       
    interval = (lo, hi)

    return interval, value, position, x, eof

def alphabet(text, max_char):
        'A function that returns all possible symbols in a given text'
        alphabet = []
        for k in range(len(text)):
                a = text[k] # symbol a
                if a not in alphabet:
                        alphabet.append(a)
                if len(alphabet) == max_char:
                        break

        return alphabet

f = open('hamlet.txt', 'r')
hamlet = f.read()
f.close()
alph = alphabet(hamlet, 67)
print(type(hamlet))

##hamlet = hamlet[0:100]
##hamlet = hamlet + 'z'
##print(hamlet)
##
##
##from itertools import groupby
##frequencies = dict([(key, len(list(group))) for key, group in groupby(sorted(hamlet))])
##Nin = sum([frequencies[a] for a in frequencies])
##p = dict([(a,frequencies[a]/Nin) for a in frequencies])
##print(f'File length: {Nin}')
##
##print(len(p))
##dyn_arith_encoded = encode(hamlet, alph)
##dyn_arith_decoded = decode(dyn_arith_encoded, alph)
##print('dad', dyn_arith_decoded )
##print('\n'+''.join(dyn_arith_decoded[:]))
