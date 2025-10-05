from pathlib import Path

import typer

from .. import __version__
from ..video.logic import Clip, ClipMode, ClipSettings

# video-editor
# schema: video-editor edit seconds input output format

app = typer.Typer(
    name="video editor",
    help="A video editing script using ffmpeg",
    add_completion=False,
)


@app.command()
def edit(seconds: int, mode_input: str, input: str) -> None:
    mode = []

    match mode_input:
        case "gif":
            mode += [ClipMode.GIF]
        case "mp4":
            mode += [ClipMode.VIDEO]
        case "both":
            mode += [ClipMode.VIDEO, ClipMode.GIF]

    path = Path(input)
    settings = ClipSettings(clip_length=seconds, mode=mode)

    editor = Clip(
        settings=settings,
        input_path=path,
        output_path=None,
    )
    editor.create_clips()

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
