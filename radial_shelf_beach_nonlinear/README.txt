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

Then make the figures that appear in the paper:

    python plot_frames.py

