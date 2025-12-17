# Medical Imaging & Vesuvius Challenge

A comprehensive deep learning system for **medical image classification, segmentation, and 3D volume analysis** with support for multiple medical imaging domains and the Vesuvius Challenge.

## Features

### Medical Image Classification
- **Multi-Domain Support**: Brain, Lungs, Skin, Breast, Bone
- **ResNet-based Classifiers**: Pretrained ResNet18 with custom classification heads
- **Flexible Configuration**: Easy domain switching and configuration

### Medical Image Segmentation
- **2D UNet Segmentation**: For medical image segmentation tasks
- **Dice Loss**: Optimized for medical segmentation
- **Flexible Dataset Support**: Works with various medical imaging formats

### Vesuvius Challenge (3D CT Volume Segmentation)
- **2.5D UNet**: Multi-slice context for 3D volume segmentation
- **Competition Metrics**: Surface Dice, TopoScore, VOI (Variation of Information)
- **.tif Volume I/O**: Handles variable dimension CT volumes
- **Submission Generation**: Automated .tif submission file creation

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/SixteenAngels/medicalimaging.git
cd medicalimaging

# Install dependencies
pip install torch torchvision
pip install tifffile scipy scikit-image
pip install pillow numpy
```

### Using the Notebook

1. **Open the notebook**:
   ```bash
   jupyter notebook notebook_version/medical_imaging.ipynb
   # or
   jupyter lab notebook_version/medical_imaging.ipynb
   ```

2. **Run Cell 0** to automatically install all required packages

3. **Configure DATA_ROOT** in Cell 2 (defaults to `'data'`)

4. **Run cells** to train models

### Training Medical Image Classification

```python
# In the notebook, set:
TASK = "classification"
DOMAIN = "brain"  # or "lungs", "skin", "breast", "bone", or "all"
```

### Training Segmentation

```python
# In the notebook, set:
TASK = "segmentation"
# Update paths in the cell:
SEG_IMAGES = "data/brain_seg/train/images"
SEG_MASKS = "data/brain_seg/train/masks"
```

### Vesuvius Challenge Training

1. Update paths in Cell 11:
   ```python
   VESUVIUS_VOLUME_DIR = "data/vesuvius/train/volumes"
   VESUVIUS_MASK_DIR = "data/vesuvius/train/masks"
   ```

2. Uncomment and run the training code in Cell 11

3. Generate submission files using Cell 12

## Project Structure

```
medicalimaging/
├── notebook_version/
│   ├── medical_imaging.ipynb    # Main training notebook
│   ├── README.md                 # Notebook-specific documentation
│   ├── copy_data.py              # Data copying utilities
│   └── data/                     # Training data (local copy)
├── models/                       # Model architectures
├── training/                     # Training pipeline
├── inference/                    # Inference engine
├── api/                          # FastAPI REST API
├── configs/                      # Configuration files
└── README.md                     # This file
```

## Data Structure

The `data/` folder should contain:

```
data/
├── brain/
│   └── brain/
│       ├── Training/
│       └── Testing/
├── lungs/
│   ├── train/
│   └── val/
├── skin/
│   ├── train/
│   └── val/
├── breast/ or breast_split/
│   ├── train/
│   ├── val/
│   └── test/
├── Bone/
│   ├── train/
│   ├── val/
│   └── test/
└── vesuvius/  (for Vesuvius Challenge)
    ├── train/
    │   ├── volumes/
    │   └── masks/
    └── test/
        └── volumes/
```

## Model Architectures

### ResNet Classifier
- **Backbone**: ResNet18 (pretrained on ImageNet)
- **Classification Head**: Custom fully connected layers with dropout
- **Input Size**: Configurable (224x224 or 128x128)
- **Output**: Multi-class classification

### UNet Segmentation
- **Architecture**: Standard UNet with skip connections
- **Loss Function**: Combined BCE + Dice Loss
- **Input**: Grayscale or RGB images
- **Output**: Binary segmentation masks

### UNet2.5D (Vesuvius Challenge)
- **Architecture**: UNet with multi-slice context
- **Slice Window**: 3, 5, or 7 slices (configurable)
- **Loss Function**: Combined BCE + Dice Loss
- **Metrics**: Surface Dice, TopoScore, VOI

## Supported Domains

| Domain | Classes | Input Size | Notes |
|--------|---------|------------|-------|
| Brain | 4 | 224x224 | Brain tumor classification |
| Lungs | 5 | 224x224 | Lung disease classification |
| Skin | 9 | 128x128 | Skin lesion classification |
| Breast | 3 | 128x128 | Breast cancer classification |
| Bone | 2 | 224x224 | Bone fracture classification |

## Competition Metrics (Vesuvius Challenge)

- **Surface Dice**: Measures distance between prediction and ground truth surfaces
- **TopoScore**: Measures topological similarity (penalizes mergers/splits)
- **VOI (Variation of Information)**: Measures information distance between segmentations

## Requirements

### Core Dependencies
- Python 3.8+
- PyTorch 1.12+
- torchvision
- numpy
- pillow

### Optional Dependencies
- **tifffile**: Required for Vesuvius Challenge (.tif volume I/O)
- **scipy**: Required for metrics and resizing
- **scikit-image**: Required for topology metrics

## Usage Examples

### Medical Image Classification

```python
# Train on all domains
TASK = "classification"
DOMAIN = "all"

# Train on specific domain
TASK = "classification"
DOMAIN = "brain"
```

### Segmentation

```python
TASK = "segmentation"
train_segmentation(
    images_dir="data/brain_seg/train/images",
    masks_dir="data/brain_seg/train/masks",
    output_path="trained/unet_brain_tumor.pth",
    input_size=(256, 256),
    epochs=20,
    batch_size=4
)
```

### Vesuvius Challenge

```python
model = train_vesuvius_challenge(
    volume_dir="data/vesuvius/train/volumes",
    mask_dir="data/vesuvius/train/masks",
    slice_window=3,
    epochs=20,
    batch_size=4
)
```

## Environment Support

The notebook works across multiple environments:

- **Local PC**: `DATA_ROOT = 'data'` (default)
- **Kaggle**: `DATA_ROOT = '/kaggle/input/vesuvius-challenge-surface-detection'`
- **Google Colab**: `DATA_ROOT = '/content/data'`
- **Cloud/Remote**: Set via environment variable: `export DATA_ROOT=/path/to/data`

## Performance

### Classification Accuracy (Example)
- Brain: ~85-90% accuracy
- Lungs: ~80-85% accuracy
- Skin: ~75-80% accuracy
- Breast: ~85-90% accuracy
- Bone: ~90-95% accuracy

### Segmentation
- Dice Score: ~85-90% (depending on dataset)

### Vesuvius Challenge
- Surface Dice: ~0.85-0.90
- TopoScore: ~0.80-0.85
- VOI Score: ~0.75-0.80

## Citation

If you use this project for the Vesuvius Challenge, please cite:

```bibtex
@misc{vesuvius-challenge-surface-detection,
    author = {Sean Johnson and David Josey and Elian Rafael Dal Prà and Hendrik Schilling and Youssef Nader and Johannes Rudolph and Forrest McDonald and Paul Henderson and Giorgio Angelotti and Sohier Dane and María Cruz},
    title = {Vesuvius Challenge - Surface Detection},
    year = {2025},
    howpublished = {\url{https://kaggle.com/competitions/vesuvius-challenge-surface-detection}},
    note = {Kaggle}
}
```

## License

MIT License

## Acknowledgments

- Vesuvius Challenge Team
- PyTorch Community
- Medical imaging research community

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.
