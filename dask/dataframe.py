#%%
import dask
import dask.bag as db
import dask.dataframe as dd
import os
import pubmed_parser as pp
from dask.multiprocessing import get
import glob
import graphviz

# %%
pubmed_paths = ['data/pubmed/pubmed20n' + str(num).zfill(4) + '.xml' for num in range(1,3)]
print(pubmed_paths)

def convert_xml_to_csv(xml_file):
    csv_file = pd.DataFrame.from_dict(pp.parse_medline_xml(xml_file))
    csv_file.to_csv(path_or_buf = re.sub(r'.xml',r'.csv',xml_file),index = False)
    pass 

for xml_file in pubmed_paths:
    convert_xml_to_csv(xml_file)

# %%
# read in csvs and construct filter operations, sample used for inferencing types
df = dd.read_csv('data/pubmed/pubmed20*.csv',sample=25000000)
df.head()

#%%
# filter for those with non-NaN abstracts 
df_filtered = df[df.abstract.notnull()] # not evaluated yet
df_filtered.head() # only evaluated when explicitly asked 

#%%
# how many partitions? 2, with 12 tasks. Tasks define the operations needed to get intended result
df_filtered

#%%
df_filtered.compute()

#%%
df_filtered.map_partitions(len).compute()