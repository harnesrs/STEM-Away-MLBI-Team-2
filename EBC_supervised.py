import numpy as np
import pandas as pd


# obtain DrugBank drug-gene pairs
# read in data
directory = ''
drug_gene_relation = pd.read_csv(directory+'pharmacologically_active.csv')
drugs = pd.read_csv(directory+'drugbank_vocabulary.csv')

# keep only relevant columns
drug_gene_relation = drug_gene_relation[['Gene Name', 'Drug IDs']]
drugs = drugs[['DrugBank ID', 'Common name', 'Synonyms']]

# obtain dataframe in which each row is a unique drug-gene pair
for i in range(drug_gene_relation.shape[0]):
    if ';' in drug_gene_relation.iloc[i]['Drug IDs']:
        tmp_list = drug_gene_relation.iloc[i]['Drug IDs'].split(';')
        drug_gene_relation.iloc[i]['Drug IDs'] = tmp_list
drug_gene_relation = drug_gene_relation.explode('Drug IDs') # requires pandas 0.25.0
drug_gene_relation.reset_index(drop=True, inplace=True)

# create mappings of drugID to common name and synonym
ID_to_names = {}
for i in range(drugs.shape[0]): 
    ID_tmp = drugs.iloc[i]['DrugBank ID']
    name_tmp = drugs.iloc[i]['Common name']
    syn_tmp = drugs.iloc[i]['Synonyms']
    names = (name_tmp,)
    if type(syn_tmp) != float: # skip over NAs 
        syn_tmp = syn_tmp.split(' | ')
        for j in range(len(syn_tmp)):
            names += (syn_tmp[j],)
    ID_to_names[ID_tmp] = names

# create set of drug-gene pairs
drug_gene_DB = set()
for i in range(drug_gene_relation.shape[0]): 
    tmp_drugID = drug_gene_relation.iloc[i]['Drug IDs'].strip()
    tmp_gene = drug_gene_relation.iloc[i]['Gene Name']
    if type(tmp_gene) == float: # skip over NAs
        continue
    tmp_names = ID_to_names[tmp_drugID]
    for drug_name in tmp_names:
        drug_gene_tmp = '('+drug_name+','+tmp_gene+')'
        drug_gene_tmp = drug_gene_tmp.lower()
        drug_gene_DB.add(drug_gene_tmp) # match the format from the original set

# read in our set of drug-gene pairs
data = pd.read_csv('data_orig.csv')
data = data[['Drug-gene', 'Dependency path', 'Relation']]
drug_gene_orig = set(data['Drug-gene'])

# read in co-occurrence matrix
C = pd.read_csv('cooccurrence.csv', header=None)
C = np.asarray(C)

# read in drug-gene pair to index dataframe
drug_gene_to_idx_df = pd.read_csv('drug_gene_idx.csv')

# find DrugBank drug-gene pairs also in our dataset 
# this will be the population we draw the seed sets from
seed_pop = drug_gene_orig.intersection(drug_gene_DB) # contains 62 drug-gene pairs

# find drug-gene pairs in our dataset that are NOT in DrugBank
## this will be the population we draw half of the test set from
test_pop_fake = drug_gene_orig.difference(drug_gene_DB) # contains 3452 drug-gene pairs

scores = {}
n_test = 100
n_iter = 1000

# original seed set sizes in paper: [1, 2, 3, 4, 5, 10, 25, 50, 100]
# seed set size >12 will not work since our seed_pop is 62
# (need 50 samples without replacement from test_pop_real)
for n_seed in [1, 2, 3, 4, 5, 10]: 
    print(f"Seed number: {n_seed}")
    scores[n_seed] = []
    for iter in range(n_iter):
        if (iter+1)%100==0:
            print(f"\tIter number: {iter+1}")
        
        # generate seed set with corresponding size
        seed_set = np.random.choice(list(seed_pop), n_seed).tolist()

        # create test_pop_real (set of drug-gene population minus seed set) 
        test_pop_real = seed_pop.difference(seed_set)

        # generate corresponding test set
        ## n_test // 2 from test_pop_real
        test_set = np.random.choice(list(test_pop_real), n_test//2).tolist()
        ## n_test // 2 from test_pop_fake
        test_set += np.random.choice(list(test_pop_fake), n_test//2).tolist()

        # compute EBC score
        ## obtain index of test set member (i)
        scoring = 0
        for i in range(n_test):
            test_pair = test_set[i]
            test_idx = drug_gene_to_idx_df.loc[drug_gene_to_idx_df['Drug-gene pair']==test_pair]['Index']
            C_vals = C[test_idx,:][0] # (row i of C, the co-occurrence matrix)

            # sort C_vals (and corresponding drug-gene IDs) from least to most coclustering
            idxs = np.arange(len(C_vals))
            zipped_lists = zip(C_vals, idxs)
            sorted_pairs = sorted(zipped_lists)
            tuples = zip(*sorted_pairs)
            C_vals_sorted, ranking = [ list(tuple) for tuple in tuples]
            for seed_pair in seed_set:
                ## find index of seed_pair
                seed_idx = int(drug_gene_to_idx_df.loc[drug_gene_to_idx_df['Drug-gene pair']==seed_pair]['Index'])
                
                ## find position of seed_pair in ranking
                pos = ranking.index(seed_idx)

                scoring += pos
        scores[n_seed].append(scoring)


scores_df = pd.DataFrame.from_dict(scores)
scores_df.to_csv('scores.csv', index=False)










