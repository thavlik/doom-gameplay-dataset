# Doom Gameplay Dataset
This is a collection of Doom I/II gameplay footage that has been preprocessed so that it is appropriate for machine learning purposes.

Sourcing batches of frames from raw 1080p video is a notoriously unwieldy process - a single CPU can rarely seek random frames faster than 3-4 fps. Multiple downsampled resolutions are provided, allowing frames to be loaded at speeds suitable for machine learning applications.

There are no class labels or ground truth; this dataset is primarily intended for unsupervised learning.


## Resolutions

| Resolution      | FPS | Size (GiB) | % Reduction
| --------------- | --- | ---------- | -----------
| 320x240         | 15  | 25.8       | 84         
| 480x320         | 15  | TODO       | TODO
| 640x480         | 15  | TODO       | TODO
| 800x600         | 15  | TODO       | TODO
| 1920x1080       | 30  | 165        | None (raw)

## Downloading

The data can be downloaded with the [AWS Command Line Interface](https://aws.amazon.com/cli/). Folders in the S3 bucket are named according to the resolution video they contain.

```
mkdir doom-gameplay-dataset
cd doom-gameplay-dataset
aws s3 sync --endpoint https://nyc3.digitaloceanspaces.com s3://doom-gameplay-dataset/320x240 320x240
```

The hosting costs for this project are negligible, but an inconsiderately written download script could easily change this. I kindly ask that you be courteous w.r.t. redundant downloads, and cache locally where appropriate.

## How To Use
There are several existing Python solutions for loading frames from a directory of videos. [decord](https://github.com/dmlc/decord) is currently the most promising, given its narrowly tailored focus of machine learning. Generally, the API entails pointing the loader at a directory containing video files:
```python
import os
import torch
from decord import VideoLoader, cpu

# Configure decord to output torch.Tensor
decord.bridge.set_bridge('torch')

width = 320
height = 240
dir = f'/data/doom-gameplay-dataset/download/{width}x{height}'
video_files = [f for f in os.listdir(dir)
               if f.endswith('.mp4')]
num_frames = 1 # Likely (but not always) synonymous with batch_size
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
# `indices` is the (video_num, frame_num)
assert indices.shape == (num_frames, 2)
``` 

## Compiling from Raw
Check out the `src` folder for the scripts used to download and resize the raw videos. [ffmpeg](https://ffmpeg.org/) does most of the heavy lifting.

## Contributors
Gameplay videos are sourced from YouTube with permission. Special thanks to the following creators for their contributions to the community and this dataset - these individuals are the lifeblood of the Doom community:
- [Timothy Brown](https://www.youtube.com/user/mArt1And00m3r11339)
- [decino](https://www.youtube.com/c/decino)
- [Zero Master](https://www.youtube.com/channel/UCiVZWY9LmrJFOg3hWGjyBbw)

If you would like to contribute, please open an issue or submit a pull request with links to YouTube videos or playlists. Note: only a small fraction of Doom videos have been added so far. People are encouraged to contribute video lists and will be credited.

## License
All videos are property of their respective creators. Permission to transform and redistribute was granted in each case. This project makes no claims of ownership to the data.

This project's code is released under MIT / Apache 2.0 dual license, which is extremely permissive.

## Related Projects
- [decord](https://github.com/dmlc/decord), for quickly loading frames
- [thavlik portfolio](https://github.com/thavlik/machine-learning-portfolio)
