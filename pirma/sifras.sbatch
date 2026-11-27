#!/bin/bash
#SBATCH -p main
#SBATCH -n24
#SBATCH -t 00:30:00
#SBATCH -o sifras_%j.out

REPO_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
if [[ -f "$REPO_DIR/pirma/sifras_mpi.py" ]]; then
    SCRIPT_DIR="$REPO_DIR/pirma"
elif [[ -f "$REPO_DIR/sifras_mpi.py" ]]; then
    SCRIPT_DIR="$REPO_DIR"
    REPO_DIR="$(dirname -- "$SCRIPT_DIR")"
else
    echo "Nerastas sifras_mpi.py kataloge $REPO_DIR arba $REPO_DIR/pirma" >&2
    exit 1
fi
VENV_DIR="$REPO_DIR/.venv-hpc"
cd "$REPO_DIR"

module load openmpi

if ! "$VENV_DIR/bin/python3" -c "import mpi4py.MPI" 2>/dev/null; then
    python3 -m venv "$VENV_DIR"
    MPICC=mpicc "$VENV_DIR/bin/pip" install --no-binary mpi4py mpi4py
fi

PYTHON_PROGRAM=${PYTHON_PROGRAM:-"$VENV_DIR/bin/python3"}
RUN_COMMAND="mpirun -p"

exec ${RUN_COMMAND} "$PYTHON_PROGRAM" "$SCRIPT_DIR/sifras_mpi.py" -r 3.61 3.62 3.63 3.64 3.65 3.66 3.67 3.68 3.69 3.71 3.72 3.73 3.74 3.75 3.76 3.77 3.78 3.79 3.8 3.6100001 -x0 0.3 -f "$SCRIPT_DIR/ivestis.txt"
