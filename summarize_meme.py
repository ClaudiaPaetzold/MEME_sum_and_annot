#!/bin/python

import os
import glob
import re
import argparse


def tail(f, nlines):
#mimics UNIX' tail command to get the last line
    lines = open(f).readlines()
    num_lines = len(lines)

    return(''.join(lines[-(num_lines if num_lines < nlines else nlines):]))



def find_rates(file):
# helper function - findes improved dnds rates for test in meme file
    with open(file, 'r') as f:
        for line in f:
            if re.search('synonymous rate ratio for \*test\*', line):
                #print(line)
                rate = float(line.split('=')[1].strip())


    return(rate)




def main():

#########################
#parse arguments
    parser = argparse.ArgumentParser(description=
            "Summarizes results in HyPhy MEME output files. Produces 3 files:\
            1) a table with genes where positive selcetion was detected incl\
            dn/ds ratios,. 2) a list of genes where no positive selection was\
            detected. 3) A list of genes raising an error in MEME analysis")
    parser.add_argument('-d', '--Directory', type=str, \
            help='Directory containing all MEME result *.txt files')
    parser.add_argument('-n', '--Name', type=str, \
            help="Name of sample or condition to be appended to outfiles")


    args = parser.parse_args()


###########################

    # writing directory
    wd = os.path.dirname(args.Directory)
    print(wd)
    # get parent direcotry for outfiles
    # outfiles, check if exists and throw error if yes:
    out_no = os.path.join(wd, 'meme_noSelection_{}.csv'.format(args.Name))
    out_yes = os.path.join(wd, 'meme_posSelection_{}.csv'.format(args.Name))
    out_err = os.path.join(wd,'meme_error_{}.txt'.format(args.Name))
    for f in [out_no, out_yes, out_err]:
        if os.path.isfile(f):
            print('Outfiles already in directory. If you want to repeat the analysis, please delete the prior results first. Thank you.')
            break
    else:
        with open(out_no, 'a') as no:
            no.write('{}\n'.format('gene'))

        with open(out_yes, 'a') as yes:
            yes.write('{}; {}; {}\n'.format('gene', 'dN/dS rate', 'num selected Sites'))

        with open(out_err, 'a') as err:
            err.write('{}\n'.format('gene'))

        for file in glob.glob(os.path.join(args.Directory, '*.txt')):
            #print(file)
            gene = os.path.basename(file).split('.')[0]
        	#print(file)
            #print(find_rates(file))
            if re.search('_0_', tail(file, 1)):
                flag = 'no positive selection detected'
                with open(out_no, 'a') as no:
                    no.write('{}\n'.format(gene))

            else:
                try:
                    num = tail(file, 1).split('_')[1]
                    rate = find_rates(file)
                    with open(out_yes, 'a') as yes:
                        yes.write('{}; {}; {}\n'.format(gene, rate, num))
                except:
                    with open(out_err, 'a') as err:
                        err.write('{}\n'.format(gene))

if __name__ == '__main__':
	main()
