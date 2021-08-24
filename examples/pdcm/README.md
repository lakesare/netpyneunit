# Resizing the Potjans-Diesmann Cortical Microcircuit (PDCM) network.

### Origin
Comes from the real-world paper comparing resized simulations in **NetPyNE**: [https://direct.mit.edu/neco/article-pdf/33/7/1993/1925382/neco_a_01400.pdf](https://direct.mit.edu/neco/article-pdf/33/7/1993/1925382/neco_a_01400.pdf) (see Github for code: [https://github.com/ceciliaromaro/PDCM_NetPyNE](https://github.com/ceciliaromaro/PDCM_NetPyNE)).  
**Salvador Dura-Bernal** (coauthor of **NetPyNE**) coauthored the paper, and has been very helpful for us by resolving any confusion around it.

### Description

Takes the **Potjans-Diesmann Cortical Microcircuit** (**PDCM**) model implemented in **NetPyNE**, resizes it using the special `Reescale` function, and tests whether various stats stay the same - this should enable researchers to experiment with smaller networks.

### Goal
With this example we're getting our feet wet in the creation of the suite of tests that can be used to evaluate any rescaled **NetPyNE** network.
To generalise this into, say, `'ResizeTestSuites'`, we want to implement at least one other paper of the kind.

___

### Running it

To compile mod files: `nrnivmodl`  
To run on single core: `python3 run.py`  
To run on multiple cores: `mpiexec -n 2 nrniv -python -mpi run.py`

### Gotchas

If you get the `AttributeError: 'CompartCell' object has no attribute 'hPointp'` error - it means you didn't compile the mod file in this directory (with `nrnivmodl`).
Try to `cd examples/pdcm`; `nrnivmodl`; `python3 run.py`.
