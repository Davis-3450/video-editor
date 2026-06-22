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
def edit(
    seconds: int,
    mode_input: str,
    input: str,
    blur_sigma: float = typer.Option(50.0, "--blur-sigma", help="Blur intensity for gaussian blur mode (default 50.0, higher = blurrier)"),
) -> None:
    mode = []

    match mode_input:
        case "gif":
            mode += [ClipMode.GIF]
        case "mp4":
            mode += [ClipMode.VIDEO]
        case "both":
            mode += [ClipMode.VIDEO, ClipMode.GIF]
        case "blur":
            mode += [ClipMode.BLUR]
        case "preview":
            mode += [ClipMode.PREVIEW]
        case _:
            typer.secho(f"Invalid mode '{mode_input}'. Use: gif, mp4, both, blur, preview.", fg=typer.colors.RED)
            raise typer.Exit(1)

    path = Path(input)
    settings = ClipSettings(clip_length=seconds, mode=mode, blur_sigma=blur_sigma)

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
