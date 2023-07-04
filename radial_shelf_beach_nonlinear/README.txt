
First run the code in 1d_radial using Clawpack with the geoclaw_1d
subdirectory.  (Clean up eventually once that's merged into GeoClaw).

    cd 1d_radial
    make topo
    make .output
    cd ..

Then run the code in this directory using version of Clawpack that includes
the Boussinesq version of GeoClaw.  PETSc is also required.

    make topo
    make .output

This make take a couple days.

Then make the figures that appear in the paper:

    python plot_frames.py
