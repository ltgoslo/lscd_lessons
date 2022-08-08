#! /bin/bash
shopt -s expand_aliases
source ~/.bash_profile

for i in 1960 1970 1980 1990 2000
do
    python3 vis_proj.py -i coha_embeddings/coha_single/big/${i}.npz -w ${1} -l
done

python3 simult_vis_proj.py -i coha_embeddings/coha_single/big/ -t ${1}
