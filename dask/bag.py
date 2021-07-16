#%%
import dask
import dask.bag as db
import dask.dataframe as dd
import pandas as pd
import os
import pubmed_parser as pp
from dask.multiprocessing import get
import glob
import graphviz


#%%
graph = {}

def load(xml_file):
    return pd.DataFrame.from_dict(pp.parse_medline_xml(xml_file))

def clean(df):
    return df[(df['abstract'].notnull()) & (df['abstract']!=u'')]

def analyze(df):
    return [len(i) for i in df]

def store(results):
    with open('data/test_data.txt' , 'w') as f:
        f.write(str(results))

os.chdir("../data")
i = 1
for file in glob.glob("*.xml"):
    graph.update( {'parse_xml-'+str(i) : (load, file)} )
    i += 1


for n in range(1,6):
    graph.update( {"filter_abstract-"+str(n): (clean, "parse_xml-"+str(n))})

graph.update( [ ('get_len' , (analyze, ['filter_abstract-%d' % i for i in [1, 6]])) , 
            ('store' , (store, 'get_len')) ])

print(graph)

# %%
dask.visualize(graph)


# %%
get(graph, 'store')