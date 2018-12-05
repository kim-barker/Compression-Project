from math import log2, ceil
from trees import *
import collections

def adaptive_huff(x, alphabet):

    y = [] # output
    
    # create starting tree xt
    xt = huffman(alphabet)

    # create dictionary to store weights of nodes
    w = {}
    for parent, childn, label in xt:
            w[label] = 1

    # update weights and trees each iteration
    for k in range(len(x)-2):
        a = x[k] # symbol in x
        c = xtree2code(xt)
        
        if a not in c:
            raise NameError('Symbol is not a leaf')
        
        y.extend(c[a])
        
        w[a] += 1
        xt = update_tree(a, w, xt)
        
    return y

def adaptive_huffman_decode(y, alphabet):
    
    x = [] # input
    
    # create starting tree xt
    xt = huffman(alphabet)

    # create dictionary to store weights of nodes
    w = {}
    for parent, childn, label in xt:
            w[label] = 1

    n = update_root(xt)
    
    for a in y:
        if len(xt[n][1]) < a:
            raise NameError('Symbol exceeds alphabet size in tree node')
        if xt[n][1][a] == -1:
            raise NameError('Symbol not assigned in tree node')
        
        n = xt[n][1][a]

        if len(xt[n][1]) == 0: # it's a leaf!
            symbol = xt[n][2]
            x.append(xt[n][2])

            w[symbol] += 1
            xt = update_tree(symbol, w, xt)
            n = update_root(xt)
    return x
    
def update_root(xt):
        'A function that returns the index of the root of a tree'
        root = [k for k in range(len(xt)) if xt[k][0]==-1]
        if len(root) != 1:
            raise NameError('Tree with no or multiple roots!')
        root = root[0]
        n = root

        return root
        
def update_tree(a, w, xt):
    'A function that updates the tree when the weight of symbol a is increased by 1'

    W = w[a] - 1 # find W, the weight of symbol a minus 1 
    
    nodes_W = [] # list to store nodes of weight W
    
    for parent, childn, label in xt:
        if w[label] == W:
            nodes_W.append([label, childn]) # add nodes of weight W to list
    
    if len(nodes_W) >= 1:
        # if more than one node of weight W, choose the one with least children
        nodes_W.sort(key=lambda tup: tup[1])
        node_swap = nodes_W[0]

        # swap node weight W with new node weight W+1
        node_swap_index = [y[2] for y in xt].index(node_swap[0])
        node_swap_parent = xt[node_swap_index][0]
        node_index = [y[2] for y in xt].index(a)
        node_parent = xt[node_index][0]
        
        xt[node_swap_index][0] = node_swap_parent
        xt[node_index][0] = node_parent
        
    else:
        # if no nodes of weight W, tree is unchanged
        pass

    return xt
    
def huffman(alphabet):

    # start with an equal probability distribution
    p = {}
    for a in alphabet:
        p[a] = (1/len(alphabet))
    
    xt = [[-1,[],a] for a in p] # create an xtree with all the source symbols orphaned
    p = [(k,p[a]) for k,a in zip(range(len(p)),p)] # label the probabilities with a "pointer"
    
    nodelabel = len(p) # label all remaining nodes with numbers starting from len(p)

    while len(p) > 1:

        p = sorted(p, key = lambda el:el[1]) # sort probabilities in ascending order

        xt.append([[-1],[],str(nodelabel)]) #append new node
        nodelabel += 1 # incremement label

        # assign parent of the nodes pointed to by the smallest probabilities 
        xt[p[0][0]][0] = len(xt)-1
        xt[p[1][0]][0] = len(xt)-1
        
        # assign the children of new node to be the nodes pointed to by p[0] and p[1]
        xt[-1][1] = [p[0][0],p[1][0]]

        # create a new entry pointing to the new node in the list of probabilities
        sumprob = p[0][1]+p[1][1]
        newEntry = (len(xt)-1,sumprob)
        p.append(newEntry)

        # remove the two nodes with the smallest probability
        p.pop(0)
        p.pop(0)
    
    xt[-1][0]=-1

    return xt

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

##f = open('hamlet.txt', 'r')
##hamlet = f.read()
##f.close()
##hamlet = hamlet[:500000] + ' '
##alphabet = alphabet(hamlet, 67)
##y = adaptive_huff(hamlet, alphabet)
##x = adaptive_huffman_decode(y, alphabet)
##print(''.join(x[:294]))
