from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import ffmpeg
import ffmpeg.filters
import typer.colors
from typer import secho


class ClipMode(str, Enum):
    VIDEO = "video"
    GIF = "gif"


@dataclass
class ClipSettings:
    fps: float | None = None
    mirror: bool = False
    clips: int = 0
    mode: list[ClipMode] = [ClipMode.VIDEO]  # video | gif

    # I dont think we need more for now


class Clip:
    """Clip creator"""

    def __init__(
        self,
        video: InputNode,
        settings: ClipSettings,
        input_path: Path,
        output_path: Path | None,
    ):
        self.video: InputNode = video
        self.input_path: Path = input_path  # this might be eitehr a file or a directory
        self.video_name: str = self.input_path.stem
        self.output_path: Path = self._set_output_path(input_path, output_path)

        self.video = ffmpeg.input(self.input_path)
        self.probe: dict = ffmpeg.probe(self.input_path)

        self.settings: ClipSettings = settings

        self.total_duration: float = self._set_total_duration()
        self.increment = self._calculate_increment()

    def create_clips(self) -> list[Path | None]:
        clips: list[Path | None] = []
        start = 0.0
        n_clips = int(self.total_duration // self.settings.clip_length)

        self.output_path.mkdir(parents=True, exist_ok=True)

        for i in range(n_clips):
            clip: Path | None = self._clip(
                start=start,
                duration=start + increment,
                path=self.output_path,
                name=self.video_name,
            )
            echo(f"video: {str(clip)} has been proccesed")

            clips.append(clip)
            start += self.settings.clip_length
            secho(f"video: {str(clip)} has been proccesed", fg=typer.colors.GREEN)

        return clips

    def _calculate_increment(self):
        return int(self.total_duration) // self.settings.clips

    def _set_total_duration(self) -> float:
        return float(self.probe["format"]["duration"])

    def _set_output_path(self, input_path: Path, output_path: Path | None) -> Path:
        """set the output path"""
        dir = "clips"

        if output_path is not None:
            return output_path

        if input_path.is_file():
            return input_path.parent / self.video_name / dir

        return input_path / self.video_name / dir

    def _clip(
        self, start: float, duration: float, path: Path, name: str
    ) -> Path | None:
        """make an individual clip from the video"""
        output_path: Path = path / name

        # TODO
        #    de.GIF in self.settings.mode:
        #         output_path = output_path.with_suffix(".gif")

        #     if ClipMode.VIDEO in self.settings.mode:
        #         output_path = output_path.with_suffix(".mp4")

        output_path = output_path.with_suffix(".mp4")

        try:
            _ = (
                ffmpeg.input(filename=self.input_path, ss=start, t=duration)
                .output(
                    filename=str(output_path),
                )
                .run()
            )
            return output_path

        except Exception:
            secho("Video failed", fg=typer.colors.RED)


# class Editor:
#     def __init__(self, video: InputNode, ):
#         self.video = video

#     @property
#     def clip(self, settings: ClipSettings) -> Clip:
#         return Clip(
#             self.video,
#             settings,
#         )
