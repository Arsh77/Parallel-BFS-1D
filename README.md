# Parallel-BFS-1D
A parallel implementation of BFS using mpi4py

Implemented parallel bfs algorithm that run on distrinuted memory architecture. 

reference : https://en.wikipedia.org/wiki/Parallel_breadth-first_search

Script: mpirun -np <number of processors> python3 <name of file>
Slurm jobs are also added
To load mpi4py module in linux env : module load mpi4py/<add version number> example -> module load mpi4py/3.0.1-py37
  
