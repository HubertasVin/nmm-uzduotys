#!/bin/bash
#SBATCH -p main
#SBATCH -n4
#SBATCH -t 00:30:00
#SBATCH -o sifras_%j.out

module load openmpi

PYTHON_PROGRAM=${PYTHON_PROGRAM:-.venv-hpv/bin/python}
RUN_COMMAND=${RUN_COMMAND:-srun --mpi=openmpi}

exec ${RUN_COMMAND} ${PYTHON_PROGRAM} sifras_mpi.py -r 3.61 3.62 3.63 3.64 3.65 3.66 3.67 3.68 3.69 3.71 3.72 3.73 3.74 3.75 3.76 3.77 3.78 3.79 3.8 -x0 0.2 -f ivestis.txt
