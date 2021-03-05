<img src="img/smart-house.png" align="right" width="150"/>

# Causality Detection
Author: Kanvaly Fadiga

This repository implements our causal relation learning algorithm and also allows us to explain events. To facilitate its 
use we have used streamlit which allows us to create a web interface with which we can interact.


# Installation

my python version: Python 3.8.5

after activating your python environment, install required package using this command:

```sh
pip install -r requirements.txt
```


# Usage

* **Web app:** To run the web app run `python main.py`

* **Simple example:** we also provide a simple python code `example.py` that learn a simple network. 
just run `python example.py` and it learn the graph and plot the difference with the groundthruth.

# Architecture

* **CausalLeaner** in `causal_learner.py`:
> contains the algorithm that learn causal relationship using intervention and interaction. 

* **BayesianNetwork** in `network.py`:
> Our implementation og bayesian network. it contain function to perform do operation and data generation

* **most_probable_explanation** and **belief_propagation** in `explanation.py`:
> perform the two methods to do abduction in a bayesian network
