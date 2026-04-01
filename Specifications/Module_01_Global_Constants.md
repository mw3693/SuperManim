
# Module 1 Global Constants:
**File location:** `/SuperManim/config/constants.py`

This module is responsible for storing the global constants of the tool. These constants can be found inside
a folder called **config/** folder at this path **/SuperManim/config/constants.py**

### Section 1.1 Operating systems Constants:
#### Subsection 1.1.1 Define the type of operating system:
We have to know what operating system is running on the system:

```python
import sys

# Standardize platform name to lowercase to prevent case-sensitivity issues
_platform_name = sys.platform.lower()

# Identify the Operating System type for environment-specific configurations
if _platform_name == "win32":
    OS_TYPE = "Windows"

elif _platform_name.startswith("linux"): 
    # Using startswith() because some older systems may return 'linux2'
    OS_TYPE = "Linux"

elif _platform_name == "darwin":
    # 'darwin' is the internal kernel name for macOS
    OS_TYPE = "macOS"

else:
    OS_TYPE = "Unknown"
```

The `OS_TYPE` constant stores the name of the operating system. This is used in later modules
to handle path separators, shell commands, and file permissions correctly.

**Possible values:**

| Value       | Meaning |
| ----------- | ------- |
| `"Windows"` | Windows |
| `"Linux"`   | Linux   |
| `"macOS"`   | macOS   |

**Edge Cases:**

* If the operating system returned by `sys.platform` does not match any of the supported values,
the tool exits immediately with an unsupported platform message.

#### Subsection 1.1.2 Define the windows reserved names:
In this subsection, we define a list of all reserved names in the Windows operating system.
These names cannot be used as file or folder names in Windows.

```python
WINDOWS_RESERVED_NAMES = frozenset({
    "CON",
    "PRN",
    "AUX",
    "NUL",

    "COM1",
    "COM2",
    "COM3",
    "COM4",
    "COM5",
    "COM6",
    "COM7",
    "COM8",
    "COM9",

    "LPT1",
    "LPT2",
    "LPT3",
    "LPT4",
    "LPT5",
    "LPT6",
    "LPT7",
    "LPT8",
    "LPT9",
}) 
```


#### Subsection 1.1.3 Define the windows invalid chars:
We also define the invalid characters that cannot be used in file or folder names in the Windows operating system.
These characters have special meanings in the Windows OS, so using them in names may cause conflicts or errors.

```python
# Invalid characters for file and folder names in Windows
WINDOWS_INVALID_CHARS = frozenset({
    "<",
    ">",
    ":",
    '"',
    "/",
    "\\",
    "|",
    "?",
    "*",
})
```


#### Subsection 1.1.4 Define the linux invalid chars:
This subsection lists characters that cannot be used in Linux file or folder names.
Only / (path separator) and \0 (null character) are invalid.

```python

# Invalid characters for file and folder names in Linux
LINUX_INVALID_CHARS = frozenset({
    "/",
    "\0",  # NULL character
})
```

---

### Section 1.2 Audio Constants:
#### Subsection 1.2.1 The Definition of the Supported Audio Formats:
We have to define a list of supported audio formats that the tool can handle correctly.

```python
# Immutable set of supported audio formats
# frozenset ensures:
# - O(1) average lookup time
# - No accidental modification
# - Clear intent: this is a constant lookup table

SUPPORTED_AUDIO_FORMATS = frozenset({
    ".mp3",
    ".wav",
    ".m4a",
    ".aac",
    ".ogg",
    ".flac",
    ".opus",
})
```

We use a frozenset because membership testing runs in constant time O(1)
regardless of the number of elements. In contrast, a list requires
iterating through elements one by one, which takes O(n) time.
Since we do not intend to modify the supported file types during program execution,
immutability here is the professional and appropriate choice.


#### Subsection 1.2.2 Define the maximum audio duration (milliseconds):

```python
# Maximum allowed audio duration
MAX_AUDIO_DURATION_MS = 3600000  # in ms  (~1 hour)
```

This constant can now be used directly in any time-based audio validation or processing function.



#### Subsection 1.2.3 Define The minimum Audio duration:
In this section we will define the minimum audio file duration that
the tool can handle it correctly the  minimum duration of the file
will be 100 millseconds which is 0.1 seconds this will protect us
from crashes caused by processing audio files that are too short to analyze reliably.

```python
MIN_AUDIO_DURATION_MS =  100    # in ms
```



#### Subsection 1.2.4 Define the default sample rate for audio file:

```python
DEFAULT_AUDIO_SAMPLE_RATE = 44100
```

#### Subsection 1.2.5 Define the maximum size of the audio file:
This constant defines the largest audio file size that the tool is allowed to process.

```python
# Maximum allowed audio file size (in megabytes)
MAX_AUDIO_FILE_SIZE_MB = 800
```
Even when the duration of the audio is limited (for example, to one hour),
some audio formats—especially uncompressed formats such as WAV—can still produce very large files.

Processing very large files may require a large amount of memory and can slow down the program
or cause it to fail.By defining a maximum file size, the tool can check the size of the audio file
before processing it.

If the file is larger than the allowed limit, the tool can reject it early and display
a clear error message instead of attempting to process a file that may consume too many system
resources.The value **800 MB** was chosen because it safely covers the approximate size of one
hour of high-quality uncompressed stereo audio while still protecting the program from extremely
large files.

#### Subsection 1.2.6 Define the supported number of audio channels

This constant defines the number of audio channels that the tool supports.

An audio file can contain one channel (Mono) or two channels (Stereo).
Most music, podcasts, and video audio use stereo sound.

By defining the supported channels, the tool can verify that the audio file
uses a format that the system can process correctly.

```python
# Supported number of audio channels
SUPPORTED_AUDIO_CHANNELS = frozenset({
    1,  # Mono audio
    2,  # Stereo audio
})
```

---

#### Subsection 1.2.7 Define the supported sample rates

This constant defines the sample rates that the tool accepts.

The sample rate represents the number of audio samples captured per second.
Different audio files may use different sample rates.

By defining supported values, the tool can validate audio files
and avoid unexpected formats that may cause processing problems.

```python
# Supported sample rates (Hz)
SUPPORTED_SAMPLE_RATES = frozenset({
    22050,
    32000,
    44100,
    48000,
})
```

The most common sample rates are **44100 Hz** for music
and **48000 Hz** for video production.

---

#### Subsection 1.2.8 Define the default audio bitrate

This constant defines the default bitrate used when exporting
or converting audio files.

The bitrate controls the amount of data used to represent the audio.
Higher bitrate usually means better sound quality but larger file size.

```python
# Default audio bitrate (bits per second)
DEFAULT_AUDIO_BITRATE = 192_000
```

A bitrate of **192 kbps** provides good audio quality while keeping
the file size reasonable.

---

#### Subsection 1.2.9 Define the silence detection threshold

This constant defines the sound level that the tool considers to be silence.

Some audio processing operations need to detect silent parts
of the audio in order to remove pauses or split segments.

```python
# Silence detection threshold (decibels)
DEFAULT_SILENCE_THRESHOLD_DB = -40
```

If the audio level falls below **-40 dB**, the tool may treat that
section as silence.

---

#### Subsection 1.2.10 Define the default fade duration

This constant defines the default time used for fade effects.

Fade effects are used to gradually increase or decrease
the volume at the beginning or end of an audio clip.

```python
# Default fade duration in milliseconds
DEFAULT_FADE_DURATION_MS = 300
```

A value of **300 milliseconds** creates a smooth and natural transition
without a sudden change in volume.




#### Subsection 1.2.11 Define the default audio channel:
```python
DEFAULT_AUDIO_CHANNEL = 2
```




#### Subsection 1.2.12 Define the default audio format:
```python
DEFAULT_AUDIO_FORMAT = "mp3"
```

---

### Section 1.3 Video Constants:

#### Subsection 1.3.1 Define the standard video presets or video resolution:

The user will determine the video resolution of the output render using a command in this form:

```
set video_resolution tiktok
set video_resolution youtube
set video_resolution YouTube
set video_resolution instagram
set video_resolution hd
set video_resolution 4k
set video_resolution uhd
```

So we need to store the standard video presets in a `VIDEO_PRESETS` dictionary because we want to
validate the user input. If the user enters `4k` then the tool will make the video 4k and the video
resolution tuple will be `(3840, 2160)` so `video_width = 3840 px` and `video_height = 2160 px`.

The tool will support the following categories.
Each category contains keywords that the user can pass through the `set video_resolution` command.

write it completely:

```python

_RES_4K = (3840, 2160)
_RES_1080 = (1920, 1080)
_RES_720 = (1280, 720)
_RES_VERTICAL = (1080, 1920)
_RES_SQUARE = (1080, 1080)
_RES_SD = (640, 480)
_RES_CINEMA = (2560, 1080)
_RES_IPAD = (1536, 2048)

VIDEO_PRESETS = {
    # --- 16:9 Widescreen ---
    "4k":        _RES_4K,
    "uhd":       _RES_4K,
    "2160p":     _RES_4K,
    "youtube":   _RES_1080,
    "fhd":       _RES_1080,
    "1080p":     _RES_1080,
    "16:9":      _RES_1080,
    "hd":        _RES_720,
    "720p":      _RES_720,
    "3840x2160": _RES_4K,
    "1920x1080": _RES_1080,
    "1280x720":  _RES_720,

    # --- 9:16 Vertical (Shorts / TikTok / Reels) ---
    "shorts":    _RES_VERTICAL,
    "tiktok":    _RES_VERTICAL,
    "reels":     _RES_VERTICAL,
    "9:16":      _RES_VERTICAL,
    "1080x1920": _RES_VERTICAL,

    # --- 1:1 Square (Instagram post) ---
    "instagram": _RES_SQUARE,
    "post":      _RES_SQUARE,
    "square":    _RES_SQUARE,
    "1:1":       _RES_SQUARE,
    "1080x1080": _RES_SQUARE,

    # --- 4:3 Classic (SD / VGA) ---
    "sd":        _RES_SD,
    "vga":       _RES_SD,
    "4:3":       _RES_SD,
    "640x480":   _RES_SD,

    # --- 21:9 UltraWide (CinemaScope) ---
    "cinemascope": _RES_CINEMA,
    "21:9":        _RES_CINEMA,
    "2560x1080":   _RES_CINEMA,

    # --- 3:4 Portrait (iPad) ---
    "ipad":      _RES_IPAD,
    "3:4":       _RES_IPAD,
    "1536x2048": _RES_IPAD,
}


```

This dictionary serves as the "Universal Translator" for the `ProjectSettings` class in `config/project_settings.py`.
It maps user-friendly keywords to high-quality Resolution Tuples (Width, Height).

All keys in this dictionary must be matched using `.lower()` on the user input so that `"YouTube"`,
`"YOUTUBE"`, and `"youtube"` all resolve to the same preset.




#### Subsection 1.3.2 Define the supported output video formats:

The `SUPPORTED_VIDEO_FORMATS` constant lists the video file formats the tool
can produce as the final output.

```python
SUPPORTED_VIDEO_FORMATS = frozenset({"mp4", "mov", "png"})
```


#### Subsection 1.3.3 Define the default output video format:
This constant define the default output video format:
```python

DEFAULT_VIDEO_FORMAT    = "mp4"
```



#### Subsection 1.3.4 Define the supported frame rates:

```python
SUPPORTED_FPS = frozenset({
    24,   # Cinematic standard
    25,   # PAL standard (Europe, Middle East)
    30,   # NTSC standard (YouTube, US)
    48,   # High Frame Rate (HFR)
    50,   # PAL High Rate
    60,   # Smooth motion and gaming
    120   # Ultra slow motion
})

```


#### Subsection 1.3.5 Define the default frame rate:

```python
DEFAULT_FPS = 30
```



#### Subsection 1.3.6 Define the default video dimensions (width, height):

These constants define the upper default  resolution limit for HD rendering.
If the user didn't determine the video dimension then the output video resolution
will be the Default video dimensions.
```python
# Default  video dimensions (Full HD - 1080p)

DEFAULT_VIDEO_WIDTH  = 1920   # Full HD width
DEFAULT_VIDEO_HEIGHT = 1080   # Full HD height

DEFAULT_VIDEO_DIMENSIONS = (DEFAULT_VIDEO_WIDTH, DEFAULT_VIDEO_HEIGHT)
```


### Section 1.3.7 Define the maximum video dimensions :


These constants define the upper  resolution limit for HD rendering.
If the user didn't determine the video dimensions then the output video resolution
will be the Default video dimensions.
```python

MAX_VIDEO_WIDTH  = 3840   # Full 4K width
MAX_VIDEO_HEIGHT = 2160   # Full 4K height

MAX_VIDEO_DIMENSIONS = (MAX_VIDEO_WIDTH, MAX_VIDEO_HEIGHT)
```



#### Subsection 1.3.8 Define the minimum video dimensions :

These constants define the lower resolution limit allowed for rendering.
The system will reject any video dimensions smaller than this threshold
to ensure stability, compatibility, and predictable encoding behavior.

```python
MIN_VIDEO_WIDTH  = 640    # Standard SD minimum width
MIN_VIDEO_HEIGHT = 480    # Standard SD minimum height

MIN_VIDEO_DIMENSIONS = (MIN_VIDEO_WIDTH, MIN_VIDEO_HEIGHT)
```



#### Subsection 1.3.9 Define the Maximum Video Duration:
Any large-scale project requires clear limits. Without these limits,
a user might attempt to process a 10-hour video or consume all available disk space,
which could cause the program to crash.

In your SRS, we defined maximum and minimum values to ensure stable performance.
The maximum video duration that the tool can handle is 1 hour only.

```python
MAX_TOTAL_VIDEO_DURATION_MS  = 3600000  # in ms
```

#### Subsection 1.3.10 Define supported video codecs

This constant lists the video codecs that the tool can use for rendering.
Codecs control how the video is compressed and stored.

```python
# Supported video codecs
SUPPORTED_VIDEO_CODECS = frozenset({
    "h264",  # Most compatible with web and devices
    "h265",  # Better compression, newer devices
    "vp9"    # Open-source, used for web streaming
})
```

---

#### Subsection 1.3.11 Define the default video codec

This constant defines which codec is used if the user doesn't choose one.

```python
# Default video codec for rendering
DEFAULT_VIDEO_CODEC = "h264"
```

H.264 is widely supported and balances quality and file size.

---

#### Subsection 1.3.12 Define default video bitrate

The bitrate controls how much data is used per second of video.
Higher bitrate means better quality but larger file size.

```python
# Default video bitrate (bits per second)
DEFAULT_VIDEO_BITRATE = 8_000_000  # 8 Mbps
```

---

#### Subsection 1.3.13 Define supported aspect ratios

This constant lists the aspect ratios the tool can handle.
It helps validate user input and ensures videos are rendered correctly.

```python
# Supported video aspect ratios
SUPPORTED_ASPECT_RATIOS = frozenset({
    "16:9",
    "9:16",
    "1:1",
    "4:3",
    "21:9"
})
```

---

#### Subsection 1.3.14 Define default render quality presets

Some rendering options use predefined quality levels.
This constant defines the available presets.

```python
# Rendering quality presets
RENDER_QUALITY_PRESETS = frozenset({
    "low",
    "medium",
    "high",
    "ultra"
})
```

These presets can control resolution, bitrate, and other settings automatically.

---

### Section 1.4 Scenes Constants:


#### Subsection 1.4.1 Define the build modes:

Build modes control the quality and speed of the render pipeline.
They are used by `core/renderer_manager.py`.

```python
BUILD_MODE_DEV        = "dev"          # Fast, low quality; for development
BUILD_MODE_FAST       = "fast"         # Medium quality; for review
BUILD_MODE_PRODUCTION = "production"   # Full quality; for final export

VALID_BUILD_MODES    = frozenset({BUILD_MODE_DEV, BUILD_MODE_FAST, BUILD_MODE_PRODUCTION})
DEFAULT_BUILD_MODE   = BUILD_MODE_PRODUCTION
```

#### Subsection 1.4.2 Define the scene status values:

These string constants represent the possible states of a scene or sub-scene
in the render pipeline.
They are used in `core/scene_manager.py` and `core/renderer_manager.py`.

```python
STATUS_PENDING  = "pending"    # Scene defined but not yet rendered
STATUS_RENDERED = "rendered"   # Scene has been successfully rendered
STATUS_MODIFIED = "modified"   # Scene code was changed after last render
STATUS_FAILED   = "failed"     # Scene render failed with an error
STATUS_SKIPPED  = "skipped"    # Scene was skipped because of a cache hit
```


#### Subsection 1.4.3 Define the Minimum Scene Duration:

The minimum scene duration that the user can add or set is 1 second only.

```python
MIN_SCENE_DURATION_MS = 1000  # in ms
```

In audio and video processing, precision is everything.
Using integers in milliseconds helps us avoid floating-point errors
that occur when adding many seconds together.

#### Section 1.4.4 Define the Minimum Number of Scenes:
We have to set the minimum number of scenes to 1 scene only — not negative or zero.
The minimum must be 1, which covers the case where the user wants to treat the entire video as a single scene.

```python
MIN_SCENES_NUMBER = 1 
```


#### Section 1.4.5 — Scene ID Format and Padding Width

The tool generates unique scene identifiers automatically using a zero-padded numerical index.
The padding width determines how many digits are used for the scene number.

```python
# Number of digits for zero-padded scene indices
# Example: With SCENE_ID_PAD_WIDTH = 2
#   scene_01, scene_02, ..., scene_99
# With SCENE_ID_PAD_WIDTH = 3
#   scene_001, scene_002, ..., scene_999

SCENE_ID_PAD_WIDTH = 2
```

**Rationale:**
- 2 digits support up to 99 scenes, which covers 99% of real-world projects.
- 3 digits would be unnecessarily verbose for most users.
- The constant allows future expansion if needed without changing code in multiple places.

**Usage in Module 6:**
```python
scene_id = f"scene_{scene_index:0{SCENE_ID_PAD_WIDTH}d}"
```

**Why this belongs in constants:**
- It is a system-wide formatting rule.
- It never changes during runtime.
- It affects file naming, JSON keys, and user-facing output.
- Centralizing it here ensures consistency across all modules that generate scene IDs.


#### Subsection 1.4.6 — Define the Default Scene Frame Rate

Some tools require a default frames-per-second (FPS) value for scene operations.
This constant sets the standard FPS to use when no other value is provided.

```python
DEFAULT_SCENE_FPS = 30
```

**Rationale:**

* Ensures consistency in video playback and editing.
* Provides a baseline for calculations like frame-based durations.

---

#### Subsection 1.4.7 — Define the Maximum Number of Scenes 

This constant defines the maximum number of scenes that a single project can contain.
Without this limit, a user could add thousands of scenes, which would cause the render
pipeline to consume too much memory and time.

```python
# Maximum number of scenes allowed in a single project
MAX_SCENES_NUMBER = 99
```

**Why 99?**
- It matches the `SCENE_ID_PAD_WIDTH = 2` setting.
  If the padding width is 2 digits, then the maximum scene number is 99.
  `scene_01` through `scene_99` — exactly 99 scenes.
- If you ever change `SCENE_ID_PAD_WIDTH` to 3, you should also change
  `MAX_SCENES_NUMBER` to 999 at the same time.
- This keeps the two constants in sync with each other.

---

### Section 1.5 Project Constants:

#### Subsection 1.5.1 Define the default base Path:
In this subsection we have to define the default base path that the
project will create inside it if the user first create a new project
all these new projects directories will be created inside one default path
in the operating system

```python
import os

# Determine the default base path in a cross-platform way
home_dir = os.path.expanduser("~")  # Works on both Linux and Windows
DEFAULT_BASE_PATH = os.path.join(home_dir, "SuperManimProjects")
```

#### Subsection 1.5.2 Define the General Base Path

The tool has two ways to determine the base path of a project:

1. The user explicitly determines and chooses the base path of the project.
2. The user does not specify a base path for the project.

In both cases, the tool must be smart and correctly determine the base path of the project.

The `BASE_PATH` can be:

1. `BASE_PATH = DEFAULT_BASE_PATH`
2. `BASE_PATH = User-Defined Path`

If the user creates the project using one of these commands:

```
create new_project "Project Name"
```

or

```
create project "Project Name"
```

then the `BASE_PATH` will be `DEFAULT_BASE_PATH`.

If the user creates the project using this command:

```
create new_project "Project Name" path "Path to New Project"
```

then the `BASE_PATH` will be `"Path to New Project"`.

#### Subsection 1.5.3 Define the Minimum Required Project Size
This is the **minimum absolute disk space required
for the tool to run properly and create the basic project structure**.

It only covers the space needed for the initial folders and
the essential project files (such as configuration and JSON files).

It does **not** include the space required later for rendering videos,
cache files, audio processing, or exports.

```python
MIN_ABS_DISK_SPACE_GB = 3.0
```

This value ensures that the tool has enough space to start safely and
create the project without immediately running into disk space issues.

#### Subsection 1.5.4 — Names of Subdirectories in the Project Folder
These are the main folders every project will have.
Each folder has a specific role, like storing media, scenes, previews,
or temporary files.


```python
PROJECT_SUBDIRS = (
    "audio_clips",   # Folder for storing audio files used in the project
    "scenes",        # Folder for the main scene scripts and render output
    "previews",      # Folder for low-quality preview renders
    "exports",       # Folder for final exported video files
    "assets",        # Folder for external media (images, videos, templates, fonts, sounds)
    "temp",          # Temporary folder for intermediate render files
    "backup",        # Folder to store backups of the project
    "cache",         # Folder for storing cached render results
)
```
---

#### Subsection 1.5.5 — Names of Subdirectories Inside the `assets` Folder
These are the folders inside the `assets` directory, organized by type of media.
This helps keep images, videos, templates, fonts, and sounds separate and easy to find.


```python
ASSETS_SUBDIRS = (
    "photos",      # Images used in the project
    "videos",      # Video clips used in the project
    "templates",   # Pre-made scene templates for Manim
    "fonts",       # Custom fonts used in the project
    "sounds",      # Short sound effects for scenes
)
```



#### Subsection 1.5.6 Define the Minimum Project Size

Instead of using a static limit (e.g., 10 GB), which may under- or overestimate requirements,
the tool now uses a **Dynamic Estimation Based on Video, Audio, and Intermediate Frames** to calculate expected disk usage.

This ensures the system verifies enough space for:

* The final encoded video export
* Temporary `cache/` files and raw frames during rendering
* All associated `audio_clips/`
* Logs, backups, and auxiliary project files

---

##### Subsubsection 1.5.3.1 Space Estimation Constants

```python
from math import ceil

# Absolute floor for disk space (safety buffer)
MIN_ABS_DISK_SPACE_GB = 2.0

# Default audio bitrate (kilobits per second)
# Can be overridden per project
DEFAULT_AUDIO_BITRATE_KBPS = 320

# Estimated compression ratio for intermediate frames (raw → compressed)
INTERMEDIATE_COMPRESSION_RATIO = 0.15

# Safety margin applied to total estimated space
SAFETY_MARGIN = 1.3
```

---

##### Subsubsection 1.5.3.2  Calculation Logic

```python
def calculate_required_space_bytes(
    video_bitrate_mbps: float,
    total_video_duration_sec: int,
    width: int = 3840,
    height: int = 2160,
    fps: int = 60,
    audio_bitrate_kbps: int = DEFAULT_AUDIO_BITRATE_KBPS,
    intermediate_compression_ratio: float = INTERMEDIATE_COMPRESSION_RATIO,
    safety_margin: float = SAFETY_MARGIN,
    min_abs_gb: float = MIN_ABS_DISK_SPACE_GB
) -> int:
    """
    Calculates the required disk space in bytes for the project.
    Takes into account video, audio, and intermediate frames, applying
    compression and a safety margin.
    """

    # 1. Estimate final video size in MB (Mbps × seconds ÷ 8)
    video_size_mb = (video_bitrate_mbps * total_video_duration_sec) / 8

    # 2. Estimate audio size in MB (Kbps × seconds ÷ 8 ÷ 1024)
    audio_size_mb = (audio_bitrate_kbps * total_video_duration_sec) / (8 * 1024)

    # 3. Estimate intermediate frames raw size in MB
    raw_frame_size_mb = width * height * 3 / (1024 ** 2)  # Each frame in MB
    num_frames = fps * total_video_duration_sec
    intermediate_size_mb = raw_frame_size_mb * num_frames * intermediate_compression_ratio

    # 4. Total estimated size with safety margin
    total_mb = (video_size_mb + audio_size_mb + intermediate_size_mb) * safety_margin

    # 5. Convert MB → bytes
    required_bytes = ceil(total_mb * 1024 ** 2)

    # 6. Ensure absolute minimum floor
    min_bytes = ceil(min_abs_gb * 1024 ** 3)
    required_bytes = max(required_bytes, min_bytes)

    return required_bytes
```

---

##### Subsubsection 1.5.3.3  Disk Space Guard

```python
import shutil

def has_enough_disk_space(path: str,
                          video_bitrate_mbps: float,
                          total_video_duration_sec: int,
                          width: int = 3840,
                          height: int = 2160,
                          fps: int = 60,
                          audio_bitrate_kbps: int = DEFAULT_AUDIO_BITRATE_KBPS
                          ) -> bool:
    """
    Checks whether the disk at 'path' has enough free space to safely start the project.
    Considers video, audio, intermediate frames, compression, and safety margin.
    """

    required_bytes = calculate_required_space_bytes(
        video_bitrate_mbps,
        total_video_duration_sec,
        width,
        height,
        fps,
        audio_bitrate_kbps
    )

    try:
        _, _, free_bytes = shutil.disk_usage(path)

        if free_bytes < required_bytes:
            print("Error: Insufficient disk space to start this project.")
            print(f"Required (with margin): {round(required_bytes / (1024**3), 2)} GB | "
                  f"Available: {round(free_bytes / (1024**3), 2)} GB")
            return False

        return True

    except (FileNotFoundError, PermissionError, OSError) as e:
        print(f"Error: Could not verify disk space. Path: {path}. Details: {e}")
        return False
```

---

#### Subsection 1.5.7 — Define the Project Database File Name 

This constant defines the standard name of the SQLite database file that lives
inside every project folder.

Every project you create gets its own folder. Inside that folder there is always
one database file called `project_data.db`. This name must be a constant so that
every part of the system that looks for the database file uses the exact same name.

If you only write the string `"project_data.db"` in ten different files by hand,
one typo in one file will cause a very hard-to-find bug. With a constant, you only
write the name once here, and every other file imports it.

```python
# The name of the SQLite database file inside every project folder
PROJECT_DB_FILENAME = "project_data.db"
```

---

#### Subsection 1.5.8 — Define the Project Name Length Limits 

These constants define how long a project name is allowed to be.

The `project_validation_service.py` uses these constants when the user runs
`create project "My Project Name"`. The tool checks the name against these limits
before creating any folder on disk. If the name is too short or too long, the tool
rejects it immediately and shows a clear error message.

```python
# Minimum number of characters a project name must have
MIN_PROJECT_NAME_LENGTH = 3

# Maximum number of characters a project name can have
# Kept short enough to work as a folder name on all operating systems
MAX_PROJECT_NAME_LENGTH = 50
```

**Why 50 characters as the maximum?**
- Windows has a maximum path length of 260 characters.
- A project name becomes a folder name. If the name is very long, the full path to
  files inside the project (like `/projects/VeryLongName/scenes/scene_01/render.mp4`)
  can exceed the Windows path limit and cause errors.
- 50 characters gives the user a generous and readable name while keeping the full
  path length safe on all operating systems.

---

### Section 1.6 — Application Data Path Constants

#### Subsection 1.6.1 — Define the Application Data Folder Path

SuperManim needs to store the `session.db` file in a permanent location on disk.
This location is different for each operating system.
The tool must find the correct location automatically without the user having to
configure anything.

The architecture document specifies these paths:

- **Windows:**  `%APPDATA%\SuperManim\`
  (expands to something like `C:\Users\Ahmed\AppData\Roaming\SuperManim\`)
- **macOS:**    `~/Library/Application Support/SuperManim/`
- **Linux:**    `~/.supermanim/`
  (or `$XDG_DATA_HOME/SuperManim/` if the `XDG_DATA_HOME` environment variable is set)

```python
import os

# The name of the application data folder used on all operating systems
APP_DATA_FOLDER_NAME = "SuperManim"

# The name of the session database file
SESSION_DB_FILENAME = "session.db"

# Compute the correct app data directory based on the operating system
if OS_TYPE == "Windows":
    # os.environ.get("APPDATA") returns the %APPDATA% path on Windows
    _app_data_root = os.environ.get("APPDATA", os.path.expanduser("~"))
    APP_DATA_DIR = os.path.join(_app_data_root, APP_DATA_FOLDER_NAME)

elif OS_TYPE == "macOS":
    APP_DATA_DIR = os.path.join(
        os.path.expanduser("~"),
        "Library",
        "Application Support",
        APP_DATA_FOLDER_NAME
    )

elif OS_TYPE == "Linux":
    # Respect the XDG Base Directory Specification if XDG_DATA_HOME is set
    _xdg_data_home = os.environ.get("XDG_DATA_HOME", "")
    if _xdg_data_home:
        APP_DATA_DIR = os.path.join(_xdg_data_home, APP_DATA_FOLDER_NAME)
    else:
        # Default Linux hidden folder in the user's home directory
        APP_DATA_DIR = os.path.join(os.path.expanduser("~"), ".supermanim")

else:
    # Fallback for any other system — use the home directory
    APP_DATA_DIR = os.path.join(os.path.expanduser("~"), ".supermanim")

# The full path to the session database file
SESSION_DB_PATH = os.path.join(APP_DATA_DIR, SESSION_DB_FILENAME)
```

**Why this belongs in constants:**

The `session.db` path is used in two places: `DatabaseConnectionManager` (to open
the database) and `AppStateService` (to know where to look). If both of them compute
the path independently, a single difference (for example, one uses `".supermanim"` and
the other uses `".SuperManim"`) causes the session file to never be found.
With one constant, both places always use the same path.

---

### Section 1.7 — Session and Recent Projects Constants 

#### Subsection 1.7.1 — Define the Maximum Number of Recent Projects

The `session.db` file stores a list of projects that the user has opened recently.
This list is shown to the user when they run `list recent` so they can quickly reopen
a past project without typing the full path.

The list must have a maximum size. Without a limit, the list grows forever. After many
months of use, the list would contain hundreds of old projects that the user no longer
cares about.

The architecture document specifies a default maximum of 10 recent projects.

```python
# Maximum number of projects stored in the recent projects list in session.db
MAX_RECENT_PROJECTS = 10
```

When a new project is opened and the list already has `MAX_RECENT_PROJECTS` entries,
the oldest entry at the bottom of the list is deleted automatically to make room
for the new entry at the top.

---

### Section 1.8 — Hash and Cache Constants 

#### Subsection 1.8.1 — Define the Hash Algorithm

SuperManim uses a fingerprinting system to detect when a scene's code file has changed.
The fingerprint is a hash — a short string that uniquely represents the content of a file.

The algorithm used to compute this hash must be a constant. If you hardcode the string
`"sha256"` in five different files and later decide to change it to `"sha512"`, you have
to find and update all five files. One constant makes this change a single-line edit.

The folder structure notes in the TDD specifically mention `HASH_ALGORITHM = "sha256"`.

```python
# The hashing algorithm used for scene fingerprinting
# Used by hash_service.py and sha256_hash_computer.py
HASH_ALGORITHM = "sha256"
```

**Why SHA-256?**
- It is fast enough for hashing small Python source code files.
- It is collision-resistant: two different files will almost never produce the same hash.
- It is available in Python's standard `hashlib` library with no extra installation needed.

---

#### Subsection 1.8.2 — Define the Cache Record Status Values

A cache record in the `cache_records` table can be in one of two states:
valid (the hash is trusted and up to date) or invalid (the hash is outdated
and the scene must be re-rendered).

```python
# Cache record validity states
CACHE_STATUS_VALID   = "valid"    # Hash is current. Scene can be skipped safely.
CACHE_STATUS_INVALID = "invalid"  # Hash is outdated. Scene must be re-rendered.
```

These string constants are used by `sqlite_cache_repository.py` when reading
and writing the `is_valid` column in the `cache_records` table, and by
`render_service.py` when deciding whether to skip or render a scene.

---

### Section 1.9 — CLI and Output Formatting Constants [

#### Subsection 1.9.1 — Define the CLI Prompt String

The CLI shell displays a prompt to the user to show it is ready for input.
This prompt string must be a constant so it is easy to change in one place.

```python
# The prompt shown to the user in the interactive CLI shell
CLI_PROMPT = "supermanim> "
```

The user sees this on their screen every time the tool is waiting for a command:
```
supermanim> _
```

#### Subsection 1.9.2 — Define the Tool Name and Version

The tool's name and version are shown when the user runs the `version` or `help`
command. They are also shown in error messages and log files.
These must be constants so that the name and version are never written as
literal strings inside logic code.

```python
# The official name of the tool
TOOL_NAME    = "SuperManim"

# The current version of the tool, following Semantic Versioning (MAJOR.MINOR.PATCH)
TOOL_VERSION = "1.0.0"
```

**Semantic Versioning explained simply:**
- `1` (MAJOR) — changes when you make a big breaking change that is not backward compatible.
- `0` (MINOR) — changes when you add a new feature that is still backward compatible.
- `0` (PATCH) — changes when you fix a small bug.

#### Subsection 1.9.3 — Define the Output Separator Line

The CLI output formatter uses a separator line to visually separate sections
of output. This makes it easier for the user to read long outputs.

```python
# A separator line used in CLI output to divide sections visually
CLI_SEPARATOR = "─" * 60
```

This produces a line of 60 dashes like this:
```
────────────────────────────────────────────────────────────
```

---

### Section 1.10 — Render Pipeline Constants 
#### Subsection 1.10.1 — Define the Render Timeout

This constant defines the maximum number of seconds that the tool will wait
for Manim to finish rendering one single scene before giving up.

Without a timeout, if Manim gets stuck (for example, because of an infinite
loop in the user's animation code), the tool will wait forever and never recover.

```python
# Maximum time in seconds to wait for one scene to finish rendering
# If Manim takes longer than this, the render is marked as FAILED
RENDER_TIMEOUT_SECONDS = 600  # 10 minutes per scene
```

**Why 600 seconds (10 minutes)?**
- A very complex 4K scene with many animations can take several minutes to render.
- 10 minutes is a generous limit that covers almost all real-world scenes.
- If a scene takes more than 10 minutes, it is almost certainly stuck in an error.

#### Subsection 1.10.2 — Define the Maximum Number of Render Retries

When a scene render fails (for example, due to a temporary system error),
the tool can try rendering it again automatically before giving up completely.

```python
# How many times to retry rendering a scene after a failure before marking it as FAILED
MAX_RENDER_RETRIES = 2
```

With `MAX_RENDER_RETRIES = 2`, the tool tries rendering up to 3 times total:
the first attempt plus 2 retries. If all 3 fail, the scene is marked as `STATUS_FAILED`.

---

### Section 1.11 — Export Constants 

#### Subsection 1.11.1 — Define the Final Output Filename Format

When the user exports their project, the tool assembles all scene clips and audio
into one final video file. This file needs a name. The name is built from the
project name using a standard format defined here.

```python
# Template for the final exported video filename
# {project_name} is replaced with the actual project name at runtime
# Example: "MyAnimation_final.mp4"
EXPORT_FILENAME_TEMPLATE = "{project_name}_final"
```

**Example usage in code:**
```python
final_filename = EXPORT_FILENAME_TEMPLATE.format(project_name="MyAnimation") + ".mp4"
# Result: "MyAnimation_final.mp4"
```

The file extension (`.mp4`, `.mov`, etc.) is added separately based on the
`DEFAULT_VIDEO_FORMAT` or the user's chosen export format.

#### Subsection 1.11.2 — Define the Maximum Export File Size

This constant defines the largest file size that the export service is allowed
to produce. This protects against filling the user's disk with an unexpectedly
huge export file.

```python
# Maximum allowed size for the final exported video file (in gigabytes)
MAX_EXPORT_FILE_SIZE_GB = 50.0
```

A 50 GB limit safely covers a one-hour 4K video at very high bitrate while still
preventing runaway exports caused by incorrect settings.


