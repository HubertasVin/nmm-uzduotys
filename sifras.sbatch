#!/bin/bash
#SBATCH -p main
#SBATCH -n4
#SBATCH -t 00:30:00
#SBATCH -o sifras_%j.out

module load openmpi
command -v mpicc >/dev/null || { echo "mpicc not found - did 'module load openmpi' succeed?" >&2; exit 1; }

# import mpi4py.MPI dlopens libmpi; bare "import mpi4py" does not
if ! .venv-hpc/bin/python3 -c "import mpi4py.MPI" 2>/dev/null; then
    rm -rf .venv-hpc
    python3 -m venv .venv-hpc
    .venv-hpc/bin/pip install --no-binary mpi4py mpi4py
fi

PYTHON_PROGRAM=${PYTHON_PROGRAM:-.venv-hpc/bin/python3}

if [ -z "${RUN_COMMAND:-}" ]; then
    # --mpi=openmpi left every rank a singleton COMM_WORLD (4x "Procesu: 1");
    # probe pmix wiring first, fall back to mpirun from the loaded module
    if timeout 60 srun --mpi=pmix -n2 ${PYTHON_PROGRAM} -c "from mpi4py import MPI; import sys; sys.exit(0 if MPI.COMM_WORLD.Get_size() == 2 else 1)"; then
        RUN_COMMAND="srun --mpi=pmix"
    else
        echo "srun --mpi=pmix probe failed, falling back to mpirun" >&2
        RUN_COMMAND="mpirun -np ${SLURM_NTASKS:-4}"
    fi
fi

exec ${RUN_COMMAND} ${PYTHON_PROGRAM} sifras_mpi.py -r 3.61 3.62 3.63 3.64 3.65 3.66 3.67 3.68 3.69 3.71 3.72 3.73 3.74 3.75 3.76 3.77 3.78 3.79 3.8 -x0 0.2 -f ivestis.txt
