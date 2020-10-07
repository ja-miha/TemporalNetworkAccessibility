#!/bin/bash
#SBATCH -J sirds                            # job name
#SBATCH -N 1                                 # number of nodes
#SBATCH -n 8                                   # number of MPI processes, here 16 per node
#SBATCH --partition=compute         # choose nodes from partition
#SBATCH -o %j.out                            # stdout file name (%j: job ID)
#SBATCH -e %j.err                             # stderr file name (%j: job ID)
#SBATCH -t 12:00:00                        # max run time (hh:mm:ss), max 72h!
#SBATCH --mail-type=END
#SBATCH --mail-user=s-jamiha@uni-greifswald.de
#SBATCH --array=1-13                 # Array range

mpiexec python simulation.py $SLURM_ARRAY_TASK_ID
