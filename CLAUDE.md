# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A CLI tool for making video clips and GIFs from longer videos using ffmpeg. Built with Python 3.13+, Typer, and typed-ffmpeg.

## Commands

```bash
# Install dependencies (uses uv)
uv sync

# Run the CLI
uv run video-editor <command>

# Run tests
uv run pytest

# Lint / format
uv run ruff check .
uv run ruff format .

# Type check
uv run pyrefly check
```

## Architecture

Entry point: `src/__main__.py` → checks ffmpeg is installed, then delegates to the Typer app.

- `src/ui/__init__.py` — Typer CLI commands (`edit`, `version`, `help`). `edit` is the primary command: takes `seconds`, `mode_input` (gif/mp4/both), and `input` path.
- `src/video/logic/editor.py` — Core logic. `ClipSettings` holds parameters; `Clip` wraps an ffmpeg input, probes the video duration, and calls `create_clips()` to split it into fixed-length segments output as `.mp4` files under `<input_dir>/<video_name>/clips/`.
- `src/utils/__init__.py` — `ffmpeg_install_check()` via subprocess.
- `src/__init__.py` — exposes `__version__`.

### Key design note

GIF output is stubbed out in `Clip._clip()` (see the TODO comment). The `mode` field on `ClipSettings` is parsed but only `.mp4` is written. Completing GIF support means wiring `ClipMode.GIF` through the ffmpeg filter chain there.
