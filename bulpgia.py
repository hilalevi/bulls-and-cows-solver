from bp import *

guess = Bool('guess')

bulls = Int('bulls')
hits = Int('hits')
x0, x1, x2, x3 = Ints('x0 x1 x2 x3')

succeeded = False


def printGuess(m):
    print (">>>>>>>>>> {}.{}.{}.{} <<<<<<<<<<".format(m[x0], m[x1], m[x2], m[x3]))


def getFeedbackFromUser():
    print("Please rank my guess.\n")

    b = int(input("How many bulls did I get? \n"))
    while not(b in range(5)):
        b = int(input("Not a legal input,try again:\n"))

    h = int(input("How many hits did I get? \n"))
    while not(h in range(5)):
        print("Not a legal input,try again.\n")
        h = int(input("Not a legal input,try again: \n"))

    return b, h


def schedule():
    while True:
        m = yield {'request': guess}

        printGuess(m)

        b, h = getFeedbackFromUser()

        yield {'request': And(bulls == b, hits == h), 'block': guess}


def guess_range():
    yield {'block': Or(x0 < 0, x0 > 9,
                       x1 < 0, x1 > 9,
                       x2 < 0, x2 > 9,
                       x3 < 0, x3 > 9)}


def guess_uniqueness():
    yield {'block': Or(x0 == x1, x0 == x2, x0 == x3, x1 == x2, x1 == x3, x2 == x3)}


def logic():
    con = false

    while True:
        gss = yield {'wait-for': guess, 'block': con}
        fbk = yield {'wait-for': Not(guess)}

        con = Or(con, hitsCon(gss, fbk[hits]), bullsCon(gss, fbk[bulls]))


def hitsCon(gss, h):
    return Not(PbEq([(x0 == gss[x1], 1), (x0 == gss[x2], 1), (x0 == gss[x3], 1),
                     (x1 == gss[x0], 1), (x1 == gss[x2], 1), (x1 == gss[x3], 1),
                     (x2 == gss[x0], 1), (x2 == gss[x1], 1), (x2 == gss[x3], 1),
                     (x3 == gss[x0], 1), (x3 == gss[x1], 1), (x3 == gss[x2], 1)], h.as_long()))


def bullsCon(gss, b):
    return Not(PbEq([(x0 == gss[x0], 1), (x1 == gss[x1], 1), (x2 == gss[x2], 1), (x3 == gss[x3], 1)], b.as_long()))


def win():
    global succeeded
    while True:
        fbk = yield {'wait-for': Not(guess)}
        if fbk[bulls] == 4:
            succeeded = True
            yield {'block': true}


bts = [win(), logic(), guess_range(), guess_uniqueness(), schedule()]
lst = run(bts)
if succeeded:
    print("Hooray!!!")
else:
    print("Your feedback is inconsistent :-(")

