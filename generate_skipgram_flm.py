import sys
from collections import deque
order = int(sys.argv[1]) if len(sys.argv) > 1 else 4


def extractions(l):
    if len(l) == 1:
        yield ((), l[0])
    else:
        for i in xrange(len(l)):
            yield (l[:i] + l[(i + 1):], l[i])


def all_combinations(l):
    l = tuple(l)
    enqueued = set()
    q = deque()  # append, popleft

    q.append(l)
    enqueued.add(l)

    while q:
        elem = q.popleft()
        if elem == ():
            yield "0 0"
        else:
            for l2, e2 in extractions(elem):
                yield "%s %s" % (",".join(elem), e2)
                if l2 not in enqueued:
                    enqueued.add(l2)
                    q.append(l2)


with open("flm_models/skip-%dgram.flm" % order, "w") as flm:
    print >>flm, 1
    print >>flm, "## skip %d-gram" % order
    print >>flm, "W : %d " % (order - 1),
    for i in xrange(1, order):
        print >>flm, "W(-%d)" % i,
    # we can use the *same* lm and count file as the regular n-gram model
    print >>flm, "flm_models/%d-gram.count.gz flm_models/%d-gram.lm.gz " % (order, order),
    combinations = list(all_combinations("W%d" % d for d in xrange(1, order)))
    print >>flm, len(combinations)
    print >>flm, "\n".join(combinations)
