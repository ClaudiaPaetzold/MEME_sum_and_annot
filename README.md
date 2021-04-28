![Logo of the project](https://raw.githubusercontent.com/jehna/readme-best-practices/master/sample-logo.png)

# MEME_sum_and_annot
Python scripts to summarize MEME (Mixed Effects Model of Evolution) results generated HyPhy and annotate selected genes.

This is a set of Python scripts that help uses a series of outputfiles generated using the [MEME](https://www.hyphy.org/methods/selection-methods/) algorithm in [HyPhy](https://www.hyphy.org/) and summarizes the output to generate an overview of all under positive selcetion or for which no selection was detected. The summaries can be intersected across samples and a functional annotation and GO profiles can be produced for intersected summaries. 

There are also some axillary scripts that produce single-gene \*-fasta files from [ProtheinOrtho](https://gitlab.com/paulklemm_PHD/proteinortho) output or remove stop codons, from alignments, as they would impede MEME analyses.

The code was written for Barke et al. (in prep). A citation incl. a link for the article will be added upon publication.

## Summary
- [Getting Started](#getting-started)
- [The core scripts](#examples)
- [Auxillary scripts](#auxillary-scripts)
- [Citation](#citation)
- [Links](#links)
- [Licensing](#licensing)


## Getting started

The scripts require Python 3 and some Python packages. The easiest way to install all necessary [dependencies](#required-packages) is using a package manager like [Anaconda](#https://www.anaconda.com/products/individual) or [Miniconda](#https://docs.conda.io/en/latest/miniconda.html).

Other than that, you can run each scipt from the command line after you downloaded the repository.

```shell
git clone https://github.com/ClaudiaPaetzold/MEME_sum_and_annot.git 

cd MEME_sum_and_annot
```


### Required Packages

Some of these scripts reqiure additional python packages. 
If you want to produce venn diagrams from the meme summaries, you will need 
`matplotlib` and `matplotlib_venn`

To generate gene\*.fasta files by filtering [ProtheinOrtho](https://gitlab.com/paulklemm_PHD/proteinortho) Results, you will need `Pandas`.

Producing GO profiles for intersected summaries, requires `goatools`

## The core scripts
The core scripts are somewhat modular and can be run according to the desired output. However, ```summarize_meme.py``` must be run first, as its output serves as basis for subsequent intersection of results between samples, graphical representation and annotation.

## File name convention
Also please consider the naming scheme used in here for meme-results files. Filenames follow the pattern of meme\_gene\_genenumber\_[otherinfo].txt. So the scripts will consider the second and third part of the filename, i.e. gene_xxx as the gene name. If you want to use the scripts as is, please adhere to this pattern. If that is not an option, please change the approbriate lines in the scripts. 

#### summarize_meme
The first script in the pipeline reads in all  \*.txt files in a directory detailing MEME results for each gene and produces two summary files, one each for genes inferred under no positive selection (\*_noSelection.csv) and another comprising all genes inferred to be under positve selection including the estimated dn/ds ratio and the number of positions selected ('*_posSelection.csv)

```python
usage: summarize_meme.py [-h] [-d DIRECTORY] [-n NAME]

Summarizes results in HyPhy MEME output files. Produces 3 files: 1) a table
with genes where positive selcetion was detected incl dn/ds ratios,. 2) a list
of genes where no positive selection was detected. 3) A list of genes raising
an error in MEME analysis

optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --Directory DIRECTORY
                        Directory containing all MEME result *.txt files
  -n NAME, --Name NAME  Name of sample or condition to be appended to outfiles

```

### Intersect summaries of different samples
##### intersect_positive
This script will produce the a file called *allpositive.csv* which comprises a table listing all genes inferred as under positive selection in all given samples in the first column. For each sample two columns list the dN/dS ratio and the number of selected sites for the specific gene. Sample names corresponding to filenames are given in tab delimited file.

```python
usage: intersectpositive.py [-h] [-n NAMES] [-o OUTFILEPREFIX]

Intersects summary files of positively selected genes created by
summarize_meme.py including values for dn/ds ratios and number of selected
sites per sample. All input files must be in same directory.

optional arguments:
  -h, --help            show this help message and exit
  -n NAMES, --Names NAMES
                        Tab-separated text file with one summary-filename
                        (full Path) and corresponding samplename per line.
  -o OUTFILEPREFIX, --OutfilePrefix OUTFILEPREFIX
                        Prefix for the output file. Default: No Prefix
```

##### intersect_negative
This script will produce the a file called *allnegative.csv* which will list all genes inferred to not be positively selected in all given samples.

```python
usage: intersectnegative.py [-h] [-f FILES [FILES ...]] [-o OUTFILEPREFIX]

Intersects the 'no selection' summary files from summarize_meme.py

optional arguments:
  -h, --help            show this help message and exit
  -f FILES [FILES ...], --Files FILES [FILES ...]
                        File names of '*noSelection.csv' files to intersect
  -o OUTFILEPREFIX, --OutfilePrefix OUTFILEPREFIX
                        Prefix for the output file. Default: No Prefix
```

##### venn_diagrams
```python
usage: venn_diagrams.py [-h] [--File1 FILE1] [--File2 FILE2] [--File3 FILE3]
                        [--Name1 NAME1] [--Name2 NAME2] [--Name3 NAME3]
                        [--color1 COLOR1] [--color2 COLOR2] [--color3 COLOR3]
                        [--Title TITLE] [--transparency TRANSPARENCY]
                        [--outname OUTNAME]

Produces Venn diagrams for three samples in *.svg and *.pdf format. Please
find names of availlable colours here:
https://matplotlib.org/stable/gallery/color/named_colors.html

optional arguments:
  -h, --help            show this help message and exit
  --File1 FILE1         MEME summary file of first sample
  --File2 FILE2         MEME summary file of second sample
  --File3 FILE3         MEME summary file of third sample
  --Name1 NAME1         Name/Title of first sample
  --Name2 NAME2         Name/Title of second sample
  --Name3 NAME3         Name/Title of third sample
  --color1 COLOR1       Color for circle corresponding to first sample.
                        Default: darkslateblue
  --color2 COLOR2       Color for circle corresponding to second sample.
                        Default: seagreen
  --color3 COLOR3       Color for circle corresponding to third sample.
                        Default: hotpink
  --Title TITLE         Title displayed above the diagram. Default: None
  --transparency TRANSPARENCY
                        Transparency of circles in diagram. Default: 0.7
  --outname OUTNAME     Names for outfiles
```

### Functional and GO Annotation
The functional annotation and the GO-terms for each gene are produced by [Trinotate](https://github.com/Trinotate/Trinotate.github.io/wiki). We used the consensus sequences of the alignments used in the MEME analysis as input, so the filenames match between either results.

##### funct_annotation
Please note: script is written for an annotation containing both blastp and blastx results against the respective database. For annotation the blastp results are preferred and blastx results are used when the former did not yield a valid hit. 
The input file to be annotated may either be the result of summarize_meme or intersect_meme.  

```python
usage: funct_annotation.py [-h] [-a ANNOTATION] [-p POSITIVE_INTERSECTION]
                           [-n NEGATIVE_INTERSECTION] [-t TAXON]

combines the results of intersect*.py outputs with the functional annotation
and the corresponding GO-Terms from the Trinotate output while filtering out
any results marked as putative contaminations where the gene did not blast to
a user-specified target taxon.

optional arguments:
  -h, --help            show this help message and exit
  -a ANNOTATION, --Annotation ANNOTATION
                        Path to Trinotate*.xls annotation result
  -p POSITIVE_INTERSECTION, --positive_intersection POSITIVE_INTERSECTION
                        Path to *.csv file containing intersection of positive
                        meme results. Default: None
  -n NEGATIVE_INTERSECTION, --negative_intersection NEGATIVE_INTERSECTION
                        Path to *.csv file containing intersection of negative
                        meme results. Default: None
  -t TAXON, --taxon TAXON
                        Taxon required for annotated gene to be valid. If this
                        taxon is not present in the annotation, the gene will
                        be considered a putative contaminant. Default:
                        Spermatophyta
```

##### GO_breakdown
In the Trinotate annotation, the reported GO-terms for each gene are usually the lowest level term; while the higher level terms are omitted. They can however be reconstructed by traversing the Gene Ontology tree backwards to the root from any given term. The script uses the results of the funct_annotation script and reports three output files, one per category (biological process, cellular component, molecular function) lissting all GO-terms found in the given dataset per level and the sum of their occurences.

```python
usage: GO_breakdown.py [-h] [-a ANNOTATEDFILE] [-o OBOFILE]

summarizes GO-terms per Level for a given annotated intersection, i.e. the
results of funct_annotation.py. Produces three tables, one each with all GO-
terms per category, biological process, molecular function and cellular
compinent.

optional arguments:
  -h, --help            show this help message and exit
  -a ANNOTATEDFILE, --annotatedFile ANNOTATEDFILE
                        Path to *intersect_annotated.csv file
  -o OBOFILE, --oboFile OBOFILE
                        Path to go-basic.obo file. If not specified, the
                        current version of the file will be downloaded
```

## Auxillary scripts
MEME analyses require alignments of coding sequences as input. To identify  orthologous genes in a specific sample set, we used [ProtheinOrtho](https://gitlab.com/paulklemm_PHD/proteinortho). 

##### ProtehinOrtho2Fasta
The script `ProtheinOrtho2Fasta.py` accepts the resulting \*.tsv file and the \*.fasta files containing the assembled contigs of each sample to produce individual \*.fasta files for each orthologous gene recovered in a user-specified minumum number of samples. These files are continuously numbered: gene_\[number].fasta

```python
usage: ProteinOrtho2Fasta.py [-h] [-p PEPFILES] [-i POFILE] [-n NUMSAMPLES]

Filters ProteinOrtho output to only single copy genes in user provided min
number of samples and writes corresponding transdecoded protein sequences to
fasta files.

optional arguments:
  -h, --help            show this help message and exit
  -p PEPFILES, --PepFiles PEPFILES
                        directory containing transdecoder *.pep files
  -i POFILE, --POfile POFILE
                        ProteinOrtho output file in *tsv format
  -n NUMSAMPLES, --numSamples NUMSAMPLES
                        minimum number of samples required in output

```

##### remove_stops
Translated Amino acid sequences and corresponding coding sequences (cds) were produced from the assembled contigs using [TransDecoder](https://github.com/TransDecoder/TransDecoder/wiki). We aligned the AA sequences of our orthlogous genes using [MAFFT](https://mafft.cbrc.jp/alignment/software/), and back-translated the for MEME analysis using the corresponding cds and the software [Revtrans](http://www.cbs.dtu.dk/services/RevTrans-2.0/web/download.php). [TransDecoder](https://github.com/TransDecoder/TransDecoder/wiki) reports coding sequences *including* stop codons, but MEME will report an error when encountering one. Consequently we replaced stopcodons in thecoding sequence alignment prior to MEME analyses using the `remove_stop.py` script.

```python
usage: remove_stops.py [-h] Path

removes the universal stopcodons from all fasta files in the specified
directory

positional arguments:
  Path        directory path to fasta files - these should be named *.fasta

optional arguments:
  -h, --help  show this help message and exit

```


## Links

Even though this information can be found inside the project on machine-readable
format like in a .json file, it's good to include a summary of most useful
links to humans using your project. You can include links like:

- Project homepage: https://github.com/ClaudiaPaetzold/
- Repository: https://github.com/ClaudiaPaetzold/MEME_sum_and_annot
- Issue tracker: https://github.com/ClaudiaPaetzold/MEME_sum_and_annot/issues
  - I am very grateful for any feedback, questions or bug reports.
- Helpful sites:
  - for venn-diagrams, please find an excellent resource for availlable colours here:
     https://matplotlib.org/stable/gallery/color/named_colors.html


## Licensing


"The code in this project is licensed under GNU General Public license version 3.0 
([GPU]https://www.gnu.org/licenses/gpl-3.0.en.html(#))."
