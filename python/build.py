"""Reproducible SYNTHETIC comparison. Run from repository root."""
import json, pathlib, subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, TwoSlopeNorm
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image
from plotstyle import P, C, apply, semantic, outside_legend

def make_data():
    rng=np.random.default_rng(4281); x=np.arange(.1,8,.2)
    bg=18*np.exp(-x/4)+4; signal=130*np.exp(-.5*((x-3)/.38)**2)
    mu=bg+signal; a=rng.poisson(mu); b=rng.poisson(bg+signal*.86)
    design=np.c_[np.exp(-x/4),np.ones_like(x),np.exp(-.5*((x-3)/.38)**2)]
    weights=1/np.sqrt(np.maximum(a,1)); coeff=np.linalg.lstsq(design*weights[:,None],a*weights,rcond=None)[0]
    mu=design@coeff
    (P/'qa/fit.json').write_text(json.dumps({'method':'weighted linear least squares; fixed peak mean 3 and width .38','parameters':coeff.tolist(),'chi2':float(np.sum((a-mu)**2/np.maximum(a,1))),'ndof':len(x)-3},indent=2))
    np.savetxt(P/'data/counts.csv',np.c_[x,a,b,bg,mu],delimiter=',',fmt='%.10g')
    q=np.linspace(-3,3,24); X,Y=np.meshgrid(q,q)
    z=rng.poisson(45*np.exp(-(X**2+Y**2)/1.6)); z[0:3,0:3]=0
    d=z-45*np.exp(-(X**2+(Y-.3)**2)/1.6)
    np.savetxt(P/'data/density.csv',np.c_[X.ravel(),Y.ravel(),z.ravel(),d.ravel()],delimiter=',',fmt='%.10g')
    corr=np.array([[1,.65,-.3,.05],[.65,1,-.15,.25],[-.3,-.15,1,.4],[.05,.25,.4,1]])
    np.savetxt(P/'data/correlation.csv',corr,delimiter=',')
    return x,a,b,bg,mu,X,Y,z,d,corr

def gallery(taste,preset,data):
    t,p=apply(taste,preset); x,a,b,bg,mu,X,Y,z,d,corr=data
    fig,axs=plt.subplots(3,3,figsize=p['gallery_inches'],layout='constrained')
    fig.set_layout_engine('constrained',rect=C['geometry']['mpl_layout_rect'])
    fig.suptitle(f'{taste} | {preset} | Matplotlib | SYNTHETIC',fontsize=p['font_pt']+3)
    ax=axs[0,0]; semantic(ax,x,a,'observed',t,np.sqrt(a)); ax.set(title='Counts / statistical errors',ylabel='Counts / 0.2 GeV'); outside_legend(ax); ax.set_ylim(0,210)
    ax=axs[0,1]; semantic(ax,x,a,'observed',t,np.sqrt(a)); ax.set(yscale='log',ylim=(.5,800),title='Log Y: zero bins excluded explicitly',ylabel='Counts / 0.2 GeV')
    ax=axs[0,2]; semantic(ax,x,a,'observed',t,np.sqrt(a)); semantic(ax,x,b,'reference',t,np.sqrt(b)); ax.set(title='Same counts normalization',ylabel='Counts / 0.2 GeV'); outside_legend(ax); ax.set_ylim(0,210)
    ax=axs[1,0]; valid=b>0; ratio=np.divide(a,b,out=np.full_like(x,np.nan),where=valid); err=ratio*np.sqrt(1/np.maximum(a,1)+1/np.maximum(b,1)); semantic(ax,x[valid],ratio[valid],'observed',t,err[valid]); ax.axhline(1,color='gray',ls='--'); ax.set(title='Ratio: observed / reference',ylim=(0,5),ylabel='Ratio'); ax.set_title('Ratio: independent Poisson errors')
    ax=axs[1,1]; sub=a-bg; semantic(ax,x,sub,'observed',t,np.sqrt(a+bg)); semantic(ax,x,mu-bg,'model',t); ax.axhline(0,color='gray'); ax.set(title='Background subtraction',ylabel='Counts / 0.2 GeV'); outside_legend(ax); ax.set_ylim(-20,210)
    ax=axs[1,2]; pull=(a-mu)/np.sqrt(mu); semantic(ax,x,pull,'observed',t); ax.axhspan(-1,1,color='#dddddd'); ax.axhline(0,color='gray'); ax.set(title='Fit residual: fixed peak shape',ylabel='(data-model) / sqrt(model)',ylim=(-3.5,3.5))
    ax=axs[2,0]; im=ax.pcolormesh(X,Y,np.ma.masked_where(z==0,z),norm=LogNorm(vmin=1,vmax=60),cmap=t['sequential'],shading='auto'); fig.colorbar(im,ax=ax,label='Counts'); ax.set(title=f'Log density: {np.sum(z==0)} zeros masked',ylabel='y [a.u.]',xlabel='x [a.u.]'); ax.set_facecolor('#eeeeee')
    ax=axs[2,1]; im=ax.pcolormesh(X,Y,d,norm=TwoSlopeNorm(vmin=-30,vcenter=0,vmax=30),cmap=t['diverging'],shading='auto'); fig.colorbar(im,ax=ax,label='Signed difference'); ax.set(title='Signed difference: center = 0',ylabel='y [a.u.]',xlabel='x [a.u.]')
    ax=axs[2,2]; im=ax.imshow(corr,origin='lower',vmin=-1,vmax=1,cmap=t['diverging']); fig.colorbar(im,ax=ax,label='Correlation'); ax.set(title='Correlation: identical scale',xticks=range(4),yticks=range(4));
    for i in range(4):
      for j in range(4): ax.text(j,i,f'{corr[i,j]:.2f}',ha='center',va='center',color='white' if abs(corr[i,j])>.55 else 'black',fontsize='small')
    for ax in axs[:2].ravel(): ax.set_xlabel('Mass [GeV]'); ax.set_xlim(0,8)
    fig.text(.5,.013,'SYNTHETIC | visible range 0-8 GeV | UF/OF = 0 by construction | stat only; no systematic band | φ, −1, nσ',ha='center',fontsize=p['font_pt']*.75)
    fig.savefig(P/'output'/f'mpl-{taste}-{preset}.png',dpi=150)
    fig.savefig(P/'output'/f'mpl-{taste}-{preset}.pdf')
    plt.close(fig)

def extra(data):
    x,a,b,bg,mu,X,Y,z,d,corr=data; t,p=apply('classic','paper')
    fig,(ax,r)=plt.subplots(2,1,sharex=True,figsize=(6.8,5.2),gridspec_kw={'height_ratios':[3,1]},layout='constrained')
    semantic(ax,x,a,'observed',t,np.sqrt(a)); semantic(ax,x,b,'reference',t,np.sqrt(b)); ax.set_ylabel('Counts / 0.2 GeV'); ax.set_title('SYNTHETIC | overlay + ratio'); outside_legend(ax); ax.set_ylim(0,210)
    v=b>0; semantic(r,x[v],a[v]/b[v],'observed',t,(a[v]/b[v])*np.sqrt(1/np.maximum(a[v],1)+1/b[v])); r.axhline(1,color='gray',ls='--'); r.set(xlabel='Mass [GeV]',ylabel='Ratio',ylim=(0,5),xlim=(0,8))
    fig.savefig(P/'output/overlay-ratio-paper.pdf'); fig.savefig(P/'output/overlay-ratio-paper.png',dpi=180); plt.close(fig)
    fig,axs=plt.subplots(1,2,sharex=True,sharey=True,figsize=(6.8,3.1),layout='constrained')
    for ax,vals,key in zip(axs,[a,b],['observed','reference']): semantic(ax,x,vals,key,t,np.sqrt(vals)); ax.set(xlabel='Mass [GeV]',title=key,ylim=(0,210));
    axs[0].set_ylabel('Counts / 0.2 GeV'); fig.suptitle('SYNTHETIC | shared axes'); fig.savefig(P/'output/shared-axes-paper.png',dpi=180); plt.close(fig)
    fig,ax=plt.subplots(figsize=(3.4,3.2),layout='constrained'); im=ax.pcolormesh(X,Y,z,vmin=0,vmax=60,cmap='viridis',shading='auto'); fig.colorbar(im,ax=ax,label='Counts'); ax.set(title='SYNTHETIC | linear density',xlabel='x [a.u.]',ylabel='y [a.u.]'); fig.savefig(P/'output/linear-density-paper.png',dpi=180); plt.close(fig)

def single(data):
    x,a,*_=data
    for preset in C['presets']:
      t,p=apply('classic',preset)
      fig,ax=plt.subplots(figsize=p['single_inches'],layout='constrained')
      semantic(ax,x,a,'observed',t,np.sqrt(a));ax.set(xlabel='Mass [GeV]',ylabel='Counts / 0.2 GeV',title='SYNTHETIC | counts',xlim=(0,8),ylim=(0,210));ax.legend(loc='upper right',frameon=False)
      fig.savefig(P/'output'/f'mpl-single-{preset}.pdf');fig.savefig(P/'output'/f'mpl-single-{preset}.png',dpi=180);plt.close(fig)

def comparison():
    plt.rcParams.update({'font.family':'DejaVu Sans','pdf.fonttype':42})
    with PdfPages(P/'output/comparison.pdf') as pdf:
      for preset in C['presets']:
       for taste in C['tastes']:
        for backend in ['mpl','root']:
         path=P/'output'/f'{backend}-{taste}-{preset}.png'
         if not path.exists(): raise RuntimeError(f'Missing executed backend: {path}')
         fig,ax=plt.subplots(figsize=(12,10)); ax.imshow(Image.open(path)); ax.axis('off'); fig.subplots_adjust(0,0,1,.95); fig.suptitle(f'{backend} / {taste} / {preset} - SYNTHETIC',fontsize=14); pdf.savefig(fig); plt.close(fig)

if __name__=='__main__':
    import sys
    if '--comparison' in sys.argv: comparison()
    else:
      data=make_data()
      for taste in C['tastes']:
       for preset in C['presets']: gallery(taste,preset,data)
      extra(data); single(data)
