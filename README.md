## CLI clip editor

A command line interface with typer for quickly making simple clips.

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
video-editor edit <clip-length> <type> <path> <output-path>
```

### Example

```bash
video-editor edit 10 video input.mp4
```

#### Arguments

- `clip-length`: Length of the clip in seconds (integer).
- `type`: Type of clip to create. Options are: `video` and `gif`.
- `path`: Path to the input video file.
- `output-path`: (Optional) Path to save the output file. If not provided, the output will be saved in the current directory with a default name.

Multiple clips of `clip-length` seconds will be created from the start of the video until the end.
