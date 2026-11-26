#!/bin/bash
#SBATCH --partition=main
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=1
#SBATCH --time=00:30:00
#SBATCH --output=uzduotis26_%j.out

set -euo pipefail
cd "${SLURM_SUBMIT_DIR:-$PWD}"
module load openmpi

PYTHON_ENV="${HOME}/.venvs/nmm-uzduotis26"
mkdir -p "$(dirname "$PYTHON_ENV")"
if ! "$PYTHON_ENV/bin/python" -c "import numpy; import mpi4py.MPI" 2>/dev/null; then
    python3 -m venv "$PYTHON_ENV"
    "$PYTHON_ENV/bin/python" -m pip install numpy
    MPICC=mpicc "$PYTHON_ENV/bin/python" -m pip install --no-binary=mpi4py mpi4py
fi

exec mpirun -np "${SLURM_NTASKS:-4}" "$PYTHON_ENV/bin/python" antra/uzduotis26_mpi.py
