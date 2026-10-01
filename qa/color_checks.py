"""Verify shared data/LUTs, vector fonts, page geometry and isolated renders."""
from pathlib import Path
import csv, json, subprocess, hashlib
import numpy as np
from PIL import Image
from pypdf import PdfReader, PdfWriter
P=Path(__file__).resolve().parents[1]
options=json.loads((P/'config/color_options.json').read_text())
rows=list(csv.reader((P/'qa/color-root-lut.csv').open()))
result={}
for name,lut in options['palettes']['samples'].items():
 actual=np.array([list(map(float,r[2:])) for r in rows if r[0]==name])
 assert actual.shape==(128,3)
 delta=float(np.abs(actual-np.array(lut)).max());assert delta<1e-6
 result[name+'_runtime_max_rgb_error']=delta
for file in ['counts.csv','density.csv','correlation.csv']:
 path=P/'data'/file
 if not path.exists(): continue
 expected=json.loads((P/'data/manifest.json').read_text())[file]
 assert hashlib.sha256(path.read_bytes()).hexdigest()==expected
result['synthetic_data_unchanged']=True
assert (np.loadtxt(P/'data/density.csv',delimiter=',')[:,2]==0).sum()==261
for name,files in [('classic-color-comparison.pdf',['color-mpl-paper.pdf','color-root-paper-embedded.pdf','color-mpl-slides.pdf','color-root-slides-embedded.pdf']),('root-vector-samples.pdf',['root-single-paper-embedded.pdf','root-single-slides-embedded.pdf','root-overlay-ratio-paper-embedded.pdf','root-overlay-ratio-slides-embedded.pdf'])]:
 writer=PdfWriter()
 for f in files: writer.append(P/'output'/f)
 writer.write(P/'output'/name)
 reader=PdfReader(P/'output'/name);assert len(reader.pages)==4
 assert all(len(page.images)==0 for page in reader.pages)
 fonts=subprocess.check_output(['pdffonts',str(P/'output'/name)],text=True)
 assert all('yes yes yes' in line for line in fonts.strip().splitlines()[2:])
 (P/'qa/color'/f'{name}-fonts.txt').write_text(fonts)
 normal=P/'qa/color'/name.replace('.pdf','')/'normal';isolated=normal.parent/'isolated'
 normal.mkdir(parents=True,exist_ok=True);isolated.mkdir(exist_ok=True)
 config=normal.parent/'empty-fonts.conf';empty=normal.parent/'empty-fonts';empty.mkdir(exist_ok=True)
 config.write_text(f'<fontconfig><dir>{empty}</dir><cachedir>{empty}/cache</cachedir></fontconfig>')
 import os
 for folder,env in [(normal,None),(isolated,dict(os.environ,FONTCONFIG_FILE=str(config),FONTCONFIG_PATH=str(config.parent)))]:
  subprocess.run(['pdftoppm','-r','90','-png',str(P/'output'/name),str(folder/'page')],env=env,check=True)
 diffs=[]
 for i in range(1,5):
  a=np.asarray(Image.open(normal/f'page-{i}.png'));b=np.asarray(Image.open(isolated/f'page-{i}.png'))
  delta=int(np.abs(a.astype(int)-b.astype(int)).max());assert delta==0;diffs.append(delta)
 result[name]={'pages':4,'images':0,'all_fonts_embedded_subset_unicode':True,'external_font_render_pixel_max_difference':diffs}
(P/'qa/color/results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
