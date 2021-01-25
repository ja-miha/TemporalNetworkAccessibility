#!/bin/bash
#SBATCH -J si_b                            # job name
#SBATCH -N 1                                 # number of nodes
#SBATCH -n 1                                   # number of MPI processes, here 16 per node
#SBATCH --partition=batch         # choose nodes from partition
#SBATCH -o %j.out                            # stdout file name (%j: job ID)
#SBATCH -e %j.err                             # stderr file name (%j: job ID)
#SBATCH -t 72:00:00                        # max run time (hh:mm:ss), max 72h!
#SBATCH --mail-type=END
#SBATCH --mail-user=s-jamiha@uni-greifswald.de

python simulation_multipro.py
