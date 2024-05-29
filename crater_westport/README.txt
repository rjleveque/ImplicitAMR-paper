Code for the example in Section 4.3 of the paper

    Implicit Adaptive Mesh Refinement for Dispersive Tsunami Propagation
    by Marsha J. Berger and Randall J. LeVeque, submitted, 2023
    (revised March, 2024)
    Preprint: https://arxiv.org/abs/2307.05816 [v2]
    Git repository: https://github.com/rjleveque/ImplicitAMR-paper

The code in this directory requires Clawpack v5.10.0, which includes
the Boussinesq version of GeoClaw in both 1d and 2d.

It also requires PETSc v3.20 for MPI and OpenMP to work well together,
and various modifications to the Makefile to link to the correct libraries.

See https://www.clawpack.org/bouss2d.html for more details.

See the main README.md file in this repository for more information.

To fetch the required topo files:
    python fetch_topo.py

To run the code:
    make .output

Then make the figures that appear in the paper:
    python plot_frames.py

Version
-------

Nov. 2023: Updated for bouss_2d branch to be merged into GeoClaw.

March 2024: Updated for resubmission of paper
