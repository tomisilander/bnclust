from functools import partial
from itertools import product
import numpy as np

from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import spectral_clustering

from sklearn.metrics import accuracy_score
from sklearn.metrics import jaccard_similarity_score

from clustercriteria import Gnorm, Hnorm

from max_correlation import max_correlation
from pic import pic


def read_data(data_file, label_file):
    le = LabelEncoder()
    return (np.loadtxt(data_file, dtype=int),
            le.fit_transform(open(label_file).read().split()))


def overlap_sim(vectors):
    return np.array([[accuracy_score(v1,v2) for v1 in vectors] 
                    for v2 in vectors])

def compute_labels(vectors, K, bn_sim):
    labels = {}

    osim = overlap_sim(vectors)
    sim = {"BN":bn_sim, "OL":osim}
    clusalg = {"CC" : partial(max_correlation, my_K=K, my_itr_num=10),
               "SP" : partial(spectral_clustering, n_clusters=K),
               # "PIC" : partial(pic, maxiter=1000, eps=1.0e-8, K=K)
              }
    for ((simname, simx), (clusname,clusalg)) in product(sim.items(),clusalg.items()):
        try:
            labelname = '_'.join((simname,clusname))
            labels[labelname] = clusalg(simx)
        except:
            print("Failed",labelname)
            if labelname in labels:
                del labels[labelname]

    return labels


def evaluate_labels(labels, vectors):
    res = dict((method, []) for method in labels.keys())
    scores = (Gnorm, Hnorm)
    for method in labels.keys():
        for score in scores:
            try:
                res[method].append(score(labels[method], vectors))
            except:
                print("Failed",method,str(score))

    return res


def write_results(filename, results):
    f = open(filename, 'wb')
    for (method, res) in results.items():
        sep = "-----------------------%s---------------------" % method
        np.savetxt(f, [sep], fmt='%s')
        np.savetxt(f, res, fmt='%0.8f')
    f.close()


def main(data_file, label_file, bn_sim_file, result_file):
    vectors, true_labels = read_data(data_file, label_file)
    K = np.size(np.unique(true_labels))
    bnsim = np.loadtxt(bn_sim_file)
    labels = compute_labels(vectors, K, bnsim)
    labels['TRUE'] = true_labels
    results = evaluate_labels(labels, vectors)
    write_results(result_file, results)

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:5])