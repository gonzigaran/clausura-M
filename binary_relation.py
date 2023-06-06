
import numpy
from folpy.utils import indent


class BinaryRelation(object):

    """
    Abstracción para trabajar con relaciones binarias, representadas como 
    matrices de transiciones.
    """

    def __init__(self, universe, pairs=None, matrix=None, name=""):
        assert not isinstance(universe, int)
        assert isinstance(universe, list), "El universo debe ser una lista"
        assert pairs or matrix, "la relación hay que cargarla por la lista de pares o la matriz"
        if matrix:
            self.matrix = matrix
        elif pairs:
            assert isinstance(pairs, list), "La relación se debe pasar como una lista de pares"
            assert all(isinstance(x, tuple) or len(x)==2 for x in pairs), "La relación se debe pasar como una lista de pares"
            self.matrix = numpy.zeros((self.universe_card, self.universe_card), 
                                      dtype=bool)
            for (i,j) in pairs:
                self.matrix[i,j] = True
        self.universe = sorted(universe)
        self.universe_card = len(self.universe)
        self.name = name
        self.class_name = type(self).__name__
    

    def __repr__(self):
        if self.name:
            return "%s(name= %s)\n" % (self.class_name, self.name)
        else:
            result = self.class_name + "(\n"
            result += indent(repr(self.universe) + ",\n")
            result += indent(repr(self.matrix) + ",\n")
            return result + ")"
    
    def __eq__(self, other):
        if self.universe != other.universe:
            return False
        if self.matrix != other.matrix:
            return False
        return True
    
    def __ne__(self, other):
        """
        Triste necesidad para la antiintuitiva logica de python
        'A==B no implica !(A!=B)'
        """
        return not self.__eq__(other)

    def T(self):
        """
        La relacion transpuesta (i.e. (a,b) in B.T() si y solo si (b,a) in B)
        """
        return BinaryRelation(self.universe, matrix=self.matrix.T)

    def intersection(self, other):
        """
        La relacion resultante de intersecar self con other
        """
        matrix = self.matrix * other.matrix
        return BinaryRelation(self.universe, matrix=matrix)

    def compose(self, other):
        """
        La relacion resultante de componer self con other
        """
        matrix = self.matrix @ other.matrix
        return BinaryRelation(self.universe, matrix=matrix)


def top_relation(universe):
    pairs = [(a,b) for a in universe for b in universe]
    return BinaryRelation(universe, pairs=pairs)

def bottom_relation(universe):
    pairs = [(a,a) for a in universe]
    return BinaryRelation(universe, pairs=pairs)