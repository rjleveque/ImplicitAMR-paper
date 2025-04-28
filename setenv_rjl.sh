
# This is the bash file used by RJL to set the parameters needed
# to run the Bouss version of GeoClaw with MPI and OpenMP.
# Adjust as needed for your system...

#export CLAW=/Users/rjl/clawpack_src/clawpack_master
#export PYTHONPATH=$CLAW
echo CLAW is set to $CLAW

# path to PETSc installation:
export PETSC_DIR=/Users/rjl/git/Clones/petsc

#export PETSC_ARCH=
# PETSC_ARCH is only needed if PETSc is installed inside the PETSc directory.
# For PETSc installs by conda or package managers, it should not be set.
export PETSC_ARCH=arch-darwin-c-opt

export PETSC_OPTIONS="-options_file $PWD/petscMPIoptions"
export OMP_NUM_THREADS=6
export BOUSS_MPI_PROCS=6

export CLAW_MPIEXEC=mpiexec
# set CLAW_MPIEXEC to mpiexec only if this command is defined in your shell,
# e.g. to use some version of MPI was installed outside of PETSc.
# Or set to the full path to this command, e.g. for the PETSc version:
#export CLAW_MPIEXEC=$PETSC_DIR/$PETSC_ARCH/bin/mpiexec  # requires PETSC_ARCH

# set CLAW_MPIFC to the proper Fortran compiler to use for MPI code
# e.g. mpif90 if that is defined in your shell, or gfortran *might* work.
# This will over-rule any FC environment variable.
export CLAW_MPIFC=mpif90
