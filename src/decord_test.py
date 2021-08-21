import os
import torch
import decord
from decord import VideoLoader, cpu

# Configure decord to output torch.Tensor
# You can also do this for Tensorflow, etc...
decord.bridge.set_bridge('torch')

width = 320
height = 240
dir = f'/data/videos'
video_files = [os.path.join(dir, f)
               for f in os.listdir(dir)
               if f.endswith('.mp4')]
num_frames = 1  # Likely (but not always) synonymous with batch_size
batch_shape = (num_frames, width, height, 3)
vl = VideoLoader(video_files,
                 ctx=[cpu(0)],
                 shape=batch_shape,
                 interval=0,
                 skip=0,
                 shuffle=1)
frame_data, indices = vl.next()
# `frame_data` contains the decoded frames
assert type(frame_data) == torch.Tensor
assert frame_data.shape == batch_shape
# `indices` is the (video_num, frame_num) for each frame
assert indices.shape == (num_frames, 2)
