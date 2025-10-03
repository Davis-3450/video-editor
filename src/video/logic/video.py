import ffmpeg
from ffmpeg.nodes import InputNode

from .editor import Clip, ClipSettings, Editor


class Video:
    def __init__(self, file_path: str, frame_rate: int):
        """
        Initialize a Video object.

        Args:
            file_path (str): The path to the video file.
            frame_rate (int): The frame rate of the video.
        """
        self.file_path = file_path
        self.editor = Editor(self._read_video())
        self.info: dict = self._read_info()

    # Read methods
    def _read_video(self) -> InputNode:
        return ffmpeg.input(self.file_path, show_streams=True)

    def _read_info(self) -> dict:
        self.info: dict = ffmpeg.probe(self.file_path)
        return self.info

    @property
    def fps(self) -> float:
        """
        Get the frame rate of the video.
        """
        return self.info["streams"][0]["avg_frame_rate"]

    # Write methods
    def create_clip(self, settings: ClipSettings) -> Clip:
        clip: Clip = self.editor.clip(settings)
        return clip.create_clips()

    #
