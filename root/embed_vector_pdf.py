"""Embed ROOT's existing vector PDF fonts without rasterizing its paths/text.

This verified local recovery uses a matching Ghostscript 10 binary/resources,
plus an isolated link to an existing libtiff5. It changes no global settings.
WinAnsi and the verified Symbol /minus override are supported; other glyph encodings fail.
Run with Python providing pypdf. See qa/VECTOR_REPORT.md for acceptance evidence.
"""
from pathlib import Path
import argparse, json, os, subprocess, tempfile, shutil
from pypdf import PdfReader, PdfWriter, Transformation
from pypdf.generic import NameObject, DecodedStreamObject, RectangleObject

P = Path(__file__).resolve().parents[1]
DEFAULT_GS = os.environ.get('GS_BINARY') or shutil.which('gs')
DEFAULT_RESOURCE = os.environ.get('GS_RESOURCE')
DEFAULT_TIFF = os.environ.get('GS_LIBTIFF5')
TARGETS = {
    'root-single-paper': (3.4, 2.8),
    'root-single-slides': (10, 7),
    'root-overlay-ratio-paper': (6.8, 5.2),
    'root-overlay-ratio-slides': (10, 7.6),
    'color-root-paper': (12, 10),
    'color-root-slides': (16, 13),
}

def winansi_cmap(overrides=None):
    overrides = overrides or {}
    entries = []
    for code in range(256):
        try:
            char = bytes([code]).decode('cp1252')
        except UnicodeDecodeError:
            continue
        entries.append(f'<{code:02X}> <{overrides.get(code, ord(char)):04X}>')
    parts = ['/CIDInit /ProcSet findresource begin', '12 dict begin', 'begincmap',
             '/CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) /Supplement 0 >> def',
             '/CMapName /WinAnsiToUnicode def', '/CMapType 2 def',
             '1 begincodespacerange', '<00> <FF>', 'endcodespacerange']
    for start in range(0, len(entries), 100):
        chunk = entries[start:start+100]
        parts += [f'{len(chunk)} beginbfchar', *chunk, 'endbfchar']
    parts += ['endcmap', 'CMapName currentdict /CMap defineresource pop', 'end', 'end']
    return ('\n'.join(parts)+'\n').encode('ascii')

def vector_counts(page):
    operations = page.get_contents().operations
    strokes = sum(op in (b'S', b's', b'B', b'B*', b'b', b'b*') for _, op in operations)
    text_runs = sum(op in (b'Tj', b'TJ', b"'", b'"') for _, op in operations)
    images = len(page.images)
    return {'path_strokes': strokes, 'text_runs': text_runs, 'images': images}

def export(stem, inches, gs, resource, tiff, temp):
    source = P/'output'/f'{stem}.pdf'
    intermediate = temp/f'{stem}.pdf'
    destination = P/'output'/f'{stem}-embedded.pdf'
    env = os.environ.copy()
    libs = temp/'libs'; libs.mkdir(exist_ok=True)
    link = libs/'libtiff.5.dylib'
    if tiff is not None and not link.exists(): link.symlink_to(tiff)
    # Only the missing library is offered. Do not expose the whole old conda lib
    # directory: it also contains an incompatible libc++.
    if tiff is not None: env['DYLD_LIBRARY_PATH'] = str(libs)
    env['GS_LIB'] = ':'.join(str(resource/x) for x in ['Resource/Init', 'lib', 'Resource/Font'])
    command = [str(gs), '-q', '-dSAFER', '-dBATCH', '-dNOPAUSE', '-sDEVICE=pdfwrite',
               '-dEmbedAllFonts=true', '-dSubsetFonts=true',
               '-sGenericResourceDir='+str(resource/'Resource')+'/',
               '-sFontResourceDir='+str(resource/'Resource/Font')+'/',
               '-sOutputFile='+str(intermediate),
               '-c', '<</NeverEmbed []>> setdistillerparams', '-f', str(source)]
    completed = subprocess.run(command, env=env, capture_output=True, text=True)
    (P/'qa/vector'/f'{stem}-gs.log').write_text(completed.stdout+completed.stderr)
    completed.check_returncode()
    reader = PdfReader(intermediate)
    assert len(reader.pages) == 1
    writer = PdfWriter(); writer.clone_document_from_reader(reader)
    page = writer.pages[0]
    page.transfer_rotation_to_content()
    # ROOT places its canvas on an A4 sheet with CropBox and /Rotate. Normalize
    # the canvas into the requested physical page, preserving aspect ratio.
    left, bottom, right, top = map(float, page.cropbox)
    width, height = (72*inches[0], 72*inches[1])
    scale = min(width/(right-left), height/(top-bottom))
    dx = (width-(right-left)*scale)/2
    dy = (height-(top-bottom)*scale)/2
    page.add_transformation(Transformation().translate(-left,-bottom).scale(scale).translate(dx,dy))
    page.mediabox = RectangleObject([0, 0, width, height])
    page.cropbox = RectangleObject([0, 0, width, height])
    for ref in page['/Resources']['/Font'].values():
        font = ref.get_object()
        encoding = font.get('/Encoding')
        overrides = {}
        if encoding != '/WinAnsiEncoding':
            if not hasattr(encoding, 'get') or encoding.get('/BaseEncoding') != '/WinAnsiEncoding':
                raise ValueError(f'Unsupported encoding: {encoding}')
            position = None
            for item in encoding.get('/Differences', []):
                if isinstance(item, int):
                    position = item
                elif item == '/minus' and position == 45:
                    overrides[position] = 0x2212
                    position += 1
                else:
                    raise ValueError(f'Unverified glyph override: {item}')
        descriptor = font['/FontDescriptor'].get_object()
        assert any(key in descriptor for key in ['/FontFile','/FontFile2','/FontFile3'])
        if '/ToUnicode' not in font:
            stream = DecodedStreamObject(); stream.set_data(winansi_cmap(overrides))
            font[NameObject('/ToUnicode')] = writer._add_object(stream)
    writer.add_metadata({'/Title':stem+' - SYNTHETIC - embedded vector', '/Subject':'Fixed-shape synthetic illustration; stat only'})
    with destination.open('wb') as output: writer.write(output)
    final = PdfReader(destination).pages[0]
    counts = vector_counts(final)
    assert counts['path_strokes'] > 100 and counts['text_runs'] >= 10 and counts['images'] == 0
    expected = ['SYNTHETIC', 'Mass [GeV]', 'observed']
    if 'overlay' in stem: expected += ['reference', 'Ratio']
    extracted = final.extract_text()
    assert all(text in extracted for text in expected), extracted
    fonts = subprocess.check_output(['pdffonts',str(destination)], text=True)
    (P/'qa/vector'/f'{stem}-fonts.txt').write_text(fonts)
    assert all('yes yes yes' in line for line in fonts.strip().splitlines()[2:]), fonts
    return {'file':destination.name,'inches':inches,'scale':scale,'fonts':'embedded/subset/ToUnicode yes',**counts}

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--gs',default=DEFAULT_GS)
    parser.add_argument('--resource',default=DEFAULT_RESOURCE)
    parser.add_argument('--libtiff',default=DEFAULT_TIFF)
    args=parser.parse_args()
    if not args.gs or not args.resource:
        parser.error('--gs/GS_BINARY and --resource/GS_RESOURCE must identify a matching Ghostscript installation')
    gs,resource = map(Path,[args.gs,args.resource])
    tiff = Path(args.libtiff) if args.libtiff else None
    for path in [gs,resource/'Resource/Init/gs_init.ps'] + ([tiff] if tiff else []):
        if not path.exists(): raise FileNotFoundError(path)
    with tempfile.TemporaryDirectory(prefix='plot-vector-') as d:
        results=[export(stem,size,gs,resource,tiff,Path(d)) for stem,size in TARGETS.items() if (P/'output'/f'{stem}.pdf').exists()]
    (P/'qa/vector/results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))
