import numpy as np
from ebc.ebc import EBC # used for more sparse and/or higher dim datasets
from ebc.ebc2d import EBC2D # used for more dense and/or 2D datasets
from ebc import matrix


'''
Changes I had to make to original code to get it to run in Python 3:

- in ebc.py and test_ebc.py, had to write "from ebc.matrix import ..." rather than the original "from matrix import ...", 
    though this may just be because of where my file is in relation to matrix.py
- in ebc.py and ebc2d.py, had to put parentheses around print statements
- in ebc.py, changed xrange (deprecated in python3) to range
- in ebc.py, changed iteritems (deprecated in python3) to iter(d.items()) for some dict d


Questions I have:
- From the paper, EBC appears to have an unsupervised step and a supervised step. Which steps are happening here? 
    Group 3 was also confused about this when they presented -- they assumed the code does both of the steps.
    Hopefully Colin's material this week will clarify this; if not we will ask him.
- Do we use EBC or EBC2D?
'''


### If using EBC

# Read in data
with open("ebc/resources/matrix-ebc-paper-dense.tsv", "r") as f:
    data = []
    for line in f:
        sl = line.split("\t")
        if len(sl) < 5:  # headers
            continue
        data.append([sl[0], sl[2], float(sl[4])]) # what is going on in this line?

# Set up SparseMatrix
n = 3514 # number of unique drug-gene pairs
m = 1232 # number of unique dependency paths (figure out a way to not hard-code these)
sparse_matrix = matrix.SparseMatrix([n, m]) 
sparse_matrix.read_data(data) # takes in list of values, populates the SparseMatrix 
sparse_matrix.normalize()

# Create dict mapping from index to drug-gene pair
idx_to_drug_gene = {}
for key, val in sparse_matrix.feature_ids[0].items():
    idx_to_drug_gene[val] = key


# Run EBC N times, create co-occurrence matrix

N = 100
C = np.zeros((n, n), dtype=int) 
for iter_num in range(N):
    # is this the right k and l (number of clusters)?
    ebc_test = EBC(sparse_matrix, n_clusters=[30, 125], max_iterations=10, jitter_max=1e-10, objective_tolerance=0.01)
    cXY, objective, iter = ebc_test.run(verbose=False)
    cluster_assignments = cXY[0]
    assert len(cluster_assignments) == n
    for i in range(n):
        clust = cluster_assignments[i]
        for j in range(i, n):
            if cluster_assignments[j] == clust:
                C[i,j] += 1
                if i != j: # don't want to duplicate along diagonal
                    C[j,i] += 1
    if (iter_num+1)%5 == 0:
        print(f"Iteration {iter_num+1} done.")

np.savetxt("cooccurrence.csv", C, delimiter=',')





'''
### If using EBC2D (wasn't fully able to get this to work)
data = np.asarray([l.split('\t') for l in open('ebc/resources/matrix-ebc-paper-dense.tsv', 'r').readlines()])
ebc_test = EBC2D(data, n_clusters=[30, 125], max_iterations=10, jitter_max=1e-10, objective_tolerance=0.01)
cXY, objective, iter = ebc_test.run()
'''






