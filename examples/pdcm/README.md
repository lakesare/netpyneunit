NetPyNE version of Potjans and Diesmann thalamocortical network.
Based on
- https://direct.mit.edu/neco/article-pdf/33/7/1993/1925382/neco_a_01400.pdf, and
- https://github.com/ceciliaromaro/PDCM_NetPyNE/tree/run_trials.

To compile mod files: `nrnivmodl`  
To run on single core: `python3 run.py`  
To run on multiple cores: `mpiexec -n 2 nrniv -python -mpi init.py`
