# Here is the code used to generate the video grid gif,
# as seen on the github home page.
from decord import VideoReader, cpu, bridge
import os
import numpy as np
from PIL import Image
import subprocess

bridge.set_bridge('torch')

input = '/mnt/e/quake-gameplay-dataset/download/320x240'
rows = 4
cols = 4
fps = 12
num_seconds = 8
num_frames = fps * num_seconds
limit = rows * cols
id_len = len('-9PA3A7h1KE')
using = {}
files = []
for f in os.listdir(input):
    # Make sure we do not use the start of any video
    if f.endswith('.mp4') and not f.endswith('0.mp4'):
        id = f[:id_len]
        if id in using:
            # Do not use the same video more than once
            print(f'Skipping {id}')
            continue
        using[id] = True
        files.append(f)
        print(f'Using video {f}')
sorted_files = sorted(files)
files = sorted_files
indices = np.random.choice(len(files), limit, replace=False)
files = [files[idx] for idx in indices]
print(f'Using {len(using)} videos: {files}')
assert len(set(files)) == len(files)
videos = [VideoReader(os.path.join(input, f)) for f in files]
frames = np.array([[vr.next().numpy() for _ in range(num_frames)]
                   for vr in videos])
for frameno in range(num_frames):
    i = 0
    complete_frame = []
    for _ in range(rows):
        items = []
        for _ in range(cols):
            frame_data = frames[i][frameno]
            items.append(frame_data)
            i += 1
        items = np.concatenate(items, axis=1)
        complete_frame.append(items)
    complete_frame = np.concatenate(complete_frame, axis=0)
    img = Image.fromarray(complete_frame)
    img = img.resize((img.width//2, img.height//2))
    out_path = 'frame_{0:04}.png'.format(frameno)
    img.save(out_path)
    print(f'Wrote {out_path}')
out_path = 'thumbnails'
print(f'Encoding video to {out_path}.mp4')
cmd = f"ffmpeg -y -r {fps} -s {img.width}x{img.height} -i frame_%04d.png -crf 25 -pix_fmt yuv420p {out_path}.mp4"
print(f'Running {cmd}')
proc = subprocess.run(
    ['bash', '-c', cmd], capture_output=True)
if proc.returncode != 0:
    msg = 'expected exit code 0 from ffmpeg, got exit code {}: {}'.format(
        proc.returncode, proc.stdout.decode('unicode_escape'))
    if proc.stderr:
        msg += ' ' + proc.stderr.decode('unicode_escape')
    raise ValueError(msg)
cmd = f"ffmpeg -y -i {out_path}.mp4 {out_path}.gif"
print(f'Running {cmd}')
proc = subprocess.run(
    ['bash', '-c', cmd], capture_output=True)
if proc.returncode != 0:
    msg = 'expected exit code 0 from ffmpeg, got exit code {}: {}'.format(
        proc.returncode, proc.stdout.decode('unicode_escape'))
    if proc.stderr:
        msg += ' ' + proc.stderr.decode('unicode_escape')
    raise ValueError(msg)
print(f'Wrote gif to {out_path}.gif')
[os.remove(f'frame_' + f'{i}.png'.rjust(8, '0')) for i in range(num_frames)]
