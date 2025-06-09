## Usage

- Copy `.env.example` to `.env` and enter your credentials
```
VESUVIUS_USERNAME=username
VESUVIUS_PASSWORD=password
```

Download segment layers within a specified range:
```bash
python download_layers.py --start 0 --count 65
```

### Surface Volume Processing
```bash
python surface_volume.py
```
This script processes the downloaded layers to create a surface volume dataset in zarr format.

### Ink Labels Processing
```bash
python ink_labels.py
```
This script processes ink labels and converts them to the zarr format.