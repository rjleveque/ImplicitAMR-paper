
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
matplotlib.rcParams['animation.embed_limit'] = 50

outdir2 = None
#outdir2 = os.path.abspath('../westcoast_OrigUncoupledMadsen/_output')
#outdir2 = os.path.abspath('../westcoastWithSGN/_outputdeepBouss5')
outdir3 = None
#outdir3 = os.path.abspath('../westcoastWithMadsen/_outputWithPetscB15tol9')
#outdir3 = os.path.abspath('../../examples/westcoastWithMadsen/_outputWithPardisoB15')
#outdir3 = os.path.abspath('../westcoastWithSGN/_outputdeepBouss2')

try:
    BoussDev = os.environ['BoussDev']
except:
    print("*** Need to define environment variable BoussDev to path")

new_python_dir = os.path.join(BoussDev, 'new_python')
sys.path.insert(0, new_python_dir)
import gridtools
sys.path = sys.path[1:]  # remove from path



# for transect:
ylat = 46.9
xmin = -126
xmax = -124

outdir_1d = None
if outdir_1d:
    print('Comparing to 1d solution in ', outdir_1d)
    sys.path.insert(0,os.path.abspath(outdir_1d))
    import mapc2p  # from outdir_1d
    reload(mapc2p)  # in case num_cells changed
    sys.path = sys.path[1:]  # remove outdir_1d from path

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

    try:
        tsudata = open(plotdata.outdir+'/geoclaw.data').readlines()
        for line in tsudata:
            if 'sea_level' in line:
                sea_level = float(line.split()[0])
                print("sea_level = ",sea_level)
    except:
        print("Could not read sea_level, setting to 0.")
        sea_level = 0.

    clim_ocean = 10 #0.2
    clim_coast = 6

    cmax_ocean = clim_ocean + sea_level
    cmin_ocean = -clim_ocean + sea_level
    cmax_coast = clim_coast + sea_level
    cmin_coast = -clim_coast + sea_level


    # To plot gauge locations on pcolor or contour plot, use this as
    # an afteraxis function:

    def addgauges(current_data):
        from clawpack.visclaw import gaugetools
        gaugetools.plot_gauge_locations(current_data.plotdata, \
             format_string='k.', add_labels=True, fontsize=6)
             #gaugenos=range(1000,1067), format_string='k.', add_labels=True,

    def timeformat(t):
        from numpy import mod
        hours = int(t/3600.)
        tmin = mod(t,3600.)
        min = int(tmin/60.)
        sec = int(mod(tmin,60.))
        timestr = '%s:%s:%s' % (hours,str(min).zfill(2),str(sec).zfill(2))
        return timestr
        
    def title_hours(current_data):
        from pylab import title
        t = current_data.t
        timestr = timeformat(t)
        title('%s after impact' % timestr,fontsize=20)

    def aframe(current_data):
        from pylab import figure, savefig

        if 0:
            tminutes = int(current_data.t / 60.)

            figure(0)
            fname = 'Pacific%s.png' % tminutes
            savefig(fname)
            print("Saved ",fname)
    
            figure(11)
            fname = 'GraysHarbor%s.png' % tminutes
            savefig(fname)
            print("Saved ",fname)

            figure(12)
            fname = 'Westport%s.png' % tminutes
            savefig(fname)
            print("Saved ",fname)
    
            figure(13)
            fname = 'Ocosta%s.png' % tminutes
            savefig(fname)
            print("Saved ",fname)
    
    #plotdata.afterframe = aframe
    

    def surface_or_depth(current_data):
        """
        Modified from geoplot version to use eta = q[-1,:,:], which
        should work for either num_eqn = 3 or 5.
        
        Return a masked array containing the surface elevation where the topo is
        below sea level or the water depth where the topo is above sea level.
        Mask out dry cells.  Assumes sea level is at topo=0.
        Surface is eta = h+topo, assumed to be output as 4th column of fort.q
        files.
        """
        import numpy

        #drytol = getattr(current_data.user, 'drytol', drytol_default)
        drytol = 1e-3
        q = current_data.q
        h = q[0,:,:]
        eta = q[-1,:,:]
        topo = eta - h

        # With this version, the land is transparent.
        surface_or_depth = numpy.ma.masked_where(h <= drytol,
                                                 numpy.where(topo<0, eta, h))

        try:
            # Use mask covering coarse regions if it's set:
            m = current_data.mask_coarse
            surface_or_depth = numpy.ma.masked_where(m, surface_or_depth)
        except:
            pass

        return surface_or_depth


    #-----------------------------------------
    # Figure for big area
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Pacific', figno=0)
    #plotfigure.kwargs = {'figsize': (9,10)}
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    #plotaxes.cmd = 'subplot(121)'
    plotaxes.title = 'Pacific'
    plotaxes.scaled = False
    # modified for debug:
    plotaxes.xlimits = [-129,-122]
    plotaxes.ylimits = [43,50]

    def aa(current_data):
        from pylab import ticklabel_format, xticks, gca, cos, pi, savefig
        title_hours(current_data)
        ticklabel_format(useOffset=False)
        xticks(rotation=20)
        a = gca()
        a.set_aspect(1./cos(46.86*pi/180.))
        #addgauges(current_data)
    plotaxes.afteraxes = aa

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = surface_or_depth  # local version
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
    # Figure for PDC 2021 abstract
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='PDC', figno=1)
    plotfigure.kwargs = {'figsize': (8,8)}
    plotfigure.show = True 

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Pacific'
    plotaxes.scaled = False
    # modified for debug:
    plotaxes.xlimits = [-128,-123]
    plotaxes.ylimits = [45,49]

    def aaPDC(current_data):
        from pylab import ticklabel_format, xticks, yticks, gca, cos, pi, savefig,\
                xlim, ylim
        from clawpack.visclaw.plottools import plotbox
        frameno = current_data.frameno
        print('frameno = ',frameno)
        title_hours(current_data)
        ticklabel_format(useOffset=False)
        xticks(rotation=20,fontsize=15)
        yticks(fontsize=15)
        a = gca()
        a.set_aspect(1./cos(46.86*pi/180.))
        #if frameno > 0:
        if 0:
            plotbox([-127.3,-123.95,45.8,48.2],
                    {'color':'k','linewidth':0.7})
        #addgauges(current_data)
        xlim(-128,-123)
        ylim(45,49)
        if 0:
            fname = 'IAMRframe%s.png' % str(frameno).zfill(2)
            savefig(fname, bbox_inches='tight', facecolor='w')
            print('Saved ',fname)

    plotaxes.afteraxes = aaPDC

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = surface_or_depth  # local version
    my_cmap = colormaps.make_colormap({-1.0: [0.0,0.0,1.0], \
                                     -0.5: [0.5,0.5,1.0], \
                                      0.0: [1.0,1.0,1.0], \
                                      0.5: [1.0,0.5,0.5], \
                                      1.0: [1.0,0.0,0.0]})
    plotitem.imshow_cmap = my_cmap
    #plotitem.imshow_cmap = geoplot.tsunami_colormap
    #plotitem.imshow_cmin = cmin_ocean
    #plotitem.imshow_cmax = cmax_ocean
    plotitem.imshow_cmin = -3.
    plotitem.imshow_cmax = 3.
    #plotitem.add_colorbar = False
    plotitem.add_colorbar = True 
    plotitem.colorbar_shrink = 0.5
    plotitem.colorbar_label = 'meters'
    plotitem.colorbar_kwargs = {'extend':'both'}
    plotitem.amr_celledges_show = [0]
    plotitem.amr_patchedges_show = [1,1,1,1,1,1,1]
    plotitem.amr_patchedges_color = ['r','b','k','m','c','k','g']
    #plotitem.amr_patchedges_color = ['k','g','r','b','m','y','g','r']
    #plotitem.amr_patchedges_color = ['k']

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



    #-----------------------------------------
    # Figure for surface with transect too
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Surface', figno=20)
    plotfigure.kwargs = {'figsize': (8,10)}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('pcolor')
    plotaxes.title = 'Surface'
    plotaxes.xlimits = [-129,-122]
    plotaxes.ylimits = [45,48]
    plotaxes.afteraxes = aa
    plotaxes.axescmd = 'axes([.15,.5,.7,.45])'

    # Water
    #plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = surface_or_depth  # local version
    plotitem.imshow_cmap = my_cmap
    #plotitem.imshow_cmap = geoplot.tsunami_colormap
    plotitem.imshow_cmin = cmin_ocean
    plotitem.imshow_cmax = cmax_ocean
    plotitem.add_colorbar = True
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
    # Figure for cross section compared to 1d_radial
    #-----------------------------------------

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('radial slice')
    plotaxes.axescmd = 'axes([.1,.1,.8,.3])'
    if outdir_1d:
        plotaxes.title = 'Transect at y = %.3f with 1d solution (black)' % ylat
    else:
        plotaxes.title = 'Transect at y = %.3f' % ylat

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
        xlim(xmin,xmax)
        #xlim(0, 2*111e3*cos(ylat*pi/180.))
        ylim(-25,25)
        grid(True)
        if outdir_1d is not None:
            eta = current_data.q[0,:]  # from 1d_radial solution
            xc = current_data.x
            xp = mapc2p.mapc2p(xc)
            plot(-xp,eta,'k')
    plotaxes.afteraxes = plot_xsec

    if outdir_1d:
        plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
        plotitem.show = (outdir_1d is not None)
        plotitem.outdir = outdir_1d
        plotitem.plot_var = 0
        plotitem.plotstyle = 'k-'
        plotitem.MappedGrid = True
        plotitem.mapc2p = mapc2p.mapc2p


    # FOR MARSHA
    

    
    plotfigure = plotdata.new_plotfigure(name="hu,hv", figno=51)
    plotfigure.kwargs = {'figsize': (11,10)}
    #plotfigure.show = False
    add = .1
    xlimits = [-125.3-add,-124.9+add]
    ylimits = [46.75-add,47.05+add]
    varlimits = [-1500,1500]   # limits to use for colormap and transects

    def aa(current_data):
        from pylab import ticklabel_format, xticks, gca, cos, pi
        #title_hours(current_data)
        ticklabel_format(useOffset=False)
        xticks(rotation=20)
        gca().set_aspect(1./cos(46.9*pi/180.))
        
    my_cmap = colormaps.make_colormap({-1.0: [0.0,0.0,1.0], \
                                     -0.5: [0.5,0.5,1.0], \
                                      0.0: [1.0,1.0,1.0], \
                                      0.5: [1.0,0.5,0.5], \
                                      1.0: [1.0,0.0,0.0]})

                                    
    # Plot axes:
    ax_top_left = 'axes([.1,.55,.35,.35])'
    ax_top_right = 'axes([.55,.55,.35,.35])'
    ax_bottom_left = 'axes([.1,.1,.35,.35])'
    ax_bottom_right = 'axes([.55,.1,.35,.35])'
    
    # TOP LEFT

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = ax_top_left
    plotaxes.title = 'hu'
    plotaxes.scaled = False
    # smaller region
    #plotaxes.xlimits = xlimits
    #plotaxes.ylimits = ylimits
    # same regions as Surface plot
    plotaxes.xlimits = [-129,-122]
    plotaxes.ylimits = [45,48]
    plotaxes.afteraxes = aa

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = 1  # hu  (3 for huc)
    plotitem.imshow_cmap = my_cmap
    plotitem.imshow_cmin = varlimits[0]
    plotitem.imshow_cmax = varlimits[1]
    plotitem.add_colorbar = True
    plotitem.colorbar_shrink = 0.5
    #plotitem.amr_data_show = [1,1,1,1,1,1,0,0]
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

    # Add contour lines of bathymetry:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    plotitem.show = False
    plotitem.plot_var = geoplot.topo
    plotitem.contour_levels = [-2100, -1000, -400, -100]
    plotitem.amr_contour_colors = ['k']  # color on each level
    plotitem.kwargs = {'linestyles':'solid','linewidths':1}
    plotitem.amr_contour_show = [0,0,1,0,0,0]
    plotitem.celledges_show = 0
    plotitem.patchedges_show = 0
    
    # BOTTOM LEFT - transect
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = ax_bottom_left
    
    def plot_xsec(current_data):
        from pylab import plot,legend,xlabel,sqrt,grid,xlim,ylim,xticks
        from numpy import cos,pi,linspace,zeros,ones,hstack
        from clawpack.pyclaw import Solution
        pd = current_data.plotdata
        frameno = current_data.frameno
        framesoln = Solution(frameno, path=pd.outdir, file_format=pd.format)
        xout = linspace(-126, -124, 1000)
        
        y0 = 46.9
        yout = y0 * ones(xout.shape)
        hu_out = gridtools.grid_output_2d(framesoln, 1, xout, yout)
        plot(xout, hu_out, 'r', label='along y = %.2f' % y0)
        
        y0 = 47.
        yout = y0 * ones(xout.shape)
        hu_out = gridtools.grid_output_2d(framesoln, 1, xout, yout)
        plot(xout, hu_out, 'b', label='along y = %.2f' % y0)
        
        legend()
        xticks(rotation=20)
        xlabel('longitude')
        #xlim(xmin,xmax)
        #ylim(varlimits)
        grid(True)
        
    plotaxes.afteraxes = plot_xsec
    plotaxes.title = 'Transect of hu'


    # TOP RIGHT

    # Set up for new axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = ax_top_right
    plotaxes.title = "hv"
    plotaxes.scaled = False
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits
    plotaxes.afteraxes = aa


    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = 2  # hv (4 for hvc)
    plotitem.imshow_cmap = my_cmap
    plotitem.imshow_cmin = varlimits[0]
    plotitem.imshow_cmax = varlimits[1]
    plotitem.add_colorbar = True
    plotitem.colorbar_shrink = 0.5
    #plotitem.amr_data_show = [1,1,1,1,1,0,0,0]
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
    plotitem.show = False
    plotitem.plot_var = geoplot.topo
    plotitem.contour_levels = [-2100, -1000, -400, -100]
    plotitem.amr_contour_colors = ['k']  # color on each level
    plotitem.kwargs = {'linestyles':'solid','linewidths':1}
    plotitem.amr_contour_show = [0,0,1,0,0,0]
    plotitem.celledges_show = 0
    plotitem.patchedges_show = 0
    
    
    # BOTTOM RIGHT - transect
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = ax_bottom_right
    
    def plot_xsec(current_data):
        from pylab import plot,legend,xlabel,sqrt,grid,xlim,ylim,xticks
        from numpy import cos,pi,linspace,zeros,ones,hstack
        from clawpack.pyclaw import Solution
        pd = current_data.plotdata
        frameno = current_data.frameno
        framesoln = Solution(frameno, path=pd.outdir, file_format=pd.format)
        xout = linspace(-126, -124, 1000)
        
        y0 = 46.9
        yout = y0 * ones(xout.shape)
        hv_out = gridtools.grid_output_2d(framesoln, 2, xout, yout)
        plot(xout, hv_out, 'r', label='along y = %.2f' % y0)
        
        y0 = 47.
        yout = y0 * ones(xout.shape)
        hv_out = gridtools.grid_output_2d(framesoln, 2, xout, yout)
        plot(xout, hv_out, 'b', label='along y = %.2f' % y0)
        
        legend()
        xticks(rotation=20)
        xlabel('longitude')
        #xlim(xmin,xmax)
        #ylim(varlimits)
        grid(True)
        
    plotaxes.afteraxes = plot_xsec
    plotaxes.title = 'Transect of hv'


 
    #-----------------------------------------
    # Figure for zoom2
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name="Gray's Harbor", figno=11)
    plotfigure.show = True
    plotfigure.kwargs = {'figsize': (11,8)}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    #plotaxes.cmd = 'subplot(122)'
    plotaxes.title = "Gray's Harbor"
    plotaxes.scaled = False

    plotaxes.xlimits = [-124.5,-123.8]
    plotaxes.ylimits = [46.75, 47.1]

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = surface_or_depth
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
        from pylab import ticklabel_format, xticks, gca, cos, pi, savefig
        #addgauges(current_data)
        title_hours(current_data)
        ticklabel_format(useOffset=False)
        xticks(rotation=20)
        a = gca()
        a.set_aspect(1./cos(46.86*pi/180.))
    plotaxes.afteraxes = aa

    def aa(current_data):
        from pylab import ticklabel_format, xticks, gca, cos, pi, imshow, savefig
        from clawpack.visclaw.plottools import plotbox
        #addgauges(current_data)
        title_hours(current_data)
        ticklabel_format(useOffset=False)
        xticks(rotation=20)
        a = gca()
        a.set_aspect(1./cos(46.86*pi/180.))
        if current_data.t > 40*60.:
            extent = (235.8756, 235.9116, 46.854, 46.8756)
            plotbox(extent)
        #imshow(OcostaGE,extent=extent, alpha=0.5)
        #extent = (235.81, 235.95, 46.85, 46.95)
        #imshow(WestportGE,extent=extent, alpha=0.8)
    plotaxes.afteraxes = aa

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
    # Figure for zoom2 with transect
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name="Harbor w/transect", figno=111)
    plotfigure.show = True
    plotfigure.kwargs = {'figsize': (9,11)}

    x1trans, x2trans = -124.5,-124.07
    #y1trans, y2trans = 46.85, 46.85
    y1trans, y2trans = 46.90, 46.90
    xtrans = linspace(x1trans, x2trans, 1000)
    ytrans = linspace(y1trans, y2trans, 1000)


    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'axes([.15,.5,.8,.45])'
    plotaxes.title = "Harbor w/transect"
    plotaxes.scaled = False

    plotaxes.xlimits = [-124.5,-123.8]
    plotaxes.ylimits = [46.75, 47.1]

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = surface_or_depth
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
        title_hours(current_data)
        ticklabel_format(useOffset=False)
        xticks(fontsize=14,rotation=20)
        yticks(fontsize=14)
        a = gca()
        a.set_aspect(1./cos(46.86*pi/180.))
        if current_data.t > 40*60.:
            extent = (235.8756, 235.9116, 46.854, 46.8756)
            plotbox(extent)
        #imshow(OcostaGE,extent=extent, alpha=0.5)
        #extent = (235.81, 235.95, 46.85, 46.95)
        #imshow(WestportGE,extent=extent, alpha=0.8)
    plotaxes.afteraxes = aa

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

        # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('transect')
    plotaxes.axescmd = 'axes([.1,.1,.8,.3])'

    def plot_xsec(current_data):
        from pylab import plot,legend,xlabel,ylabel,sqrt,grid,xlim,ylim,nan,where,title
        from numpy import cos,pi,linspace,zeros,ones,hstack
        from clawpack.pyclaw import Solution
        pd = current_data.plotdata
        frameno = current_data.frameno
        framesoln = Solution(frameno, path=pd.outdir, file_format=pd.format)
        eta_trans = gridtools.grid_output_2d(framesoln, -1, xtrans, ytrans)
        h_trans = gridtools.grid_output_2d(framesoln, 0, xtrans, ytrans)
        B_trans = eta_trans - h_trans
        eta_wet = where(h_trans>0, eta_trans, nan)
        plot(xtrans, B_trans, 'g', label='topography')
        #plot(xtrans, eta_wet, 'b', label='Surface transect, SGN')
        plot(xtrans, eta_wet, 'b', label='SGN, α=1.153')

        if outdir2 is not None:
            framesoln = Solution(frameno, path=outdir2, file_format=pd.format)
            eta_trans = gridtools.grid_output_2d(framesoln, -1, xtrans, ytrans)
            h_trans = gridtools.grid_output_2d(framesoln, 0, xtrans, ytrans)
            B_trans = eta_trans - h_trans
            eta_wet = where(h_trans>0, eta_trans, nan)
            #plot(xtrans, eta_wet, 'm', label='Surface transect, orig MS')
            plot(xtrans, eta_wet, 'm', label='SGN, deepBouss 5')
            #plot(xtrans, B_trans, 'g', label='topography')

        if outdir3 is not None:
            framesoln = Solution(frameno, path=outdir3, file_format=pd.format)
            eta_trans = gridtools.grid_output_2d(framesoln, -1, xtrans, ytrans)
            h_trans = gridtools.grid_output_2d(framesoln, 0, xtrans, ytrans)
            B_trans = eta_trans - h_trans
            eta_wet = where(h_trans>0, eta_trans, nan)
            plot(xtrans, eta_wet, 'r', label='Madsen, B=1/15')
            #plot(xtrans, B_trans, 'g', label='topography')
            #plot(xtrans, eta_wet, 'r', label='SGN, deepBouss 2')

        xlabel('distance',fontsize=20)
        ylabel('height (m)',fontsize=20)
        #xlabel('longitude along transect')
        xlim(x1trans,x2trans)
        ylim(-12,13)
        grid(True)
        title('Along transect at y=%.2f' % y1trans,fontsize=20)
        legend(fontsize=15)
        matplotlib.pyplot.xticks(fontsize=14,rotation=20)
        matplotlib.pyplot.yticks(fontsize=14)

    plotaxes.afteraxes = plot_xsec




    #-----------------------------------------
    # Figure for corrections
    #-----------------------------------------

    plotfigure = plotdata.new_plotfigure(name="huc,hvc", figno=50)
    plotfigure.kwargs = {'figsize': (11,8)}
    #plotfigure.show = False
    xlimits = [-125.3,-124.9]
    ylimits = [46.75,47.05]

    # Plot axes:
    ax_top_left = 'axes([.1,.55,.35,.35])'
    ax_top_right = 'axes([.55,.55,.35,.35])'
    ax_bottom_left = 'axes([.1,.1,.35,.35])'
    ax_bottom_right = 'axes([.55,.1,.35,.35])'

    def aa(current_data):
        from pylab import ticklabel_format, xticks, gca, cos, pi
        #title_hours(current_data)
        ticklabel_format(useOffset=False)
        xticks(rotation=20)
        gca().set_aspect(1./cos(46.9*pi/180.))
        
    my_cmap = colormaps.make_colormap({-1.0: [0.0,0.0,1.0], \
                                     -0.5: [0.5,0.5,1.0], \
                                      0.0: [1.0,1.0,1.0], \
                                      0.5: [1.0,0.5,0.5], \
                                      1.0: [1.0,0.0,0.0]})

                                    
    # Plot on left:
    
    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = ax_top_left
    plotaxes.title = 'huc'
    plotaxes.scaled = False

    # smaller region
    add = .1
    xlimits = [-125.3-add,-124.9+add]
    ylimits = [46.75-add,47.05+add]

    #plotaxes.xlimits = xlimits
    #plotaxes.ylimits = ylimits

    # same region as surface
    plotaxes.xlimits = [-129,-122]
    plotaxes.ylimits = [45,48]
    plotaxes.afteraxes = aa


    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = 3
    plotitem.imshow_cmap = my_cmap
    plotitem.imshow_cmin = -0.1
    plotitem.imshow_cmax = 0.1
    plotitem.add_colorbar = True
    plotitem.colorbar_shrink = 0.5
    #plotitem.amr_data_show = [1,1,1,1,1,1,0,0]
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [0,0,0,1,1,1,1,1]
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
    #plotitem.show = False
    plotitem.plot_var = geoplot.topo
    plotitem.contour_levels = [-2100, -1000, -400, -100]
    plotitem.amr_contour_colors = ['k']  # color on each level
    plotitem.kwargs = {'linestyles':'solid','linewidths':1}
    plotitem.amr_contour_show = [0,0,1,0,0,0]
    plotitem.celledges_show = 0
    plotitem.patchedges_show = 0


    # BOTTOM LEFT - transect

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = ax_bottom_left

    def plot_xsec(current_data):
        from pylab import plot,legend,xlabel,sqrt,grid,xlim,ylim,xticks
        from numpy import cos,pi,linspace,zeros,ones,hstack
        from clawpack.pyclaw import Solution
        pd = current_data.plotdata
        frameno = current_data.frameno
        framesoln = Solution(frameno, path=pd.outdir, file_format=pd.format)
        xout = linspace(-126, -124, 1000)

        y0 = 46.9
        yout = y0 * ones(xout.shape)
        hu_out = gridtools.grid_output_2d(framesoln, 3, xout, yout)
        plot(xout, hu_out, 'r', label='along y = %.2f' % y0)

        y0 = 47.
        yout = y0 * ones(xout.shape)
        hu_out = gridtools.grid_output_2d(framesoln, 3, xout, yout)
        plot(xout, hu_out, 'b', label='along y = %.2f' % y0)

        legend()
        xticks(rotation=20)
        xlabel('longitude')
        #xlim(xmin,xmax)
        #ylim(varlimits)
        grid(True)

    plotaxes.afteraxes = plot_xsec
    plotaxes.title = 'Transect of huc'



    # Plot on right

    # Set up for new axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = ax_top_right
    plotaxes.title = "hvc"
    plotaxes.scaled = False

    add = .1
    xlimits = [-125.3-add,-124.9+add]
    ylimits = [46.75-add,47.05+add]

    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits
    #plotaxes.xlimits = [-124.6,-123.8]
    #plotaxes.ylimits = [46.75, 47.1]
    plotaxes.afteraxes = aa


    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = 4 #surface_or_depth
    my_cmap = colormaps.make_colormap({-1.0: [0.0,0.0,1.0], \
                                      -0.5: [0.5,0.5,1.0], \
                                       0.0: [1.0,1.0,1.0], \
                                       0.5: [1.0,0.5,0.5], \
                                       1.0: [1.0,0.0,0.0]})
    plotitem.imshow_cmap = my_cmap
    plotitem.imshow_cmin = -0.1
    plotitem.imshow_cmax = 0.1
    plotitem.add_colorbar = True
    plotitem.colorbar_shrink = 0.5
    #plotitem.amr_data_show = [1,1,1,1,1,0,0,0]
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [0,0,0,1,1,1,1,1]
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

    # BOTTOM RIGHT - transect
   
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = ax_bottom_right
   
    def plot_xsec(current_data):
        from pylab import plot,legend,xlabel,sqrt,grid,xlim,ylim,xticks
        from numpy import cos,pi,linspace,zeros,ones,hstack
        from clawpack.pyclaw import Solution
        pd = current_data.plotdata
        frameno = current_data.frameno
        framesoln = Solution(frameno, path=pd.outdir, file_format=pd.format)
        xout = linspace(-126, -124, 1000)
    
        y0 = 46.9
        yout = y0 * ones(xout.shape)
        hv_out = gridtools.grid_output_2d(framesoln, 4, xout, yout)
        plot(xout, hv_out, 'r', label='along y = %.2f' % y0)
    
        y0 = 47.
        yout = y0 * ones(xout.shape)
        hv_out = gridtools.grid_output_2d(framesoln, 4, xout, yout)
        plot(xout, hv_out, 'b', label='along y = %.2f' % y0)
    
        legend()
        xticks(rotation=20)
        xlabel('longitude')
        #xlim(xmin,xmax)
        #ylim(varlimits)
        grid(True)

    plotaxes.afteraxes = plot_xsec
    plotaxes.title = 'Transect of hvc'


    #-----------------------------------------
    # Figure for zoom
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Washington', figno=10)
    plotfigure.show = False

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Washington'
    plotaxes.scaled = False
    plotaxes.afteraxes = aa

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = surface_or_depth
    my_cmap = colormaps.make_colormap({-1.0: [0.0,0.0,1.0], \
                                      -0.5: [0.5,0.5,1.0], \
                                       0.0: [1.0,1.0,1.0], \
                                       0.5: [1.0,0.5,0.5], \
                                       1.0: [1.0,0.0,0.0]})
    plotitem.imshow_cmap = my_cmap
    plotitem.imshow_cmin = cmin_ocean
    plotitem.imshow_cmax = cmax_ocean
    plotitem.add_colorbar = True
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [1]

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = geoplot.land
    plotitem.imshow_cmap = geoplot.land_colors
    plotitem.imshow_cmin = 0.0
    plotitem.imshow_cmax = 100.0
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [1]
    #plotaxes.xlimits = [235,236.5] 
    #plotaxes.ylimits = [46,49]
    plotaxes.afteraxes = aa

    
 
    #-----------------------------------------
    # Figure for zoom3
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Approaching', figno=12)
    plotfigure.show = True 
    plotfigure.kwargs = {'figsize': (7,8)}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Offshore'
    plotaxes.scaled = False

    #plotaxes.bg_image = WestportGE
    #plotaxes.bg_extent = [-124.165,-124.025,46.84,46.92]
    #my_cmap_trans = colormaps.make_colormap({0.0: [1.0,1.0,1.0,0.], \
    #                                   0.1: [1.0,0.5,0.5,1.], \
    #                                   1.0: [1.0,0.0,0.0,1.]})

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    #plotitem.show = False
    plotitem.plot_var = surface_or_depth
    plotitem.imshow_cmap = my_cmap
    plotitem.imshow_cmin = cmin_coast
    plotitem.imshow_cmax = cmax_coast
    plotitem.add_colorbar = True
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [1,1,1,1,1,1,1,1]
    plotitem.amr_patchedges_color = ['k','g','r','b','m','y','g','r']

    plotaxes.xlimits =   [-124.6,-123.8]
    plotaxes.ylimits = [46.7,47.4]

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = geoplot.land
    plotitem.imshow_cmap = geoplot.land_colors
    plotitem.imshow_cmin = 0.0
    plotitem.imshow_cmax = 10.0
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [0]

    def aa(current_data):
        from pylab import ticklabel_format, xticks, gca, cos, pi, imshow, savefig
        from clawpack.visclaw.plottools import plotbox
        #addgauges(current_data)
        title_hours(current_data)
        ticklabel_format(useOffset=False)
        xticks(rotation=20)
        #extent = (235.8756, 235.9116, 46.854, 46.8756)
        #plotbox(extent)
        if current_data.t == 0.:
            extent = [-124.165,-124.025,46.84,46.92]
            #imshow(WestportGE,extent=extent, alpha=1.0)
        a = gca()
        a.set_aspect(1./cos(46.86*pi/180.))

    plotaxes.afteraxes = aa

    # add contour lines of bathy if desired:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    plotitem.show = False
    plotitem.plot_var = geoplot.topo
    plotitem.contour_levels = [0.0]
    plotitem.amr_contour_colors = ['k']  # color on each level
    plotitem.kwargs = {'linestyles':'solid','linewidths':2}
    plotitem.amr_contour_show = [0,0,0,0,1,0]
    plotitem.celledges_show = 0
    plotitem.patchedges_show = 0

    #-----------------------------------------
    # Figure for zoom4
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Ocosta', figno=13)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize': (12,8)}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Ocosta'
    plotaxes.scaled = False

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    #plotitem.show=False
    plotitem.plot_var = geoplot.depth
    #plotitem.plot_var = surface_or_depth
    my_cmap = colormaps.make_colormap({0.0: [1.0,1.0,1.0], \
                                       0.5: [1.0,0.8,0.0], \
                                       1.0: [1.0,0.0,0.0]})
    plotitem.imshow_cmap = my_cmap
    plotitem.imshow_cmin = 0.
    plotitem.imshow_cmax = 3.
    plotitem.add_colorbar = True
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [1]

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    #plotitem.show=False
    plotitem.plot_var = geoplot.land
    plotitem.imshow_cmap = geoplot.land_colors
    plotitem.imshow_cmin = 0.0
    plotitem.imshow_cmax = 20.0
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [1]

    #plotaxes.xlimits = [235.88, 235.905] 
    #plotaxes.ylimits = [46.855, 46.87]
    plotaxes.xlimits = [235.88-360, 235.935-360] 
    plotaxes.ylimits = [46.845, 46.875]
    def aa(current_data):
        from pylab import ticklabel_format, xticks, gca, cos, pi, imshow, savefig
        addgauges(current_data)
        title_hours(current_data)
        ticklabel_format(useOffset=False)
        xticks(rotation=20)
        extent = (235.8756, 235.9116, 46.854, 46.8756)
        #imshow(OcostaGE,extent=extent, alpha=0.5)
        a = gca()
        a.set_aspect(1./cos(46.86*pi/180.))
        #extent = (235.81, 235.95, 46.85, 46.95)
        #imshow(WestportGE,extent=extent, alpha=0.8)
    plotaxes.afteraxes = aa

    # add contour lines of bathy if desired:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    #plotitem.show = False
    plotitem.plot_var = geoplot.topo
    plotitem.contour_levels = [0.]
    plotitem.amr_contour_colors = ['k']  # color on each level
    plotitem.kwargs = {'linestyles':'solid','linewidths':2}
    plotitem.amr_contour_show = [0,0,0,0,1,0]
    plotitem.celledges_show = 0
    plotitem.patchedges_show = 0

 
 
    #-----------------------------------------
    # Figure for zoom4 speed
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Ocosta speed', figno=14)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize': (12,8)}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Ocosta'
    plotaxes.scaled = False

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    #plotitem.show=False
    def speed(current_data):
        from numpy import sqrt,where
        c = current_data
        q = current_data.q
        h = q[0,:,:]
        hu = q[1,:,:]
        hv = q[2,:,:]
        u = where(h>0.01, hu/h, 0.)
        v = where(h>0.01, hv/h, 0.)
        speed = sqrt(u**2 + v**2)
        if 0:
            if c.level==1:
                import pdb; pdb.set_trace()
            if c.level == 6:
                print("+++ xlower, ylower, dx,dy: ",c.xlower,c.xupper,c.dx,c.dy)
                print("+++ q.shape: ",c.q.shape)
                print("+++ minspeed, maxspeed: ", speed.min(), speed.max())
                if (c.xlower>235.915) and (c.xlower<235.916) and \
                   (c.level==6):    #(c.ylower>46.861) and (c.ylower<46.862):
                    import pdb; pdb.set_trace()
        return speed

    plotitem.plot_var = speed
    #plotitem.plot_var = surface_or_depth
    my_cmap = colormaps.make_colormap({0.0: [0.0,0.0,1.0], \
                                       0.5: [1.0,1.0,1.0], \
                                       1.0: [1.0,0.0,0.0]})
    plotitem.imshow_cmap = my_cmap
    plotitem.imshow_cmin = -3.
    plotitem.imshow_cmax = 3.
    plotitem.add_colorbar = True
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [1]

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    #plotitem.show=False
    plotitem.plot_var = geoplot.land
    plotitem.imshow_cmap = geoplot.land_colors
    plotitem.imshow_cmin = 0.0
    plotitem.imshow_cmax = 20.0
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [1]

    #plotaxes.xlimits = [235.88, 235.905] 
    #plotaxes.ylimits = [46.855, 46.87]
    #plotaxes.xlimits = [235.88, 235.935] 
    #plotaxes.ylimits = [46.845, 46.875]
    def aa(current_data):
        from pylab import ticklabel_format, xticks, gca, cos, pi, imshow, savefig
        addgauges(current_data)
        title_hours(current_data)
        ticklabel_format(useOffset=False)
        xticks(rotation=20)
        extent = (235.8756, 235.9116, 46.854, 46.8756)
        #imshow(OcostaGE,extent=extent, alpha=0.5)
        a = gca()
        a.set_aspect(1./cos(46.86*pi/180.))
        #extent = (235.81, 235.95, 46.85, 46.95)
        #imshow(WestportGE,extent=extent, alpha=0.8)
    #plotaxes.afteraxes = aa

    # add contour lines of bathy if desired:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    #plotitem.show = False
    plotitem.plot_var = geoplot.topo
    plotitem.contour_levels = [0.]
    plotitem.amr_contour_colors = ['k']  # color on each level
    plotitem.kwargs = {'linestyles':'solid','linewidths':2}
    plotitem.amr_contour_show = [0,0,0,0,1,0]
    plotitem.celledges_show = 0
    plotitem.patchedges_show = 0


    #-----------------------------------------
    # Plot along transect:
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='x-section', figno=15)
    # doesn't show up this way, need to use 1d_from_2d_data?
    #plotfigure.show = False
    #plotfigure.kwargs = {'figsize': (6,8)}

    # Set up for axes in this figure:
    #plotaxes = plotfigure.new_plotaxes()
    #plotaxes.title = 'Transect'
    #plotitem = plotaxes.new_plotitem(plot_type='2d_contour')


    def eta(q):
        eta = where(q[0,:,:]>0, q[3,:,:], nan)
        return eta

    def B(q):
        return q[3,:,:]-q[0,:,:]


    def plot_xsec(current_data):
        from pylab import plot, title, subplot, xlim, ylim, linspace, ones
        from pylab import figure, ticklabel_format, fill_between, clf, draw
        from pylab import annotate, savefig
        #from clawpack.visclaw import gridtools
        from clawpack.pyclaw import Solution
        pd = current_data.plotdata
        frameno = current_data.frameno
        framesoln = Solution(frameno, path=pd.outdir, file_format=pd.format)

        #ylat = 46.95
        ylat = 46.9  #46.908
        xb = [-134, -124.25, -124.0]
        mx = [4000,4000]
        xlimits = [-129, -124]
        figure(15,figsize=(6,8))
        clf()
        for k in range(len(mx)):
            xout = linspace(xb[k],xb[k+1],mx[k])
            yout = ylat*ones(xout.shape)
    
            eta = gridtools.grid_output(framesoln, 3, xout, yout)
            topo = gridtools.grid_output(framesoln, B, xout, yout)
            xlimits = [-129, -124]
            topo_color = [.8,1,.8]
            water_color = [.5,.5,1]
    
            subplot(311)
            fill_between(xout, eta, topo, color=water_color)
            fill_between(xout, topo, -10000, color=topo_color)
            plot(xout, eta, 'b')
            plot(xout, topo, 'g')
            xlim(xlimits)
            ylim(-40,70)
            timestr = timeformat(framesoln.t)
            annotate('Ocean scale',xy=(.05,.85),xycoords='axes fraction')
            title('Transect along latitude %6.3f at time %s' % (ylat,timestr))
    
            subplot(312)
            fill_between(xout, eta, topo, color=water_color)
            fill_between(xout, topo, -10000, color=topo_color)
            plot(xout, eta, 'b')
            plot(xout, topo, 'g')
            xlim(xlimits)
            ylim(-3000,150)
    
            subplot(313)
            fill_between(xout, eta, topo, color=water_color)
            fill_between(xout, topo, -10000, color=topo_color)
            plot(xout, eta, 'b')
            plot(xout, topo, 'g')
            annotate('Zoom on Westport',xy=(.05,.85),xycoords='axes fraction')
            ticklabel_format(useOffset=False)
            ylim(-15,15)
            xlim(-124.2,-124.06)
        draw()
        if 0:
            fname = os.path.join(plotdata.plotdir, \
                    'Transect_%s.png' % str(frameno).zfill(4))
            savefig(fname)
            print("Created %s" % fname)

    #plotdata.afterframe = plot_xsec
 
 

    #-----------------------------------------
    # Figures for gauges
    #-----------------------------------------

    def fix_gauge(current_data):
        from pylab import plot, legend, xticks, floor, yticks,\
            xlabel,savefig,xlim,where,nan,ones,grid
        t = current_data.t
        gaugeno = current_data.gaugeno
        q = current_data.q

        h = q[0,:]
        h0 = q[0,0] * ones(h.shape)
        level = current_data.gaugesoln.level
        #B = current_data.gaugesoln.aux[0,:]
        dh_refine = 0.
        for j in range(1,len(h0)):
            if level[j] != level[j-1]:
                dh_refine = dh_refine + h[j] - h[j-1]  #B[j-1]-B[j] 
            h0[j] = h0[j] + dh_refine

        ddepth = q[0,:] - h0[:]
        #plot(t, ddepth, 'b-')

        n = int(floor(t.max()/1800.) + 2)
        xticks([1800*i for i in range(n)],[str(i/2.) for i in range(n)],\
          fontsize=15)
        yticks(fontsize=15)
        xlabel("Hours")
        grid(True)
        #save_gauge(current_data)


    plotfigure = plotdata.new_plotfigure(name='gauge eta,ddepth', figno=301, \
                    type='each_gauge')
    #plotfigure.clf_each_gauge = False
    plotfigure.kwargs = {'figsize':(12,5)}


    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = [0.5*3600, 1.5*3600]
    plotaxes.ylimits = [-12,12]
    plotaxes.title = 'Surface elevation '

    #def ddepth(current_data):
    #    q = current_data.q
    #    return q[0,:] - q[0,0]
        
    # Plot ddepth as blue curve:
    #plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    #plotitem.plot_var = ddepth
    #plotitem.plotstyle = 'b-'

    # plot eta as red curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 3
    plotitem.plotstyle = 'r-'
    plotaxes.afteraxes = fix_gauge


    #-----------------------------------------
    
    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via clawpack.visclaw.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    #plotdata.print_framenos = range(0,201,20)     # list of frames to print
    #plotdata.print_framenos = [31,91,151,211,271,331,391]     # list of frames to print
    #plotdata.print_framenos = [91,151,211,271]     # list of frames to print
    #plotdata.print_framenos = [0]     # list of frames to print
    plotdata.print_fignos = 'all'            # list of figures to print
    #plotdata.print_fignos = [1,111]            # list of figures to print
    plotdata.print_gaugenos = 'all'          # list of gauges to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?
    plotdata.parallel = True

    return plotdata

    
