"""Shared semantic style API, independent of synthetic gallery generation."""
import json,pathlib
import matplotlib.pyplot as plt
P=pathlib.Path(__file__).resolve().parents[1]
C=json.loads((P/'config/styles.json').read_text())

def apply(taste,preset):
    plt.style.use(str(P/'styles'/f'{taste}-{preset}.mplstyle'))
    return C['tastes'][taste],C['presets'][preset]

def semantic(ax,x,y,key,t,errors=None):
    """Draw statistical series as points; only the model is a curve."""
    s=C['conditions'][key]
    color=t['colors'][s['index']]
    marker_size=max(4.,plt.rcParams['font.size']*.35)
    if errors is None and key=='model':
        ax.plot(x,y,label=key,color=color,ls=s['line'],lw=C['geometry']['line_pt'])
    elif errors is None:
        ax.plot(x,y,label=key,color=color,marker=s['marker'],ms=marker_size,ls='none')
    else:
        ax.errorbar(x,y,yerr=errors,label=key,color=color,fmt=s['marker'],ms=marker_size,
                    ls='none',elinewidth=C['geometry']['line_pt'],capsize=2)

def outside_legend(ax):
    # Reserved headroom; actual data-specific checks still required.
    ax.legend(loc='upper right',fontsize='small',frameon=False)
    lo,hi=ax.get_ylim(); ax.set_ylim(lo,hi+(hi-lo)*.32)


# User-selected rendering policy; does not force the calculation backend.
S=json.loads((P/'config/selection.json').read_text())

def apply_selected(preset='paper'):
    """Apply approved classic layout and stable option-4 semantic colors."""
    taste, geometry = apply(S['layout'],preset)
    options=json.loads((P/'config/color_options.json').read_text())
    mapping=options['candidates'][S['semantic_color']]['conditions']
    return dict(taste,colors=[mapping[key] for key in C['conditions']]),geometry

def selected_palette(kind='density'):
    """Return the shared exact LUT, with signed data centered at zero by caller."""
    from matplotlib.colors import ListedColormap
    options=json.loads((P/'config/color_options.json').read_text())
    name=S['density_color'] if kind=='density' else S['signed_difference']
    cmap=ListedColormap(options['palettes']['samples'][name],name=name+'-selected')
    cmap.set_bad('#eeeeee')
    return cmap
