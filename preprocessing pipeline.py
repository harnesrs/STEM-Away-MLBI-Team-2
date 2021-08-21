# %%
# importing necessary libraries
import os
import collections
import re
import gzip
import json
import io
import xml.etree.ElementTree as ET
import pubmed_parser as pp 
import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import sent_tokenize as st
from nltk.corpus import stopwords
from nltk.parse import stanford
pd.options.display.max_colwidth=None

#%%
#reading the medline data
pubmed_paths = ['./pubmed21n' + str(num).zfill(4) + '.xml.gz' for num in range(1,3)]
print(pubmed_paths)
parsed_file = [pd.DataFrame.from_dict(pp.parse_medline_xml(path)) for path in pubmed_paths]
pubmed_df = pd.concat(parsed_file)

#%%
# seeing the number of publications and their attributes in the 3 files that have been read
print(pubmed_df.shape)
# %%
# outputting the first five papers' details
pubmed_df.head()
# %%
#extracting the abstracts column
abstracts = pubmed_df['abstract']
print(abstracts.shape)
# %%
# outputting the first five abstracts
abstracts.head()
# %%
# printing duplicated indexes
print(abstracts.index.duplicated())
# %%
# rmoving duplicates
abstracts = abstracts.loc[~abstracts.index.duplicated()]
# %%
# number of abstracts after removing duplicates
abstracts.shape
# %%
# removing empty abstracts
non_empty = abstracts[abstracts != '']

# %%
# printing the first five non-empty abstracts
non_empty.head()
# %%
# printing the number of non-empty abstracts 
non_empty.shape

# %%
# read the list of drugs
drugbank_df=pd.read_csv("<drugs list file>")
drugbank_df

#%%
# reading the drug names
drugs = list(set(drugbank_df['Name']))
drugs = [str(x) for x in drugs]
print(drugs[0:5])
print(len(drugs))
drugs = [x for x in drugs if x != 'nan']
#drugs = [' ' + x + ' ' for x in drugs]
print(drugs[0:5])
print(len(drugs))
#%%
# generating a dictionary of drug names and indexes
dict_drugs = {i:j for i,j in enumerate(drugs)}


# %%
# reading the genes list
data = pd.read_csv("<gene list file>",error_bad_lines=False, sep = '\t')
data.head()

# %%
# reading the gene names
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
# generating a dictionary of gene names and indexes
dict_genes = {i:j for i,j in enumerate(genes)}

# %%
# extracting sentences that contain drug gene pairs and appending them in a dataFrame
d = pd.DataFrame(columns = ['sentence','drug','gene'])

import re
for i in range(len(non_empty)):
    paragraph = non_empty.iloc[i]
    sentences = paragraph.split(". ")
    for sentence in sentences:
        words = re.split(' |, |-', sentence)
        j = 0
        for word in words:      
            if word in drugs:
                position = sentence.index(word)
                previous = sentence[:position]
                comma = previous.count(",")
                right = previous.count("(")
                left = previous.count(")")
                index_drug = words.index(word) + 1 + comma + right + left
                drug = word
                j += 1
                break
        for word in words:
            if word in genes:
                position = sentence.index(word)
                previous = sentence[:position]
                comma = previous.count(",")
                right = previous.count("(")
                left = previous.count(")")
                index_gene = words.index(word) + 1 + comma + right + left
                gene = word
                j += 1
                break
        if j == 2:
            to_append = [sentence,drug,gene]
            d = d.append(pd.DataFrame([to_append],columns = ['sentence','drug','gene']),ignore_index=True)
            print(d.shape)
            if d.shape == (100, 3):
                break

print(i)

#%%
#printing the shape of the dataframe
d.shape

#%%
# a function to get the dependency path of a drug-gene pair in a specific sentence
def get_dependency_path(sentence, drug, gene):
    """
    Input: sentence, drug, gene
    Output: dependency path
    """

    #java_path = r'C:\Program Files (x86)\Common Files\Oracle\Java\javapath\java.exe'
    #os.environ['JAVAHOME'] = java_path
    os.environ['STANFORD_PARSER'] = '/stanford-parser-full-2014-10-31/stanford-parser.jar'
    os.environ['STANFORD_MODELS'] = '/stanford-parser-full-2014-10-31/stanford-parser-3.5.0-models.jar'
    dependency_parser = stanford.StanfordDependencyParser(path_to_jar='/home/aims/stanford-parser-full-2014-10-31/stanford-parser.jar', path_to_models_jar=r'/home/aims/stanford-parser-full-2014-10-31/stanford-parser-3.5.0-models.jar')

    # cover edge case where [] and {} cannot be parsed
    sentence = sentence.replace('[','(').replace(']',')').replace('{','(').replace('}',')')

    try:
        result = dependency_parser.raw_parse(sentence)
        dep = next(result)

    except:
        print(f"Error parsing the following sentence:\n {sentence} \n------------------")
        result = []

    if result == []:
        return []
        
    # make dependency tuple into list
    try:
        dependency_list = []
        for relation in dep.triples():
            temp_list=[]
            for item in relation:
                if type(item).__name__ == 'tuple':
                    temp_list.append(str(item[0]))
                else:
                    temp_list.append(str(item))
            dependency_list.append(temp_list)
    except:
        return []

    # Obtain drug and gene path
    drug_path = []
    gene_path = []
    drug_path_search = []
    gene_path_search = []

    restart_loop = True
    loop_counter = 0
    while restart_loop == True:
        loop_counter += 1
        
        # specific cases where code keeps running while dependency_list is empty
        if len(dependency_list)==0 and loop_counter > 200:
            drug_path = []
            gene_path = []
            break
        
        for i in range(len(dependency_list)):
            relation = dependency_list[i]
            if relation[2] == drug:
                drug_path.append(relation[2])
                drug_path.append(relation[1])
                drug_path.append(relation[0])
                drug_path_search = relation[0]
                dependency_list.pop(i)
                loop_counter = 0
                break
            elif relation[2] == drug_path_search:
                drug_path.append(relation[1])
                drug_path.append(relation[0])
                drug_path_search = relation[0]
                dependency_list.pop(i)
                loop_counter = 0
                break
            elif relation[2] == gene:
                gene_path.append(relation[2])
                gene_path.append(relation[1])
                gene_path.append(relation[0])
                gene_path_search = relation[0]
                dependency_list.pop(i)
                loop_counter = 0
                break
            elif relation[2] == gene_path_search:
                gene_path.append(relation[1])
                gene_path.append(relation[0])
                gene_path_search = relation[0]
                dependency_list.pop(i)
                loop_counter = 0
                break
            elif i == (len(dependency_list)-1):
                restart_loop = False
                break

    # Combine drug and gene path into dependency path
    if drug in gene_path:
        ind = gene_path.index(drug)
        dependency_path = gene_path[1:ind]
    elif gene in drug_path:
        ind = drug_path.index(gene)
        dependency_path = drug_path[1:ind][::-1]
    else:
        dependency_path = gene_path[1:] + drug_path[::-1][1:-1]

    return dependency_path


#%%
# testing the function to see if it is able to extract a dependency path
sentence = "Clonidine noncompetitively inhibited acetylcholinesterase activity in vitro and after in vivo administration at protective doses. (3761196)"
drug = "Clonidine"
gene = "acetylcholinesterase"
get_dependency_path(sentence, drug, gene)



#%%
# getting the dependency matrix that consist of a drug-gene pair and their dependency path
def get_dependency_matrix(abs_filt):
    """
    Input: Dataframe of filtered abstract with columns of abstract, sentence, drug, and gene
    Output: Dependency matrix in the form: dependency_paths, drug_gene_pairs, relation (always 1)
    """

    dependency_matrix = pd.DataFrame(columns = ['dependency_paths','drug_gene_pairs','relation'])
    for i, sentence in enumerate(abs_filt["sentence"]):
        print('-------------------------')
        print(sentence)
        drug = abs_filt["drug"].iloc[i]
        gene = abs_filt["gene"].iloc[i]
        dependency_path = get_dependency_path(sentence, drug, gene)
    #     print(drug)
    #     print(gene)
    #     print('----dependency path----')
    #     print(dependency_path)
    #     print('-----------------------')
        if len(dependency_path) > 0 and dependency_path[0]!='conj':
            drug_gene_pair = '('+ drug+','+gene+ ')'
            to_append = [drug_gene_pair,str(dependency_path),1.0]
            dependency_matrix = dependency_matrix.append(pd.DataFrame([to_append],columns = ['dependency_paths','drug_gene_pairs','relation']),ignore_index=True)
            print('append to matrix')
        print('done')
            
    return dependency_matrix




#%%
# the function takes as input the dataframe of sentences/ drugs/ and genes. and outputs the dependency matrix that can be used by the EBC algorithm
dep_mat = get_dependency_matrix(d)
#%%
#printing the dependency matrix
dep_mat

# the dependency matrix gcan be input diectly to ebc
# %%
# the required output
data = dep_mat.to_numpy().tolist()
data[0]

