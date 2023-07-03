from pylab import *
from clawpack.pyclaw.gauges import GaugeSolution


if 0:
    event = 'Fujii'
    outdir1 = './_output_sgn_fujii'
    outdir2 = './_output_swe_fujii'

else:
    event = 'UCSB'
    outdir1 = './_output_sgn_ucsb'
    outdir2 = './_output_swe_ucsb'


gaugeno1 = 5680
gaugeno2 = gaugeno1

gauge1 = GaugeSolution(gauge_id=gaugeno1, path=outdir1)
gauge2 = GaugeSolution(gauge_id=gaugeno2, path=outdir2)

observed = loadtxt('1615680_detided.txt')

fs1 = 15
fs2 = 13

figure(500,figsize=(13,4))
clf()

plot(gauge2.t/60., gauge2.q[-1,:], 'b', label='SWE')
plot(gauge1.t/60., gauge1.q[-1,:], 'r', label='SGN')
plot(observed[:,0]*60., observed[:,1], 'k', label='Obs')
xlabel('Minutes after earthquake',fontsize=fs2)

legend(loc='lower left',framealpha=1,fontsize=fs1)
xlim(430,680)
ylim(-4,3)
grid(True)
ylabel('meters',fontsize=fs2)
xticks(fontsize=fs2)
yticks(fontsize=fs2)

title('Gauge 5680 comparison using %s source' % event,fontsize=fs1)

fname = 'Gauge5680_%s.pdf' %  event
savefig(fname, bbox_inches='tight')
print('Created ',fname)

