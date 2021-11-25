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

def read_exclude(controlfile):
    clist = []
    with open(controlfile, 'r') as c:
        for line in c:
            clist.append(line.split(';')[0])
    return clist

def main():
#############

    parser = argparse.ArgumentParser(description=
            "Intersects summary files of positively selected genes created by \
            summarize_meme.py including values for dn/ds ratios and number of \
            selected sites per sample. All input files must be in same directory.")
    parser.add_argument('-n', '--Names', type=str, \
            help="Tab-separated text file with one summary-filename (full Path) \
            and corresponding samplename per line. ")
    parser.add_argument('-o', '--OutfilePrefix', help='Prefix for the output \
            file. Default: No Prefix', default=False)
    parser.add_argument('-f', '--FilterControl', dest='FilterControl', \
            action='store_true', help='Flag. Enable if you want to \
            exclude genes, that are also positively selected in a control group \
            e.g. parental species, negative control etc.')
    parser.set_defaults(FilterControl=False)
    parser.add_argument('-c', '--Controlfile', type=str, help='Path to summary_meme_file \
            serving as control')
    args = parser.parse_args()
###################
    names={}
    with open(args.Names, 'r') as n:
        items = n.readlines()
        s1f, s1name = items[0].strip().split('\t')
        for i in items[1:]:
            filename, samplename = i.strip().split('\t')
            names[filename] = samplename
    # store name of outfile
    if args.OutfilePrefix:
        outname = os.path.join(os.path.dirname(s1f), args.OutfilePrefix + '_positiveintersect.csv')
    else:
        outname = os.path.join(os.path.dirname(s1f), 'positiveintersect.csv')
    print('outfile = ', outname)
    # create initial dictionary from first file
    intdict, shead = create_dict(s1f)
    inthead = [shead[0]]+ ['{}_{}'.format(i, s1name) for i in shead[1:]]

    # loop through remaining files and add metrics for genes found in ...
    #... 1st and current
    for file in names.keys():
        #print(file)
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

    if args.FilterControl:
        del_control = []
        to_excl = read_exclude(args.Controlfile)
        for i in to_excl:
            if i in intdict.keys():
                del intdict[i]
        if args.OutfilePrefix:
            outexclude = os.path.join(os.path.dirname(s1f), args.OutfilePrefix + '_positiveIntLessControl.csv')
        else:
            outexclude = os.path.join(os.path.dirname(s1f), 'positiveIntLessControl.csv')
        with open(outexclude, 'w') as out:
            fmtstr = ('{};' *(len(inthead)-1) ) + '{}\n'
            out.write(fmtstr.format(*inthead))
            for gene in intdict.keys():
                linefmtstr = ('{};' *(len(intdict[gene])) ) + '{}\n'
                out.write(linefmtstr.format(gene, *intdict[gene]))


if __name__ == '__main__':
    main()
