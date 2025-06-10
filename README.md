## Install
```
pip install -r requirements.txt
```

## Download

Skip this step if you already have locally data on your device.

Create `.env` and enter your credentials and data info.
```
VESUVIUS_USERNAME=username
VESUVIUS_PASSWORD=password

BASE_URL=https://.../segmentID/layers/
BASE_DIR=/Users/.../segmentID/layers/
```

Download segment layers within a specified range:
```bash
python download_layers.py --start 0 --count 65
```

## Generate Surface Volume Ome-Zarr

Generate Zarr format (version 2) of surface volume for a given region. (zo, yo, xo) is min point and (zp, yp, xp) is max point of the bounding box.
```bash
python surface_volume.py --zo 0 --yo 3047 --xo 13152 --zp 65 --yp 3863 --xp 14128
```
And data will be generated in `hello-world-dataset` folder.

Now, we can transform Zarr format into Ome-Zarr format.
```
python zarr_to_ome.py ./hello-world-dataset/surface_volume ./hello-world-dataset/surface_volume.zarr
```

## Generate Ink Labels Ome-Zarr

If you have ink_labels.png, turn it into Ome-Zarr format as well. Make sure that ink_labels.png and layers tif images are the same size (w, h).
```bash
python ink_labels.py ./PATH_TO_INK_LABELS_PNG ./hello-world-dataset/ink_labels
```

Then, transform Zarr format into Ome-Zarr format.
```
python zarr_to_ome.py ./hello-world-dataset/ink_labels ./hello-world-dataset/ink_labels.zarr
```

## WebKnossos Dataset

Now, the `hello-world-dataset` folder is a WebKnossos dataset. By the way, you can remove the original Zarr format data because we already have Ome-Zarr data.

You may need to manually adjust some parameters in `datasource-properties.json` (I think it's more flexible and simple than programmatic editing).

If you want to generate them programmatically, you can checkout [WebKnossos Python CLI](https://docs.webknossos.org/cli/) and [WebKnossos Dataset documentation](https://docs.webknossos.org/api/webknossos/dataset/dataset.html).

## Open in WebKnossos

To view the dataset in WebKnossos application. You can upload them to the official cloud directly. But I prefer to run them locally, to do that, you can run the Docker container [here](https://github.com/scalableminds/webknossos/tree/master/tools/hosting). Once finished, you can directly drag the `hello-world-dataset` folder into WebKnossos application.

```
webknossos/tools/hosting/binaryData/your_organization_name/
    hello-world-dataset/
        surface_volume.zarr/
        ink_labels.zarr/
        datasource-properties.json
```