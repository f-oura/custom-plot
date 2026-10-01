"""Accepted palettes on synthetic data; Python rendering, any compute backend."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize,LogNorm,TwoSlopeNorm
from plotstyle import apply_selected,selected_palette
P=Path(__file__).resolve().parents[1]
d=np.loadtxt(P/'data/density.csv',delimiter=',')
z=d[:,2].reshape(24,24);diff=d[:,3].reshape(24,24)
for preset,size in [('paper',(9,3.7)),('slides',(15,6.1))]:
 apply_selected(preset)
 fig,axes=plt.subplots(1,3,figsize=size,layout='constrained')
 for ax,values,cmap,norm,title in zip(axes,[z,np.ma.masked_where(z<=0,z),diff],[selected_palette(),selected_palette(),selected_palette('signed')],[Normalize(0,60),LogNorm(1,60),TwoSlopeNorm(0,-30,30)],['viridis | linear counts','viridis | log counts','RdBu_r | signed difference']):
  ax.set_facecolor('#eeeeee')
  im=ax.imshow(values,origin='lower',extent=[-3.130434783,3.130434783]*2,cmap=cmap,norm=norm,interpolation='nearest')
  ax.set(xlabel='x [a.u.]',ylabel='y [a.u.]',title=title)
  ax.tick_params(top=True,right=True)
  cb=fig.colorbar(im,ax=ax,shrink=.8,pad=.02)
  cb.solids.set_rasterized(False);cb.solids.set_edgecolor('face')
 fig.suptitle('SYNTHETIC | classic | Python standard | '+preset)
 fig.supxlabel('linear 0–60 · log 1–60; 261 zero bins masked gray · signed −30…+30, centered at 0',fontsize=plt.rcParams['font.size']*.75)
 for suffix in ['pdf','png']:fig.savefig(P/'output'/f'selected-density-{preset}.{suffix}',dpi=180)
 plt.close(fig)
