# Public release verification

The original local research-plot-style repository and its full working history remain preserved. This custom-plot release starts from its adopted snapshot and uses a fresh public history, so private environment paths and model authentication work notes are not exposed. No real research data, model/API credentials or private Library identifiers are included. Example CSVs are synthetic; SHA256 hashes are retained in data/manifest.json.

Before initial push: GitHub target f-oura/custom-plot was public, main default branch, size0 and no git refs. No remote history was overwritten. Selected settings and examples remain classic / option4 / viridis / centered RdBu_r; Python rendering standard and ROOT exceptions are documented.

Portable publication_checks.py passed locally using already installed dependencies: semantic option4 exact mapping, unknown condition rejection, synthetic data hashes, embedded PDF fonts and ToUnicode. Selected 1D/2D Python outputs were regenerated. Generalized ROOT embed_vector_pdf.py was executed with explicit existing GS10/resource/libtiff paths and passed for all six PDFs; color_checks.py passed with SHA256 manifest, exact LUT, font portability and pixel-identical external-font-free renders. Official skill validator passed. No local software installation or global configuration change.

Python GitHub Actions workflow regenerates the four selected example files and checks the same portable conditions. It does not certify ROOT or visual inspection. Visual and scientific limits remain in ADOPTION_REPORT.md, COLOR_REPORT.md and VECTOR_REPORT.md, including unverified Japanese ROOT glyphs and final printer/projector/data QA.
