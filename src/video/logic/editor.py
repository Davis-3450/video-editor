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

    def __init__(self, video: InputNode, settings: ClipSettings):
        self.video = video
        self.output_path: Path
        self.settings = settings

    def create_clips(self) -> list[Path]:
        pass


class Editor:
    def __init__(self, video: InputNode):
        self.video = video

    @property
    def clip(self, settings: ClipSettings) -> Clip:
        return Clip(
            self.video,
            settings,
        )
