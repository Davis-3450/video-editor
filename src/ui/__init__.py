from pathlib import Path

import typer

from .. import __version__
from ..video.logic import Clip, ClipMode, ClipSettings

VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".m4v", ".flv"}

app = typer.Typer(
    name="video editor",
    help="A video editing script using ffmpeg",
    add_completion=False,
)


def _resolve_videos(input: str) -> list[Path]:
    path = Path(input)
    if path.is_file():
        return [path]
    if path.is_dir():
        return [f for f in sorted(path.iterdir()) if f.suffix.lower() in VIDEO_EXTENSIONS]
    typer.secho(f"Path not found: {input}", fg=typer.colors.RED)
    raise typer.Exit(1)


def _parse_mode(mode_input: str, allow_both: bool = False) -> list[ClipMode]:
    match mode_input:
        case "gif":
            return [ClipMode.GIF]
        case "mp4":
            return [ClipMode.VIDEO]
        case "both" if allow_both:
            return [ClipMode.VIDEO, ClipMode.GIF]
        case "blur":
            return [ClipMode.BLUR]
        case "preview":
            return [ClipMode.PREVIEW]
        case _:
            valid = "gif, mp4, both, blur, preview" if allow_both else "gif, mp4, blur, preview"
            typer.secho(f"Invalid mode '{mode_input}'. Use: {valid}.", fg=typer.colors.RED)
            raise typer.Exit(1)


@app.command()
def edit(
    seconds: int,
    mode_input: str,
    input: str,
    blur_sigma: float = typer.Option(50.0, "--blur-sigma", help="Blur intensity for gaussian blur mode (default 50.0, higher = blurrier)"),
) -> None:
    mode = _parse_mode(mode_input, allow_both=True)
    settings = ClipSettings(clip_length=seconds, mode=mode, blur_sigma=blur_sigma)

    for video_path in _resolve_videos(input):
        editor = Clip(settings=settings, input_path=video_path, output_path=None)
        editor.create_clips()

    typer.secho("Success")


@app.command()
def preview(
    seconds: int,
    input: str,
    mode_input: str = typer.Argument("mp4"),
    blur_sigma: float = typer.Option(50.0, "--blur-sigma", help="Blur intensity (only applies to blur/preview modes)"),
) -> None:
    """Extract a single clip of SECONDS from the beginning of the video."""
    mode = _parse_mode(mode_input)
    settings = ClipSettings(clip_length=seconds, mode=mode, blur_sigma=blur_sigma)

    input_path = Path(input)
    shared_output = input_path.parent / f"{input_path.stem} (clips)"

    for video_path in _resolve_videos(input):
        editor = Clip(settings=settings, input_path=video_path, output_path=shared_output)
        editor.create_preview()

    typer.secho("Success")


@app.command()
def version() -> None:
    """Show version information."""
    typer.secho(f"version: {__version__}", fg=typer.colors.CYAN)


@app.command()
def help() -> None:
    """Show help"""
    typer.secho("Configuration:", fg=typer.colors.YELLOW, bold=True)


if __name__ == "__main__":
    app()
