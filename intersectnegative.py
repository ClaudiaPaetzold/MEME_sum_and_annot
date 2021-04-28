import os
import argparse

def main():

#########################
#parse arguments
    parser = argparse.ArgumentParser(description=
            "Intersects the 'no selection' summary files from summarize_meme.py ")
    parser.add_argument('-f', '--Files', nargs='+', \
            help="File names of '*noSelection.csv' files to intersect")
    parser.add_argument('-o', '--OutfilePrefix', help='Prefix for the output \
            file. Default: No Prefix', default=False)

    args = parser.parse_args()
#####################################

    genelist = []

    for file in args.Files:
        with open(file, 'r') as f:
            fhead = f.readline()
            for line in f:
                genelist.append(line.strip())

    final = []
    # count occurences of 'gene' in genelist and keep those with ...
    # ... num occurences = num samples
    for gene in genelist:
        if genelist.count(gene) == len(args.Files):
            final.append(gene)

    if args.OutfilePrefix:
        allnegout = os.path.join(os.path.dirname(args.Files[0]), \
        args.OutfilePrefix +'_negativeintersect.csv')
    else:
        allnegout = os.path.join(os.path.dirname(args.Files[0]), \
        'negativeintersect.csv')
    print('outfile = ', allnegout)
    with(open(allnegout, 'w')) as out:
        for gene in set(final):
            out.write('{}\n'.format(gene))


if __name__ == '__main__':
    main()
