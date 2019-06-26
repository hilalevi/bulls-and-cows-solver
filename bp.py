
from z3 import *

true = BoolSort().cast(True)
false = BoolSort().cast(False)


def run(bthreads):
    superstep([{'bt': bt} for bt in bthreads], None)


def superstep(lst, m):
    while m != 'no next event':
        advanceBThreads(m, lst)
        m = nextEvent(lst)
        

def nextEvent(lst):
    (request, block) = (false, false)

    # Collect request and block statements
    for l in lst:
        request = Or(request, l['request'])
        block = Or(block, l['block'])

    # Compute a satisfying assignment 
    sl = Solver()
    sl.add(And(request, Not(block)))
    if sl.check() == sat:
        return sl.model()
    else:
        return 'no next event'



def advanceBThreads(m, lst):
    for l in lst:
        if m is None or is_true(m.eval(Or(l['wait-for'], l['request']))):
            l.update({'wait-for': false, 'request': false, 'block': false})
            try: 
            	l.update(l['bt'].send(m))
            except StopIteration:
            	lst.remove(l)
