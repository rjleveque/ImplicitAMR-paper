# Makefile for Clawpack code in this directory.
# This version only sets the local files and frequently changed
# options, and then includes the standard makefile pointed to by CLAWMAKE.
CLAWMAKE = $(CLAW)/clawutil/src/Makefile.common

# See the above file for details and a list of make options, or type
#   make .help
# at the unix prompt.


# Adjust these variables if desired:
# ----------------------------------

CLAW_PKG = geoclaw                  # Clawpack package to use

# These environment variables need to be set properly, usually in your shell:
# (or set these variable explicitly here in the Makefile)
#PETSC_DIR=/Users/rjl/petsc
#PETSC_ARCH=arch-darwin-c-opt
#PETSC_OPTIONS=-options_file /Users/rjl/petscMPIoptions
# sets the PETSc convergence criteria, etc.
# the settings used for the paper are in  ImplicitAMR-paper/petscMPIoptions

EXE = $(PWD)/xgeoclaw
RUNEXE="${PETSC_DIR}/${PETSC_ARCH}/bin/mpiexec -n 6 "
SETRUN_FILE = setrun.py           # File containing function to make data
OUTDIR = _output                  # Directory for output
SETPLOT_FILE = setplot.py         # File containing function to set plots
PLOTDIR = _plots                  # Directory for plots


# Environment variable FC should be set to fortran compiler, e.g. gfortran

FC = gfortran

# Some compiler flags below are needed for PETSc
PETSC_INCLUDE = $(PETSC_DIR)/include $(PETSC_DIR)/$(PETSC_ARCH)/include         
INCLUDE += $(PETSC_INCLUDE)
PETSC_LFLAGS = $(shell PKG_CONFIG_PATH=$(PETSC_DIR)/$(PETSC_ARCH)/lib/pkgconfig pkg-config --libs-only-L --libs-only-l PETSc)

FFLAGS ?= -O  -gno-strict-dwarf -fbounds-check  -fopenmp \
      -std=legacy -ffpe-trap='invalid,overflow,zero'
FFLAGS += -DHAVE_PETSC -ffree-line-length-none
LFLAGS += $(PETSC_LFLAGS) -fopenmp


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
  ./starting_module.f90 \

SOURCES = \
  ./qinit.f90 \
  ./setprob.f90 \



#-------------------------------------------------------------------
# Include Makefile containing standard definitions and make options:
include $(CLAWMAKE)

# Construct the topography data
.PHONY: topo all
topo:
	python fetch_topo.py

all: 
	$(MAKE) topo
	$(MAKE) .plots
	$(MAKE) .htmls

run:
	$(RUNEXE)
