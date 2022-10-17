# Multimodal BCIs for Pandemic Scenarios
This repository contains code accompanying the paper [Multimodal collaborative brain-computer interfaces aid human-machine team decision-making in a pandemic scenario](https://doi.org/10.1088/1741-2552/ac96a5) authored by Davide Valeriani, Lena C. O'Flynn, Alexis Worthley, Azadeh Hamzehei Sichani, Kristina Simonyan.

# How to install

To clone and run this application, you'll need [Git](https://git-scm.com) and [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed on your computer. From your Anaconda prompt command line:

```bash
# Clone this repository
$ git clone https://github.com/simonyanlab/DoD-BARI-BCI-Data-Repository.git

# Create a new conda environment
$ conda create --name bari python=3.9.6

# Activate environment
$ conda activate bari

# Go into the repository
$ cd DoD-BARI-BCI-Data-Repository

# Install dependencies
$ pip install -r requirements.txt
```

# How to run fMRI preprocessing

Make sure [AFNI](https://afni.nimh.nih.gov/) is installed. Open command line:

```bash
# Go into the scripts folder of the repository
$ cd DoD-BARI-BCI-Data-Repository/scripts

# Run AFNI script
$ sh ./afni_preproc
```

# How to use analytical scripts

```bash
# Activate environment
$ conda activate bari

# Go into the scripts folder of the repository
$ cd DoD-BARI-BCI-Data-Repository/scripts

# Run jupyter notebook
$ jupyter notebook

# In the browser window that appears, click on Behavioral_Analysis or EEG_Analysis to open up detailed code.
```

# How to create stimuli images

To create stimuli images, open Anaconda prompt command line:

```bash
# Activate environment
$ conda activate bari

# Go into the scripts folder of the repository
$ cd DoD-BARI-BCI-Data-Repository/scripts

# Launch script and visualize parameters to learn how to run it
python make_map_stimuli.py -h
```

You can generate the background images from [https://azgaar.github.io/Fantasy-Map-Generator/](here).

# License

MIT
