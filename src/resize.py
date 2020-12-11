import argparse
import json
import os
import sys
import subprocess
import time
import glob

parser = argparse.ArgumentParser(
    description='resize videos')
parser.add_argument('--input',  '-i',
                    dest="input",
                    metavar='INPUT',
                    help='path to dir with mp4 files',
                    default='/mnt/e/doom')
parser.add_argument('--output', '-o',
                    dest="output",
                    metavar='OUTPUT',
                    help='output dir',
                    default='/mnt/e/doom-processed')
parser.add_argument('--width',
                    dest="width",
                    metavar='WIDTH',
                    help='output resolution x',
                    default=320)
parser.add_argument('--height',
                    dest="height",
                    metavar='HEIGHT',
                    help='output resolution y',
                    default=240)
parser.add_argument('--skip-frames',
                    dest="skip_frames",
                    metavar='SKIP_FRAMES',
                    help='number of frames to skip',
                    default=1)
parser.add_argument('--segment-time',
                    dest="segment_time",
                    metavar='SEGMENT_TIME',
                    help='max segment length',
                    default='00:5:00')
args = parser.parse_args()
denom = args.skip_frames + 1

print(
    f'Output resolution: {args.width}x{args.height} @ {30//denom} fps, {args.segment_time} segments')

if not os.path.exists(args.output):
    os.makedirs(args.output)

files = sorted([f for f in os.listdir(args.input)
                if f.endswith('.mp4')])
completed_path = os.path.join(args.output, 'completed.txt')
if os.path.exists(completed_path):
    with open(completed_path, 'r') as f:
        completed = [line for line in f]
else:
    completed = []


def add_completed(file):
    completed.append(file)
    with open(completed_path, 'w') as f:
        f.write(json.dumps(completed))


print(f'Processing {len(files)} files ({len(completed)} already completed)')
total_in = 0
total_out = 0
total_start = time.time()
for i, file in enumerate(files):
    file = file[:-len('.mp4')]
    if file in completed:
        print(f'Skipping {file} (already converted)')
        continue
    start = time.time()
    input = os.path.join(args.input, file).replace('\\', '/') + '.mp4'
    output = os.path.join(args.output, file).replace('\\', '/')
    in_size = os.path.getsize(input)
    total_in += in_size
    in_size //= 1000*1000
    print(f'[{i+1}/{len(files)}] Processing {input} ({in_size} MiB)')
    cmd = f"ffmpeg -i {input} -s {args.width}x{args.height} -y -c:a copy -an -vf select='not(mod(n\\,{denom})), setpts={1.0/denom}*PTS' -reset_timestamps 1 -map 0 -segment_time {args.segment_time} -f segment {output}%03d.mp4"
    proc = subprocess.run(
        ['bash', '-c', cmd], capture_output=True)
    if proc.returncode != 0:
        msg = 'expected exit code 0 from ffmpeg, got exit code {}: {}'.format(
            proc.returncode, proc.stdout.decode('unicode_escape'))
        if proc.stderr:
            msg += ' ' + proc.stderr.decode('unicode_escape')
        raise ValueError(msg)
    add_completed(file)
    delta = time.time() - start
    out_files = glob.glob(output + '*.mp4')
    out_size = sum(os.path.getsize(f)
                   for f in out_files)
    total_out += out_size
    out_size //= 1000*1000
    pct = (1.0 - out_size / in_size) * 100
    print(f'[{i+1}/{len(files)}] Wrote {out_files} in {delta} seconds ({out_size} MiB, {int(pct)}% reduction)')
delta = time.time() - total_start
reduction = int((1.0 - total_out / total_in) * 100)
print(f'Completed in {delta} seconds, total reduction of {reduction}%')
