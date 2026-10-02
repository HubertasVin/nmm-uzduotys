#!/bin/bash
#SBATCH -p main
#SBATCH -n12
#SBATCH -t 00:30:00
#SBATCH -o sifras_%j.out

module load openmpi

if ! .venv-hpc/bin/python3 -c "import mpi4py.MPI" 2>/dev/null; then
    rm -rf .venv-hpc
    python3 -m venv .venv-hpc
    .venv-hpc/bin/pip install --no-binary mpi4py mpi4py
fi

PYTHON_PROGRAM=${PYTHON_PROGRAM:-.venv-hpc/bin/python3}
RUN_COMMAND="mpirun -np ${SLURM_NTASKS:-12}"

exec ${RUN_COMMAND} ${PYTHON_PROGRAM} sifras_mpi.py -r 3.61 3.62 3.63 3.64 3.65 3.66 3.67 3.68 3.69 3.71 3.72 3.73 3.74 3.75 3.76 3.77 3.78 3.79 3.8 -x0 0.2 -f ivestis.txt
