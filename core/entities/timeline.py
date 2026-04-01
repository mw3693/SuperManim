# File location: /home/mina/SuperManim/core/entities/timeline.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Timeline:
    """
    The Timeline Entity represents the ordered arrangement of all scenes
    in a project and the computed overall duration of the final video.

    It is a pure data container. It holds ordering information and
    calculated totals. It does not compute anything itself — the
    TimelineService computes all values and stores them here.

    All timing values are in milliseconds as integers.
    """

    # ── GROUP 2 — SUMMARY ─────────────────────────────────────────────
    total_duration:         int             = 0
    scene_count:            int             = 0

    # ── GROUP 3 — ORDERED SCENE IDs ──────────────────────────────────
    ordered_scene_ids:      List[int]       = field(default_factory=list)

    # ── GROUP 4 — SYNCHRONIZATION ─────────────────────────────────────
    audio_total_duration:   Optional[float] = None
    is_synced_with_audio:   bool            = False

    # ── GROUP 5 — VALIDATION ──────────────────────────────────────────
    has_gaps:               bool            = False
    is_complete:            bool            = False

   
