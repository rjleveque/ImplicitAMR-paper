# These environment variables need to be properly set for your computer:

export CLAW=/Users/rjl/clawpack_src/clawpack-v5.10.0
export PYTHONPATH=$CLAW  # not needed if you pip install clawpack
echo CLAW is set to $CLAW

export PETSC_DIR=/Users/rjl/git/Clones/petsc
export PETSC_ARCH=arch-darwin-c-opt

export OMP_NUM_THREADS=6

