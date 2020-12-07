# npm-centrality

## Setup Environment

Install miniconda from https://docs.conda.io/en/latest/miniconda.html.

### Linux
```shell
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
sh Miniconda3-latest-Linux-x86_64.sh
```

### Create conda environment
```shell
conda update conda
conda env create -f environment.yml
```

### Activate environment
```shell
conda activate npm-centrality
```

## Data

### The final data is in `~/data/wallet_complete_with_failed.json`