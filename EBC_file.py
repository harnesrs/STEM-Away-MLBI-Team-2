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
    To me it looks like it's the unsupervised step because it's clustering, but the unsupervised step is supposed to output an nxn co-occurence matrix.
    Our final matrix is 2 x 3514, so I'm not really sure what our output matrix is.
    Hopefully Colin's material this week will clarify this; if not we will ask him.
'''




# If using EBC
with open("ebc/resources/matrix-ebc-paper-dense.tsv", "r") as f:
    data = []
    for line in f:
        sl = line.split("\t")
        if len(sl) < 5:  # headers
            continue
        data.append([sl[0], sl[2], float(sl[4])]) # what is going on in this line?

sparse_matrix = matrix.SparseMatrix([3514, 1232]) # why these numbers?
sparse_matrix.read_data(data) # takes in list of values, populates the SparseMatrix 
sparse_matrix.normalize()

ebc_test = EBC(sparse_matrix, n_clusters=[30, 125], max_iterations=10, jitter_max=1e-10, objective_tolerance=0.01)
cXY, objective, iter = ebc_test.run()
print(f'# rows: {len(cXY)}\n# cols: {len(cXY[0])}') 

# cXY is of shape 2 x 3514; the 3514 is the num rows in sparse_matrix and (from Group 3's presentation) the 2 should be 
#   cluster assignments for drug-gene pairs and dependency paths, respectively.
# Overall, I'm still not super sure of what this cXY is and what it's used for
# The documentation says "cXY: a list of list of cluster assignments along each dimension e.g. [C(X), C(Y), ...]"
# I tried reading the paper again but it was a little over my head; let's ask Colin at our next meeting


'''
# If using EBC2D (wasn't fully able to get this to work)
data = np.asarray([l.split('\t') for l in open('ebc/resources/matrix-ebc-paper-dense.tsv', 'r').readlines()])
ebc_test = EBC2D(data, n_clusters=[30, 125], max_iterations=10, jitter_max=1e-10, objective_tolerance=0.01)
cXY, objective, iter = ebc_test.run()
'''






