from itertools import groupby
import numpy as np 
from scipy.stats import entropy


def gen_groups(labels, vectors):
    keyfunc = lambda x:x[0]
    svectors = sorted(zip(labels,vectors),key=keyfunc)

    for l,group in groupby(svectors,key=keyfunc):
        glist = list(x for _l,x in group)
        yield l, np.array(glist)


def G(xs):
    _vals, n_gc = np.unique(xs, return_counts=True)
    n_g = float(len(xs))
    return 1 - ((n_gc/n_g)**2).sum()


def Gnorm(labels,vectors):
    K = np.apply_along_axis(lambda x: len(np.unique(x)),0, vectors)
    (n,m) = vectors.shape
    return sum(len(group) * sum(K[c]*G(group[:,c])/(K[c]-1) for c in np.arange(m))
               for l,group in gen_groups(labels, vectors)) / (n*m)


def H(xs):
    _vals, n_gc = np.unique(xs, return_counts=True)
    n_g = float(len(xs))
    return entropy(n_gc/n_g)


def Hnorm(labels,vectors):
    (n,m) = vectors.shape
    K = np.apply_along_axis(lambda x: len(np.unique(x)),0, vectors)
    return sum((len(group) * sum(H(group[:,c])/np.log(K[c]) for c in np.arange(m)))
               for l,group in gen_groups(labels, vectors)) / (n*m)


def PSF(f, labels, vectors):
    n = len(labels)
    k = len(np.unique(labels))
    f1 = f(np.zeros(n,dtype='i1'), vectors)
    fk = f(labels,vectors)
    return (n-k)*(f1-fk)/(k-1)/fk


if __name__ == "__main__":
    labels = np.array([0,1,1,2,1,0], dtype='i1')
    vectors = np.array([ [0,1,1,0,0,1],
                [0,1,0,0,1,1],
                [1,0,1,0,1,2],
                [0,1,1,1,0,2],
                [0,1,1,1,0,1],
                [0,1,1,0,0,0]], dtype='i4')
    print(PSF(Gnorm,labels,vectors))
    print(PSF(Hnorm,labels,vectors))