
# ImplicitAMR-paper

This repository contains the code used to set up and run the examples in the
manuscript

    Implicit Adaptive Mesh Refinement for Dispersive Tsunami Propagation
    by Marsha J. Berger and Randall J. LeVeque, submitted, 2023
    (Revised manuscript submitted March, 2024 with updated examples)

which is available as a [preprint](https://arxiv.org/abs/2307.05816).
**[v2]**

This paper has now been accepted for publication in the [SIAM Journal on
Scientific Computing](https://www.siam.org/publications/journals/siam-journal-on-scientific-computing-sisc).

The python scripts setrun.py in each directory may be useful to see more
clearly how each run was set up.


**Notes:** (Revised June 2024)

 - The version of [GeoClaw](http://www.geoclaw.org)
   needed to run the code in this repository
   was recently released in Clawpack v5.10.0.
   See https://www.clawpack.org/releases.html for links and release notes.
   
   All releases of Clawpack are also permanently archived on Zenodo and at this
   DOI: https://doi.org/10.17605/osf.io/kmw6h.

 - Clawpack v5.10.0 includes both:

     - A 2D version of GeoClaw with implicit timestepping coupled with AMR,
       and applied to the Boussinesq-type equations described in the paper. 
       See https://www.clawpack.org/bouss2d.html.
       
     - A 1D version of GeoClaw that also supports the solution of some 
       Boussinesq-type equations, along with shallow water equations.
       The 1D code is used to compute reference radially-symmetric solutions
       for comparison with the 2D simulations for the example in
       `radial_shelf_beach_nonlinear`.
       See https://www.clawpack.org/geoclaw1d.html.

 - To run the codes using MPI for the implicit solves via PETSc,
   combined with OpenMP for the explicit time stepping in the shallow
   water steps (distributing grid patches between threads), it is
   necessary to use PETSc Version 3.20 (or later) with enhancements
   added by Barry Smith.
   
 - The `file setenv_rjl.sh` is a bash script for the environment
   variables as set by RJL on the laptop where the timings
   were performed.  These environment variables must be set properly
   for your computer.
   
 - The file `petscMPIoptions` lists the PETSc options used for the
   linear solvers. You must set an environment variable `PETSC_OPTIONS` to
   be the full path to this file. 

 - Alternatively, rather than setting environment variables, you can
   modify the `Makefile` in each example directory as indicated in the lines
   that are commented out.

 - The version of this repository used for the resubmitted paper is tagged as
   `resubmitted_march2024`.  This code was cleaned up a bit more
   and tagged `publication` for the version to be archived in the
   Supplementary Materials for the paper, and is also archived at
   [DOI 10.5281/zenodo.12709453](https://zenodo.org/doi/10.5281/zenodo.12709451).

