
# ImplicitAMR-paper

This repository contains the code used to set up and run the examples in the
manuscript

    Implicit Adaptive Mesh Refinement for Dispersive Tsunami Propagation
    by Marsha J. Berger and Randall J. LeVeque, submitted, 2023
    Preprint: https://arxiv.org/abs/???

The python scripts setrun.py in each directory may be useful to see more
clearly how each run was set up.

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
the figures in the paper was commit a079486205 from the repository
    https://github.com/rjleveque/geoclaw_1d
while the 2D code runs in conjunction with commit ??? from a private
repository 
    https://github.com/rjleveque/BoussDev
Please contact the authors for more details.


