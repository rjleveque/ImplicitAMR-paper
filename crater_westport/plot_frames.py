"""
Make plots for the paper.
"""

from pylab import *
import setplot

plotdata = setplot.setplot()

#plotdata.printfigs = False
plotdata.printfigs = True

plotdata.outdir = '_output'

figno = 1
plotdata.print_fignos = [figno]
for frameno in [2,3]:
    plotdata.plotframe(frameno)
    fname = 'frame%sfig%s.pdf' % (frameno,figno)
    savefig(fname, bbox_inches='tight')
    print('Created ',fname)

figno = 111
plotdata.print_fignos = [figno]
for frameno in [4,5]:
    plotdata.plotframe(frameno)
    fname = 'frame%sfig%s.pdf' % (frameno,figno)
    savefig(fname, bbox_inches='tight')
    print('Created ',fname)

