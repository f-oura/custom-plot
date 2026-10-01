"""Numerical/embedding checks complement, never replace, visual QA."""
import pathlib,json,subprocess
import numpy as np
from PIL import Image
p=pathlib.Path(__file__).resolve().parents[1]
v=np.loadtxt(p/'data/counts.csv',delimiter=',');z=np.loadtxt(p/'data/density.csv',delimiter=',');c=np.loadtxt(p/'data/correlation.csv',delimiter=',')
assert v.shape==(40,5) and z.shape==(576,4)
assert np.all(v[:,1:3]>=0) and np.all(v[:,1:3]==np.round(v[:,1:3]))
assert np.all(v[:,4]>0) and np.sum(z[:,2]==0)==261
assert np.min(z[:,3])>=-30 and np.max(z[:,3])<=30
assert np.allclose(c,c.T) and np.allclose(np.diag(c),1) and np.linalg.eigvalsh(c).min()>0
fit=json.loads((p/'qa/fit.json').read_text());assert fit['ndof']==37 and abs(fit['chi2']-38.016924585)<1e-6
# Gaussian ratio approximation is illustrative, not exact low-count inference.
r=v[:,1]/v[:,2]; e=r*np.sqrt(1/np.maximum(v[:,1],1)+1/v[:,2]);assert (r+e).max()<5
embedded=[]; raw=[]
for pdf in sorted((p/'output').glob('*.pdf')):
 out=subprocess.check_output(['pdffonts',str(pdf)],text=True)
 (p/'qa'/f'{pdf.stem}-fonts.txt').write_text(out)
 lines=out.strip().splitlines()[2:]
 if 'root' in pdf.name and not all('yes yes yes' in line for line in lines): raw.append(pdf.name);continue
 assert lines and all('yes yes yes' in line for line in lines),out
 embedded.append(pdf.name)
for backend in ['mpl','root']:
 for taste in ['classic','clean','ink']:
  for preset in ['paper','slides']:
   im=np.asarray(Image.open(p/'output'/f'{backend}-{taste}-{preset}.png').convert('RGB'));assert im.std()>10
info=subprocess.check_output(['pdfinfo',str(p/'output/comparison.pdf')],text=True);assert 'Pages:           12' in info
result={'numerical_checks':'pass','backend_galleries':12,'embedding_ToUnicode_pass':embedded,'raw_ROOT_PDF_embedding':'FAIL: unembedded Type1 fonts; excluded from publication acceptance','raw_ROOT_PDF_files':raw,'zero_density_bins':261,'ratio_max_with_error':float((r+e).max()),'visual_QA':'See REPORT.md; not automated pass'}
(p/'qa/automated.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
