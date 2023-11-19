# These environment variables need to be properly set for your computer:

#export CLAW=/Users/rjl/clawpack_src/clawpack_bouss  # WIP version during merge
#export PYTHONPATH=$CLAW
echo CLAW is set to $CLAW

export PETSC_DIR=/Users/rjl/git/Clones/petsc
export PETSC_ARCH=arch-darwin-c-opt
export PETSC_OPTIONS="-options_file /Users/rjl/git/ImplicitAMR-paper/petscMPIoptions"

export OMP_NUM_THREADS=6

