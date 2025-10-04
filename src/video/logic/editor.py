from dataclasses import dataclass
from pathlib import Path

import ffmpeg
from ffmpeg.nodes import InputNode

# import ffmpeg


@dataclass
class ClipSettings:
    frame_rate: int | None = None
    output_path: Path | None = None
    mirror: bool = False
    clip_duration: float | None = None
    clip_fps: float | None = None
    mode: list[str] = ["video"]  # video | gif

    # I dont think we need more for now


class Clip:
    """Clip cerator"""

    def __init__(self, video: InputNode, settings: ClipSettings, input_path: Path, output_path: Path | None):
        self.video: InputNode = video
        self.input_path: Path = input_path # this might be eitehr a file or a directory
        self.output_path: Path = self._set_output_path(input_path, output_path)
        self.settings: ClipSettings = settings
        self.video_name: str = input_path.stem

    def create_clips(self) -> list[Path]:
        pass

    def _set_output_path(self, input_path: Path, output_path: Path | None) -> Path:
        """set the output path"""
        dir = "clips"
        if output_path is not None:
            return output_path

        if input_path.is_file():
            return input_path.parent / self.video_name / dir

        return input_path / self.video_name / dir

class Editor:
    def __init__(self, video: InputNode):
        self.video = video

    @property
    def clip(self, settings: ClipSettings) -> Clip:
        return Clip(
            self.video,
            settings,
        )
