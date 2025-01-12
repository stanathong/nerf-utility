#
# This script generates camera-path.json from transforms.json.
#
#       transforms.json is obtained after successfully running ns-process-data
#       camera-path.json is to be used when running ns-render camera-path

import json
from pathlib import Path
import os
import math

# TODO: Adjust path to transforms and path to store output file
camera_transform_path = 'data/custom/transforms.json'
output_folder = 'renders/camera-path-output/'
original_height_width = (810,1440) # None

def compute_aspect_ratio(height, width):
    return height/width

def compute_fov(height, width, fx, fy, use_aspect_ratio=False):
    aspect_ratio = compute_aspect_ratio(height, width)
    fov = 2.0 * math.atan(0.5 * height / fy)
    fov = fov * 180.0 / math.pi
    if use_aspect_ratio:
        fov = fov * aspect_ratio
    return fov


transforms = json.loads(open(camera_transform_path).read())
metainfo = {key : value for key, value in transforms.items() if key != 'frames'}
frames = sorted(transforms['frames'], key=lambda x: 
    (''.join([d for d in Path(x['file_path']).stem if d.isdigit()])))

print(f'Number of frames in transforms: {len(frames)}')

null = None
output = {
            'camera_type': 'perspective',
            'render_height': metainfo['h'],
            'render_width': metainfo['w'],
            'camera_path': [],
            'fps': 1,
            'seconds': len(frames),
            'smoothness_value': 0,
            'is_cycle': False,
            'crop': null
        }

if original_height_width is None:
    fov = compute_fov(metainfo['h'], metainfo['w'], metainfo['fl_x'], metainfo['fl_y']) 
else:
    fov = compute_fov(original_height_width[0], original_height_width[1], metainfo['fl_x'], metainfo['fl_y']) 

print(fov)

for frame in frames:
    camera = {
        'camera_to_world': [x for row in frame['transform_matrix'] for x in row], 'fov': fov, 'aspect': 1, 'file_path': frame['file_path']
    }
    output['camera_path'].append(camera)

outstr = json.dumps(output, indent=4)
with open(os.path.join(output_folder, 'camera_path_distored_fov.json'), mode='w') as f:
    f.write(outstr)
