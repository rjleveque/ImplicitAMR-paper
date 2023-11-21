
"""
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.

"""

from clawpack.visclaw import geoplot

#--------------------------
def setplot(plotdata=None):
#--------------------------

    """
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of clawpack.visclaw.data.ClawPlotData.
    Output: a modified version of plotdata.

    """


    from clawpack.visclaw import colormaps
    from numpy import linspace
    
    if plotdata is None:
        from clawpack.visclaw.data import ClawPlotData
        plotdata = ClawPlotData()
    

    plotdata.clearfigures()  # clear any old figures,axes,items data

    plotdata.format = 'binary'

    # To plot gauge locations on pcolor or contour plot, use this as
    # an afteraxis function:

    def addgauges(current_data):
        from clawpack.visclaw import gaugetools
        gaugetools.plot_gauge_locations(current_data.plotdata, \
             gaugenos=[21413,21418], format_string='ko', add_labels=True)

    def fixup(current_data):
        import pylab
        addgauges(current_data)
        t = current_data.t
        t = t / 3600.  # hours
        pylab.title('Surface at %4.2f hours' % t, fontsize=20)
        #pylab.xticks(fontsize=15)
        #pylab.yticks(fontsize=15)


    #-----------------------------------------
    # Figure for imshow plot
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Domain', figno=1)

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('imshow')
    plotaxes.title = 'Surface'
    plotaxes.scaled = True

    plotaxes.afteraxes = fixup

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    # plotitem.plot_var = geoplot.surface
    plotitem.plot_var = geoplot.surface_or_depth
    plotitem.imshow_cmap = geoplot.tsunami_colormap
    plotitem.imshow_cmin = -0.5
    plotitem.imshow_cmax = 0.5
    plotitem.add_colorbar = True
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.patchedges_show = 0
    #plotitem.amr_patchedges_show = [1,1,1,0,0]  # only coarse levels

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = geoplot.land
    plotitem.imshow_cmap = geoplot.land_colors
    plotitem.imshow_cmin = 0.0
    plotitem.imshow_cmax = 100.0
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.patchedges_show = 0
    #plotitem.amr_patchedges_show = [1,1,1,0,0]  # only coarse levels
    plotaxes.xlimits = 'auto'
    plotaxes.ylimits = 'auto'

    # add contour lines of bathy if desired:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    plotitem.show = False
    plotitem.plot_var = geoplot.topo
    plotitem.contour_levels = linspace(-2000,0,5)
    plotitem.amr_contour_colors = ['y']  # color on each level
    plotitem.kwargs = {'linestyles':'solid','linewidths':2}
    plotitem.amr_contour_show = [1,0,0]
    plotitem.celledges_show = 0
    plotitem.patchedges_show = 0


    #-----------------------------------------
    # Figure for Bouss paper
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Source', figno=11)
    plotfigure.kwargs = {'figsize':(9,7), 'facecolor':'w'}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('imshow')
    plotaxes.title = 'Surface'
    plotaxes.scaled = True

    # 2 hours:
    #plotaxes.xlimits = [132,165]
    #plotaxes.ylimits = [20,50]

    # 3 hours:
    plotaxes.xlimits = [132,175]
    plotaxes.ylimits = [15,45]
    
    def fixup(current_data):
        import pylab
        addgauges(current_data)
        t = current_data.t
        t = t / 3600.  # hours
        pylab.title('Surface at %4.2f hours' % t, fontsize=15)
        pylab.xticks(fontsize=12)
        pylab.yticks(fontsize=12)
        pylab.xlabel('longitude',fontsize=12)
        pylab.ylabel('latitude',fontsize=12)

    plotaxes.afteraxes = fixup

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    # plotitem.plot_var = geoplot.surface
    plotitem.plot_var = geoplot.surface_or_depth
    plotitem.imshow_cmap = geoplot.tsunami_colormap
    plotitem.imshow_cmin = -1.
    plotitem.imshow_cmax = 1.
    plotitem.add_colorbar = True
    plotitem.colorbar_kwargs = {'extend':'both', 'shrink':0.7}
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.patchedges_show = 0
    #plotitem.amr_patchedges_show = [1,1,1,0,0]  # only coarse levels

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = geoplot.land
    plotitem.imshow_cmap = geoplot.land_colors
    plotitem.imshow_cmin = 0.0
    plotitem.imshow_cmax = 100.0
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.patchedges_show = 0
    #plotitem.amr_patchedges_show = [1,1,1,0,0]  # only coarse levels



    #-----------------------------------------
    # Figure for zoom plot
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Maui', figno=2)
    plotfigure.show = False

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('imshow')
    plotaxes.title = 'Surface'
    plotaxes.scaled = True

    plotaxes.afteraxes = fixup

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    # plotitem.plot_var = geoplot.surface
    plotitem.plot_var = geoplot.surface_or_depth
    plotitem.imshow_cmap = geoplot.tsunami_colormap
    plotitem.imshow_cmin = -1.
    plotitem.imshow_cmax = 1.
    plotitem.add_colorbar = True
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.patchedges_show = 0

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = geoplot.land
    plotitem.imshow_cmap = geoplot.land_colors
    plotitem.imshow_cmin = 0.0
    plotitem.imshow_cmax = 100.0
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.patchedges_show = 0
    plotaxes.xlimits = [203.2, 204.1]
    plotaxes.ylimits = [20.4, 21.3]

    # add contour lines of bathy if desired:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    plotitem.show = False
    plotitem.plot_var = geoplot.topo
    plotitem.contour_levels = linspace(-2000,0,5)
    plotitem.amr_contour_colors = ['y']  # color on each level
    plotitem.kwargs = {'linestyles':'solid','linewidths':2}
    plotitem.amr_contour_show = [1,0,0]
    plotitem.celledges_show = 0
    plotitem.patchedges_show = 0


    #-----------------------------------------
    # Figure for zoom plot
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Kahului Harbor', figno=3)
    plotfigure.show = False

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('imshow')
    plotaxes.title = 'Surface'
    plotaxes.scaled = True

    plotaxes.afteraxes = fixup

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    # plotitem.plot_var = geoplot.surface
    plotitem.plot_var = geoplot.surface_or_depth
    plotitem.imshow_cmap = geoplot.tsunami_colormap
    plotitem.imshow_cmin = -0.2
    plotitem.imshow_cmax = 0.2
    plotitem.add_colorbar = True
    plotitem.celledges_show = 0
    plotitem.patchedges_show = 0

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = geoplot.land
    plotitem.imshow_cmap = geoplot.land_colors
    plotitem.imshow_cmin = 0.0
    plotitem.imshow_cmax = 10.0
    plotitem.add_colorbar = False
    plotitem.celledges_show = 0
    plotitem.patchedges_show = 0
    plotaxes.xlimits = [203.48, 203.57]
    plotaxes.ylimits = [20.88, 20.94]

    # add contour lines of bathy if desired:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    plotitem.show = False
    plotitem.plot_var = geoplot.topo
    #plotitem.contour_levels = linspace(-2000,0,5)
    plotitem.contour_levels = linspace(0,8,9)
    plotitem.amr_contour_colors = ['y']  # color on each level
    plotitem.kwargs = {'linestyles':'solid','linewidths':2}
    plotitem.amr_contour_show = [0,0,0,0,0,1]
    plotitem.celledges_show = 0
    plotitem.patchedges_show = 0


    #-----------------------------------------
    # Figures for gauges
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Surface', figno=300, \
                    type='each_gauge')
    plotfigure.clf_each_gauge = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    #plotaxes.axescmd = 'subplot(2,1,1)'
    plotaxes.title = 'Surface'

    # Plot surface as blue curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = -1
    plotitem.plotstyle = 'b-'
    plotitem.kwargs = {'linewidth':2}


    #-----------------------------------------
    # Plots of timing (CPU and wall time):

    def make_timing_plots(plotdata):
        from clawpack.visclaw import plot_timing_stats
        import os,sys
        try:
            timing_plotdir = plotdata.plotdir + '/_timing_figures'
            os.system('mkdir -p %s' % timing_plotdir)
            # adjust units for plots based on problem:
            units = {'comptime':'seconds', 'simtime':'hours', 
                     'cell':'millions'}
            plot_timing_stats.make_plots(outdir=plotdata.outdir, 
                                          make_pngs=True,
                                          plotdir=timing_plotdir, 
                                          units=units)
        except:
            print('*** Error making timing plots')

    otherfigure = plotdata.new_otherfigure(name='timing plots',
                    fname='_timing_figures/timing.html')
    otherfigure.makefig = make_timing_plots



    #-----------------------------------------

    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via clawpack.visclaw.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'         # list of frames to print
    plotdata.print_gaugenos = 'all'          # list of gauges to print
    plotdata.print_fignos = [1,2,3,11,300,301]           # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = False                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?
    plotdata.parallel = True

    return plotdata
