
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

# MS results:
#outdir2 = '/Users/rjl/como/git/BoussDev/examples/westcoast_dxdy/_output'
outdir2 = None

# SWE results:
#outdir3 = os.path.abspath('_output_SWE')
outdir3 = None

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
    # Figure with transect for paper
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name="Grays Harbor w/transect", figno=111)
    plotfigure.show = True
    plotfigure.kwargs = {'figsize': (8,8)}

    x1trans, x2trans = -124.5,-124.07
    y1trans, y2trans = 46.90, 46.90
    xtrans = linspace(x1trans, x2trans, 1000)
    ytrans = linspace(y1trans, y2trans, 1000)


    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'axes([.15,.5,.8,.45])'
    plotaxes.title = "h:m:s after impact"
    plotaxes.scaled = False

    plotaxes.xlimits = [-124.5,-123.8]
    plotaxes.ylimits = [46.75, 47.1]

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

    def aa(current_data):
        from pylab import ticklabel_format, xticks, yticks, gca, cos, pi, imshow, savefig
        from clawpack.visclaw.plottools import plotbox
        #addgauges(current_data)
        ticklabel_format(useOffset=False)
        xticks(fontsize=10,rotation=20)
        yticks(fontsize=10)
        a = gca()
        a.set_aspect(1./cos(46.86*pi/180.))
    plotaxes.afteraxes = aa


    # Set up axes for transect:
    plotaxes = plotfigure.new_plotaxes('transect')
    plotaxes.axescmd = 'axes([.1,.1,.8,.3])'

    def plot_xsec(current_data):
        from pylab import plot,legend,xlabel,ylabel,sqrt,grid,xlim,ylim,\
                    nan,where,title,fill_between,xticks,yticks,text
        from numpy import cos,pi,linspace,zeros,ones,hstack
        from clawpack.pyclaw import Solution
        pd = current_data.plotdata
        frameno = current_data.frameno
        framesoln = Solution(frameno, path=pd.outdir, file_format=pd.format)
        eta_trans = gridtools.grid_output_2d(framesoln, -1, xtrans, ytrans)
        h_trans = gridtools.grid_output_2d(framesoln, 0, xtrans, ytrans)
        B_trans = eta_trans - h_trans
        eta_wet = where(h_trans>0, eta_trans, nan)
        fill_between(xtrans, -100*ones(xtrans.shape), B_trans, color=[.8,1,.8])
        plot(xtrans, B_trans, 'g', label='topography')
        #plot(xtrans, eta_wet, 'b', label='Surface transect, SGN')
        plot(xtrans, eta_wet, 'b', label='SGN, α=1.153')


        if outdir2 is not None:
            framesoln = Solution(frameno, path=outdir2, file_format=pd.format)
            eta_trans = gridtools.grid_output_2d(framesoln, -1, xtrans, ytrans)
            h_trans = gridtools.grid_output_2d(framesoln, 0, xtrans, ytrans)
            B_trans = eta_trans - h_trans
            eta_wet = where(h_trans>0, eta_trans, nan)
            plot(xtrans, eta_wet, 'r', label='Madsen, B=1/15')

        if outdir3 is not None:
            framesoln = Solution(frameno, path=outdir3, file_format=pd.format)
            eta_trans = gridtools.grid_output_2d(framesoln, -1, xtrans, ytrans)
            h_trans = gridtools.grid_output_2d(framesoln, 0, xtrans, ytrans)
            B_trans = eta_trans - h_trans
            eta_wet = where(h_trans>0, eta_trans, nan)
            plot(xtrans, eta_wet, 'k', lw=0.8, label='SWE')

        #xlabel('distance',fontsize=10)
        ylabel('surface elevation (m)',fontsize=10)
        xlabel('longitude along transect', fontsize=10)
        xlim(x1trans,x2trans)
        ylim(-12,13)
        grid(True)
        title('Along transect at y=%.2f' % y1trans,fontsize=12)
        legend(loc='upper left', fontsize=8)
        xticks(fontsize=10,rotation=20)
        yticks(fontsize=10)
        x1 = -124.19
        x2 = x1 + 2000/(111e3*cos(pi*47/180))
        y1 = -8
        plot([x1,x2],[y1,y1],'k',lw=3)
        text(0.5*(x1+x2), y1+0.5, '2 km', fontsize=10, ha='center',va='bottom')

    plotaxes.afteraxes = plot_xsec


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

    
