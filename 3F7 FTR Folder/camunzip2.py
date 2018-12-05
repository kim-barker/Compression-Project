from trees import *
from vl_codes import *
from adaptive_arithmetic import adaptive_arithmetic_decode
from adaptive_huffman import adaptive_huffman_decode
from adaptive_arithmetic import alphabet as alph
import arithmetic
from json import load
from sys import argv, exit


def camunzip(filename, alphabet):
    if (filename[-1] == 'h'):
        method = 'huffman'
    elif (filename[-1] == 's'):
        method = 'shannon_fano'
    elif (filename[-1] == 'a'):
        method = 'arithmetic'
    elif (filename[-1] == 'f'):
        method = 'adaptive_huffman'
    elif (filename[-1] == 'r'):
        method = 'adaptive_arithmetic'
    else:
        raise NameError('Unknown compression method')
    
    with open(filename, 'rb') as fin:
        y = fin.read()
    y = bytes2bits(y)

    pfile = filename[:-1] + 'p'
    with open(pfile, 'r') as fp:
        frequencies = load(fp)
    n = sum([frequencies[a] for a in frequencies])
    p = dict([(int(a),frequencies[a]/n) for a in frequencies])

    if method == 'huffman' or method == 'shannon_fano':
        if (method == 'huffman'):
            xt = huffman(p)
            c = xtree2code(xt)
        else:
            c = shannon_fano(p)
            xt = code2xtree(c)

        x = vl_decode(y, xt)

    elif method == 'arithmetic':
        x = arithmetic.decode(y,p,n)

    elif method == 'adaptive_huffman':
        x = adaptive_huffman_decode(y, alphabet)

    elif method == 'adaptive_arithmetic':
        x = adaptive_arithmetic_decode(y, alphabet)

    else:
        raise NameError('This will never happen (famous last words)')
    
    # '.cuz' for Cam UnZipped (don't want to overwrite the original file...)
    outfile = filename[:-4] + '.cuz' 

    with open(outfile, 'wb') as fout:
        fout.write(bytes(x))


##if __name__ == "__main__":
##    if (len(argv) != 2):
##        print('Usage: python %s filename\n' % argv[0])
##        print('Example: python %s hamlet.txt.czh' % argv[0])
##        print('or:      python %s hamlet.txt.czs' % argv[0])
##        print('or:      python %s hamlet.txt.cza' % argv[0])
##        exit()
##
##    camunzip(argv[1])
