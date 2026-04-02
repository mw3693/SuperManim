# File location: /home/mina/SuperManim/core/entities/render_settings.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class RenderSettings:
    """
    RenderSettings stores all configuration for how Manim renders
    animation scenes in a project, along with cached statistics
    counters that track scene progress.

    It describes resolution, frame rate, background color, quality
    presets, output directory, and the current count of scenes
    broken down by status.

    This entity does not perform rendering, invoke Manim, or manage files.
    It is a pure data container — a set of instructions that rendering
    services read to know how each scene should be drawn and how far
    along the project is.

    These values serve as project-level defaults. Individual Scene
    entities can override the rendering values with their own
    scene_resolution, scene_fps, and scene_background_color fields.

    The statistics counters are automatically maintained by the scene
    management service and must always satisfy:
        project_total_scenes == project_rendered_scenes
                              + project_pending_scenes
                              + project_failed_scenes
    """

        
    # === Scene Statistics (cached counters) ===
    project_total_scenes:         int   = 0
    project_rendered_scenes:      int   = 0
    project_pending_scenes:       int   = 0
    project_failed_scenes:        int   = 0

# === Visual Quality ===
    render_resolution:           Optional[str]    = "1920x1080"
    render_fps:                   Optional[int]   = 30
