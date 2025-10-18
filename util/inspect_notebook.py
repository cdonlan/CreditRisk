import json

def inspect_notebook(path):
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    print('Cells:', len(nb.get('cells', [])))
    print('Has metadata:', 'metadata' in nb)
    print('nbformat:', nb.get('nbformat'), 'nbformat_minor:', nb.get('nbformat_minor'))
    # Check for any remaining problematic MIME types
    problem_mimes = set()
    for i, cell in enumerate(nb.get('cells', []), 1):
        if cell.get('cell_type') == 'code':
            for output in cell.get('outputs', []):
                for k in output.keys():
                    if k not in ('output_type', 'name', 'text'):
                        problem_mimes.add(k)
    print('Problematic MIME types found:', problem_mimes)
    # Check for VS Code-specific cell ids and language in metadata
    ids = [cell.get('id') for cell in nb.get('cells', []) if cell.get('id')]
    print('Example cell id present:', bool(ids))
    # Check for VS Code-specific metadata keys in cells
    vs_keys = set()
    for cell in nb.get('cells', []):
        for k in cell.get('metadata', {}).keys():
            if 'vscode' in k.lower() or 'datawrangler' in k.lower() or k.startswith('vsc'):
                vs_keys.add(k)
    print('VS Code-specific metadata keys present in cells:', vs_keys)
    # Show top-level metadata keys
    print('Top-level metadata keys:', set(nb.get('metadata', {}).keys()))

if __name__ == '__main__':
    inspect_notebook(r'c:/Code/CreditRisk/credit_risk_analysis.ipynb')
