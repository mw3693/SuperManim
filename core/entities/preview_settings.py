# File location: /home/mina/SuperManim/core/entities/preview_settings.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class PreviewSettings:
    """
    PreviewSettings stores the configuration for generating quick
    preview videos of individual scenes.

    Every value in this entity is a system constant — they are not
    designed to be changed by the user. The entire preview system
    is built around the assumption that previews always use 480p
    resolution and 30 FPS to guarantee fast generation.

    Preview files are stored separately from full render files to
    prevent any mix-up between draft and production output.

    This entity does not perform rendering, invoke Manim, or play
    video files. It is a pure data container — a set of fixed
    instructions that the preview service reads to know how to
    configure Manim for quick draft generation.
    """

    # === Preview Visual Quality (system constants — not user-configurable) ===
    preview_resolution: str = "854x480"    # 480p. Fixed for speed.
    preview_fps:        int = 30           # Half of render fps. Fixed for speed.

    # === Preview Output Location ===
    preview_output_dir: str = "previews/"  # Separate from render output to avoid mix-ups.
