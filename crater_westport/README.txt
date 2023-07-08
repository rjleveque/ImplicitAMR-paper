The code in this directory requires a version of Clawpack that includes
the Boussinesq version of GeoClaw.  

It also requires an appropriate version of PETSc and various modifications
to the Makefile to link to the correct libraries.

See the main README.md file in this repository for more information.

To fetch the required topo files:
    python fetch_topo.py

To run the code:
    make .output

Then make the figures that appear in the paper:
    python plot_frames.py
