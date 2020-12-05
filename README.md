# Doom Gameplay Dataset
![Example Thumbnails](images/thumbnails.gif)

**UPDATE DEC 12, 2020: VERSION 1.0 @ 320x240 IS RELEASED, 640x480 AND RAW ARE UPLOADING. THANK YOU FOR YOUR PATIENCE.**

This is a collection of Doom I/II gameplay footage that has been preprocessed such that it is appropriate for machine learning purposes. Current estimates place the total duration at around 170 hours (and growing!)

There are no class labels or ground truth; this dataset is primarily intended for unsupervised learning.

Custom maps and a few weapon/enemy mods made their way into dataset. Future efforts may be directed at "purifying" the data in ways such as omitting these custom weapons.

## Resolutions

| Resolution      | FPS | Size (GiB) | % Reduction | Download (.zip)
| --------------- | --- | ---------- | ----------- | --------
| 320x240         | 15  | 25.8       | 84          | [Link](https://doom-gameplay-dataset.nyc3.digitaloceanspaces.com/320x240.zip)
| 640x480         | 15  | 74.6       | 55          | TODO
| 1920x1080*      | 30  | 165        | None (raw)  | TODO

\* Most raw videos are at 1080p/720p but some are at lower resolutions

Note: the .zip files provide almost no compression, and are provided only for convenience

## S3 Hosting

The data can be downloaded with the [AWS Command Line Interface](https://aws.amazon.com/cli/) or compatible S3 API. Folders in the S3 bucket are named according to the resolution video they contain. Because the bucket contains all resolutions in both .mp4 and .zip format, syncing the entire bucket is highly redundant and discouraged. `s3 sync` is the recommended download method for slow or interruptible connections, as it can stopped and resumed without issue.

```bash
mkdir doom-gameplay-dataset
cd doom-gameplay-dataset
# Sync only the folder with the resolution you want
# --no-sign-request allows use of awscli without credentials
aws s3 sync --endpoint https://nyc3.digitaloceanspaces.com --no-sign-request s3://doom-gameplay-dataset/320x240 320x240
```

The hosting costs for this project are negligible, but an inconsiderately written download script could easily change this. I kindly ask that you be courteous w.r.t. redundant downloads, and cache locally where appropriate. If necessary, I will delist the .mp4 files from the bucket and only make the zip files available.

## How To Use
There are several existing Python solutions for loading frames from a directory of videos. [decord](https://github.com/dmlc/decord) is currently the most promising, given its narrowly tailored focus of machine learning. Generally, the API entails pointing the loader at a directory containing video files:
```python
import os
import torch
from decord import VideoLoader, cpu

# Configure decord to output torch.Tensor
# You can also do this for Tensorflow, etc...
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
# `indices` is the (video_num, frame_num) for each frame
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

## Future Improvements
As you can see from the thumbnail videos, the resizing process is carried out without regard to the original video's aspect ratio. There are also some frames, usually at the beginnings and ends of videos, that are not Doom gameplay, and should be excluded.

This will be addressed by training a per-frame variational autoencoder, clustering the latent space into a small number of dimensions using t-SNE, and rejecting the clusters unassociated with gameplay. The end result is an additional pass over the videos to determine true start/end times, as well as if any irregularities were encountered during gameplay (e.g. the player encountered a crash to desktop). Some longer videos, such as live streams, may be sliced up to remove segments of non-gameplay.

## License
All videos are property of their respective creators. Permission to transform and redistribute was granted in each case. This project makes no claims of ownership to the data.

This project's code is released under MIT / Apache 2.0 dual license, which is extremely permissive.

## Related Projects
- [decord](https://github.com/dmlc/decord), for quickly loading frames
- [thavlik portfolio](https://github.com/thavlik/machine-learning-portfolio)
