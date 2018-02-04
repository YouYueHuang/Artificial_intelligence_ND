# Artificial intelligence nanodegree project

<img src="./img/ai_cover.png" alt="Overview" width="400px" height="267px">

## Overview

This repository is for Udacity artificial intelligence Nanodegree. The working environment is based on python 3.6.1 virtualenv and jupyter notebook.

##  Get started
------

* Download Anaconda 3.6 in official site
[Anaconda Distribution](https://www.anaconda.com/download/#windows)

* Download the `hmmlearn-0.2.1-cp35-cp35m-win_amd64.whl`
[hmmlearn-0.2.1-cp35-cp35m-win_amd64.whl](https://www.lfd.uci.edu/~gohlke/pythonlibs/#hmmlearn)

* Install C/C++ compiler for building the required packages
[Visual C++ 2015 Build Tools](http://landinghub.visualstudio.com/visual-cpp-build-tools)

* Install the wheel
`pip install hmmlearn-0.2.1-cp35-cp35m-win_amd64.whl`

* Open a terminal and run `conda env create -f aind-universal.yml -n aind python=3.5` to create the environment.

* Run `activate aind` to activate the environment

* Install z3
`pip install git+https://github.com/hmmlearn/hmmlearn.git`
`pip install z3-solver`

* Run `deactivate` to deactivate the environment

* Update pip, conda and conda-env to latest version with `conda install -c anaconda pip`

* Jupyter Notebook

  - install Jupyter Notebook `pip install jupyter`

  - Launch an jupyter notebook server `jupyter notebook`

## Dependencies 
------
* export packages `conda list -e > requirement.txt`
* install all packages `conda create --name <env> --requirement.txt`

If you would like to install packages separately, this [link](Package_description.md) would help you.