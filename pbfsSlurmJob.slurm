#!/bin/bash
#SBATCH --job-name=py-job        
#SBATCH --nodes=64
#SBATCH --ntasks-per-node=2
#SBATCH --partition=general-compute
#SBATCH --qos=general-compute                        
#SBATCH --time=00:10:00          
#SBATCH --mail-type=begin        
#SBATCH --mail-type=end          
#SBATCH --mail-user=arshabhs@buffalo.edu
#SBATCH --out=outputsNewG/output_n_128.out
#SBATCH --exclusive
#SBATCH --constraint=IB

module load mpi4py/3.0.1-py37

mpirun -np 128 python3 parallelBFS6.py 128
