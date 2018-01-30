
from numpy import sum, fabs, matrix, ones, diag, array
from scipy.cluster.vq import kmeans2


def calcNorm1(v):
    return sum(fabs(v))


def calcDelta(v, v2):
    return sum(fabs(v2 - v))


def normalize(v):
    max = v.max()
    min = v.min()
    return (v - min) / (max - min)


def initVector(m):
    n = m.shape[0]
    ovec = matrix(ones(n)).T
    v = m * ovec
    sinv = 1.0 / sum(v)
    return v * sinv


def pic(a, maxiter, eps, K):
    m = matrix(a)
    d1 = matrix(diag(a.sum(0))).I
    w = d1 * m
    n = w.shape[0]
    # v=matrix(random.random(n)).T#
    v = initVector(m)
    for i in range(maxiter):
        v2 = w * v
        ninv = 1.0 / calcNorm1(v2)
        v2 *= ninv
        delta = calcDelta(v, v2)
        v = v2
        if (delta * n) < eps:
            break

    return kmeans2(normalize(v), K)


if __name__ == '__main__':
    mx = array([[10.0000, 0.7071, 0.3333, 0.2774, 0.3714],
                [0.7071, 10.0000, 0.4472, 0.2774, 0.2857],
                [0.3333, 0.4472, 10.0000, 0.5000, 0.3124],
                [0.2774, 0.2774, 0.5000, 10.0000, 0.4851],
                [0.3714, 0.2857, 0.3124, 0.4851, 10.0000]])
    res = pic(mx, 10000, 1.0e-5, 2)
    print(res[1])
    # print kmeans2(v,2)
