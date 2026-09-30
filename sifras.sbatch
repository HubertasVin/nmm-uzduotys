#!/bin/bash
#SBATCH -p main
#SBATCH -n4
#SBATCH -t 00:30:00
#SBATCH -o sifras_%j.out

module load openmpi
module load python3

# Debian system python is externally managed (PEP 668) -> use a venv
VENV=.venv-hpc
python3 -m venv "$VENV" || { echo "ERROR: venv creation failed (python3-venv missing?)" >&2; exit 1; }
PY="$VENV/bin/python"

# mpi4py needs mpicc from the loaded openmpi module if it has to compile
"$PY" -c "import mpi4py" 2>/dev/null || "$PY" -m pip install -q mpi4py
"$PY" -c "import mpi4py" 2>/dev/null || { echo "ERROR: mpi4py unavailable for $PY" >&2; exit 1; }

mpirun "$PY" sifras_mpi.py -r 3.61 3.62 3.63 3.64 3.65 3.66 3.67 3.68 3.69 3.71 3.72 3.73 3.74 3.75 3.76 3.77 3.78 3.79 3.8 -x0 0.2 -f ivestis.txt
