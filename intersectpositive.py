import os
import argparse


def create_dict(summaryfile):
    with open(summaryfile) as s:
        #clist = []
        sdict = {}
        shead = s.readline().strip().split(';')
        for line in s:
            sdict[line.strip().split(';')[0]] = line.strip().split(';')[1:]
    return(sdict, shead)


def main():
#############

    parser = argparse.ArgumentParser(description=
            "Intersects summary files of positively selected genes created by \
            summarize_meme.py including values for dn/ds ratios and number of \
            selected sites per sample. All input files must be in same directory.")
    parser.add_argument('-n', '--Names', type=str, \
            help="Tab-separated text file with one summary-filename (full Path) \
            and corresponding samplename per line. ")


    args = parser.parse_args()
###################
    names={}
    with open(args.Names, 'r') as n:
        items = n.readlines()
        s1f, s1name = items [0].strip().split('\t')
        for i in items[1:]:
            filename, samplename = i.strip().split('\t')
            names[filename] = samplename
    # store name of outfile
    outname = os.path.join(os.path.dirname(s1f), 'positiveintersect.csv')
    # create initial dictionary from first file
    intdict, shead = create_dict(s1f)
    inthead = [shead[0]]+ ['{}_{}'.format(i, s1name) for i in shead[1:]]

    # loop through remaining files and add metrics for genes found in ...
    #... 1st and current
    for file in names.keys():
        print(file)
        samplename = names[file]
        with open(file) as sample:
            new_header = ['{}_{}'.format(i, samplename) for i in sample.readline().strip().split(';')[1:]]
            inthead += new_header
            for line in sample:
                gene = line.strip().split(';')[0]
                    #append all genes in both files
                if gene in intdict.keys():
                    metric = line.strip().split(';')[1:]
                    intdict[gene] += (metric)
    # get rid of genes with lists not of required length, ...
    # ... which is number of (samples * 2)
    to_delete = []
    for gene in intdict.keys():
        if not len(intdict[gene]) == (len(names) + 1) * 2:
            to_delete.append(gene)

    for gene in to_delete:
        del intdict[gene]


    # write out dictionary to file
    with open(outname, 'w') as out:
        fmtstr = ('{};' *(len(inthead)-1) ) + '{}\n'
        out.write(fmtstr.format(*inthead))
        for gene in intdict.keys():
            linefmtstr = ('{};' *(len(intdict[gene])) ) + '{}\n'
            out.write(linefmtstr.format(gene, *intdict[gene]))


if __name__ == '__main__':
    main()
