# core/entities/render_settings.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from pathlib import Path

from constants import DEFAULT_FPS


@dataclass(slots=True, kw_only=True)
class RenderSettings:
    """
    RenderSettings stores the Manim rendering configuration applied to
    every scene in the project.

    A project is composed of multiple scenes. Each scene is an independent
    Manim animation that gets rendered separately into its own video clip.
    These clips are later stitched together by the export service to
    produce the final video.

    The values defined here are project-level defaults. Individual Scene
    entities can override render_quality and render_fps with their own
    scene-level fields.

    This entity does not invoke Manim, write files, or manage processes.
    It is a pure data container read by the rendering service to know
    how each scene clip should be drawn.
    """

    # === Quality / Resolution ===

    # Manim quality preset that controls the output video dimensions.
    # Accepted values and their resolutions:
    #   "low"           →  854 x 480   (-ql)
    #   "medium"        → 1280 x 720   (-qm)
    #   "high"          → 1920 x 1080  (-qh)
    #   "production_4k" → 3840 x 2160  (-qk)
    render_quality: str = "medium"

    # === Frame Rate ===

    # Frames per second for the rendered scene output.
    render_fps: int = DEFAULT_FPS

    # === Output ===

    # Directory where Manim writes the rendered scene clip.
    # Defaults to None — the rendering service resolves the actual path
    # from the project folder structure at runtime.
    render_output_dir: Optional[Path] = None
