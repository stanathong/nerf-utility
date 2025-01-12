#
# This script generates camera-path.json from transforms.json [and dataparser_transforms.json]
#
# Prerequisite:
# Obtain camera transforms using ns-export
#   ns-export cameras --load-config PATH/TO/config.yml --output-dir PATH/TO/OUTPUT/DIR
#
# Note: For the case that cameras are optimised prior to training, 
#       no success in applying dataparser_transforms.json so far

import json
import numpy as np
from pathlib import Path
import os
import math

# TODO: UPDATE THE CAMERA PARAMETERS from ns-process-data
camera_params = {
    "w": 1418,
    "h": 798,
    "fl_x": 1146.0330543044938,
    "fl_y": 1157.3885044122358,
    "cx": 689.61558717465448,
    "cy": 367.3775146331069
} 

camera_transform_path = 'data/custom/transforms.json'
dataparser_transform_path = ''
output_folder = 'renders/camera-path-output/'



def compute_aspect_ratio():
    return float(camera_params['h'])/camera_params['w']

def compute_fov(use_aspect_ratio=False):
    aspect_ratio = compute_aspect_ratio()
    fov = 2.0 * math.atan(0.5 * camera_params['h'] / camera_params['fl_y'])
    fov = fov * 180.0 / math.pi
    if use_aspect_ratio:
        fov = fov * aspect_ratio
    return fov

def homogeneous(c2w):
    if len(c2w) == 3:
        c2w += [[0, 0, 0, 1]]
    return c2w

transforms = json.loads(open(camera_transform_path).read())
transforms = sorted(transforms, key=lambda x:x['file_path'])

print('Number of items in transforms: ', len(transforms))

use_dataparser = False
if dataparser_transform_path:
    use_dataparser = True
    data_parser_transforms = json.load(open(dataparser_transform_path))
    data_transform = data_parser_transforms['transform']
    data_scale = data_parser_transforms['scale']
    np_data_transform = np.vstack([data_transform, [0,0,0,1]])
    print('data_transform\n:', data_transform)
    print('data_scale\n:', data_scale)

null = None
output = {
        'camera_type': 'perspective',
        'render_height': camera_params['h'],
        'render_width': camera_params['w'],
        'camera_path': [],
        'fps': 1,
        'seconds': len(transforms),
        'smoothness_value': 0,
        'is_cycle': False,
        'crop': null
        }

fov = compute_fov() 
for i in range(len(transforms)):
    pose = homogeneous(transforms[i]['transform'])
    np_pose = np.asarray(pose)
    # Apply dataparser_transform
    # TODO: Check why applying dataparser_transform doesn't seem to work as expect.
    if use_dataparser:
        np_pose = np.matmul(np_pose, np_data_transform)
        np_pose[0:3,3] *= data_scale
    np_pose = np_pose.ravel()
    camera = {
        'camera_to_world': np_pose.tolist(), 'fov': fov, 'aspect': 1, 'file_path': transforms[i]['file_path']
    }
    output['camera_path'].append(camera)

outstr = json.dumps(output, indent=4)
with open(os.path.join(output_folder, 'camera_path.json'), mode='w') as f:
    f.write(outstr)
