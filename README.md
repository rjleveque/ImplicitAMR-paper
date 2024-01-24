
# ImplicitAMR-paper

This repository contains the code used to set up and run the examples in the
manuscript

    Implicit Adaptive Mesh Refinement for Dispersive Tsunami Propagation
    by Marsha J. Berger and Randall J. LeVeque, submitted, 2023

which is available as a [preprint](https://arxiv.org/abs/2307.05816).

The python scripts setrun.py in each directory may be useful to see more
clearly how each run was set up.

**Note:** (November 2023)
This repository is currently being updated to use the code that
will be merged into GeoClaw.  The git tag `submitted_aug2023` points to the
version used for plots in the submitted paper.

Currently it is not easy to actually run these codes, since they depend on
two sets of new enhancements to GeoClaw that are still under active
development:

 - A 1D version of GeoClaw that will support the solution of some Boussinesq
   equations along with shallow water equations.
   The 1D code was used to compute reference radially-symmetric solutions
   for comparison with the 2D simulations for some examples.
   This code was recently committed to the
   [master branch of clawpack/geoclaw](https://github.com/clawpack/geoclaw/).

 - A 2D version of GeoClaw with implicit timestepping coupled with AMR, as
   described in the paper.  This code is currently on a separate branch of
   clawpack/geoclaw, https://github.com/clawpack/geoclaw/tree/bouss_2d

To run the codes using MPI for the implicit solves via PETSc,
combined with OpenMP for the explicit time stepping in the shallow
water steps (distributing grid patches between threads), it is
necessary to use PETSc Version 3.20 (or later) with enhancements
added by Barry Smith.
