import logging

from itertools import chain, combinations 
from folpy.utils.parser.parser import Parser
from binary_relation import BinaryRelation, one_rel_closure, two_rels_closure


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

if __name__ == "__main__":
    logging.basicConfig(
        filename='TwoMajorityClones.log',
        format='%(asctime)s - %(levelname)s: %(message)s',
        level=logging.DEBUG
        )

    DM = Parser("Models/DM.model").parse()

    logging.info("Carga de Modelo OK")

    DM2 = DM * DM

    binary_relations = set()
    lozetas = {}

    i=0
    for sub in DM2.subuniverses(proper=False):
        br = BinaryRelation(DM.universe, pairs=sub)
        binary_relations.add(br)
        i += 1
        logging.info("%s : %s %s" % (i, sub, br.repr_by_T()))

        if br == br.repr_by_T():
            closure = one_rel_closure(br)
            if closure not in lozetas.values():
                lozetas[br] = closure
    
    
    logging.info("%s : %s" % ("Tamaño lozetas ", len(lozetas)))

    coclones = list(lozetas.values()).copy()

    for s in powerset(lozetas.values()):
        closure = set()
        for x in s:
            closure = two_rels_closure(closure, x)
            if closure not in coclones:
                coclones.append(closure)

    logging.info("%s : %s" % ("Tamaño coclones ", len(coclones)))

