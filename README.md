## Usage

Create `.env` and enter your credentials
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

### WebKnossos Dataset

Take segment 20230702185753 as an example. The dataset folder is the structure that you can upload into Webknossos Dataset.

```bash
./dataset/surface_volume/1/0/z_axis/y_axis/x_axis
./dataset/ink_labels/1/0/z_axis/y_axis/x_axis
```

You can manually edit `datasource-properties.json` and `.zarray` if you use different segment.