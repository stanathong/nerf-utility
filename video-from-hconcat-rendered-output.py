import os
import PIL
import PIL.Image
import cv2

# Adjust parameters
working_dir = "renders/dataset"
output_names = ["gt-rgb", "rgb", "depth", "accumulation"]
output_dir = "renders/output"

os.makedirs(output_dir, exist_ok=True)

def create_video():
    image_names = []
    for filename in os.listdir(output_dir):
        if filename.endswith(tuple(support_image_types)):
            image_names.append(filename)

    image_names = sorted(image_names)

    frame = cv2.imread(os.path.join(output_dir, image_names[0]))
    height, width, channels = frame.shape

    video_name = "_".join(output_names)
    video_name = (os.path.join(output_dir, "video-" + video_name + '.mp4'))
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    video = cv2.VideoWriter(video_name, fourcc, 1, (width, height))

    for filename in image_names:
        image = cv2.imread(os.path.join(output_dir, filename))
        video.write(image)
    video.release()

    print(f"Create video {video_name} success")


# Iterate through groundtruth
support_image_types = [".jpg", ".png"]
for filename in os.listdir(os.path.join(working_dir, output_names[0])):

    if not filename.endswith(tuple(support_image_types)):
        continue

    print(f"Processing {filename} ...")
    name, ext = filename.split(".")[0], "." + filename.split(".")[1]
    print(name, ext)

    output = {}
    max_width = 0
    max_height = 0

    all = True
    for o in range(len(output_names)):
        output[output_names[o]] = {}
        folder = os.path.join(working_dir, output_names[o])
        print(f"Processing {os.path.join(folder, filename)} ...")
        image = PIL.Image.open(os.path.join(folder, filename))
        output[output_names[o]]["image"] = image
        width, height = image.size
        channel = len(image.getbands())
        output[output_names[o]]["width"], output[output_names[o]]["height"] = width, height
        if channel != 3:
            image = image.convert(mode='RGB')
        max_width += width
        max_height = max(max_height, height)

    if all == False:
        output.clear()
        continue

    # Concatenate
    width_idx = 0
    concat_image = PIL.Image.new("RGB", (max_width, max_height))
    for o in range(len(output_names)):
        concat_image.paste(output[output_names[o]]["image"], (width_idx, 0))
        width_idx += output[output_names[o]]["width"]
    
    concat_image.save(os.path.join(output_dir, filename))

create_video()
