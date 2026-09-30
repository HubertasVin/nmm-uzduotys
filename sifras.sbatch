#!/bin/bash
#SBATCH -p main
#SBATCH -n4
#SBATCH -t 00:30:00
#SBATCH -o sifras_%j.out

module load openmpi

# Python module names differ between clusters; try common ones
PY=$(command -v python3 || true)
if [ -z "$PY" ]; then
    for m in python3 python Python3 Python anaconda3 miniconda3; do
        if module avail 2>&1 | grep -qiE "(^|[/ ])$m([/ .:]|$)"; then
            module load "$m"
            break
        fi
    done
    PY=$(command -v python3 || command -v python || true)
fi
if [ -z "$PY" ]; then
    echo "ERROR: no python on node; available modules:" >&2
    module avail python 2>&1
    exit 1
fi

# mpi4py needs mpicc from the loaded openmpi module if it has to compile
"$PY" -c "import mpi4py" 2>/dev/null || "$PY" -m pip install --user -q mpi4py
"$PY" -c "import mpi4py" 2>/dev/null || { echo "ERROR: mpi4py unavailable for $PY" >&2; exit 1; }

mpirun "$PY" sifras_mpi.py -r 3.61 3.62 3.63 3.64 3.65 3.66 3.67 3.68 3.69 3.71 3.72 3.73 3.74 3.75 3.76 3.77 3.78 3.79 3.8 -x0 0.2 -f ivestis.txt
