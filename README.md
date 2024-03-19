
# ImplicitAMR-paper

This repository contains the code used to set up and run the examples in the
manuscript

    Implicit Adaptive Mesh Refinement for Dispersive Tsunami Propagation
    by Marsha J. Berger and Randall J. LeVeque, submitted, 2023
    (Revised manuscript submitted March, 2024 with updated examples)

which is available as a [preprint](https://arxiv.org/abs/2307.05816).
**[v2]**

The python scripts setrun.py in each directory may be useful to see more
clearly how each run was set up.

Running the code requires Clawpack v5.10.0 (or later),
which *will soon be* available from https://www.clawpack.org/releases.html and permanently archived on Zenodo and also at this DOI: https://doi.org/10.17605/osf.io/kmw6h.  This code was recently merged into the master branch of https://github.com/clawpack/geoclaw and is also available there.

**Notes:** (March 2024)

 - Revised after resubmission of paper the release of Clawpack v5.10.0,
   *(very soon!)*.
 
 - Clawpack v5.10.0 includes both:

     - A 1D version of GeoClaw that will support the solution of some Boussinesq
       equations along with shallow water equations.
       The 1D code was used to compute reference radially-symmetric solutions
       for comparison with the 2D simulations for some examples.
       See https://www.clawpack.org/geoclaw1d.html.

     - A 2D version of GeoClaw with implicit timestepping coupled with AMR, and applied to the Boussinesq-type
     equations described in the paper. 
       See https://www.clawpack.org/bouss2d.html.


 - To run the codes using MPI for the implicit solves via PETSc,
   combined with OpenMP for the explicit time stepping in the shallow
   water steps (distributing grid patches between threads), it is
   necessary to use PETSc Version 3.20 (or later) with enhancements
   added by Barry Smith.

 - The code used for the resubmitted paper is tagged as
   `resubmitted_march2024`.  A zip file of the code used for the final
   published paper will eventually be archived on Zenodo.
