#!/usr/bin/env python3
"""
Script to clean Jupyter notebook for GitHub rendering
Removes problematic outputs and keeps only basic text/plain outputs
"""

import json
import sys

def clean_notebook_for_github(notebook_path):
    """Clean notebook outputs for GitHub compatibility"""
    
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    cleaned_cells = 0
    total_cells = len(notebook['cells'])
    
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            if 'outputs' in cell and cell['outputs']:
                original_outputs = len(cell['outputs'])
                
                # Keep only simple text outputs, remove complex MIME types
                clean_outputs = []
                for output in cell['outputs']:
                    if output.get('output_type') == 'stream':
                        # Keep simple stream outputs (print statements)
                        clean_outputs.append(output)
                    elif output.get('output_type') == 'execute_result':
                        # Filter execute_result to only text/plain
                        if 'data' in output:
                            filtered_data = {}
                            if 'text/plain' in output['data']:
                                filtered_data['text/plain'] = output['data']['text/plain']
                            
                            if filtered_data:
                                new_output = {
                                    'output_type': 'execute_result',
                                    'execution_count': output.get('execution_count'),
                                    'data': filtered_data,
                                    'metadata': {}
                                }
                                clean_outputs.append(new_output)
                    elif output.get('output_type') == 'display_data':
                        # Keep only basic display data
                        if 'data' in output:
                            filtered_data = {}
                            if 'text/plain' in output['data']:
                                filtered_data['text/plain'] = output['data']['text/plain']
                            
                            if filtered_data:
                                new_output = {
                                    'output_type': 'display_data',
                                    'data': filtered_data,
                                    'metadata': {}
                                }
                                clean_outputs.append(new_output)
                
                cell['outputs'] = clean_outputs
                if original_outputs > len(clean_outputs):
                    cleaned_cells += 1
            
            # Reset execution count to None for cleaner diffs
            cell['execution_count'] = None
    
    # Clean notebook metadata
    if 'metadata' in notebook:
        # Keep minimal metadata
        notebook['metadata'] = {
            "kernelspec": notebook['metadata'].get('kernelspec', {}),
            "language_info": notebook['metadata'].get('language_info', {})
        }
    
    # Save cleaned notebook
    backup_path = notebook_path.replace('.ipynb', '_backup.ipynb')
    
    # Create backup
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)
    
    # Save cleaned version
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Notebook cleaned for GitHub!")
    print(f"📊 Statistics:")
    print(f"   • Total cells: {total_cells}")
    print(f"   • Cells cleaned: {cleaned_cells}")
    print(f"   • Backup saved: {backup_path}")
    print(f"   • Problematic outputs removed")
    print(f"   • Custom MIME types filtered")
    print(f"   • Execution counts reset")

if __name__ == "__main__":
    notebook_path = "credit_risk_analysis.ipynb"
    clean_notebook_for_github(notebook_path)
