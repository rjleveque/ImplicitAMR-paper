"""
Module to set up run time parameters for Clawpack.

The values set in the function setrun are then written out to data files
that will be read in by the Fortran code.

"""

import os
import numpy as np

try:
    CLAW = os.environ['CLAW']
except:
    raise Exception("*** Must first set CLAW enviornment variable")



#------------------------------
def setrun(claw_pkg='geoclaw'):
#------------------------------

    """
    Define the parameters used for running Clawpack.

    INPUT:
        claw_pkg expected to be "geoclaw" for this setrun.

    OUTPUT:
        rundata - object of class ClawRunData

    """

    from clawpack.clawutil import data

    assert claw_pkg.lower() == 'geoclaw',  "Expected claw_pkg = 'geoclaw'"

    num_dim = 2
    rundata = data.ClawRunData(claw_pkg, num_dim)


    #------------------------------------------------------------------
    # Problem-specific parameters to be written to setprob.data:
    #------------------------------------------------------------------
    
    #probdata = rundata.new_UserData(name='probdata',fname='setprob.data')


    #------------------------------------------------------------------
    # GeoClaw specific parameters:
    #------------------------------------------------------------------

    rundata = setgeo(rundata)   # Defined below

    #------------------------------------------------------------------
    # Standard Clawpack parameters to be written to claw.data:
    #   (or to amr2ez.data for AMR)
    #------------------------------------------------------------------

    clawdata = rundata.clawdata  # initialized when rundata instantiated


    # Set single grid parameters first.
    # See below for AMR parameters.


    # ---------------
    # Spatial domain:
    # ---------------

    # Number of space dimensions:
    clawdata.num_dim = num_dim

    # Lower and upper edge of computational domain:
    clawdata.lower[0] = 132.0          # xlower
    clawdata.upper[0] = 210.0          # xupper
    clawdata.lower[1] = 9.0          # ylower
    clawdata.upper[1] = 53.0          # yupper

    # Number of grid cells:
    clawdata.num_cells[0] = 39      # mx
    clawdata.num_cells[1] = 22      # my
    
    # ---------------
    # Size of system:
    # ---------------

    # Number of equations in the system:
    clawdata.num_eqn = 5

    # Number of auxiliary variables in the aux array (initialized in setaux)
    clawdata.num_aux = 3

    # Index of aux array corresponding to capacity function, if there is one:
    clawdata.capa_index = 2

    
    
    # -------------
    # Initial time:
    # -------------

    clawdata.t0 = 0.0


    # Restart from checkpoint file of a previous run?
    # If restarting, t0 above should be from original run, and the
    # restart_file 'fort.chkNNNNN' specified below should be in 
    # the OUTDIR indicated in Makefile.

    clawdata.restart = False              # True to restart from prior results
    clawdata.restart_file = 'fort.chk00096'  # File to use for restart data

    # -------------
    # Output times:
    #--------------

    # Specify at what times the results should be written to fort.q files.
    # Note that the time integration stops after the final output time.
    # The solution at initial time t0 is always written in addition.

    clawdata.output_style = 1

    if clawdata.output_style==1:
        # Output nout frames at equally spaced times up to tfinal:
        clawdata.num_output_times = 24
        clawdata.tfinal = 12*3600.
        clawdata.output_t0 = True  # output at initial (or restart) time?

    elif clawdata.output_style == 2:
        # Specify a list of output times.
        clawdata.output_times = [1.0, 900.]

    elif clawdata.output_style == 3:
        # Output every iout timesteps with a total of ntot time steps:
        clawdata.output_step_interval = 1
        clawdata.total_steps = 4
        clawdata.output_t0 = True
        

    clawdata.output_format = 'binary'      # 'ascii' or 'binary' 

    clawdata.output_q_components = 'all'   # need all
    clawdata.output_aux_components = 'none'  # eta=h+B is in q
    clawdata.output_aux_onlyonce = False    # output aux arrays each frame



    # ---------------------------------------------------
    # Verbosity of messages to screen during integration:
    # ---------------------------------------------------

    # The current t, dt, and cfl will be printed every time step
    # at AMR levels <= verbosity.  Set verbosity = 0 for no printing.
    #   (E.g. verbosity == 2 means print only on levels 1 and 2.)
    clawdata.verbosity = 1



    # --------------
    # Time stepping:
    # --------------

    # if dt_variable==1: variable time steps used based on cfl_desired,
    # if dt_variable==0: fixed time steps dt = dt_initial will always be used.
    clawdata.dt_variable = True

    # Initial time step for variable dt.
    # If dt_variable==0 then dt=dt_initial for all steps:
    clawdata.dt_initial = 0.016

    # Max time step to be allowed if variable dt used:
    clawdata.dt_max = 1e+99

    # Desired Courant number if variable dt used, and max to allow without
    # retaking step with a smaller dt:
    clawdata.cfl_desired = 0.75
    clawdata.cfl_max = 1.0

    # Maximum number of time steps to allow between output times:
    clawdata.steps_max = 5000




    # ------------------
    # Method to be used:
    # ------------------

    # Order of accuracy:  1 => Godunov,  2 => Lax-Wendroff plus limiters
    clawdata.order = 2
    
    # Use dimensional splitting? (not yet available for AMR)
    clawdata.dimensional_split = 'unsplit'
    
    # For unsplit method, transverse_waves can be 
    #  0 or 'none'      ==> donor cell (only normal solver used)
    #  1 or 'increment' ==> corner transport of waves
    #  2 or 'all'       ==> corner transport of 2nd order corrections too
    clawdata.transverse_waves = 2

    # Number of waves in the Riemann solution:
    clawdata.num_waves = 3
    
    # List of limiters to use for each wave family:  
    # Required:  len(limiter) == num_waves
    # Some options:
    #   0 or 'none'     ==> no limiter (Lax-Wendroff)
    #   1 or 'minmod'   ==> minmod
    #   2 or 'superbee' ==> superbee
    #   3 or 'mc'       ==> MC limiter
    #   4 or 'vanleer'  ==> van Leer
    clawdata.limiter = ['mc', 'mc', 'mc']

    clawdata.use_fwaves = True    # True ==> use f-wave version of algorithms
    
    # Source terms splitting:
    #   src_split == 0 or 'none'    ==> no source term (src routine never called)
    #   src_split == 1 or 'godunov' ==> Godunov (1st order) splitting used, 
    #   src_split == 2 or 'strang'  ==> Strang (2nd order) splitting used,  not recommended.
    clawdata.source_split = 'godunov'


    # --------------------
    # Boundary conditions:
    # --------------------

    # Number of ghost cells (usually 2)
    clawdata.num_ghost = 2

    # Choice of BCs at xlower and xupper:
    #   0 => user specified (must modify bcN.f to use this option)
    #   1 => extrapolation (non-reflecting outflow)
    #   2 => periodic (must specify this at both boundaries)
    #   3 => solid wall for systems where q(2) is normal velocity

    clawdata.bc_lower[0] = 'extrap'
    clawdata.bc_upper[0] = 'extrap'

    clawdata.bc_lower[1] = 'extrap'
    clawdata.bc_upper[1] = 'extrap'



    # --------------
    # Checkpointing:
    # --------------

    # Specify when checkpoint files should be created that can be
    # used to restart a computation.

    clawdata.checkpt_style = -2

    if clawdata.checkpt_style == 0:
        # Do not checkpoint at all
        pass

    elif np.abs(clawdata.checkpt_style) == 1:
        # Checkpoint only at tfinal.
        pass

    elif np.abs(clawdata.checkpt_style) == 2:
        # Specify a list of checkpoint times.  
        clawdata.checkpt_times = np.arange(1,12)*3600.

    elif np.abs(clawdata.checkpt_style) == 3:
        # Checkpoint every checkpt_interval timesteps (on Level 1)
        # and at the final time.
        clawdata.checkpt_interval = 5


    # ---------------
    # AMR parameters:
    # ---------------
    amrdata = rundata.amrdata

    # maximum size of patches in each direction (matters in parallel):
    amrdata.max1d = 60

    # max number of refinement levels:
    amrdata.amr_levels_max = 6   # Set to 6 for full resolution

    # List of refinement ratios at each level (length at least amr_level_max-1)
    # 2 degree, 24', 4', 1', 10", 1/3"
    amrdata.refinement_ratios_x = [5, 6, 4, 6, 30]
    amrdata.refinement_ratios_y = [5, 6, 4, 6, 30]
    amrdata.refinement_ratios_t = [5, 6, 4, 6, 30]

    # Specify type of each aux variable in amrdata.auxtype.
    # This must be a list of length maux, each element of which is one of:
    #   'center',  'capacity', 'xleft', or 'yleft'  (see documentation).

    amrdata.aux_type = ['center','capacity','yleft']


    # Flag using refinement routine flag2refine rather than richardson error
    amrdata.flag_richardson = False    # use Richardson?
    amrdata.flag_richardson_tol = 0.002  # Richardson tolerance
    amrdata.flag2refine = True

    # steps to take on each level L between regriddings of level L+1:
    amrdata.regrid_interval = 3

    # width of buffer zone around flagged points:
    # (typically the same as regrid_interval so waves don't escape):
    amrdata.regrid_buffer_width  = 2

    # clustering alg. cutoff for (# flagged pts) / (total # of cells refined)
    # (closer to 1.0 => more small grids may be needed to cover flagged cells)
    amrdata.clustering_cutoff = 0.700000

    # print info about each regridding up to this level:
    amrdata.verbosity_regrid = 0  

    #  ----- For developers ----- 
    # Toggle debugging print statements:
    amrdata.dprint = False      # print domain flags
    amrdata.eprint = False      # print err est flags
    amrdata.edebug = False      # even more err est flags
    amrdata.gprint = False      # grid bisection/clustering
    amrdata.nprint = False      # proper nesting output
    amrdata.pprint = False      # proj. of tagged points
    amrdata.rprint = False      # print regridding summary
    amrdata.sprint = False      # space/memory output
    amrdata.tprint = False       # time step reporting each level
    amrdata.uprint = False      # update/upbnd reporting
    
    # More AMR parameters can be set -- see the defaults in pyclaw/data.py

    # ---------------
    # Regions:
    # ---------------
    regions = rundata.regiondata.regions
    # to specify regions of refinement append lines of the form
    #  [minlevel,maxlevel,t1,t2,x1,x2,y1,y2]

    inf = 1e9

    # Region 0 : Global region.  This assures a maximum refinement in any 
    # regions not covered by other regions listed below.
    
    regions.append([1, 2, 0., inf, 0, 360, -90, 90])

    # Region 1 : (from the dtopo file, below).  
    # Time interval taken from dtopo file : [0,1]
    regions.append([4, 4, 0, 2, 140., 146., 35., 41.])

    # Region 2 : Large region encompassing lower 3/4 of domain.
    # Time interval :  (0,18000)
    regions.append([1, 3, 0., 5.*3600., 132., 220., 5., 40.])

    # Region 3 : Region including all Hawaiian Islands.
    # Time interval  (18000,28800)
    regions.append([1, 3, 5.*3600.,  8.*3600., 180., 220., 5., 40.])

    # Region 4 : Region including Molekai and Maui. 
    # Time interval : (23400.0, inf)
    regions.append([4, 4, 6.5*3600., inf, 202.5,204,20.4,21.4])

    # Region 5 : Strip including north shore of Maui.
    # Time interval :  (25200, inf)
    regions.append([5, 5, 7.*3600., inf, 203.0, 203.7, 20.88333, 21.])

    # Region 6 :  Includes port at Kailua.
    # Time interval :  (26100.0, inf)
    regions.append([6, 6,  7.25*3600., inf, 203.52,    203.537, 20.89,   20.905])

    # tracking main wave:
    regions.append([1, 4, 0., 3.*3600., 132., 175., 25., 40.])
    regions.append([1, 4, 3.*3600., 6*3600., 165., 200., 20., 32.])
    regions.append([1, 4, 6.*3600., 7*3600., 185., 205., 17., 30.])


    # ---------------
    # Gauges:
    # ---------------
    gauges = rundata.gaugedata.gauges = []
    # for gauges append lines of the form  [gaugeno, x, y, t1, t2]
    gauges.append([21401, 152.583, 42.617,  1800., 1.e10])   
    gauges.append([21413, 152.1167, 30.5153,  1800., 1.e10])   
    gauges.append([21414, 178.281, 48.938,  1800., 1.e10])
    gauges.append([21415, 171.849, 50.183,  1800., 1.e10])
    #gauges.append([21416, 163.505, 48.052,  1800., 1.e10])
    gauges.append([21418, 148.694, 38.711,     0., 1.e10])   
    gauges.append([21419, 155.736, 44.455,  1800., 1.e10])  
    #gauges.append([51407, 203.484, 19.642, 22000., 1.e10])
    gauges.append([52402, 154.116, 11.883, 10000., 1.e10])    
    #gauges.append([1, 145.5, 37.6, 0., 1.e10]) 
    gauges.append([2, 145.5, 37.4, 0., 1.e10])
    gauges.append([3, 165, 29.5, 0., 1.e10])    
    
    # Hawaii current velocity:
    gauges.append([1123, 203.52825, 20.9021333, 7.0*3600., 1.e9]) #Kahului
    # more accurate coordinates from Yong Wei at PMEL:
    gauges.append([5680, 203.530944, 20.895, 7.0*3600., 1.e9]) #TG Kahului



    # To use Boussinesq solver, add bouss_data parameters here
    # Also make sure to use the correct Makefile pointing to bouss version
    from clawpack.geoclaw.data import BoussData
    rundata.add_data(BoussData(),'bouss_data')
    
    rundata.bouss_data.bouss_equations = 2    # 0=SWE, 1=MS, 2=SGN
    rundata.bouss_data.bouss_min_level = 1    # coarsest level to apply bouss
    rundata.bouss_data.bouss_max_level = 10   # finest level to apply bouss
    rundata.bouss_data.bouss_min_depth = 20.  # depth to switch to SWE
    rundata.bouss_data.bouss_solver = 3       # 1=GMRES, 2=Pardiso, 3=PETSc
    rundata.bouss_data.bouss_tstart = 0.      # time to switch from SWE



    return rundata
    # end of function setrun
    # ----------------------


#-------------------
def setgeo(rundata):
#-------------------
    """
    Set GeoClaw specific runtime parameters.
    For documentation see ....
    """

    try:
        geo_data = rundata.geo_data
    except:
        print("*** Error, this rundata has no geo_data attribute")
        raise AttributeError("Missing geo_data attribute")
       
    # == Physics ==
    geo_data.gravity = 9.81
    geo_data.coordinate_system = 2
    geo_data.earth_radius = 6367.5e3

    # == Forcing Options
    geo_data.coriolis_forcing = False

    # == Algorithm and Initial Conditions ==
    geo_data.sea_level = 0.0
    geo_data.dry_tolerance = 1.e-3
    geo_data.friction_forcing = True
    geo_data.manning_coefficient =.025
    geo_data.friction_depth = 1e6

    # Refinement settings
    refinement_data = rundata.refinement_data
    refinement_data.variable_dt_refinement_ratios = True
    refinement_data.wave_tolerance = 0.1

    # == settopo.data values ==
    topo_data = rundata.topo_data
    # for topography, append lines of the form
    #    [topotype, fname]
    

    topodir = './'
    topo_data.topofiles.append([3, 1, 1, 0.0, 1e10, \
                os.path.join(topodir,'etopo1min130E210E0N60N.asc')])
    # hawaii_6s topofile not needed, results very similar either way
    #topofiles.append([3, 1, 1, 0.0, 1e10, os.path.join(topodir,'hawaii_6s.txt')])
    topo_data.topofiles.append([3, 1, 1, 0., 1.e10, \
                os.path.join(topodir,'kahului_1s.txt')])                          

    # == setdtopo.data values ==
    dtopo_data = rundata.dtopo_data
    # for moving topography, append lines of the form :   (<= 1 allowed for now!)
    #   [topotype, fname]
    
    #dtopodir = '/Users/rjl/git/tohoku2011-paper1/sources/'
    dtopodir = './'
    dtopo_data.dtopofiles.append([1,1,4,dtopodir+'UCSB3.txydz'])
    #dtopo_data.dtopofiles.append([1,1,1,dtopodir+'fujii.txydz'])

    dtopo_data.dt_max_dtopo = 0.2


    # == setqinit.data values ==
    rundata.qinit_data.qinit_type = 0
    rundata.qinit_data.qinitfiles = []
    # for qinit perturbations, append lines of the form: (<= 1 allowed for now!)
    #   [fname]

    # == fgout grids ==
    # new style as of v5.9.0 (old rundata.fixed_grid_data is deprecated)
    # set rundata.fgout_data.fgout_grids to be a 
    # list of objects of class clawpack.geoclaw.fgout_tools.FGoutGrid:
    #rundata.fgout_data.fgout_grids = []

    return rundata
    # end of function setgeo
    # ----------------------



if __name__ == '__main__':
    # Set up run-time parameters and write all data files.
    import sys
    from clawpack.geoclaw import kmltools

    rundata = setrun(*sys.argv[1:])
    rundata.write()

    kmltools.make_input_data_kmls(rundata)
