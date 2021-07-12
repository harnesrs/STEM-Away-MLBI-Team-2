import numpy as np
from ebc.ebc import EBC
from ebc import matrix


'''
Changes I had to make to original code to get it to run:

- in ebc.py and test_ebc.py, had to write "from ebc.matrix import ..." rather than the original "from matrix import ...", though this may just be because of where my file is in relation to matrix.py
- in ebc.py, had to put parentheses around print statements
- in ebc.py, changed xrange (deprecated in python3) to range
- in ebc.py, changed iteritems (deprecated in python3) to iter(d.items()) for some dict d
'''


# basically running test_ebc.py
with open("ebc/resources/matrix-ebc-paper-dense.tsv", "r") as f:
    data = []
    for line in f:
        sl = line.split("\t")
        if len(sl) < 5:  # headers
            continue
        data.append([sl[0], sl[2], float(sl[4])])
sparse_matrix = matrix.SparseMatrix([3514, 1232]) # why these numbers?
sparse_matrix.read_data(data) # takes in list of values, populates the SparseMatrix 
sparse_matrix.normalize()

ebc_test = EBC(sparse_matrix, n_clusters=[30, 125], max_iterations=10, jitter_max=1e-10, objective_tolerance=0.01)
cXY, objective, iter = ebc_test.run()

print(f'# rows: {len(cXY)}\n# cols: {len(cXY[0])}') 
# cXY is of shape 2 x 3514; the 3514 is the num rows in sparse_matrix but I'm not sure where the 2 comes from
# Overall, I'm still not super sure of what this cXY is and what it's used for
# The documentation says "cXY: a list of list of cluster assignments along each dimension e.g. [C(X), C(Y), ...]"
# I tried reading the paper again but it was a little over my head; let's ask Colin at our next meeting



