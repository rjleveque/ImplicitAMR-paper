
# ImplicitAMR-paper

This repository contains the code used to set up and run the examples in the
manuscript

    Implicit Adaptive Mesh Refinement for Dispersive Tsunami Propagation
    by Marsha J. Berger and Randall J. LeVeque, submitted, 2023
    Preprint: https://arxiv.org/abs/2307.05816

The python scripts setrun.py in each directory may be useful to see more
clearly how each run was set up.

**Note:** (November 2023)
This repository is currently being updated to use the code that
will be merged into GeoClaw.  The git tag `submitted_aug2023` points to the
version described below...

Currently it is not easy to actually run these codes, since they depend on
two sets of new enhancements to GeoClaw that are still under active
development:

 - A 1D version of GeoClaw that will support the solution of some Boussinesq
   equations along with shallow water equations.

 - A 2D version of GeoClaw with implicit timestepping coupled with AMR, as
   described in the paper.

The 1D code was used to compute reference radially-symmetric solutions for
comparison with the 2D simulations for some examples.

Neither code has been merged into the main Clawpack/GeoClaw code yet, and
since they were branched at different times before some of the recent
development in the main development branch, some refactoring will be
required to perform this merge and make the codes easier to use for other
users.  Once that has been done, we plan to update this repository to
facilitate reproducibility.

In the meantime, we note that the 1D version used to perform the runs for
the figures in the paper was commit a0794862 from the repository
    https://github.com/rjleveque/geoclaw_1d
while the 2D code runs in conjunction with commit e17719fa from a private
repository 
    https://github.com/rjleveque/BoussDev
Please contact the authors for more details.

To run the codes using MPI for the implicit solves via PETSc,
combined with OpenMP for the explicit time stepping in the shallow
water steps (distributing grid patches between threads), it is
necessary to use PETSc Version 3.20 (or later) with enhancements
added by Barry Smith.
