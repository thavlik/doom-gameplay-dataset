# Doom Gameplay Dataset
This is a collection of Doom I/II gameplay footage that has been downsampled to 320x240 @ 15fps, for a total size of about 17 Gb. The raw footage is mostly 1080p, totals ~170 Gb, and can only be randomly sampled at 3 frames/sec. The downsampling process allows frames to be loaded at speeds appropriate for machine learning applications.

There are no class labels or ground truth; this dataset is primarily intended for unsupervised learning.

## Downloading
You can either use `download.py` or you can grab it from S3 directly:
```
mkdir doom-gameplay-dataset
cd doom-gameplay-dataset
aws s3 sync --endpoint https://nyc3.digitaloceanspaces.com s3://doom-gameplay-dataset .
```

## Contributors
Gameplay videos are sourced from YouTube with permission. Special thanks to the following creators for their contributions to the community and this dataset - these individuals are the lifeblood of the Doom community:
- [Timothy Brown](https://www.youtube.com/user/mArt1And00m3r11339)
- [decino](https://www.youtube.com/c/decino)
- [Zero Master](https://www.youtube.com/channel/UCiVZWY9LmrJFOg3hWGjyBbw)

If you would like to contribute, please open an issue or submit a pull request with links to YouTube videos or playlists. Note: only a small fraction of Doom videos have been added so far. People are encouraged to contribute video lists and will be credited.

## License
All videos are property of their respective creators. Permission to transform and redistribute was granted in each case. This project makes no claims of ownership to the data.

## Related Projects
- [decord](https://github.com/dmlc/decord), for quickly loading frames
- [thavlik portfolio](https://github.com/thavlik/machine-learning-portfolio)
