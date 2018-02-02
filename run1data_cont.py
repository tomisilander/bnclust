import numpy as np

from sklearn.mixture import GaussianMixture
from sklearn.cluster import spectral_clustering
from sklearn.cluster import k_means
from sklearn.metrics import adjusted_rand_score
from sklearn.metrics import adjusted_mutual_info_score
from sklearn.metrics import v_measure_score
from scipy.spatial.distance import cdist

from max_correlation import max_correlation
from pic import pic


def read_data(data_file, label_file):
    return (np.loadtxt(data_file),
            np.fromfile(label_file, dtype=int, sep=' '))


def compute_labels(vectors, K, bn_sim):
    N = vectors.shape[0]
    labels = {}

    labels["BN_CC"] = max_correlation(bn_sim, K, 10)

    pw_distances = cdist(vectors, vectors, 'seuclidean')  # cosine
    pw_sims = np.max(pw_distances) - pw_distances + np.min(pw_distances)
    Q = np.eye(N) - (1.0 / N) * np.dot(np.ones((N, 1)), np.ones((1, N)))
    Corr_Mat = np.dot(np.dot(Q, pw_sims), Q)
    labels["CC"] = max_correlation(Corr_Mat, K, 10)

    labels["Kmeans"] = k_means(vectors, n_clusters=K, n_init=10)[1]

    clf = GaussianMixture(n_components=K, covariance_type='full', n_init=10)
    clf.fit(vectors)
    labels["GMM"] = clf.predict(vectors)

    labels["SP"] = spectral_clustering(pw_sims, K)

    labels["PIC"] = pic(pw_sims, 1000, 1.0e-8, K)[1]

    return labels


def evaluate_labels(labels, true_labels):
    res = dict((method, []) for method in labels.keys())
    scores = (adjusted_mutual_info_score, adjusted_rand_score, v_measure_score)
    for method in labels.keys():
        for score in scores:
            res[method].append(score(true_labels, labels[method]))
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
    results = evaluate_labels(labels, true_labels)
    write_results(result_file, results)

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:5])