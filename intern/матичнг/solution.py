from typing import List
from typing import Tuple


def extend_matches(pairs: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    '''return real pairs'''
    if pairs == []:

        return []

    if len(pairs) == 1:

        return pairs

    if  len(pairs) > 1:
        def sor(pairs):
            new_pairs = [x for x in pairs]

            for i in pairs:
                for j in pairs:
                    abd = tuple(set(i) ^ set(j))
                    if len(abd) == 2:
                        new_pairs.append(abd)
            return new_pairs

        return sorted(set([values for values in 
                    sor(sor(pairs)) if list(values)[0] <= list(values)[1]]))


