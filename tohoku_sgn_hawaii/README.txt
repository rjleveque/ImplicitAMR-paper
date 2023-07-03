
Running this code requires the correct version of GeoClaw with Boussinesq
terms, currently under development.

It also requires PETSc and various modifications to the Makefile to link
to the correct libraries.

Topo files can be downloaded using fetch_topo.py

The UCSB and Fujii source dtopo files can be downloaded using fetch_dtopo.py
which gets them from:
    https://github.com/rjleveque/tohoku2011-paper1/tree/master/sources

In setrun.py:

To run with SWE on all levels:
    probdata.add_param('minLevelBouss', 10,' minlevel for Bouss terms')
    probdata.add_param('maxLevelBouss', 10,' maxlevel for Bouss terms')

To run with SGN on all levels:
    probdata.add_param('minLevelBouss', 1,' minlevel for Bouss terms')
    probdata.add_param('maxLevelBouss', 10,' maxlevel for Bouss terms')

The plotting scripts assume output is moved to files with names like
    _output_sgn_ucsb
for the SGN output using the UCSB source.

Detided DART data included here is from:
https://github.com/rjleveque/tohoku2011-paper1/tree/master/dart

Detided Kahului tide gauge data came from running code in this notebook:
https://github.com/clawpack/tsunami-examples/blob/master/tohoku2011_hawaii_currents/compare_results.ipynb

