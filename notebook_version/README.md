# Notebook Version - Medical Imaging & Vesuvius Challenge

This folder contains a self-contained version of the training notebook with duplicated data folders.

## Contents

- `medical_imaging.ipynb` - Complete training notebook (medical imaging + Vesuvius Challenge)
- `data/` - Duplicated data folder (run `copy_data.py` to create)

## Setup

1. **Copy the data folder** (if not already copied):
   
   **Windows (Recommended - Fastest):**
   ```cmd
   copy_data_robocopy.bat
   ```
   
   **Windows/Linux/Mac (Python script):**
   ```bash
   python copy_data.py
   ```
   
   **Linux/Mac (Shell script):**
   ```bash
   chmod +x copy_data.sh
   ./copy_data.sh
   ```
   
   **Manual copy:**
   ```bash
   # Windows
   xcopy /E /I /Y ..\data data
   
   # Linux/Mac
   cp -r ../data .
   ```

2. **Open the notebook**:
   - Jupyter Notebook: `jupyter notebook train_notebook.ipynb`
   - JupyterLab: `jupyter lab train_notebook.ipynb`
   - VS Code: Open `train_notebook.ipynb`

3. **Run Cell 0** to install required packages

4. **Configure DATA_ROOT** in Cell 2 if needed (defaults to `'data'`)

5. **Run the cells** to train models

## Features

- ✅ Medical Image Classification (brain, lungs, skin, breast, bone)
- ✅ 2D Segmentation with UNet
- ✅ Vesuvius Challenge 3D Volume Segmentation
- ✅ Competition Metrics (Surface Dice, TopoScore, VOI)
- ✅ Automatic Package Installation
- ✅ Portable Data Paths (works on multiple PCs/cloud)

## Data Structure

The `data/` folder should contain:
```
data/
├── brain/
├── lungs/
├── skin/
├── breast/
├── Bone/
└── vesuvius/  (for Vesuvius Challenge)
    ├── train/
    │   ├── volumes/
    │   └── masks/
    └── test/
        └── volumes/
```

## Notes

- All paths are relative to `DATA_ROOT` (configurable in Cell 2)
- The notebook is self-contained - no external Python files needed
- Works on Kaggle, Google Colab, and local Jupyter environments

