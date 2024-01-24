
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
""" 


import pylab
import glob, os, sys
from importlib import reload
from numpy import loadtxt
from matplotlib import image
import matplotlib

from clawpack.visclaw import gridtools


# for transect:
ylat = 46.9
xmin = -126
xmax = -124


# --------------------------
def setplot(plotdata=None):
# --------------------------
    
    """ 
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of clawpack.visclaw.data.ClawPlotData.
    Output: a modified version of plotdata.
    
    """ 


    from clawpack.visclaw import colormaps, geoplot
    if plotdata is None:
        from clawpack.visclaw.data import ClawPlotData
        plotdata = ClawPlotData()

    plotdata.clearfigures()  # clear any old figures,axes,items dat
    plotdata.format = "binary"


    clim_ocean = 3. #0.2
    clim_coast = 6

    cmax_ocean = clim_ocean
    cmin_ocean = -clim_ocean
    cmax_coast = clim_coast
    cmin_coast = -clim_coast


    # To plot gauge locations on pcolor or contour plot, use this as
    # an afteraxis function:

    def addgauges(current_data):
        from clawpack.visclaw import gaugetools
        gaugetools.plot_gauge_locations(current_data.plotdata, \
             format_string='k.', add_labels=True, fontsize=6)
             #gaugenos=range(1000,1067), format_string='k.', add_labels=True,



    #-----------------------------------------
    # Figure for big area
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Domain', figno=0)
    plotfigure.figsize = (7,8)
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Surface h:m:s after impact'
    plotaxes.scaled = False
    plotaxes.xlimits = [-129,-122]
    plotaxes.ylimits = [43,50]
    plotaxes.aspect_latitude = 46.86  # correct aspect ratio at this latitude
    plotaxes.xticks_kwargs = {'rotation':20}


    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = geoplot.surface_or_depth
    my_cmap = colormaps.make_colormap({-1.0: [0.0,0.0,1.0], \
                                     -0.5: [0.5,0.5,1.0], \
                                      0.0: [1.0,1.0,1.0], \
                                      0.5: [1.0,0.5,0.5], \
                                      1.0: [1.0,0.0,0.0]})
    plotitem.imshow_cmap = my_cmap
    #plotitem.imshow_cmap = geoplot.tsunami_colormap
    plotitem.imshow_cmin = cmin_ocean
    plotitem.imshow_cmax = cmax_ocean
    plotitem.add_colorbar = True
    plotitem.colorbar_shrink = 0.5
    plotitem.colorbar_label = 'meters'
    plotitem.colorbar_kwargs = {'extend':'both'}
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [1]
    plotitem.amr_patchedges_show = [1,1,1,1,1,1,1,1]
    plotitem.amr_patchedges_color = ['k','g','r','b','m','y','g','r']

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = geoplot.land
    plotitem.imshow_cmap = geoplot.land_colors
    plotitem.imshow_cmin = 0.0
    plotitem.imshow_cmax = 100.0
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [0]

    # Add contour lines of bathymetry:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    plotitem.show = False
    plotitem.plot_var = geoplot.topo
    from numpy import arange, linspace
    plotitem.contour_levels = linspace(-6000,0,7)
    plotitem.amr_contour_colors = ['g']  # color on each level
    plotitem.kwargs = {'linestyles':'solid'}
    plotitem.amr_contour_show = [0,0,1,0]  # show contours only on finest level
    plotitem.celledges_show = 0
    plotitem.patchedges_show = 0

    # Add contour lines of topography:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    plotitem.show = False
    plotitem.plot_var = geoplot.topo
    from numpy import arange, linspace
    plotitem.contour_levels = arange(0., 11., 1.)
    plotitem.amr_contour_colors = ['g']  # color on each level
    plotitem.kwargs = {'linestyles':'solid'}
    plotitem.amr_contour_show = [0,0,0,1]  # show contours only on finest level
    plotitem.celledges_show = 0
    plotitem.patchedges_show = 0




    #-----------------------------------------
    # Figure for surface with transect too
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Surface', figno=20)
    plotfigure.figsize = (8,8)

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('pcolor')
    plotaxes.title = 'Surface h:m:s after impact'
    plotaxes.xlimits = [-128,-123]
    plotaxes.ylimits = [45.75,47.75]
    plotaxes.axescmd = 'axes([.15,.5,.8,.45])'
    plotaxes.aspect_latitude = 46.86  # correct aspect ratio at this latitude
    plotaxes.xticks_kwargs = {'rotation':20}

    # Water
    #plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = geoplot.surface_or_depth
    plotitem.imshow_cmap = my_cmap
    #plotitem.imshow_cmap = geoplot.tsunami_colormap
    plotitem.imshow_cmin = cmin_coast
    plotitem.imshow_cmax = cmax_coast
    plotitem.add_colorbar = True
    plotitem.colorbar_shrink = 0.5
    plotitem.colorbar_label = 'meters'
    plotitem.colorbar_extend = 'both'
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [0,0,1,1,1,1,1,1]
    plotitem.amr_patchedges_color = ['k','g','r','b','m','y','g','r']


    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = geoplot.land
    plotitem.imshow_cmap = geoplot.land_colors
    plotitem.imshow_cmin = 0.0
    plotitem.imshow_cmax = 100.0
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [0]


    # add contour lines of bathy if desired:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    #plotitem.show = False
    plotitem.plot_var = geoplot.topo
    plotitem.contour_levels = [-2100, -1000, -400, -100]
    plotitem.amr_contour_colors = ['k']  # color on each level
    plotitem.kwargs = {'linestyles':'solid','linewidths':1}
    plotitem.amr_contour_show = [0,0,1,0,0,0]
    plotitem.celledges_show = 0
    plotitem.patchedges_show = 0

    #-----------------------------------------
    # Figure for transect
    #-----------------------------------------

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('radial slice')
    plotaxes.axescmd = 'axes([.1,.1,.8,.3])'

    def plot_xsec(current_data):
        from pylab import plot,legend,xlabel,sqrt,grid,xlim,ylim,nan,where
        from numpy import cos,pi,linspace,zeros,ones,hstack
        from clawpack.pyclaw import Solution
        pd = current_data.plotdata
        frameno = current_data.frameno
        framesoln = Solution(frameno, path=pd.outdir, file_format=pd.format)
        eps = 1e-3
        #xout = linspace(xmin,xmax,1001)
        xout = hstack((linspace(-126,-124.75,1001), linspace(-124.75,-124,7500)))
        yout = ylat*ones(xout.shape) + eps
        eta_out = gridtools.grid_output_2d(framesoln, -1, xout, yout)
        h_out = gridtools.grid_output_2d(framesoln, 0, xout, yout)
        B_out = eta_out - h_out
        eta_wet = where(h_out>0, eta_out, nan)
        #plot((xout-xmin)*111e3*cos(ylat*pi/180.), eta_out, 
        #     'b', label='along y=%.3f' % ylat)
        plot(xout, eta_wet, 'b', label='along y=%.3f' % ylat)
        plot(xout, B_out, 'g', label='topography')
        legend()
        #xlabel('radial distance')
        xlabel('longitude')
        #xlim(xmin,xmax)
        xlim(-124.5,-124.08)
        ylim(-12,12)
        grid(True)
    plotaxes.afteraxes = plot_xsec


    #-----------------------------------------
    # Figure for zoom
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name="Gray's Harbor", figno=11)
    #plotfigure.show = False
    plotfigure.figsize = (9,7)

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    #plotaxes.cmd = 'subplot(122)'
    plotaxes.title = "Grays Harbor h:m:s after impact"
    plotaxes.scaled = False

    plotaxes.xlimits = [-124.5,-123.8]
    plotaxes.ylimits = [46.75, 47.1]
    plotaxes.aspect_latitude = 46.86  # correct aspect ratio at this latitude
    plotaxes.xticks_kwargs = {'rotation':20}

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = geoplot.surface_or_depth
    my_cmap = colormaps.make_colormap({-1.0: [0.0,0.0,1.0], \
                                      -0.5: [0.5,0.5,1.0], \
                                       0.0: [1.0,1.0,1.0], \
                                       0.5: [1.0,0.5,0.5], \
                                       1.0: [1.0,0.0,0.0]})
    plotitem.imshow_cmap = my_cmap
    plotitem.imshow_cmin = cmin_coast
    plotitem.imshow_cmax = cmax_coast
    plotitem.add_colorbar = True
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.colorbar_shrink = 0.7
    plotitem.colorbar_label = 'meters'
    plotitem.colorbar_kwargs = {'extend':'both'}
    plotitem.amr_patchedges_show = [1,1,1,1,1,1,1,1]
    #plotitem.amr_patchedges_color = ['k','g','r','b','m','y','g','r']
    plotitem.amr_patchedges_color = ['r','b','k','m','c','k','g']

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = geoplot.land
    plotitem.imshow_cmap = geoplot.land_colors
    plotitem.imshow_cmin = 0.0
    plotitem.imshow_cmax = 100.0
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [0]
    plotaxes.xlimits = [-124.5,-123.8]
    plotaxes.ylimits = [46.75, 47.1]


    # add contour lines of bathy if desired:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    plotitem.show = False
    plotitem.plot_var = geoplot.topo
    plotitem.contour_levels = [0.]
    plotitem.amr_contour_colors = ['k']  # color on each level
    plotitem.kwargs = {'linestyles':'solid','linewidths':2}
    plotitem.amr_contour_show = [0,0,0,0,1,0]
    plotitem.celledges_show = 0
    plotitem.patchedges_show = 0


    #-----------------------------------------
    
    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via clawpack.visclaw.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.print_gaugenos = 'all'          # list of gauges to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?
    plotdata.parallel = True

    return plotdata

    
