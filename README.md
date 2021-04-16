![Logo of the project](https://raw.githubusercontent.com/jehna/readme-best-practices/master/sample-logo.png)

# MEME_sum_and_annot
Python scripts to summarize MEME (Mixed Effects Model of Evolution) results generated HyPhy and annotate selected genes.

This is a set of Python scripts that help uses a series of outputfiles generated using the [MEME](https://www.hyphy.org/methods/selection-methods/) 
algorithm in [HyPhy](https://www.hyphy.org/) and summarizes the output to generate an overview of all under positive selcetion or for which no 
selection was detected. The summaries can be intersected across samples and a functional annotation and GO profiles can be produced 
for intersected summaries. 

There are also some axillary scripts that produce single-gene fastafiles from [ProtheinOrtho](https://gitlab.com/paulklemm_PHD/proteinortho) output or remove stop codons, which would impede MEME analysis from alignments.

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

#### Additional Software



## The core scripts



```shell
run one
```

And state what happens step-by-step.

#### one code

## Auxillary scripts

#### ProtehinOrtho2Fasta

#### remove_stops

## Links

Even though this information can be found inside the project on machine-readable
format like in a .json file, it's good to include a summary of most useful
links to humans using your project. You can include links like:

- Project homepage: https://your.github.com/awesome-project/
- Repository: https://github.com/your/awesome-project/
- Issue tracker: https://github.com/your/awesome-project/issues
  - In case of sensitive bugs like security vulnerabilities, please contact
    my@email.com directly instead of using issue tracker. We value your effort
    to improve the security and privacy of this project!
- Related projects:
  - Your other project: https://github.com/your/other-project/
  - Someone else's project: https://github.com/someones/awesome-project/


## Licensing


"The code in this project is licensed under GNU General Public license version 3.0 
([GPU]https://www.gnu.org/licenses/gpl-3.0.en.html(#))."
