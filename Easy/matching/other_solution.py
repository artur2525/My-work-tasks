from typing import List
from typing import Tuple


def extend_matches(pairs: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    '''return real pairs'''
    if pairs == []:

        return []

    elif len(pairs) == 1:

        return pairs

    else:
        def sor(pairs):
            new_pairs = []
            values = []
            for i in pairs:
                for j in pairs:
                    if set(i).isdisjoint(set(j)) == False:
                        abd = tuple(set(i) | set(j))
                        values.append(abd)
                new_pairs.append(max(values, key=lambda i: len(i)))
                values = []
            return new_pairs

        return sorted(set([ tuple(sorted(list(values)))
                           for values in sor(sor(pairs)) ]))
