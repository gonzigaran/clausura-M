import logging
from itertools import product, combinations
import numpy as np
import datetime
from collections import defaultdict

from coclon_utils import gen_coclones


class Node(object):

    def __init__(self, partial_func, code) -> None:
        self.partial_func = partial_func
        self.code = code
    
    def copy(self):
        from copy import deepcopy
        return deepcopy(self)

def lt_list(list1, list2):
    return all(a <= b for a in list1 for b in list2)

def next_pair(a, b, n):
    if b < n-1:
        return (a, b+1)
    elif b == n - 1 and a < n-1:
        return (a+1, 0)
    return (0, 0)  

def generate_preserv_table(relations, universe):
    n = len(universe)
    table = {}

    for ((a, b) , (c, d)) in combinations(product(universe, repeat=2), 2):
        for fab, fcd in product(universe, repeat=2):
            pair1, pair2 = (a, b, fab), (c, d, fcd)
            code = [True]*len(relations)
            for i in range(len(relations)):
                rel = relations[i]
                preserve = pair_preserve_relation(pair1, pair2, rel) and \
                            pair_preserve_relation(pair2, pair1, rel)
                code[i] = preserve
            table[(pair1, pair2)] = code

    return table

def pair_preserve_relation(pair1, pair2, relation):
    (a, b, fab), (c, d, fcd) = pair1, pair2
    if ((a,a) in relation) and ((b,b) in relation) and ((fab, fab) not in relation):
        return False
    if ((a,c) in relation) and ((b,d) in relation) and ((fab, fcd) not in relation):
        return False
    return True


def gen_clones(algebra, coclones_and_generators=None):
    universe = algebra.universe
    assert universe == list(range(len(universe)))
    n = len(universe)
    if coclones_and_generators:
        assert len(coclones_and_generators) == 2
        (coclones, generators) = coclones_and_generators
    else:
        (coclones, generators) = gen_coclones(algebra)

    subuniverses = list(set.union(*[set(g) for g in generators]))
    relations = [sub.list_of_pairs() for sub in subuniverses]
    table = generate_preserv_table(relations, universe)

    clones = defaultdict(list)
    coclones_indexes = range(len(coclones))
    gen_codes = {}
    for i in coclones_indexes:
        code = [sub in coclones[i] for sub in subuniverses]
        gen_codes[i] = code
        clones[i] = []
    
    print(gen_codes)

    nodes_queue = []

    for x in range(n):
        code = [True]*len(relations)
        nodes_queue.append(Node([(0,0,x)], code))
    
    max_len_partial_func = 1

    while nodes_queue:
        node = nodes_queue.pop(0)
        if len(node.partial_func) > max_len_partial_func:
            max_len_partial_func = len(node.partial_func)
            print("máxima cantidad de pares del dominio: %s" % len(node.partial_func))
        last_pair = node.partial_func[-1]
        (a, b) = next_pair(last_pair[0], last_pair[1], n)
        for x in range(n):
            if len(nodes_queue) % 100000 == 0:
                print("quedan %s nodos" % len(nodes_queue))
            new_node = node.copy()
            new_pair = (a, b, x)
            for pair in new_node.partial_func:
                new_node.code = [a and b for a, b in zip(new_node.code, table[(pair, new_pair)])]
            new_node.partial_func.append(new_pair)
            if a == n-1 and b == n-1:
                if new_node.code in gen_codes.values():
                    code_index = list(gen_codes.values()).index(new_node.code)
                    clones[code_index].append(new_node.partial_func)
            elif (
                not lt_list(new_node.code, gen_codes[19]) and
                not lt_list(new_node.code, gen_codes[0]) and
                not lt_list(new_node.code, gen_codes[2]) and
                not lt_list(new_node.code, gen_codes[5]) and
                not lt_list(new_node.code, gen_codes[25])
            ):
                nodes_queue.append(new_node)

    return clones

        

