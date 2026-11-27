#!/bin/bash
#SBATCH -p main
#SBATCH -n24
#SBATCH -t 00:30:00
#SBATCH -o sifras_%j.out

set -euo pipefail
cd "${SLURM_SUBMIT_DIR:-$PWD}"
DIR=pirma
[[ -f "$DIR/sifras_mpi.py" ]] || DIR=.
module load openmpi

if ! .venv-hpc/bin/python3 -c "import mpi4py.MPI" 2>/dev/null; then
    python3 -m venv .venv-hpc
    MPICC=mpicc .venv-hpc/bin/pip install --no-binary mpi4py mpi4py
fi

exec mpirun -np "${SLURM_NTASKS:-24}" .venv-hpc/bin/python3 "$DIR/sifras_mpi.py" \
    -r 3.61 3.62 3.63 3.64 3.65 3.66 3.67 3.68 3.69 3.71 3.72 3.73 3.74 3.75 3.76 3.77 3.78 3.79 3.8 3.6100001 \
    -x0 0.3 -f "$DIR/ivestis.txt"
