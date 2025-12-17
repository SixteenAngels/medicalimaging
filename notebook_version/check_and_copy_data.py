"""
Check notebook for errors/duplicates and copy training data.
"""
import json
import os
import shutil
from pathlib import Path

def check_notebook_errors():
    """Check notebook for errors and duplicates."""
    notebook_path = Path(__file__).parent / "train_notebook.ipynb"
    
    if not notebook_path.exists():
        print(f"[ERROR] Notebook not found: {notebook_path}")
        return False
    
    print("="*60)
    print("Checking Notebook for Errors and Duplicates")
    print("="*60)
    
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    # Check for duplicates
    cell_contents = {}
    duplicates = []
    
    for i, cell in enumerate(nb['cells']):
        cell_type = cell.get('cell_type', 'unknown')
        source = ''.join(cell.get('source', []))
        
        # Create a signature for the cell
        if cell_type == 'code':
            # For code cells, check function definitions
            if 'def ' in source:
                func_name = source.split('def ')[1].split('(')[0].strip()
                if func_name in cell_contents:
                    duplicates.append((i, func_name, cell_contents[func_name]))
                else:
                    cell_contents[func_name] = i
            elif 'CONFIG = {' in source:
                if 'CONFIG' in cell_contents:
                    duplicates.append((i, 'CONFIG', cell_contents['CONFIG']))
                else:
                    cell_contents['CONFIG'] = i
    
    if duplicates:
        print(f"\n[WARNING] Found {len(duplicates)} potential duplicates:")
        for dup_idx, name, orig_idx in duplicates:
            print(f"   - {name} appears in cells {orig_idx} and {dup_idx}")
    else:
        print("\n[OK] No duplicates found!")
    
    # Check for empty cells
    empty_cells = []
    for i, cell in enumerate(nb['cells']):
        source = ''.join(cell.get('source', [])).strip()
        if not source and cell.get('cell_type') == 'markdown':
            empty_cells.append(i)
    
    if empty_cells:
        print(f"\n[WARNING] Found {len(empty_cells)} empty markdown cells: {empty_cells}")
    else:
        print("[OK] No empty cells found!")
    
    print(f"\n[INFO] Notebook Statistics:")
    print(f"   Total cells: {len(nb['cells'])}")
    print(f"   Code cells: {sum(1 for c in nb['cells'] if c.get('cell_type') == 'code')}")
    print(f"   Markdown cells: {sum(1 for c in nb['cells'] if c.get('cell_type') == 'markdown')}")
    
    return len(duplicates) == 0 and len(empty_cells) == 0

def copy_training_data():
    """Copy training data to notebook_version/data folder."""
    print("\n" + "="*60)
    print("Copying Training Data")
    print("="*60)
    
    # Find source data directory
    possible_sources = [
        Path(__file__).parent.parent / "data",
        Path(__file__).parent.parent / "main_project" / "data",
        Path("e:/medical imaging/data"),
        Path("e:/data"),
    ]
    
    source_dir = None
    for src in possible_sources:
        if src.exists() and src.is_dir():
            source_dir = src
            break
    
    if not source_dir:
        print("\n[ERROR] Source data directory not found!")
        print("   Checked locations:")
        for src in possible_sources:
            print(f"   - {src}")
        return False
    
    dest_dir = Path(__file__).parent / "data"
    
    print(f"\n[INFO] Source: {source_dir}")
    print(f"[INFO] Destination: {dest_dir}")
    
    # Check what's in source
    if source_dir.exists():
        subdirs = [d.name for d in source_dir.iterdir() if d.is_dir()]
        files = [f.name for f in source_dir.iterdir() if f.is_file()]
        print(f"\n[INFO] Source contains:")
        print(f"   Directories: {', '.join(subdirs[:10])}{'...' if len(subdirs) > 10 else ''}")
        if files:
            print(f"   Files: {', '.join(files[:5])}{'...' if len(files) > 5 else ''}")
    
    # Check if destination exists
    if dest_dir.exists():
        print(f"\n[WARNING] Destination '{dest_dir}' already exists.")
        print("   Skipping copy (data already present).")
        print("   To force copy, delete the existing folder first.")
        return True
    
    print("\n[INFO] Copying data folder (this may take a while for large datasets)...")
    
    try:
        shutil.copytree(source_dir, dest_dir)
        
        # Calculate size
        total_size = sum(f.stat().st_size for f in dest_dir.rglob('*') if f.is_file())
        size_gb = total_size / (1024**3)
        
        print(f"\n[SUCCESS] Data folder copied successfully!")
        print(f"   Total size: {size_gb:.2f} GB")
        
        # List what was copied
        copied_dirs = [d.name for d in dest_dir.iterdir() if d.is_dir()]
        print(f"   Copied directories: {', '.join(copied_dirs)}")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Error copying data folder: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Check notebook
    notebook_ok = check_notebook_errors()
    
    # Copy data
    copy_success = copy_training_data()
    
    print("\n" + "="*60)
    print("Summary")
    print("="*60)
    print(f"Notebook check: {'[OK] Passed' if notebook_ok else '[WARNING] Issues found'}")
    print(f"Data copy: {'[OK] Success' if copy_success else '[ERROR] Failed'}")
    print("="*60)
