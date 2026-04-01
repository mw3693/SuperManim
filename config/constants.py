"""
SuperManim — Global Constants Module
=====================================
File: /SuperManim/config/constants.py

This module is the single source of truth for all compile-time constants used
across the SuperManim tool.  Every value that is fixed at design time — such as
supported formats, dimension limits, default settings, path conventions, and
pipeline parameters — is declared here once and imported wherever it is needed.

Why centralise constants?
--------------------------
* **Consistency** — every module that reads ``MAX_AUDIO_DURATION_MS`` gets
  exactly the same value; there is no risk of two modules using slightly
  different magic numbers.
* **Maintainability** — changing a project-wide setting (e.g. the hash
  algorithm or the CLI prompt) is a single-line edit in one file.
* **Readability** — named constants communicate intent far better than raw
  literals scattered through business logic.
* **Testability** — tests can import and verify constants directly rather
  than relying on implicit behaviour buried inside functions.

Organisation
-------------
The constants are grouped into numbered sections that mirror the Technical
Design Document (TDD):

    1.1  Operating-System Constants
    1.2  Audio Constants
    1.3  Video Constants
    1.4  Scene Constants
    1.5  Project Constants
    1.6  Application Data Path Constants
    1.7  Session and Recent-Projects Constants
    1.8  Hash and Cache Constants
    1.9  CLI and Output-Formatting Constants
    1.10 Render Pipeline Constants
    1.11 Export Constants

Usage
------
    from SuperManim.config.constants import (
        OS_TYPE,
        SUPPORTED_AUDIO_FORMATS,
        VIDEO_PRESETS,
        DEFAULT_FPS,
        ...
    )

Note: This module has **no side-effects** beyond computing the OS-dependent
path values at import time.  It is safe to import from anywhere in the project.
"""

from __future__ import annotations
from math import ceil

from pathlib import Path
import platform 
from platformdirs import user_data_dir



# ──────────────────────────────────────────────────────────────────────────────
# __all__
# Explicitly controls what is exported when a caller does ``from constants import *``.
# Every public constant defined below is listed here in the same order as it
# appears in the module so that the list is easy to keep in sync.
# ──────────────────────────────────────────────────────────────────────────────
__all__ = [
    # § 1.1 — Operating System
    "OS_TYPE",
    "WINDOWS_RESERVED_NAMES",
    "WINDOWS_INVALID_CHARS",
    "LINUX_INVALID_CHARS",

    # § 1.2 — Audio
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

    # § 1.3 — Video
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

    # § 1.4 — Scenes
    "BUILD_MODE_DEV",
    "BUILD_MODE_FAST",
    "BUILD_MODE_PRODUCTION",
    "VALID_BUILD_MODES",
    "DEFAULT_BUILD_MODE",
    "STATUS_PENDING",
    "STATUS_RENDERED",
    "STATUS_MODIFIED",
    "STATUS_FAILED",
    "STATUS_SKIPPED",
    "MIN_SCENE_DURATION_MS",
    "MIN_SCENES_NUMBER",
    "SCENE_ID_PAD_WIDTH",
    "DEFAULT_SCENE_FPS",
    "MAX_SCENES_NUMBER",

    # § 1.5 — Project
    "DEFAULT_BASE_PATH",
    "MIN_ABS_DISK_SPACE_GB",
    "PROJECT_SUBDIRS",
    "ASSETS_SUBDIRS",
    "DEFAULT_AUDIO_BITRATE_KBPS",
    "INTERMEDIATE_COMPRESSION_RATIO",
    "SAFETY_MARGIN",
    "PROJECT_DB_FILENAME",
    "MIN_PROJECT_NAME_LENGTH",
    "MAX_PROJECT_NAME_LENGTH",

    # § 1.6 — Application Data Paths
    "APP_DATA_FOLDER_NAME",
    "SESSION_DB_FILENAME",
    "APP_DATA_DIR",
    "SESSION_DB_PATH",

    # § 1.7 — Session / Recent Projects
    "MAX_RECENT_PROJECTS",

    # § 1.8 — Hash and Cache
    "HASH_ALGORITHM",
    "CACHE_STATUS_VALID",
    "CACHE_STATUS_INVALID",

    # § 1.9 — CLI and Output Formatting
    "CLI_PROMPT",
    "TOOL_NAME",
    "TOOL_VERSION",
    "CLI_SEPARATOR",

    # § 1.10 — Render Pipeline
    "RENDER_TIMEOUT_SECONDS",
    "MAX_RENDER_RETRIES",

    # § 1.11 — Export
    "EXPORT_FILENAME_TEMPLATE",
    "MAX_EXPORT_FILE_SIZE_GB",
]


# ══════════════════════════════════════════════════════════════════════════════
# § 1.1 — OPERATING-SYSTEM CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

# Standardise the platform identifier to lower-case so comparisons are
# case-insensitive regardless of what sys.platform returns.
_sys = platform.system().lower()
OS_TYPE = "Windows" if _sys == "windows" else "Linux" if _sys == "linux" else "macOS" if _sys == "darwin" else "Unknown"

# ---------------------------------------------------------------------------
# Windows reserved device names — cannot be used as file or folder names.
# frozenset gives O(1) membership testing and prevents accidental mutation.
# ---------------------------------------------------------------------------
WINDOWS_RESERVED_NAMES: frozenset[str] = frozenset({
    "CON", "PRN", "AUX", "NUL",
    "COM1", "COM2", "COM3", "COM4", "COM5",
    "COM6", "COM7", "COM8", "COM9",
    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5",
    "LPT6", "LPT7", "LPT8", "LPT9",
})

# Characters that Windows forbids inside file and folder names.
WINDOWS_INVALID_CHARS: frozenset[str] = frozenset({
    "<", ">", ":", '"', "/", "\\", "|", "?", "*",
})

# Characters that Linux forbids inside file and folder names.
# Only the path separator and the null byte are illegal on Linux.
LINUX_INVALID_CHARS: frozenset[str] = frozenset({
    "/",
    "\0",  # NULL character — terminates C strings in the kernel
})


# ══════════════════════════════════════════════════════════════════════════════
# § 1.2 — AUDIO CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

# File-extension formats the tool can accept as audio input.
# frozenset: O(1) lookup, immutable by design.
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


# ══════════════════════════════════════════════════════════════════════════════
# § 1.3 — VIDEO CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

# ---------------------------------------------------------------------------
# Private resolution tuples — referenced by VIDEO_PRESETS below.
# Using private aliases avoids repeating the same tuple multiple times and
# makes it trivial to change a resolution in one place.
# ---------------------------------------------------------------------------
_RES_4K       = (3840, 2160)   # 16:9  UHD / 4K
_RES_1080     = (1920, 1080)   # 16:9  Full HD
_RES_720      = (1280, 720)    # 16:9  HD
_RES_VERTICAL = (1080, 1920)   # 9:16  Shorts / TikTok / Reels
_RES_SQUARE   = (1080, 1080)   # 1:1   Instagram post
_RES_SD       = (640,  480)    # 4:3   Standard Definition / VGA
_RES_CINEMA   = (2560, 1080)   # 21:9  CinemaScope / UltraWide
_RES_IPAD     = (1536, 2048)   # 3:4   iPad portrait

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


# ══════════════════════════════════════════════════════════════════════════════
# § 1.4 — SCENE CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

# Build modes — control the quality / speed trade-off in the render pipeline.
BUILD_MODE_DEV:        str = "dev"         # Fast, low-quality; for rapid iteration
BUILD_MODE_FAST:       str = "fast"        # Medium quality; for review passes
BUILD_MODE_PRODUCTION: str = "production"  # Full quality; for final export

VALID_BUILD_MODES: frozenset[str] = frozenset({
    BUILD_MODE_DEV,
    BUILD_MODE_FAST,
    BUILD_MODE_PRODUCTION,
})

DEFAULT_BUILD_MODE: str = BUILD_MODE_PRODUCTION

# Scene lifecycle states used by scene_manager.py and renderer_manager.py.
STATUS_PENDING:  str = "pending"    # Defined but not yet rendered
STATUS_RENDERED: str = "rendered"   # Successfully rendered
STATUS_MODIFIED: str = "modified"   # Source changed after last render
STATUS_FAILED:   str = "failed"     # Render ended with an error
STATUS_SKIPPED:  str = "skipped"    # Skipped due to a valid cache hit

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


# ══════════════════════════════════════════════════════════════════════════════
# § 1.5 — PROJECT CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

# Cross-platform default directory where new projects are created.
# os.path.expanduser("~") resolves to the user's home folder on every OS.

DEFAULT_BASE_PATH: Path = Path.home() / "SuperManimProjects"

# Absolute floor for available disk space — must be free before the tool
# even attempts to create the initial project structure.
MIN_ABS_DISK_SPACE_GB: float = 3.0  # gigabytes

# Ordered tuple of top-level subdirectories created inside every project folder.
# A tuple (not a list) signals that this sequence is fixed and should not change.
PROJECT_SUBDIRS: tuple[str, ...] = (
    "audio_clips",  # Audio files used in the project
    "scenes",       # Scene scripts and their render output
    "previews",     # Low-quality preview renders
    "exports",      # Final exported video files
    "assets",       # External media (images, videos, fonts, sounds, templates)
    "temp",         # Intermediate render files; may be cleaned automatically
    "backup",       # Project backups
    "cache",        # Cached render results for incremental builds
)

# Subdirectories created inside the ``assets/`` folder, organised by media type.
ASSETS_SUBDIRS: tuple[str, ...] = (
    "photos",     # Static image files
    "videos",     # Video clip files
    "templates",  # Pre-built Manim scene templates
    "fonts",      # Custom font files
    "sounds",     # Short sound effects
)

# ── Dynamic disk-space estimation ────────────────────────────────────────────

# Default audio bitrate used in space-estimation calculations.
DEFAULT_AUDIO_BITRATE_KBPS: int = 320  # kilobits per second

# Ratio of actual disk usage to raw uncompressed frame size.
# 0.15 means compressed frames occupy ~15 % of the raw pixel data.
INTERMEDIATE_COMPRESSION_RATIO: float = 0.15

# Multiplier applied to the raw estimate to create a safety buffer.
SAFETY_MARGIN: float = 1.3

# Name of the SQLite database file residing inside every project folder.
# Defining it here ensures all modules reference the identical filename.
PROJECT_DB_FILENAME: str = "project_data.db"

# Project-name length limits.
# Windows has a 260-character path ceiling; keeping names ≤ 50 chars leaves
# ample room for deep subdirectory trees within that limit.
MIN_PROJECT_NAME_LENGTH: int = 3
MAX_PROJECT_NAME_LENGTH: int = 50


# ══════════════════════════════════════════════════════════════════════════════
# § 1.6 — APPLICATION DATA PATH CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════
APP_DATA_FOLDER_NAME: str = "SuperManim"
SESSION_DB_FILENAME: str = "session.db"

APP_DATA_DIR: Path = Path(user_data_dir(APP_DATA_FOLDER_NAME))
SESSION_DB_PATH: Path = APP_DATA_DIR / SESSION_DB_FILENAME


# ══════════════════════════════════════════════════════════════════════════════
# § 1.7 — SESSION AND RECENT-PROJECTS CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

# Maximum entries kept in the "recently opened projects" list inside session.db.
# When the list is full, the oldest entry is evicted to make room for the new one.
MAX_RECENT_PROJECTS: int = 10


# ══════════════════════════════════════════════════════════════════════════════
# § 1.8 — HASH AND CACHE CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

# Hashing algorithm used by hash_service.py and sha256_hash_computer.py to
# fingerprint scene source files and detect changes between renders.
# SHA-256 is fast for small files, collision-resistant, and available in
# Python's built-in hashlib without any third-party dependency.
HASH_ALGORITHM: str = "sha256"

# Validity states for rows in the cache_records database table.
CACHE_STATUS_VALID:   str = "valid"    # Fingerprint is current; scene may be skipped
CACHE_STATUS_INVALID: str = "invalid"  # Fingerprint is stale; scene must be re-rendered


# ══════════════════════════════════════════════════════════════════════════════
# § 1.9 — CLI AND OUTPUT-FORMATTING CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

# Prompt string displayed in the interactive shell while awaiting user input.
CLI_PROMPT: str = "supermanim> "

# Official tool name — used in help output, error messages, and log files.
TOOL_NAME: str = "SuperManim"

# Semantic version (MAJOR.MINOR.PATCH).
# Increment MAJOR on breaking changes, MINOR on new backward-compatible
# features, and PATCH on bug fixes.
TOOL_VERSION: str = "1.0.0"

# Horizontal rule used to separate sections in CLI output.
# 60 "─" characters produce a clean, readable divider on standard terminals.
CLI_SEPARATOR: str = "─" * 60


# ══════════════════════════════════════════════════════════════════════════════
# § 1.10 — RENDER PIPELINE CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

# Maximum wall-clock seconds the tool will wait for Manim to render one scene.
# If the process exceeds this limit it is killed and the scene is marked FAILED.
# 600 s (10 min) is generous enough for complex 4K scenes yet short enough
# to catch runaway or deadlocked processes promptly.
RENDER_TIMEOUT_SECONDS: int = 600  # 10 minutes per scene

# Number of automatic retries after a scene render failure before the scene is
# permanently marked as STATUS_FAILED.
# With MAX_RENDER_RETRIES = 2, total attempts = 1 (initial) + 2 (retries) = 3.
MAX_RENDER_RETRIES: int = 2


# ══════════════════════════════════════════════════════════════════════════════
# § 1.11 — EXPORT CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

# Template for the final exported video's base filename (without extension).
# The file extension is appended separately based on the chosen video format.
#
# Example:
#   EXPORT_FILENAME_TEMPLATE.format(project_name="MyAnimation") + ".mp4"
#   → "MyAnimation_final.mp4"
EXPORT_FILENAME_TEMPLATE: str = "{project_name}_final"

# Hard ceiling on the size of the final exported video file.
# 50 GB comfortably covers a 1-hour 4K video at very high bitrate while still
# protecting against runaway exports caused by misconfigured settings.
MAX_EXPORT_FILE_SIZE_GB: float = 50.0  # gigabytes
