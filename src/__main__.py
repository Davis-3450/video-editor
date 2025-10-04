from sys import exit

from typer import secho
from typer.colors import RED

from .ui import app
from .utils import ffmpeg_install_check

if __name__ == "__main__":
    if not ffmpeg_install_check():
        secho("ffmpeg is not installed", fg=RED)
        exit()
    app()
