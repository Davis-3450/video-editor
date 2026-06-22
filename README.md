## CLI clip editor

A command line interface with typer for quickly making simple clips and GIFs from longer videos using ffmpeg.

### Installation (dev mode for now)

```bash
git clone https://github.com/Davis-3450/video-editor
cd video-editor
```

```bash
uv sync
```

The `video-editor` command should now be available in your terminal.

### Usage

```bash
video-editor edit <seconds> <mode> <path> [options]
```

### Examples

```bash
# Split a video into 10-second MP4 clips
video-editor edit 10 mp4 input.mp4

# Split into 10-second GIF clips
video-editor edit 10 gif input.mp4

# Split into both MP4 and GIF clips
video-editor edit 10 both input.mp4

# Split with blur applied
video-editor edit 10 blur input.mp4 --blur-sigma 15
```

#### Arguments

- `seconds`: Length of each clip in seconds (integer).
- `mode`: Output format. Options: `mp4`, `gif`, `both`, `blur`.
- `path`: Path to the input video file.

#### Options

- `--blur-sigma <int>`: Blur intensity when using `blur` mode (default: `40`).

### Output

Clips are saved under `<input_dir>/<video_name>/clips/` with names like `<video_name>_1.mp4`, `<video_name>_2.mp4`, etc. Blur clips get a `_blur` suffix.

### Other commands

```bash
video-editor version   # Show version
video-editor help      # Show help
```
