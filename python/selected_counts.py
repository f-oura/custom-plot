"""User-selected classic/option4 1D style, fixed synthetic data."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from plotstyle import apply_selected,semantic
P=Path(__file__).resolve().parents[1]
x,o,r,b,m=np.loadtxt(P/'data/counts.csv',delimiter=',').T
for preset,size in [('paper',(6.8,5.2)),('slides',(10,7.6))]:
 taste,_=apply_selected(preset)
 fig,(up,dn)=plt.subplots(2,1,figsize=size,sharex=True,gridspec_kw={'height_ratios':[3,1]},layout='constrained')
 semantic(up,x,o,'observed',taste,errors=np.sqrt(o))
 semantic(up,x,r,'reference',taste,errors=np.sqrt(r))
 semantic(up,x,m,'model',taste)
 up.set(ylabel='Counts / 0.2 GeV',ylim=(0,210),title='SYNTHETIC | counts and fixed-shape model')
 up.legend(loc='upper right',frameon=False)
 valid=(o>0)&(r>0);ratio=o[valid]/r[valid]
 dn.errorbar(x[valid],ratio,yerr=ratio*np.sqrt(1/o[valid]+1/r[valid]),fmt='o',linestyle='none',color=taste['colors'][0],ms=max(4.,plt.rcParams['font.size']*.35))
 dn.axhline(1,color='#666666',ls='--',lw=.8)
 dn.set(xlim=(0,8),ylim=(0,5),xlabel='Mass [GeV]',ylabel='Observed / reference')
 for ax in [up,dn]:ax.tick_params(top=True,right=True)
 fig.supxlabel('Synthetic demo · statistical errors only · low-count bins are illustrative',fontsize=plt.rcParams['font.size']*.9)
 for suffix in ['pdf','png']:fig.savefig(P/'output'/f'selected-counts-{preset}.{suffix}',dpi=180)
 plt.close(fig)
