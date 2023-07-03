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


fs1 = 15
fs2 = 13

for k,gaugeno in enumerate([21413, 21418]):
    gaugeno1 = gaugeno
    gaugeno2 = gaugeno

    gauge1 = GaugeSolution(gauge_id=gaugeno1, path=outdir1)
    gauge2 = GaugeSolution(gauge_id=gaugeno2, path=outdir2)

    #fname = '/Users/rjl/git/tohoku2011-paper1/dart/%s_notide.txt' % gaugeno1
    fname = '%s_notide.txt' % gaugeno1
    observed = loadtxt(fname)

    figure(502+k,figsize=(13,4))
    clf()

    if 0:
        plot(gauge2.t/3600., gauge2.q[-1,:], 'b', label='SWE')
        plot(gauge1.t/3600., gauge1.q[-1,:], 'r', label='SGN')
        plot(observed[:,0]/3600., observed[:,1], 'k', label='Obs',linewidth=0.8)
        xlim(0,3)
        xlabel('Hours after earthquake',fontsize=fs2)
    if 1:
        plot(gauge2.t/60., gauge2.q[-1,:], 'b', label='SWE')
        plot(gauge1.t/60., gauge1.q[-1,:], 'r', label='SGN')
        plot(observed[:,0]/60., observed[:,1], 'k.-', label='Obs',linewidth=0.8)
        if gaugeno1 == 21413: 
            xlim(60,180)
            if event == 'Fujii':
                ylim(-1,1.5)
            else:
                ylim(-1,1.5)
        if gaugeno1 == 21418: 
            xlim(20,90)
            if event == 'Fujii':
                ylim(-1,2)
            else:
                ylim(-2,2)
        xlabel('Minutes after earthquake',fontsize=fs2)



    legend(loc='upper right',fontsize=fs1)
    xticks(fontsize=fs2)
    yticks(fontsize=fs2)
    grid(True)
    ylabel('meters',fontsize=fs2)

    title('Gauge %s comparison using %s source' % (gaugeno1,event),
          fontsize=fs1)
    fname = 'DART%s_%s.pdf' %  (gaugeno1,event)
    savefig(fname, bbox_inches='tight')
    print('Created ',fname)
