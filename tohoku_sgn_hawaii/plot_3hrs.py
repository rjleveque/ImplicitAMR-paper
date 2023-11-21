"""
Plot frames at t = 3 hours for the paper,
Assumes the code has been run for both cases to create
output with both SWE and SGN equations, using the UCSB source and is in
directories _output_swe_ucsb and _output_sgn_ucsb.
"""

from pylab import *
import setplot

plotdata = setplot.setplot()

plotdata.printfigs = False
plotdata.print_fignos = [11]  # plot specified in setplot.py for figno=11

event = 'UCSB'

#-------- SWE --------------

plotdata.outdir = '_output_swe_%s' % event.lower()
plotdata.plotframe(6)
title('SWE at 3 hours, %s source' % event, fontsize=15)

# Add transect line:
plot([163.454,170.631], [31.1458,26.5282], color='k', linewidth=1.0)


fname = '%s_SWE_3hrs.png' % event
savefig(fname, bbox_inches='tight')
print('Created ',fname)


#-------- SGN --------------

plotdata.outdir = '_output_sgn_%s' % event.lower()
plotdata.plotframe(6)
title('SGN at 3 hours, %s source' % event, fontsize=15)

# Add transect line:
plot([163.454,170.631], [31.1458,26.5282], color='k', linewidth=1.0)

fname = '%s_SGN_3hrs.png' % event
savefig(fname, bbox_inches='tight')
print('Created ',fname)
