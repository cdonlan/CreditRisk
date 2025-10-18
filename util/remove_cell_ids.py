import json
import shutil

def remove_cell_ids(path):
    backup = path.replace('.ipynb', '_noids_backup.ipynb')
    shutil.copy2(path, backup)
    print('Backup created:', backup)
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    removed = 0
    for cell in nb.get('cells', []):
        if 'id' in cell:
            del cell['id']
            removed += 1
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)
    print('Removed id from', removed, 'cells')

if __name__ == '__main__':
    remove_cell_ids(r'c:/Code/CreditRisk/credit_risk_analysis.ipynb')
