from sympy.core import Basic
from sympy.functions import floor

class Prufer(Basic):
    """
    The Prufer correspondence is an algorithm that describes the
    bijection between labeled trees and the Prufer code. A Prufer
    code of a labeled tree is unique upto isomorphism and has
    a length of n - 2.
    Prufer sequences were first used by Heinz Prufer to give a
    proof of Cayley's formula.

    Reference:
    [1] http://mathworld.wolfram.com/LabeledTree.html
    """
    _prufer_repr = None
    _tree_repr = None
    _nodes = None
    _rank = None

    @property
    def prufer_repr(self):
        if self._prufer_repr is None:
            self._prufer_repr = self.to_prufer(self.tree_repr, self.nodes)
        return self._prufer_repr

    @property
    def tree_repr(self):
        if self._tree_repr is None:
            self._tree_repr = self.to_tree(self.prufer_repr)
        return self._tree_repr

    @property
    def nodes(self):
        return self._nodes

    @property
    def rank(self):
        if self._rank is None:
            self._rank = self.prufer_rank()
        return self._rank

    @staticmethod
    def to_prufer(tree, n):
        """
        Convert to Prufer code.

        Examples:
        >>> from sympy.combinatorics.prufer import Prufer
        >>> a = Prufer([[0, 1], [0, 2], [0, 3]], 4)
        >>> a.prufer_repr
        [0, 0]
        """
        d = [0] * n
        L = [0] * n
        for edge in tree:
            list.sort(edge)
            d[edge[0]] += 1
            d[edge[1]] += 1
        for i in xrange(0, n - 2):
            x = n - 1
            while d[x] != 1:
                x -= 1
            y = n - 1
            while True:
                e = [x, y]
                list.sort(e)
                if e in tree:
                    break
                y -= 1
            L[i] = y
            d[x] -= 1
            d[y] -= 1
            tree.remove(e)
        return L[:2]

    @staticmethod
    def to_tree(prufer):
        """
        Converts to tree representation.

        Examples:
        >>> from sympy.combinatorics.prufer import Prufer
        >>> a = Prufer([0, 2], 4)
        >>> a.tree_repr
        [[3, 0], [1, 2], [2, 0]]
        """
        tree = []
        prufer.append(0)
        n = len(prufer) + 1
        d = [1] * n
        for i in xrange(0, n - 2):
            d[prufer[i]] += 1
        for i in xrange(0, n - 1):
            x = n - 1
            while d[x] != 1:
                x -= 1
            y = prufer[i]
            d[x] -= 1
            d[y] -= 1
            tree.append([x, y])
        return tree

    def prufer_rank(self):
        """
        Computes the rank of a Prufer sequence.

        Examples:
        >>> from sympy.combinatorics.prufer import Prufer
        >>> a = Prufer([[0, 1], [0, 2], [0, 3]], 4)
        >>> a.rank
        0
        """
        r = 0
        p = 1
        for i in xrange(self.nodes - 3, -1, -1):
            r = r + p*self.prufer_repr[i]
            p = p*self.nodes
        return r

    @classmethod
    def unrank(self, rank, n):
        """
        Finds the unranked Prufer sequence.

        Examples:
        >>> from sympy.combinatorics.prufer import Prufer
        >>> Prufer.unrank(0, 4)
        Prufer([0, 0])
        """
        L = [0] * (n - 2)
        for i in xrange(n - 3, -1, -1):
            L[i] = rank % n + 1
            rank = int(floor((rank - L[i] + 1)/n))
        return Prufer(map(lambda x: x - 1, L))

    def __new__(cls, *args, **kw_args):
        """
        The constructor for the Prufer object.

        Examples:
        >>> from sympy.combinatorics.prufer import Prufer
        >>> a = Prufer([[0, 1], [0, 2], [0, 3]], 4)
        >>> a.prufer_repr
        [0, 0]
        >>> b = Prufer([1, 3])
        >>> b.tree_repr
        [[2, 1], [1, 3], [3, 0]]
        """
        ret_obj = Basic.__new__(cls, *args, **kw_args)
        if isinstance(args[0][0], list):
            ret_obj._tree_repr = args[0]
            ret_obj._nodes = args[1]
        else:
            ret_obj._prufer_repr = args[0]
            ret_obj._nodes = len(ret_obj._prufer_repr) + 2
        return ret_obj
