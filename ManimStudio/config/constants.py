# =========================================
# Project Directory Constants
# =========================================

from __future__ import annotations
from pathlib import Path

__all__ = (
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
)

# =========================================
# Audio directories
# =========================================
AUDIO_CLIPS_DIR: Path     = Path("audio_clips")        # Main audio folder
AUDIO_RAW_DIR: Path       = AUDIO_CLIPS_DIR / "raw"    # Original audio files
AUDIO_EDITED_DIR: Path    = AUDIO_CLIPS_DIR / "edited" # Edited audio files
AUDIO_PROCESSED_DIR: Path = AUDIO_CLIPS_DIR / "processed" # Final audio outputs

# =========================================
# Video directories
# =========================================
VIDEO_CLIPS_DIR: Path     = Path("video_clips")        # Main video folder
VIDEO_RAW_DIR: Path       = VIDEO_CLIPS_DIR / "raw"    # Original video files
VIDEO_EDITED_DIR: Path    = VIDEO_CLIPS_DIR / "edited" # Edited video files
VIDEO_PROCESSED_DIR: Path = VIDEO_CLIPS_DIR / "processed" # Final video outputs

# =========================================
# Scenes directories
# =========================================
SCENES_DIR: Path          = Path("scenes")             # Main scenes folder


# =========================================
# Previews and exports
# =========================================
PREVIEWS_DIR: Path        = Path("previews")           # Project previews
EXPORTS_DIR: Path         = Path("exports")            # Final exported videos

# =========================================
# Cache directory
# =========================================
CACHE_DIR: Path           = Path("cache")              # Temporary data storage


# =========================================
# The name of the SQLite database file
# =========================================
# Name of the SQLite database file residing inside every project folder.
# Defining it here ensures all modules reference the identical filename.
PROJECT_DB_FILENAME: str = "project_data.db"

