import json, os
p = r'c:/Code/CreditRisk/credit_risk_analysis.ipynb'
print('Local file exists:', os.path.exists(p))
print('Size (bytes):', os.path.getsize(p))
with open(p, 'r', encoding='utf-8') as f:
    nb = json.load(f)
# Check if any code cell has non-empty outputs
cells_with_outputs = 0
total_outputs = 0
mimetypes = set()
for cell in nb.get('cells', []):
    if cell.get('cell_type') == 'code':
        outputs = cell.get('outputs', [])
        if outputs:
            cells_with_outputs += 1
            total_outputs += len(outputs)
            for out in outputs:
                for k in out.keys():
                    if k not in ('output_type', 'name', 'text'):
                        mimetypes.add(k)
print('Cells with outputs:', cells_with_outputs)
print('Total outputs:', total_outputs)
print('Non-standard mime keys present in outputs:', mimetypes)
# Check for any cell-level metadata that looks large
large_meta_cells = []
for i, cell in enumerate(nb.get('cells', []),1):
    meta = cell.get('metadata', {})
    if meta and len(str(meta))>200:
        large_meta_cells.append((i, len(str(meta))))
print('Cells with large metadata (>200 chars):', large_meta_cells)
print('\nTop-level metadata keys:', list(nb.get('metadata', {}).keys()))
print('\nnbformat', nb.get('nbformat'), 'nbformat_minor', nb.get('nbformat_minor'))
