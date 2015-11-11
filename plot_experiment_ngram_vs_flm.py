import pylab

s = open("SALIDA").read()

tt = map(
    lambda r: map(float, r.split()),
    s.split('\n')
)

h = ['size', 'cloze', 'cloze_cache', '3gram', '3gram_cache', '4gram', '4gram_cache', 'flm', 'flm_cache']


def get(t, i):
    return [row[i] for row in t if row]

dim = len(h)
pylab.close()
for i in xrange(3, dim):
    pylab.plot(get(tt, 0), get(tt, i), "--" if "cache" not in h[i] else "-", label=h[i])
pylab.legend(loc='upper right')
pylab.show()
