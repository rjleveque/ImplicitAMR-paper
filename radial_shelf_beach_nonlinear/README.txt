
Code for the example in Section 4.1 of the paper

    Implicit Adaptive Mesh Refinement for Dispersive Tsunami Propagation
    by Marsha J. Berger and Randall J. LeVeque, submitted, 2023
    Preprint: https://arxiv.org/abs/2307.05816
    Git repository: https://github.com/rjleveque/ImplicitAMR-paper

The code in this directory requires a version of Clawpack that includes
the Boussinesq version of GeoClaw, and a version that includes the 
1d version of GeoClaw.

It also requires an appropriate version of PETSc and various modifications
to the Makefile to link to the correct libraries.

See the main README.md file in this repository for more information.

First run the code in 1d_radial using Clawpack with the geoclaw_1d
subdirectory. 

    cd 1d_radial
    make topo
    make .output
    cd ..

Then run the code in this directory using a version of Clawpack that includes
the Boussinesq version of GeoClaw.

    make topo
    make .output

This make take a couple days.
(Reduce amrdata.amr_levels_max in setrun.py for a faster run with less
resolution of the narrow solitary waves that develop close to shore.)

Then make the figures that appear in the paper:

    python plot_frames.py


Version
-------

Nov. 2023: Updated for bouss_2d branch to be merged into GeoClaw.
