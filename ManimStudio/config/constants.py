from __future__ import annotations
from pathlib import Path

__all__ = (
    # ── Directories ───────────────────────────────────────────────────────
    "AUDIO_CLIPS_DIR",
    "AUDIO_RAW_DIR",
    "AUDIO_EDITED_DIR",
    "AUDIO_PROCESSED_DIR",
    "VIDEO_CLIPS_DIR",
    "VIDEO_RAW_DIR",
    "VIDEO_EDITED_DIR",
    "VIDEO_PROCESSED_DIR",
    "SCENES_DIR",
    "PREVIEWS_DIR",
    "EXPORTS_DIR",
    "CACHE_DIR",
    # ── Project ───────────────────────────────────────────────────────────
    "PROJECT_DB_FILENAME",
    # ── Audio ─────────────────────────────────────────────────────────────
    "SUPPORTED_AUDIO_FORMATS",
    "MAX_AUDIO_DURATION_MS",
    "MIN_AUDIO_DURATION_MS",
    "DEFAULT_AUDIO_SAMPLE_RATE",
    "MAX_AUDIO_FILE_SIZE_MB",
    "SUPPORTED_AUDIO_CHANNELS",
    "SUPPORTED_SAMPLE_RATES",
    "DEFAULT_AUDIO_BITRATE",
    "DEFAULT_SILENCE_THRESHOLD_DB",
    "DEFAULT_FADE_DURATION_MS",
    "DEFAULT_AUDIO_CHANNEL",
    "DEFAULT_AUDIO_FORMAT",
    # ── Video ─────────────────────────────────────────────────────────────
    "VIDEO_PRESETS",
    "SUPPORTED_VIDEO_FORMATS",
    "DEFAULT_VIDEO_FORMAT",
    "SUPPORTED_FPS",
    "DEFAULT_FPS",
    "DEFAULT_VIDEO_WIDTH",
    "DEFAULT_VIDEO_HEIGHT",
    "DEFAULT_VIDEO_DIMENSIONS",
    "MAX_VIDEO_WIDTH",
    "MAX_VIDEO_HEIGHT",
    "MAX_VIDEO_DIMENSIONS",
    "MIN_VIDEO_WIDTH",
    "MIN_VIDEO_HEIGHT",
    "MIN_VIDEO_DIMENSIONS",
    "MAX_TOTAL_VIDEO_DURATION_MS",
    "SUPPORTED_VIDEO_CODECS",
    "DEFAULT_VIDEO_CODEC",
    "DEFAULT_VIDEO_BITRATE",
    "SUPPORTED_ASPECT_RATIOS",
    "RENDER_QUALITY_PRESETS",
    # ── Scenes ────────────────────────────────────────────────────────────
    "STATUS_PENDING",
    "STATUS_RENDERED",
    "STATUS_MODIFIED",
    "STATUS_FAILED",
    "STATUS_SKIPPED",
    "MIN_SCENE_DURATION_MS",
    "MIN_SCENES_NUMBER",
    "MAX_SCENES_NUMBER",
    "SCENE_ID_PAD_WIDTH",
    "DEFAULT_SCENE_FPS",
)


# =========================================
# Project Directory Constants
# =========================================

# Audio directories

AUDIO_CLIPS_DIR: Path     = Path("audio_clips")           # Main audio folder
AUDIO_RAW_DIR: Path       = AUDIO_CLIPS_DIR / "raw"       # Original audio files
AUDIO_EDITED_DIR: Path    = AUDIO_CLIPS_DIR / "edited"    # Edited audio files
AUDIO_PROCESSED_DIR: Path = AUDIO_CLIPS_DIR / "processed" # Final audio outputs

# Video directories

VIDEO_CLIPS_DIR: Path     = Path("video_clips")           # Main video folder
VIDEO_RAW_DIR: Path       = VIDEO_CLIPS_DIR / "raw"       # Original video files
VIDEO_EDITED_DIR: Path    = VIDEO_CLIPS_DIR / "edited"    # Edited video files
VIDEO_PROCESSED_DIR: Path = VIDEO_CLIPS_DIR / "processed" # Final video outputs

# Scenes directories

SCENES_DIR: Path = Path("scenes")  # Main scenes folder

# Previews and exports

PREVIEWS_DIR: Path = Path("previews")  # Project previews
EXPORTS_DIR: Path  = Path("exports")   # Final exported videos

# Cache directory

CACHE_DIR: Path = Path("cache")  # Temporary data storage

# Name of the SQLite database file residing inside every project folder.
# Defining it here ensures all modules reference the identical filename.
PROJECT_DB_FILENAME: str = "project_data.db"


# =========================================
# Audio Constants
# =========================================

SUPPORTED_AUDIO_FORMATS: frozenset[str] = frozenset({
    ".mp3",
    ".wav",
    ".m4a",
    ".aac",
    ".ogg",
    ".flac",
    ".opus",
})

# Maximum audio file duration the tool will process (~1 hour).
MAX_AUDIO_DURATION_MS: int = 3_600_000  # milliseconds

# Minimum audio file duration.
# Files shorter than 100 ms may crash signal-processing algorithms.
MIN_AUDIO_DURATION_MS: int = 100  # milliseconds

# Standard CD-quality sample rate used as the project default.
DEFAULT_AUDIO_SAMPLE_RATE: int = 44_100  # Hz

# Upper bound on audio file size.
# Even within the 1-hour duration limit, uncompressed WAV files can be huge.
# Rejecting oversized files early prevents memory exhaustion.
MAX_AUDIO_FILE_SIZE_MB: int = 800  # megabytes

# Mono (1) and Stereo (2) are the only channel layouts the tool handles.
SUPPORTED_AUDIO_CHANNELS: frozenset[int] = frozenset({
    1,  # Mono
    2,  # Stereo
})

# Sample rates accepted by the audio pipeline.
# 44 100 Hz → music  |  48 000 Hz → video/broadcast
SUPPORTED_SAMPLE_RATES: frozenset[int] = frozenset({
    22_050,
    32_000,
    44_100,
    48_000,
})

# Default export/conversion bitrate.
# 192 kbps balances perceptual quality with reasonable file size.
DEFAULT_AUDIO_BITRATE: int = 192_000  # bits per second

# dB level below which a segment is classified as silence.
DEFAULT_SILENCE_THRESHOLD_DB: int = -40  # decibels

# Duration of fade-in / fade-out effects applied to audio clips.
# 300 ms feels natural without being perceptibly long.
DEFAULT_FADE_DURATION_MS: int = 300  # milliseconds

# Default number of audio channels for new projects.
DEFAULT_AUDIO_CHANNEL: int = 2  # Stereo

# Default container format for exported audio.
DEFAULT_AUDIO_FORMAT: str = "mp3"


# =========================================
# Video Constants
# =========================================

# ---------------------------------------------------------------------------
# Private resolution tuples — referenced by VIDEO_PRESETS below.
# Using private aliases avoids repeating the same tuple multiple times and
# makes it trivial to change a resolution in one place.
# ---------------------------------------------------------------------------
_RES_4K       = (3840, 2160)  # 16:9  UHD / 4K
_RES_1080     = (1920, 1080)  # 16:9  Full HD
_RES_720      = (1280,  720)  # 16:9  HD
_RES_VERTICAL = (1080, 1920)  # 9:16  Shorts / TikTok / Reels
_RES_SQUARE   = (1080, 1080)  # 1:1   Instagram post
_RES_SD       = ( 640,  480)  # 4:3   Standard Definition / VGA
_RES_CINEMA   = (2560, 1080)  # 21:9  CinemaScope / UltraWide
_RES_IPAD     = (1536, 2048)  # 3:4   iPad portrait

# Universal keyword-to-resolution map.
# All keys must be matched with .lower() so "YouTube", "YOUTUBE", and
# "youtube" all resolve to the same (width, height) tuple.
VIDEO_PRESETS: dict[str, tuple[int, int]] = {
    # ── 16:9 Widescreen ──────────────────────────────────────────────────────
    "4k":        _RES_4K,
    "uhd":       _RES_4K,
    "2160p":     _RES_4K,
    "3840x2160": _RES_4K,
    "youtube":   _RES_1080,
    "fhd":       _RES_1080,
    "1080p":     _RES_1080,
    "16:9":      _RES_1080,
    "1920x1080": _RES_1080,
    "hd":        _RES_720,
    "720p":      _RES_720,
    "1280x720":  _RES_720,

    # ── 9:16 Vertical (Shorts / TikTok / Reels) ──────────────────────────────
    "shorts":    _RES_VERTICAL,
    "tiktok":    _RES_VERTICAL,
    "reels":     _RES_VERTICAL,
    "9:16":      _RES_VERTICAL,
    "1080x1920": _RES_VERTICAL,

    # ── 1:1 Square (Instagram post) ──────────────────────────────────────────
    "instagram": _RES_SQUARE,
    "post":      _RES_SQUARE,
    "square":    _RES_SQUARE,
    "1:1":       _RES_SQUARE,
    "1080x1080": _RES_SQUARE,

    # ── 4:3 Classic (SD / VGA) ───────────────────────────────────────────────
    "sd":        _RES_SD,
    "vga":       _RES_SD,
    "4:3":       _RES_SD,
    "640x480":   _RES_SD,

    # ── 21:9 UltraWide (CinemaScope) ─────────────────────────────────────────
    "cinemascope": _RES_CINEMA,
    "21:9":        _RES_CINEMA,
    "2560x1080":   _RES_CINEMA,

    # ── 3:4 Portrait (iPad) ──────────────────────────────────────────────────
    "ipad":      _RES_IPAD,
    "3:4":       _RES_IPAD,
    "1536x2048": _RES_IPAD,
}

# Container formats the tool can produce as final output.
SUPPORTED_VIDEO_FORMATS: frozenset[str] = frozenset({"mp4", "mov", "png"})

# Default output container when the user has not specified one.
DEFAULT_VIDEO_FORMAT: str = "mp4"

# Frame rates supported by the render pipeline.
SUPPORTED_FPS: frozenset[int] = frozenset({
    24,   # Cinematic standard
    25,   # PAL / Europe / Middle East
    30,   # NTSC / YouTube / US broadcast
    48,   # High Frame Rate (HFR)
    50,   # PAL high-rate
    60,   # Smooth motion and gaming
    120,  # Ultra-slow-motion capture
})

# Default frame rate when the user has not specified one.
DEFAULT_FPS: int = 30

# Default output resolution (Full HD 1080p).
DEFAULT_VIDEO_WIDTH:      int = 1920
DEFAULT_VIDEO_HEIGHT:     int = 1080
DEFAULT_VIDEO_DIMENSIONS: tuple[int, int] = (DEFAULT_VIDEO_WIDTH, DEFAULT_VIDEO_HEIGHT)

# Upper resolution ceiling — 4K UHD.
MAX_VIDEO_WIDTH:      int = 3840
MAX_VIDEO_HEIGHT:     int = 2160
MAX_VIDEO_DIMENSIONS: tuple[int, int] = (MAX_VIDEO_WIDTH, MAX_VIDEO_HEIGHT)

# Lower resolution floor — Standard Definition.
# Dimensions below this threshold are rejected before rendering begins.
MIN_VIDEO_WIDTH:      int = 640
MIN_VIDEO_HEIGHT:     int = 480
MIN_VIDEO_DIMENSIONS: tuple[int, int] = (MIN_VIDEO_WIDTH, MIN_VIDEO_HEIGHT)

# Maximum video project duration — 1 hour.
MAX_TOTAL_VIDEO_DURATION_MS: int = 3_600_000  # milliseconds

# Codecs the render pipeline is allowed to use.
SUPPORTED_VIDEO_CODECS: frozenset[str] = frozenset({
    "h264",  # Widest device / browser compatibility
    "h265",  # Better compression; requires newer hardware decode
    "vp9",   # Open-source; preferred for web streaming
})

# Default codec — H.264 offers the best out-of-the-box compatibility.
DEFAULT_VIDEO_CODEC: str = "h264"

# Default video bitrate; 8 Mbps suits Full-HD at 30 fps comfortably.
DEFAULT_VIDEO_BITRATE: int = 8_000_000  # bits per second

# Aspect-ratio strings accepted as user input.
SUPPORTED_ASPECT_RATIOS: frozenset[str] = frozenset({
    "16:9",
    "9:16",
    "1:1",
    "4:3",
    "21:9",
})

# Named quality tiers that map to combinations of resolution, bitrate, etc.
RENDER_QUALITY_PRESETS: frozenset[str] = frozenset({
    "low",
    "medium",
    "high",
    "ultra",
})


# =========================================
# Scenes Constants
# =========================================

# Scene lifecycle states used by scene_manager.py and renderer_manager.py.
STATUS_PENDING:  str = "pending"   # Defined but not yet rendered
STATUS_RENDERED: str = "rendered"  # Successfully rendered
STATUS_MODIFIED: str = "modified"  # Source changed after last render
STATUS_FAILED:   str = "failed"    # Render ended with an error
STATUS_SKIPPED:  str = "skipped"   # Skipped due to a valid cache hit

# Shortest scene the user is allowed to create — 1 second.
# Milliseconds are used throughout to avoid floating-point accumulation errors.
MIN_SCENE_DURATION_MS: int = 1_000  # milliseconds

# A project must contain at least one scene.
MIN_SCENES_NUMBER: int = 1

# Number of digits used for the zero-padded scene index in generated IDs.
# SCENE_ID_PAD_WIDTH = 2  →  scene_01 … scene_99
# SCENE_ID_PAD_WIDTH = 3  →  scene_001 … scene_999
# Usage: f"scene_{index:0{SCENE_ID_PAD_WIDTH}d}"
SCENE_ID_PAD_WIDTH: int = 2

# Default FPS for scene-level operations when no project value is available.
DEFAULT_SCENE_FPS: int = 30

# Maximum number of scenes per project.
# Kept in sync with SCENE_ID_PAD_WIDTH: pad width 2 → max index 99.
MAX_SCENES_NUMBER: int = 99



# =========================================
# Preview Constants
# =========================================

# Manim's lowest built-in quality preset (-ql), 480p at 15 fps.
PREVIEW_VIDEO_WIDTH:  int = 854   # pixels
PREVIEW_VIDEO_HEIGHT: int = 480   # pixels
PREVIEW_FPS:          int = 15    # frames per second

# CRF for libx264 — 35 is fast to encode with acceptable draft quality.
# Range: 0 (lossless) → 51 (worst quality).
PREVIEW_CRF:          int = 35
