# Makefile for Clawpack code in this directory.

# Version for Boussinesq solvers in GeoClaw that DO NOT require PETSc,
# introduced in v5.15.0.  For this version, you must set
#   rundata.bouss_data.bouss_solver = 1
# in setrun.py.   See https://www.clawpack.org/bouss2d.html
#
# Do `make new` if using this Boussinesq version for the first time.

# This version only sets the local files and frequently changed
# options, and then includes the standard makefile pointed to by CLAWMAKE.
CLAWMAKE = $(CLAW)/clawutil/src/Makefile.common

# See the above file for details and a list of make options, or type
#   make .help
# at the unix prompt.


# Adjust these variables if desired:
# ----------------------------------

CLAW_PKG = geoclaw                  # Clawpack package to use


EXE = $(PWD)/xgeoclaw
SETRUN_FILE = setrun.py           # File containing function to make data
OUTDIR = _output                  # Directory for output
SETPLOT_FILE = setplot.py         # File containing function to set plots
PLOTDIR = _plots                  # Directory for plots

# Environment variable FC should be set to fortran compiler, e.g. gfortran

# Compiler flags can be specified here or set as an environment variable
FFLAGS ?= -O  -gno-strict-dwarf -fbounds-check  -fopenmp \
      -std=legacy -ffpe-trap='invalid,overflow,zero'


# ---------------------------------
# package sources for this program:
# ---------------------------------

# BOUSSLIB contains library code for Boussinesq solvers,
# AMRLIB and GEOLIB are standard libraries, defined in case you need to
# exclude some modele or source file from one of these.
BOUSSLIB = $(CLAW)/geoclaw/src/2d/bouss
AMRLIB = $(CLAW)/amrclaw/src/2d
GEOLIB = $(CLAW)/geoclaw/src/2d/shallow

# See this Makefile for the list of library routines used:
include $(BOUSSLIB)/Makefile.bouss

# ---------------------------------------
# package sources specifically to exclude
# (i.e. if a custom replacement source
#  under a different name is provided)
# ---------------------------------------

EXCLUDE_MODULES = \

EXCLUDE_SOURCES = \

# ----------------------------------------
# List of custom sources for this program:
# ----------------------------------------


MODULES = \

SOURCES = \


#-------------------------------------------------------------------
# Include Makefile containing standard definitions and make options:
include $(CLAWMAKE)

.PHONY: topo all check

topo:
	python fetch_topo.py
	python fetch_dtopo.py

all: 
	$(MAKE) topo
	$(MAKE) .plots
	$(MAKE) .htmls
