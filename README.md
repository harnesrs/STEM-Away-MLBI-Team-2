# STEM-Away-MLBI-Team-2
This repository includes an unofficial inplementation of the paper entitled: "Learning the Structure of Biomedical
Relationships from Unstructured Text" authored by Bethany Percha, Russ B. Altman at stanford university.

This implementation was part of [STEM-Away](https://stemaway.com) virtual internships in summer of 2021. 

The goal of the paper is to use the novel ensemble biclustering for classification (EBC) algorithm extract drug-target relationships from biomedical literature. The implementation is divided into 3 sections:

# 1- Preprocessing pipeline: 
this section includes the preparation of the data before using it as input to the EBC. It includes reading the publications database, parsing the sentences, filtering in the sentences that contain drug-gene pairs, and using the Stanford PArser to extract the dependency path between each pair of drugs and genes. THe final output of this pipline is a dependency matrix that consists of 3 columns: drug, gene, and dependency path. This matrix can go directly into EBC.

# 2- Parallel-processing pipline:

# 3- EBC:

# Collaborators:
1- [Baishali Mondal](https://github.com/baishali123314)\
2- [Lawrence Nguyen](https://github.com/law-nguyen)\
3- [Rachel Harness](https://github.com/harnesrs)\
4- [Sahil Bolar](https://github.com/sahil-bolar)\
5- [Sunnie Wang](https://github.com/Sunnie912)\
6- [Wafaa Mohammed](https://github.com/Wafaa014)

(names in alphabetical order)
