#%%
import os
import pubmed_parser as pp 
import pandas as pd
import numpy as np
import re
pd.options.display.max_colwidth=None

#%%
pubmed_paths = ['/home/aims/Desktop/stem-away/pubmed21n' + str(num).zfill(4) + '.xml.gz' for num in range(1,3)]
print(pubmed_paths)
parsed_file = [pd.DataFrame.from_dict(pp.parse_medline_xml(path)) for path in pubmed_paths]
pubmed_df = pd.concat(parsed_file)

#%%
print(pubmed_df.shape)

# %%
pubmed_df.head()
# %%
abstracts = pubmed_df['abstract']
print(abstracts.shape)
# %%
abstracts.head()
# %%
print(abstracts.index.duplicated())
# %%
abstracts = abstracts.loc[~abstracts.index.duplicated()]
# %%
abstracts.shape
# %%
non_empty = abstracts[abstracts != '']
# %%
type(non_empty)
# %%
non_empty.head()
# %%
non_empty.shape
# %%
data = pd.read_csv("/home/aims/Desktop/stem-away/var_drug_ann.tsv",error_bad_lines=False, sep = '\t')
data.head()
# %%
genes = list(set(list(data['Gene'])))
genes = [str(x) for x in genes]
print(genes[0:5])
print(len(genes))
genes = [x for x in genes if x != 'nan']
#for x in genes:
 #   x = x.strip()
#genes = [' ' + x + ' ' for x in genes]
print(genes)
print(len(genes))

#%%
drugs = list(set(list(data['Drug(s)'])))  
drugs = [str(x) for x in drugs]
print(drugs[0:5])
print(len(drugs))
drugs = [x for x in drugs if x != 'nan']
#drugs = [' ' + x + ' ' for x in drugs]
print(drugs[0:5])
print(len(drugs))
#%%
dict_genes = {i:j for i,j in enumerate(genes)}
dict_drugs = {i:j for i,j in enumerate(drugs)}

#%%
print(dict_drugs)
#%%
print(dict_genes)
#%%
print(genes)
#%%
print(dict_genes.values())
# %%
paragraph = non_empty.iloc[0]
sentences = paragraph.split(". ")
sentences

#%%
f = open('output.txt', 'r+')
f.truncate(0)
# %%
f = open('output.txt', 'w')
import re
for i in range(len(non_empty)):
    paragraph = non_empty.iloc[i]
    sentences = paragraph.split(". ")
    for sentence in sentences:
        words = re.split(' |, |-', sentence)
        j = 0
        for word in words:      
            if word in drugs:
                index_drug = words.index(word) + 1
                drug = word
                j += 1
                break
        for word in words:
            if word in genes:
                index_gene = words.index(word) + 1
                gene = word
                j += 1
                break
        if j == 2:
            print("Drug: " + drug + " /Index: " + str(index_drug))
            f.write(str(index_drug) + "\n")
            print("Gene: " + gene + " /Index: " + str(index_gene))
            f.write(str(index_gene) + "\n")
            print("Sentence:" + sentence + "\n")
            f.write(sentence + "\n")
            print(words)

print(i)

# %%
f.close()
# %%
f = open("output.txt", "r")
print(int(f.readline()))
print(int(f.readline()))
print(f.readline())
# %%
l = "my name, is wafaa"
a = l.split(" ")
a2 = []
for word in a:
   x = word.split(",")
   a2.extend(x)
for word in a2:
    if word == '':
        a2[a2.index(word)] = ','
a2[2]        
# %%
