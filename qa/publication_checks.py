"""Portable checks for adopted configuration and generated PDF fonts/data."""
from pathlib import Path
import sys,json,hashlib
from pypdf import PdfReader
P=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(P/'python'))
from plotstyle import apply_selected,semantic,S
assert S['render_backend']=='matplotlib' and S['semantic_color']=='4'
assert S['density_color']=='viridis' and S['signed_difference']=='RdBu_r'
assert apply_selected()[0]['colors']==['#222222','#0072B2','#D55E00']
try: semantic(None,[],[],'unmapped-fourth-condition',apply_selected()[0])
except KeyError: pass
else: raise AssertionError('Unknown condition silently accepted')
for name,expected in json.loads((P/'data/manifest.json').read_text()).items():
 assert hashlib.sha256((P/'data'/name).read_bytes()).hexdigest()==expected
for kind in ['counts','density']:
 for preset in ['paper','slides']:
  page=PdfReader(P/'output'/f'selected-{kind}-{preset}.pdf').pages[0]
  for font in page['/Resources']['/Font'].values():
   font=font.get_object();assert '/ToUnicode' in font
   descendants=font.get('/DescendantFonts',[font])
   for ref in descendants:
    child=ref.get_object();descriptor=child['/FontDescriptor'].get_object()
    assert any(k in descriptor for k in ['/FontFile','/FontFile2','/FontFile3'])
print('adopted semantic mapping, unknown-key rejection, synthetic data hashes and PDF embedded fonts PASS')
