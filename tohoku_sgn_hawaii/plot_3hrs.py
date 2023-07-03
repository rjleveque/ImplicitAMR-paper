"""
Plot frames at t = 3 hours for the paper,
Assumes the code has been run for both cases to create
output with both SWE and SGN equations, using the UCSB source.
"""

from pylab import *
import setplot_hawaii

plotdata = setplot_hawaii.setplot()

plotdata.printfigs = False
plotdata.print_fignos = [11]

plotdata.outdir = '_output_swe_ucsb'
plotdata.plotframe(6)
fname = 'UCSB_SWE_3hrs.pdf'
savefig(fname, bbox_inches='tight')
print('Created ',fname)

plotdata.outdir = '_output_sgn_ucsb'
plotdata.plotframe(6)
fname = 'UCSB_SGN_3hrs.pdf'
savefig(fname, bbox_inches='tight')
print('Created ',fname)


