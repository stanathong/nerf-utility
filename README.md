# Utility Scripts

## nerfstudio

### camera-path.json for ns-render camera-path

* [Script](convert_transforms_to_camera_path.py) Convert transforms.json obtained after running colmap through `ns-process-data` to camera-path.json

* [Script](convert_exported_cam_to_camera_path.py) Convert transforms.json obtained from `ns-export cameras` to camera-path.json

```
ns-export cameras --load-config PATH/TO/config.yml --output-dir PATH/TO/OUTPUT/DIR
```

### render output from trained nerf model using camera-path.json

```
ns-render camera-path --load-config PATH/TO/config.yml --image-format png --output-format images --output-path PATH/TO/OUTPUT/DIR --camera-path-filename PATH/TO/camera_path.json
```