
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class SubScene:
    """
    The SubScene Entity represents one animation block inside a Scene.

    It represents a distinct phase or moment within the Scene's animation
    sequence. Like the Scene Entity, it is a pure data container.
    It holds information only. It does not call any external tools,
    does not run Manim, and does not talk to any database.

    TIMING CONVENTION:
    All timing fields (subscene_duration, subscene_start_time,
    subscene_end_time) are stored as integers in MILLISECONDS,
    consistent with the parent Scene entity.

    IMPORTANT RULE:
    The sum of all subscene_duration values within one Scene MUST
    equal the parent Scene's scene_duration. If they do not add up
    correctly, the SubScenes do not fully cover the Scene, which is
    a data integrity error.
    """

    # ── GROUP 1 — IDENTITY ────────────────────────────────────────────
    subscene_id:            int
    subscene_name:          Optional[str]    = None
    subscene_index:         int              = 0
    parent_scene_id:        int              = 0

    # ── GROUP 2 — TIMING (relative to start of parent Scene, in ms) ───
    subscene_duration:      Optional[int]    = None
    subscene_start_time:    Optional[int]    = None
    subscene_end_time:      Optional[int]    = None

    # ── GROUP 3 — CONTENT ─────────────────────────────────────────────
    subscene_content:       Optional[str]    = None
    subscene_code_path:     Optional[str]    = None
    subscene_hash:          Optional[str]    = None

    # ── GROUP 4 — STATUS ──────────────────────────────────────────────
    subscene_status:        str              = "pending"
    subscene_output_path:   Optional[str]    = None

    # ── ALLOWED VALUES FOR subscene_status ────────────────────────────
    # "pending"   → block exists but has not been processed yet
    # "rendered"  → block was rendered successfully
    # "failed"    → processing was attempted but failed
    # "skipped"   → skipped because nothing changed (hash match)


@dataclass
class Scene:
    """
    The Scene Entity represents one section of the animation video.

    This is a pure data container — a filing card that holds all the
    information about one scene. It does not call any external tools,
    does not open databases, does not run Manim, does not call print().
    It is just structured data.

    A Scene can contain zero or more SubScene objects inside its
    scene_map list. SubScenes represent the individual animation
    blocks that make up this scene.

    TIMING CONVENTION:
    All timing fields (scene_duration, scene_start_time, scene_end_time)
    are stored as integers in MILLISECONDS.
    Example: 16.8 seconds is stored as 16800.
    This avoids floating-point rounding errors in arithmetic.
    """

    # ── GROUP 1 — IDENTITY ────────────────────────────────────────────
    scene_id:                       int
    scene_name:                     Optional[str]   = None
    scene_index:                    int             = 0
    previous_scene_id:              Optional[int]   = None
    next_scene_id:                  Optional[int]   = None

    # ── GROUP 2 — TIMING (stored in milliseconds as integers) ─────────
    scene_duration:                 Optional[int]   = None
    scene_start_time:               Optional[int]   = None
    scene_end_time:                 Optional[int]   = None
    scene_start_marker:             Optional[str]   = None
    scene_end_marker:               Optional[str]   = None

    # ── GROUP 3 — CODE ────────────────────────────────────────────────
    scene_code_path:                Optional[str]   = None
    scene_code_content:             Optional[str]   = None

    # ── GROUP 4 — HASH FINGERPRINTS ───────────────────────────────────
    scene_code_hash:                Optional[str]   = None
    scene_assets_hash:              Optional[str]   = None
    scene_audio_hash:               Optional[str]   = None
    final_scene_hash:               Optional[str]   = None

    # ── GROUP 5 — CONTENT AND VISUAL SETTINGS ─────────────────────────
    scene_content:                  Optional[str]   = None
    scene_background_color:         str             = "#000000"
    scene_resolution:               str             = "1920x1080"
    scene_fps:                      int             = 60

    # ── GROUP 6 — STATUS AND OUTPUT ───────────────────────────────────
    scene_status:                   str             = "pending"
    scene_output_path:              Optional[str]   = None
    scene_preview_path:             Optional[str]   = None
    scene_error_message:            Optional[str]   = None
    scene_rendered_at:              Optional[str]   = None
    scene_render_duration:          Optional[float] = None

    # ── GROUP 7 — AUDIO ───────────────────────────────────────────────
    related_audio_clip_path:        Optional[str]   = None
    synced_with_audio:              bool            = False

    # ── GROUP 8 — SUBSCENES ───────────────────────────────────────────
    # field(default_factory=list) is used instead of [] because in Python
    # mutable default arguments are shared between instances. Using
    # default_factory=list gives each Scene its own fresh empty list.
    scene_map:                      List["SubScene"] = field(default_factory=list)

    # ── ALLOWED VALUES FOR scene_status ───────────────────────────────
    # "pending"   → scene exists but has never been rendered
    # "rendered"  → scene was rendered successfully
    # "failed"    → render was attempted but failed with an error
    # "skipped"   → render was skipped because nothing changed (hash match)
