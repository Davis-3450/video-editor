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
    BLUR = "blur"
    PREVIEW = "preview"  # censored mini preview


@dataclass
class ClipSettings:
    fps: float | None = None
    mirror: bool = False
    clip_length: int = 0
    mode: list[ClipMode] | None = None  # video | gif | blur | preview
    blur_sigma: float = 2.0

    # mini preview (censored) tuning
    preview_height: int = 240
    preview_fps: float = 12.0
    pixel_size: int = 24

    # I dont think we need more for now


class Clip:
    """Clip creator"""

    def __init__(
        self,
        settings: ClipSettings,
        input_path: Path,
        output_path: Path | None,
    ):
        self.input_path: Path = input_path  # this might be eitehr a file or a directory
        self.video_name: str = self.input_path.stem
        self.output_path: Path = self._set_output_path(input_path, output_path)

        self.video = ffmpeg.input(self.input_path)
        self.probe: dict = ffmpeg.probe(self.input_path)

        self.settings: ClipSettings = settings

        self.total_duration: float = self._set_total_duration()

    def create_preview(self) -> Path | None:
        """Extract a single clip of `clip_length` seconds from the start."""
        self.output_path.mkdir(parents=True, exist_ok=True)
        clip = self._clip(
            start=0.0,
            duration=self.settings.clip_length,
            path=self.output_path,
            name=f"{self.video_name}_preview",
        )
        if clip:
            secho(f"preview: {str(clip)} has been processed", fg=typer.colors.YELLOW)
        return clip

    def create_clips(self) -> list[Path | None]:
        clips: list[Path | None] = []
        start = 0.0
        n_clips = int(self.total_duration // self.settings.clip_length)

        self.output_path.mkdir(parents=True, exist_ok=True)

        for i in range(n_clips):
            clip: Path | None = self._clip(
                start=start,
                duration=self.settings.clip_length,
                path=self.output_path,
                name=f"{self.video_name}_{i + 1}",
            )

            clips.append(clip)
            start += self.settings.clip_length
            secho(f"video: {str(clip)} has been processed", fg=typer.colors.YELLOW)

        return clips

    def _set_total_duration(self) -> float:
        return float(self.probe["format"]["duration"])

    def _has_audio(self) -> bool:
        return any(
            s.get("codec_type") == "audio" for s in self.probe.get("streams", [])
        )

    def _set_output_path(self, input_path: Path, output_path: Path | None) -> Path:
        if output_path is not None:
            return output_path
        return input_path.parent / self.video_name / "clips"

    def _clip(
        self, start: float, duration: float, path: Path, name: str
    ) -> Path | None:
        """make an individual clip from the video"""
        mode = self.settings.mode or []

        if ClipMode.PREVIEW in mode:
            suffix = "_preview"
        elif ClipMode.BLUR in mode:
            suffix = "_blur"
        else:
            suffix = ""
        output_path: Path = (path / f"{name}{suffix}").with_suffix(".mp4")

        try:
            stream = ffmpeg.input(filename=self.input_path, ss=start, t=duration)
            video = stream.video

            if ClipMode.PREVIEW in mode:
                # Censored mini preview: shrink, pixelate and heavily blur.
                px = self.settings.pixel_size
                video = (
                    video.fps(fps=str(self.settings.preview_fps))
                    .scale(w="-2", h=str(self.settings.preview_height))
                    # pixelate: downscale then upscale with nearest-neighbor blocks
                    .scale(
                        w=f"ceil(iw/{px}/2)*2", h=f"ceil(ih/{px}/2)*2", flags="neighbor"
                    )
                    .scale(w=f"iw*{px}", h=f"ih*{px}", flags="neighbor")
                    .gblur(sigma=self.settings.blur_sigma, steps=3)
                )
            elif ClipMode.BLUR in mode:
                # steps > 1 makes a high sigma actually look blurred.
                video = video.gblur(sigma=self.settings.blur_sigma, steps=3)
            else:
                video = None  # straight copy, no re-encode of the video filter chain

            if video is None:
                _ = stream.output(filename=str(output_path)).run(overwrite_output=True)
            elif self._has_audio():
                _ = ffmpeg.output(video, stream.audio, filename=str(output_path)).run(
                    overwrite_output=True
                )
            else:
                _ = ffmpeg.output(video, filename=str(output_path)).run(
                    overwrite_output=True
                )
            return output_path

        except Exception as e:
            secho(f"Video failed: {e}", fg=typer.colors.RED)


# class Editor:
#     def __init__(self, video: InputNode, ):
#         self.video = video

#     @property
#     def clip(self, settings: ClipSettings) -> Clip:
#         return Clip(
#             self.video,
#             settings,
#         )
