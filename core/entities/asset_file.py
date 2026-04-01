# File location: /home/mina/SuperManim/core/entities/asset_file.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class AssetFile:
    """
    The AssetFile Entity represents one supporting file used by a
    Manim animation scene — such as an image, SVG, or font file.

    It is a pure data container. It holds the path, type, and metadata
    of the asset file, and links it to the scene that uses it.

    It does NOT read files from disk. It does NOT load images.
    It is just structured data.
    """

    # ── GROUP 1 — IDENTITY ────────────────────────────────────────────
    asset_file_id:              int

    # ── GROUP 2 — LINKING ─────────────────────────────────────────────
    scene_id:                   Optional[int]   = None

    # ── GROUP 3 — LOCATION ────────────────────────────────────────────
    asset_file_path:            Optional[str]   = None
    asset_file_original_name:   Optional[str]   = None

    # ── GROUP 4 — TYPE AND FORMAT ─────────────────────────────────────
    asset_file_type:            str             = "image"
    asset_file_format:          Optional[str]   = None

    # ── GROUP 5 — TECHNICAL PROPERTIES ───────────────────────────────
    asset_file_size_bytes:      Optional[int]   = None

    # ── GROUP 6 — HASH ────────────────────────────────────────────────
    asset_file_hash:            Optional[str]   = None

