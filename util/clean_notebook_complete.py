#!/usr/bin/env python3
"""
Complete notebook cleaner for GitHub compatibility.
Removes ALL outputs and execution counts to ensure GitHub rendering.
"""

import json
import shutil
from datetime import datetime

def clean_notebook_completely(input_file, output_file=None):
    """
    Remove ALL outputs and execution data from Jupyter notebook for GitHub compatibility.
    
    Args:
        input_file: Path to input notebook
        output_file: Path to output notebook (optional, defaults to overwriting input)
    """
    
    if output_file is None:
        output_file = input_file
    
    # Create backup with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = input_file.replace('.ipynb', f'_backup_{timestamp}.ipynb')
    shutil.copy2(input_file, backup_file)
    print(f"Created backup: {backup_file}")
    
    # Load notebook
    with open(input_file, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Clean all cells
    cells_processed = 0
    outputs_removed = 0
    execution_counts_reset = 0
    
    for cell in notebook.get('cells', []):
        cells_processed += 1
        
        # Remove ALL outputs for code cells
        if cell.get('cell_type') == 'code':
            if 'outputs' in cell and cell['outputs']:
                outputs_removed += len(cell['outputs'])
                cell['outputs'] = []
            
            # Reset execution count
            if 'execution_count' in cell and cell['execution_count'] is not None:
                execution_counts_reset += 1
                cell['execution_count'] = None
    
    # Reset notebook-level execution data
    if 'metadata' in notebook:
        # Remove kernel info that might cause issues
        if 'kernelspec' in notebook['metadata']:
            # Keep only essential kernel info
            kernelspec = notebook['metadata']['kernelspec']
            notebook['metadata']['kernelspec'] = {
                'display_name': kernelspec.get('display_name', 'Python 3'),
                'language': 'python',
                'name': 'python3'
            }
        
        # Remove language info that might be VS Code specific
        if 'language_info' in notebook['metadata']:
            language_info = notebook['metadata']['language_info']
            notebook['metadata']['language_info'] = {
                'name': 'python',
                'version': language_info.get('version', '3.12.0'),
                'mimetype': 'text/x-python',
                'file_extension': '.py'
            }
    
    # Save cleaned notebook
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Notebook cleaning complete!")
    print(f"   📄 Processed {cells_processed} cells")
    print(f"   🗑️  Removed {outputs_removed} outputs")
    print(f"   🔄 Reset {execution_counts_reset} execution counts")
    print(f"   💾 Cleaned notebook saved to: {output_file}")
    
    return True

if __name__ == "__main__":
    notebook_file = "credit_risk_analysis.ipynb"
    
    print("🧹 Starting complete notebook cleaning for GitHub compatibility...")
    print(f"📁 Target file: {notebook_file}")
    
    try:
        clean_notebook_completely(notebook_file)
        print("\n🎉 Notebook is now ready for GitHub!")
        print("📋 Changes made:")
        print("   • Removed ALL cell outputs")
        print("   • Reset ALL execution counts")
        print("   • Cleaned metadata for compatibility")
        print("   • Created backup file")
        
    except Exception as e:
        print(f"❌ Error cleaning notebook: {e}")
        exit(1)
