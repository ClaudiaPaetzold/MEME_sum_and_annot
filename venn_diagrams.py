# this script reads in the summary files ceated by summarize_meme.py ...
# ... and creates venn diagrams for the ones with detected positive selection ..
# ... and the ones with where no positive selection was detected

# if you want to use it, replace the filenames and descriptions ...
#  (e.g. hyb1, venn_positve.svg etc) ...
# ... with the approbriate names and filepaths.
# you may also change the colors of the circles, please see here the colors ...
# available : https://matplotlib.org/stable/gallery/color/named_colors.html
# then change e.g. 'tab:red' ot 'darkslateblue' to any color you like


import os
from matplotlib import pyplot as plt
from matplotlib_venn import venn3
from matplotlib_venn import venn3_circles

hyb1 = "meme_posSelection_hyb1.csv"
hyb2 = "meme_posSelection_hyb2.csv"
parents = "meme_posSelection_Parents.csv"


poshyb1 = []
with open(hyb1, 'r') as c:
    header = c.readline()
    for line in c:
        gene = line.split(';')[0].split('_')[3]
        poshyb1.append(gene)

poshyb2 = []
with open(hyb2, 'r') as f:
    header = f.readline()
    for line in f:
        gene = line.split(';')[0].split('_')[3]
        poshyb2.append(gene)

posp = []
with open(parents, 'r') as p:
    header = p.readline()
    for line in p:
        gene = line.split(';')[0].split('_')[3]
        posp.append(gene)

# for the positives

venn3([set(poshyb1), set(poshyb2), set(posp)], ('hyb1', 'hyb2', 'Parents'), ('tab:red', 'tab:olive', 'tab:cyan'), alpha = 0.7)

plt.title('Positive selection detected', fontsize=20)

plt.draw()
plt.savefig("venn_positive.svg", format='svg')
plt.savefig("venn_positive.pdf", format='pdf')

plt.show()


# for the negatives

neghyb1 = "meme_noSelection_Hyb2.csv"
neghyb2 = "meme_noSelection_Hyb1.csv"
negparents = "meme_noSelection_Parents.csv"

# read in negative files:


neghyb1 = []
with open(hyb1, 'r') as c:
    header = c.readline()
    for line in c:
        gene = line.split(';')[0].split('_')[3]
        neghyb1.append(gene)

neghyb2 = []
with open(hyb2, 'r') as f:
    header = f.readline()
    for line in f:
        gene = line.split(';')[0].split('_')[3]
        neghyb2.append(gene)

negp = []
with open(parents, 'r') as p:
    header = p.readline()
    for line in p:
        gene = line.split(';')[0].split('_')[3]
        negp.append(gene)

venn3([set(neghyb1), set(neghyb2), set(negp)], ('hyb1', 'hyb2', 'Parents'), ('darkslateblue', 'seagreen', 'hotpink'), alpha = 0.7)

plt.title('No selection detected', fontsize=20)
plt.draw()
plt.savefig("venn_negative.svg", format='svg')
plt.savefig("venn_negative.pdf", format='pdf')

plt.show()
