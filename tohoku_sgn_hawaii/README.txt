Code for the example in Section 4.2 of the paper

    Implicit Adaptive Mesh Refinement for Dispersive Tsunami Propagation
    by Marsha J. Berger and Randall J. LeVeque, submitted, 2023
    (revised March, 2024)
    Preprint: https://arxiv.org/abs/2307.05816
    Git repository: https://github.com/rjleveque/ImplicitAMR-paper

The code in this directory requires Clawpack v5.10.0, which includes
the Boussinesq version of GeoClaw in both 1d and 2d.

It also requires PETSc v3.20 for MPI and OpenMP to work well together,
and various modifications to the Makefile to link to the correct libraries.

See https://www.clawpack.org/bouss2d.html for more details.

See the main README.md file in this repository for more information.

Topo files can be downloaded using fetch_topo.py

The UCSB and Fujii source dtopo files can be downloaded using fetch_dtopo.py
which gets them from:
    https://github.com/rjleveque/tohoku2011-paper1/tree/master/sources

In setrun.py:

Uncomment one of these two lines to select the desired dtopo file:

    dtopo_data.dtopofiles.append([1,1,4,dtopodir+'UCSB3.txydz'])
or
    dtopo_data.dtopofiles.append([1,1,1,dtopodir+'fujii.txydz'])

To run with SWE on all levels:
    rundata.bouss_data.bouss_equations = 0    # 0=SWE, 1=MS, 2=SGN

To run with SGN on all levels:
    rundata.bouss_data.bouss_equations = 2    # 0=SWE, 1=MS, 2=SGN
    rundata.bouss_data.bouss_min_level = 1    # coarsest level to apply bouss
    rundata.bouss_data.bouss_max_level = 10   # finest level to apply bouss

The plotting scripts for figures as in the paper assume the output is moved
to files with names like:
    _output_sgn_ucsb
for the SGN output using the UCSB source.

After running the UCSB source with both SWE and SGN,
Figure 10 in the paper can be created with this script:
    plot_3hrs.py
Figure 11 in the paper can be created with this script:
    plot_transect.py

The gauge comparisons are created with:
    compare_gauges_dart.py
    compare_gauges_kahului.py

Detided DART data included here is from:
https://github.com/rjleveque/tohoku2011-paper1/tree/master/dart

Detided Kahului tide gauge data came from running code in this notebook:
https://github.com/clawpack/tsunami-examples/blob/master/tohoku2011_hawaii_currents/compare_results.ipynb

Version
-------

Nov. 2023: Updated for bouss_2d branch to be merged into GeoClaw.

March 2024: Updated for resbumission of paper
