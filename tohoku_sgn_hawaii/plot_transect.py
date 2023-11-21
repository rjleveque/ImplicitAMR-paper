
from pylab import *
from clawpack.pyclaw import Solution
from clawpack.visclaw import gridtools

event = 'UCSB'

frameno = 6
method = 'linear'  # for interpolation from 2D output

figure(101,figsize=(9,5))
clf()
ax = subplot(111)

# from Popinet (personal comm.): (163.454,31.1458) to (170.631,26.5282)
xout = linspace(163.454, 170.631, 1000)
yout = linspace(31.1458, 26.5282, 1000)


outdir = '_output_sgn_%s' % event.lower()
framesoln = Solution(frameno, path=outdir, file_format='binary')
etaout = gridtools.grid_output_2d(framesoln, -1, xout, yout, method=method)
plot(xout,etaout,'r',linewidth=1.8,label='SGN')


outdir = '_output_swe_%s' % event.lower()
framesoln = Solution(frameno, path=outdir, file_format='binary')
etaout = gridtools.grid_output_2d(framesoln, -1, xout, yout, method=method)
plot(xout,etaout,'b',linewidth=1.8,label='SWE')


#xlim(150,165)
xlim(163,171)
ylim(-3,4)
yticks(range(-2,4,1),fontsize=12)
ylabel('meters',fontsize=13)
grid(True)
#xticks(range(163,171,1),[])
xticks(range(163,172,1),fontsize=12)
xlabel('longitude (degrees)',fontsize=12)
legend(loc='upper right',framealpha=1,fontsize=12)
thours = framesoln.t / 3600.
title('Surface elevation on transect at time %.2f hours, %s source' \
        % (thours,event), fontsize=15)

fname = '%s_Transect3hrs.png' % event
savefig(fname)
print('Created ',fname)
