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
sparse_matrix = matrix.SparseMatrix([3514, 1232]) 
sparse_matrix.read_data(data) # takes in list of values, populates the SparseMatrix 
sparse_matrix.normalize()

# Run EBC
ebc_test = EBC(sparse_matrix, n_clusters=[30, 125], max_iterations=10, jitter_max=1e-10, objective_tolerance=0.01)
cXY, objective, iter = ebc_test.run()
print(f'# of lists: {len(cXY)}\n# elements in first list: {len(cXY[0])}\n# elements in second list: {len(cXY[1])}') 
print(cXY)

# The documentation says "cXY: a list of list of cluster assignments along each dimension e.g. [C(X), C(Y), ...]"
# In our case, cXY is a list of two lists 
#   the first list is of length 3514 (cluster assignment for each drug-gene pairs)
#   the second list is of length 1232 (cluster assignment for each dependency path)
# Overall, I'm still not super sure of how we use this cXY going forward


'''
### If using EBC2D (wasn't fully able to get this to work)
data = np.asarray([l.split('\t') for l in open('ebc/resources/matrix-ebc-paper-dense.tsv', 'r').readlines()])
ebc_test = EBC2D(data, n_clusters=[30, 125], max_iterations=10, jitter_max=1e-10, objective_tolerance=0.01)
cXY, objective, iter = ebc_test.run()
'''






