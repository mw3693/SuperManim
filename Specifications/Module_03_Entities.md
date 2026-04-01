# Module_03_Entities

---

# Section 3.1: Introduction to the Core

## Subsection 3.1.1: What Is "The Core"?

Before we talk about what is inside the Core, we need to deeply understand
what the Core actually IS as a concept. Most people hear the word "Core"
and think it just means "the important code." That is not precise enough.
Let us build the understanding from the ground up.

### Subsubsection 3.1.1.1: The External World Around SuperManim

When SuperManim runs on your computer, it has to deal with many things
that exist OUTSIDE of SuperManim itself. These things were built by other
people. They have their own rules. SuperManim just uses them.

```
+=====================================================================+
|                 THE EXTERNAL WORLD AROUND SUPERMANIM                |
+=====================================================================+
|                                                                     |
|   SQLite          A database engine. Stores data in .db files.      |
|                   Built by the SQLite team. Not by us.              |
|                                                                     |
|   Manim           An animation engine. Draws shapes and videos.     |
|                   Built by the Manim community. Not by us.          |
|                                                                     |
|   FFmpeg          An audio/video processor. Cuts, converts files.   |
|                   Built by the FFmpeg team. Not by us.              |
|                                                                     |
|   The Terminal    The black window where you type commands.          |
|                   Built into your operating system. Not by us.      |
|                                                                     |
|   The File System Your computer's folders and files on disk.        |
|                   Part of the operating system. Not by us.          |
|                                                                     |
|   librosa         A Python library for audio analysis.              |
|                   Built by a third party. Not by us.                |
|                                                                     |
+=====================================================================+
```

All of these external things are REAL. SuperManim must use them to work.
Without Manim, it cannot draw animations.
Without SQLite, it cannot remember scene data.
Without FFmpeg, it cannot process audio.

But here is the critical question that the entire architecture is built around:

```
+---------------------------------------------------------------------+
|                                                                     |
|   If all these external things can change —                         |
|   if SQLite could be replaced by a JSON file,                       |
|   if Manim could be replaced by another animation tool,             |
|   if the terminal could be replaced by a GUI window —               |
|                                                                     |
|   HOW MUCH OF SUPERMANIM'S CODE WOULD HAVE TO CHANGE?              |
|                                                                     |
|   The answer we want:  ZERO.                                        |
|   The answer without architecture:  EVERYTHING.                     |
|                                                                     |
+---------------------------------------------------------------------+
```

The Core is the answer to this question.

### Subsubsection 3.1.1.2: The Core Is a Protected Island

Imagine the external world as an ocean. The ocean is noisy, unpredictable,
and full of things that can change at any time. SQLite might be upgraded.
Manim might change its command-line arguments. FFmpeg might change its flags.

The Core is an island in the middle of that ocean. It sits protected,
completely unaware that the ocean even exists.

```
+=====================================================================+
|                                                                     |
|   ~~~  OCEAN (the external world)  ~~~                              |
|                                                                     |
|   [SQLite]  [Manim]  [FFmpeg]  [Terminal]  [File System]           |
|                                                                     |
|   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~               |
|   ~                                                   ~             |
|   ~         +-----------------------------+           ~             |
|   ~         |                             |           ~             |
|   ~         |         THE CORE            |           ~             |
|   ~         |                             |           ~             |
|   ~         |   This island does not      |           ~             |
|   ~         |   know the ocean exists.    |           ~             |
|   ~         |                             |           ~             |
|   ~         |   It only knows its own     |           ~             |
|   ~         |   rules and its own data.   |           ~             |
|   ~         |                             |           ~             |
|   ~         +-----------------------------+           ~             |
|   ~                                                   ~             |
|   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~               |
|                                                                     |
+=====================================================================+
```

The Core is completely isolated. It does not import SQLite. It does not
import subprocess to run Manim. It does not call `print()` to talk to the
terminal. It does not use `os.path` to touch the file system.

If you open any Python file inside the Core folder and see any of these:

```python
import sqlite3          # NO. This belongs in an Adapter.
import subprocess       # NO. This belongs in an Adapter.
import os               # NO. This belongs in an Adapter.
from manim import *     # NO. This belongs in an Adapter.
print("something")      # NO. This belongs in an Adapter.
```

Something is wrong. That code does not belong in the Core.

## Subsection 3.1.2: What Does the Core Know About?

The Core only knows about three things:

```
+=====================================================================+
|            THE ONLY THREE THINGS THE CORE KNOWS ABOUT              |
+=====================================================================+
|                                                                     |
|   1. ITS OWN DATA SHAPES (Entities)                                 |
|      What is a Scene? What fields does it have?                     |
|      What is a Project? What does it contain?                       |
|      What is an AudioClip? What are its properties?                 |
|                                                                     |
|   2. ITS OWN RULES (Business Rules / Validators)                    |
|      What makes a Scene valid?                                      |
|      When can a project be exported?                                |
|      When do two durations "match"?                                 |
|      What happens when a scene's code has not changed?              |
|                                                                     |
|   3. ITS OWN WORKFLOWS (Business Logic / Use Cases)                 |
|      What are the exact steps to render a scene?                    |
|      What are the exact steps to export a project?                  |
|      What are the exact steps to sync a scene with audio?           |
|                                                                     |
+=====================================================================+
```

These three things — Entities, Business Rules, and Business Logic —
are the three components of the Core. This document focuses entirely
on the first component: **Entities**.

---

# Section 3.2: Component 1 — What Is an Entity?

## Subsection 3.2.1: The Definition of an Entity

An Entity is a data object. It is a Python class that represents one
real "thing" that SuperManim works with. Think of it as a structured
container that holds all the information about that one thing and nothing
more.

An Entity does **not DO** anything complex. It does not talk to databases.
It does not run Manim. It does not print anything to the screen. It is just
a clean collection of related data fields, grouped together under a
meaningful name.

The word "Entity" comes from the word "thing that exists."
A Scene exists. A Project exists. An AudioClip exists.
These are real things in the world of SuperManim, and each one
is represented in code as an Entity.

### Subsubsection 3.2.1.1: What an Entity IS and What It Is NOT

It is very important to understand both sides clearly.

```
+=====================================================================+
|                  WHAT AN ENTITY IS — AND IS NOT                     |
+=====================================================================+
|                                                                     |
|   AN ENTITY IS:                                                     |
|   ─────────────────────────────────────────────────────────────    |
|   - A Python @dataclass with named fields and type annotations      |
|   - A container for related data about one real "thing"             |
|   - A pure data object — no side effects, no external calls         |
|   - Something that can be created in memory with zero external deps |
|   - The single source of truth about one specific domain object     |
|                                                                     |
|   AN ENTITY IS NOT:                                                 |
|   ─────────────────────────────────────────────────────────────    |
|   - A function that runs Manim or calls FFmpeg                      |
|   - A class that reads or writes to a database (SQLite)             |
|   - A class that calls print() to show things on screen             |
|   - A class that reads or writes files from disk using os.path      |
|   - A class that validates itself (validation lives in Validators)  |
|   - A class that runs business logic (that lives in Services)       |
|                                                                     |
+=====================================================================+
```

### Subsubsection 3.2.1.2: The Python @dataclass Decorator

All Entities in SuperManim are written using Python's `@dataclass`
decorator. This is a standard Python feature that automatically generates
some boilerplate code for you — like `__init__` and `__repr__` — based
on the fields you declare.

```python
# WITHOUT @dataclass (messy — you have to write __init__ manually):
class Scene:
    def __init__(self, scene_id, scene_name=None, scene_duration=None):
        self.scene_id       = scene_id
        self.scene_name     = scene_name
        self.scene_duration = scene_duration
    # ... and you'd have to write __repr__ too, and __eq__, and more

# WITH @dataclass (clean — Python generates everything from declarations):
from dataclasses import dataclass
from typing import Optional

@dataclass
class Scene:
    scene_id:       int
    scene_name:     Optional[str] = None
    scene_duration: Optional[int] = None
    # Done. Python generates __init__, __repr__, __eq__ automatically.
```

Using `@dataclass` keeps our Entities short, readable, and consistent.

## Subsection 3.2.2: Why Do We Need Entities?

Without Entities, data floats around as loose variables scattered all over
the code. You would have `scene_id`, `scene_duration`, `scene_code_path`,
`scene_status`, `scene_hash` all as separate variables in different places.
When you need to pass a scene to a function, you would have to pass five,
ten, or even fifteen separate arguments. When you want to check something
about a scene, you have to remember every variable name exactly.

With Entities, all of that information lives together in one object.
You pass ONE Scene object to a function. Inside that function you access
`scene.duration`, `scene.code_path`, `scene.status`. Everything about a
scene is in one place, under one name.

```
+=====================================================================+
|              WITHOUT ENTITIES vs WITH ENTITIES                      |
+=====================================================================+
|                                                                     |
|   WITHOUT ENTITIES (messy, fragile):                                |
|   ─────────────────────────────────────────────────────────────    |
|   def render_scene(scene_id, duration, code_path, status, hash,    |
|                    output_path, fps, resolution, bg_color,          |
|                    audio_clip_path, synced_with_audio, ...):        |
|       # 10+ arguments. Miss one and the program crashes.            |
|       # Add a new field and you must update EVERY call site.        |
|       pass                                                          |
|                                                                     |
|   WITH ENTITIES (clean, robust):                                    |
|   ─────────────────────────────────────────────────────────────    |
|   def render_scene(scene: Scene):                                   |
|       # One object carries everything.                              |
|       # Adding a new field to Scene does not break any call.        |
|       pass                                                          |
|                                                                     |
+=====================================================================+
```

## Subsection 3.2.3: The Complete List of Entities in SuperManim

SuperManim has the following Entities, each stored in its own Python file
inside the `core/entities/` directory:

```
+=====================================================================+
|               ALL ENTITIES IN SUPERMANIM                            |
+=====================================================================+
|                                                                     |
|   Entity        File                      Purpose                   |
|   ──────────────────────────────────────────────────────────────   |
|   Scene         core/entities/scenes.py   One video section         |
|   SubScene      core/entities/scenes.py   One block inside a Scene  |
|   Project       core/entities/project.py  One full production       |
|   MediaUnit     core/entities/media_unit.py Abstract base class     |
|   AudioClip     core/entities/audio_clip.py One cut audio piece     |
|   VideoClip     core/entities/video_clip.py One cut video piece     |
|   AudioFile     core/entities/audio_file.py One full audio file     |
|   VideoFile     core/entities/video_file.py One full video file     |
|   AssetFile     core/entities/asset_file.py One image/font/asset    |
|   Timeline      core/entities/timeline.py  The ordered sequence     |
|                                                                     |
+=====================================================================+
```

The folder structure on disk looks like this:

```
[mina@mina ~]$ pwd
/home/mina/SuperManim/core/entities

[mina@mina entities]$ tree .
.
├── __init__.py
├── asset_file.py
├── audio_clip.py
├── audio_file.py
├── media_unit.py
├── project.py
├── scenes.py
├── timeline.py
├── video_clip.py
└── video_file.py

1 directory, 10 files
```

---

# Section 3.3: Entity 1 — Scene

## Subsection 3.3.1: What Is a Scene?

Before we look at any code, let us build a completely clear picture of
what a Scene actually IS inside SuperManim.

A Scene is one section of your video. Think of your final video like a
book. Your book has chapters. Each chapter is one Scene. Chapter 1 plays
first, Chapter 2 plays after it, Chapter 3 plays after that, all the way
to the end of the video.

If your video is 60 seconds long and has 4 sections, you have 4 Scenes.

```
+=====================================================================+
|                 YOUR 60-SECOND VIDEO — 4 SCENES                     |
+=====================================================================+
|                                                                     |
|  0ms ─────── 12500ms ─────── 31000ms ──── 47800ms ───── 60000ms   |
|  |              |                 |              |          |       |
|  |  SCENE 1     |    SCENE 2      |   SCENE 3    | SCENE 4  |       |
|  | Introduction | Main Concept    |   Example    |Conclusion|       |
|  |  12500ms     |   18500ms       |  16800ms     |  12200ms |       |
|  |              |                 |              |          |       |
+=====================================================================+
```

Now here is the important thing to understand: a Scene is **NOT** the
video file on disk. A Scene is **NOT** the Python animation code.
A Scene is the **RECORD** that SuperManim keeps about all the information
surrounding one section of the video.

Think of a Scene like a filing card in a cabinet. The filing card says:
"Scene 3. Duration: 16800 ms. Code file: example.py. Status: rendered.
Audio: clip_003.mp3. Synced: yes. Video at: output/scene_03/scene_03.mp4."

The filing card itself is just information. The actual video file, audio
file, and code file are stored separately on disk. The Scene Entity is
that filing card — the central record that knows where everything is and
what state everything is in.

### Subsubsection 3.3.1.1: Where Is the Scene Class Defined on Disk?

The `Scene` class is defined in this file:

```
/home/mina/SuperManim/core/entities/scenes.py
```

Both the `Scene` class and the `SubScene` class live in this same file.
`SubScene` is defined below `Scene` in the file because `Scene` references
`SubScene` in its `scene_map` property.

## Subsection 3.3.2: The Two Levels of a Scene

A Scene in SuperManim has two levels inside it.

**Level 1** is the Scene itself — one complete section of the video.

**Level 2** is the SubScene — one smaller animation block or moment
inside that section.

A single Scene can be divided into multiple SubScenes. Each SubScene is
a mini-scene — a smaller, more granular piece of animation within the
bigger Scene.

Think of it like this:

```
+=====================================================================+
|                      SCENE  AND  SUBSCENES                          |
+=====================================================================+
|                                                                     |
|   SCENE 3 (16800 ms total)                                          |
|   ─────────────────────────────────────────────────────────────    |
|   |                                                               | |
|   |  SubScene A          SubScene B         SubScene C            | |
|   |  (0 → 5500ms)        (5500 → 11200ms)   (11200 → 16800ms)    | |
|   |  "Title appears"     "Graph draws"      "Conclusion fades in" | |
|   |  5500ms              5700ms             5600ms                | |
|   |                                                               | |
|   ─────────────────────────────────────────────────────────────    |
|                                                                     |
|   The Scene is the big container.                                   |
|   The SubScenes are the smaller blocks inside that container.       |
|                                                                     |
|   5500 + 5700 + 5600 = 16800 ms  ← SubScenes must add up exactly   |
|                                                                     |
+=====================================================================+
```

When you write Manim code for Scene 3, you might have multiple animation
phases: first a title animates in, then a graph draws itself, then a
conclusion text fades in. Each of those phases is a SubScene.

The SubScene allows SuperManim to track these individual animation blocks
separately — their timing, their content, their order within the Scene.

We will define the SubScene entity fully in Section 3.4.

## Subsection 3.3.3: The Full Python Class of the Scene Entity

An Entity is a Python dataclass. It is a pure data container. It does not
run Manim, does not talk to SQLite, does not call `print()`. It is just
fields with types and default values. That is all. That is exactly what
makes it clean and safe.

The Scene Entity is the most important Entity in all of SuperManim because
almost every command, every service, every business rule, and every workflow
reads or updates a Scene object.

### Subsubsection 3.3.3.1: The Complete Scene Class Code

```python
# File location: /home/mina/SuperManim/core/entities/scenes.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List


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
```

## Subsection 3.3.4: Every Property of the Scene Entity Explained in Depth

The properties are grouped into 8 groups. Each group handles one aspect
of what the Scene needs to know about itself.

Here is a quick reference table before we dive into the details:

```
+================================================================+
|         SCENE ENTITY — COMPLETE PROPERTY REFERENCE            |
+================================================================+
|                                                                |
|  GROUP 1 — IDENTITY                                            |
|  ──────────────────────────────────────────────────────────── |
|  scene_id            int           Required. Unique ID.        |
|  scene_name          str | None    Human label. Optional.      |
|  scene_index         int           Position in sequence. 0-based|
|  previous_scene_id   int | None    ID of the scene before this. |
|  next_scene_id       int | None    ID of the scene after this.  |
|                                                                |
|  GROUP 2 — TIMING  (all values are milliseconds)               |
|  ──────────────────────────────────────────────────────────── |
|  scene_duration      int | None    Length in ms.               |
|  scene_start_time    int | None    Where this scene starts.    |
|  scene_end_time      int | None    Where this scene ends.      |
|  scene_start_marker  str | None    Audio cue label at start.   |
|  scene_end_marker    str | None    Audio cue label at end.     |
|                                                                |
|  GROUP 3 — CODE                                                |
|  ──────────────────────────────────────────────────────────── |
|  scene_code_path     str | None    Path to the .py file.       |
|  scene_code_content  str | None    Full text of the .py file.  |
|                                                                |
|  GROUP 4 — HASH FINGERPRINTS                                   |
|  ──────────────────────────────────────────────────────────── |
|  scene_code_hash     str | None    SHA-256 of code file.       |
|  scene_assets_hash   str | None    SHA-256 of all asset files. |
|  scene_audio_hash    str | None    SHA-256 of audio clip.      |
|  final_scene_hash    str | None    Master combined hash.        |
|                                                                |
|  GROUP 5 — CONTENT AND VISUAL                                  |
|  ──────────────────────────────────────────────────────────── |
|  scene_content           str | None    Description of scene.   |
|  scene_background_color  str           Hex color. Default black.|
|  scene_resolution        str           e.g. "1920x1080".       |
|  scene_fps               int           Frames per second.      |
|                                                                |
|  GROUP 6 — STATUS AND OUTPUT                                   |
|  ──────────────────────────────────────────────────────────── |
|  scene_status            str           pending/rendered/...    |
|  scene_output_path       str | None    Path to final .mp4.     |
|  scene_preview_path      str | None    Path to preview .mp4.   |
|  scene_error_message     str | None    Error text if failed.   |
|  scene_rendered_at       str | None    Timestamp of render.    |
|  scene_render_duration   float | None  How long render took.   |
|                                                                |
|  GROUP 7 — AUDIO                                               |
|  ──────────────────────────────────────────────────────────── |
|  related_audio_clip_path str | None    Path to audio clip.     |
|  synced_with_audio       bool          True = render w/ audio. |
|                                                                |
|  GROUP 8 — SUBSCENES                                           |
|  ──────────────────────────────────────────────────────────── |
|  scene_map               List[SubScene] Blocks inside scene.   |
|                                                                |
+================================================================+
```

### Subsubsection 3.3.4.1: GROUP 1 — Identity Properties

These properties answer the question: "Which Scene is this, and how does
it connect to the other Scenes in the project?"

#### Subsubsubsection 3.3.4.1.1: scene_id

**Type:** `int`
**Default:** Required — you must always provide it. There is no default.
**Example value:** `3`

The `scene_id` is the unique number that permanently identifies this
specific Scene within the project. No two Scenes in the same project can
share the same `scene_id`. This number is used everywhere in the system.

When you type `render scene 3`, the system loads the Scene whose
`scene_id` is `3`. When the database stores a Scene, it uses `scene_id`
as the primary key. When the audio clip is named `clip_003.mp3`, the `003`
comes directly from the `scene_id`.

```
scene_id is the permanent fingerprint of identity.
Everything that references a scene uses scene_id.

render scene 3          → loads scene where scene_id = 3
clip_003.mp3            → audio for scene where scene_id = 3
output/scene_03/...     → video folder for scene where scene_id = 3
```

#### Subsubsubsection 3.3.4.1.2: scene_name

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"Introduction"`, `"Main Concept"`, `"Conclusion"`

The `scene_name` is a human-readable label for the scene. While `scene_id`
is a number used by the computer, `scene_name` is a word used by the human
developer. The `scene_name` is completely optional. The system works
perfectly without it. But it makes your project much easier to navigate.

```
WITHOUT scene_name:               WITH scene_name:
  Scene 1 | rendered                Scene 1 (Introduction)    | rendered
  Scene 2 | rendered                Scene 2 (Main Concept)    | rendered
  Scene 3 | rendered                Scene 3 (Example)         | rendered
  Scene 4 | pending                 Scene 4 (Practice)        | pending
  Scene 5 | FAILED                  Scene 5 (Conclusion)      | FAILED
```

The version with names tells you immediately what each scene is about
without having to remember which number corresponds to which topic.

#### Subsubsubsection 3.3.4.1.3: scene_index

**Type:** `int`
**Default:** `0`
**Example value:** `2` (meaning this is the third scene; counting starts at 0)

The `scene_index` is the current position of the Scene in the video's
playback sequence. It uses zero-based counting: the first scene has
`scene_index = 0`, the second has `scene_index = 1`, the third has
`scene_index = 2`, and so on.

You might wonder: if we already have `scene_id`, why do we also need
`scene_index`? The reason is that `scene_id` is a **permanent identity**
that never changes for the entire life of the project. Scene 3 always has
`scene_id = 3`. But `scene_index` is the **current playback order**, and
that CAN change when you reorder scenes.

```
+-------------------------------------------------------------+
|   scene_id  vs  scene_index — the key difference           |
+-------------------------------------------------------------+
|                                                             |
|   scene_id    = permanent identity. Never changes.         |
|                  Used for: database lookup, file naming     |
|                                                             |
|   scene_index = current position in the playback sequence. |
|                  Changes when you move scenes around.       |
|                  Used for: ordering, timeline calculation   |
|                                                             |
|   Example: user runs "move scene 5 to position 2"          |
|                                                             |
|   BEFORE:                                                   |
|   scene_index 0  →  scene_id=1                             |
|   scene_index 1  →  scene_id=2                             |
|   scene_index 2  →  scene_id=3                             |
|   scene_index 3  →  scene_id=4                             |
|   scene_index 4  →  scene_id=5                             |
|                                                             |
|   AFTER:                                                    |
|   scene_index 0  →  scene_id=1  (unchanged)                |
|   scene_index 1  →  scene_id=5  (was last, now second!)    |
|   scene_index 2  →  scene_id=2  (shifted right)            |
|   scene_index 3  →  scene_id=3  (shifted right)            |
|   scene_index 4  →  scene_id=4  (shifted right)            |
|                                                             |
|   scene_id=5 kept its identity. Only its position changed. |
+-------------------------------------------------------------+
```

#### Subsubsubsection 3.3.4.1.4: previous_scene_id

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `2` (the scene that plays immediately before this one)

The `previous_scene_id` stores the `scene_id` of the Scene that comes
just before this Scene in the playback order. For Scene 3,
`previous_scene_id = 2`. For Scene 1 (the very first scene),
`previous_scene_id = None` because there is nothing before it.

```
Scene 1  →  previous_scene_id = None   (nothing before Scene 1)
Scene 2  →  previous_scene_id = 1
Scene 3  →  previous_scene_id = 2
Scene 4  →  previous_scene_id = 3
Scene 5  →  previous_scene_id = 4
```

#### Subsubsubsection 3.3.4.1.5: next_scene_id

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `4` (the scene that plays immediately after this one)

The `next_scene_id` stores the `scene_id` of the Scene that comes just
after this Scene. For Scene 3, `next_scene_id = 4`. For the last Scene,
`next_scene_id = None`.

Together, `previous_scene_id` and `next_scene_id` form a doubly-linked
list. You can navigate in both directions without doing any searches.

```
+-------------------------------------------------------------+
|   THE DOUBLY-LINKED SCENE CHAIN                             |
+-------------------------------------------------------------+
|                                                             |
|   None ← [Scene 1] ←→ [Scene 2] ←→ [Scene 3] ←→ [Scene 4] → None  |
|                                                             |
|   Scene 3:                                                  |
|     previous_scene_id = 2   ← points backward to Scene 2  |
|     next_scene_id     = 4   → points forward to Scene 4   |
|                                                             |
|   To go backward from Scene 3: load scene_id = 2           |
|   To go forward  from Scene 3: load scene_id = 4           |
|   No search needed. Just follow the links.                  |
|                                                             |
+-------------------------------------------------------------+
```

### Subsubsection 3.3.4.2: GROUP 2 — Timing Properties

These properties answer the question: "How long is this Scene, and exactly
where does it sit in the overall video timeline?"

**IMPORTANT RULE:** All timing values in this group are stored as
**integers in milliseconds (ms)**. For example, 16.8 seconds is stored
as `16800`. This is a deliberate design choice to avoid floating-point
rounding errors. When you add up many float values like `12.5 + 18.5 +
16.8 + 12.2`, tiny rounding errors can accumulate. With integers in
milliseconds, `12500 + 18500 + 16800 + 12200 = 60000` — always exact.

#### Subsubsubsection 3.3.4.2.1: scene_duration

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `16800` (meaning 16.8 seconds)

The `scene_duration` is the total length of this scene in milliseconds.
It is the most important timing value in the entire Scene entity. Every
other timing value in this group either comes from this value or is
compared against it.

When the user types `set scene 3 duration 16.8`, the system multiplies
16.8 by 1000 and stores `16800` here.

The `scene_duration` is also the value that gets compared to the
`audio_clip_duration` during the `sync scene` command. For a scene to
be synchronized with audio, both must match within 1 millisecond.

```
User types:  set scene 3 duration 16.8
System stores:  scene_duration = 16800  (16.8 × 1000 = 16800 ms)

Later, the audio clip for Scene 3 is cut to match:
  audio_clip_duration = 16.8 seconds = 16800 ms

Sync check:
  scene_duration       = 16800
  audio_clip_duration  = 16800
  Difference:          = 0
  Result:              MATCH → sync is approved
```

#### Subsubsubsection 3.3.4.2.2: scene_start_time

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `31000` (meaning 31.0 seconds into the full video)

The `scene_start_time` is the millisecond mark in the overall video
where this scene begins playing. This is NOT set by the user directly.
It is computed automatically by the `TimelineService` by adding up the
durations of all scenes that come before this one.

```
Scene 1:  scene_duration = 12500ms  →  scene_start_time = 0
Scene 2:  scene_duration = 18500ms  →  scene_start_time = 12500
Scene 3:  scene_duration = 16800ms  →  scene_start_time = 31000
Scene 4:  scene_duration = 12200ms  →  scene_start_time = 47800
```

This value tells the audio system exactly where to start playing the
audio clip for this scene in the final video.

#### Subsubsubsection 3.3.4.2.3: scene_end_time

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `47800` (meaning 47.8 seconds into the full video)

The `scene_end_time` is the millisecond mark in the overall video where
this scene stops playing. It is always computed as:

```
scene_end_time = scene_start_time + scene_duration

For Scene 3:
scene_end_time = 31000 + 16800 = 47800 ms
```

This is also auto-computed by the `TimelineService`. You never set it
manually.

#### Subsubsubsection 3.3.4.2.4: scene_start_marker

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"[CHAPTER 3 BEGIN]"`

A text label that marks the beginning of this scene's section in the
audio file. Some audio editors allow you to place named markers (also
called cue points or chapter marks) at specific timestamps in an audio
file. If your audio file has a marker at the 31-second mark with the
label `"[CHAPTER 3 BEGIN]"`, you can store that label here.

This is optional. The system does not require markers to function.
Markers are purely for human reference and display purposes.

#### Subsubsubsection 3.3.4.2.5: scene_end_marker

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"[CHAPTER 3 END]"`

A text label that marks the end of this scene's section in the audio
file. Works exactly the same way as `scene_start_marker`. Optional.

### Subsubsection 3.3.4.3: GROUP 3 — Code Properties

These properties answer the question: "What Python file contains the
Manim animation code for this scene, and what is in that file?"

#### Subsubsubsection 3.3.4.3.1: scene_code_path

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"my_scenes/example.py"`

The `scene_code_path` is the file path to the Python file that contains
the Manim animation code for this scene. When the user runs
`set scene 3 code my_scenes/example.py`, the system stores that path here.

When the render command runs, the system reads `scene_code_path` to know
which Python file to pass to the Manim CLI. If `scene_code_path` is `None`,
the scene cannot be rendered and the system refuses the command.

```
scene_code_path = "my_scenes/example.py"

The Manim CLI command will be approximately:
  manim my_scenes/example.py ExampleScene --quality high

Without scene_code_path, rendering is impossible:
  [Error] Scene 3 has no code file assigned.
  Use:  set scene 3 code path/to/your/animation.py
```

#### Subsubsubsection 3.3.4.3.2: scene_code_content

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"from manim import *\nclass Example(Scene):\n    def construct(self): ..."`

The `scene_code_content` stores the complete text content of the Python
animation file. It is a cached snapshot of the file's code at the moment
it was last read by the system.

This field exists as a convenience — instead of reading the file from
disk every time some part of the system needs its text, the system reads
it once and caches the full text here inside the Scene object. This is
especially useful for the `show scene 3 code` display command.

### Subsubsection 3.3.4.4: GROUP 4 — Hash Fingerprint Properties

These properties are the heart of SuperManim's incremental render system.
They are the "magic" that lets SuperManim skip re-rendering scenes that
have not changed.

To understand how this works, you first need to understand what a
**hash fingerprint** is. A hash is a short, fixed-length string (like
`"a3f8c2d1e4b9ff37..."`) that is computed from the full content of a
file using a mathematical algorithm. The SHA-256 algorithm is used here.

Two key properties of SHA-256:
1. If even ONE single character in a file changes, the resulting hash
   changes completely and unpredictably.
2. If the file is completely unchanged, the hash is always identical.

```
+=====================================================================+
|              HOW HASH FINGERPRINTS ENABLE SMART RENDERING           |
+=====================================================================+
|                                                                     |
|   BEFORE RENDERING A SCENE:                                         |
|   ─────────────────────────────────────────────────────────────    |
|   System computes a FRESH hash from the current code file on disk.  |
|   System compares it to the STORED hash saved in the Scene entity.  |
|                                                                     |
|   New hash == Stored hash?                                          |
|     YES  → Nothing changed. Skip. Use the existing saved video.    |
|     NO   → Something changed. Must re-render this scene.           |
|                                                                     |
|   RESULT:                                                           |
|   In a 20-scene project, if you fix one scene, only that one scene  |
|   has a different hash. The other 19 are skipped instantly.         |
|   You wait 5 minutes instead of 100 minutes.                        |
|                                                                     |
+=====================================================================+
```

SuperManim tracks FOUR separate hashes for each scene. This allows it to
detect not just THAT something changed, but specifically WHAT changed —
was it the code? The asset files? The audio clip? Each type of change
has a different implication for what needs to be re-done.

#### Subsubsubsection 3.3.4.4.1: scene_code_hash

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"a3f8c2d1e4b9ff37c128a6d9e0b45721c3f4a9b2..."`

The SHA-256 fingerprint of the Python animation code file
(`scene_code_path`). If this hash changes, the user edited the animation
code. The scene must be fully re-rendered with Manim.

#### Subsubsubsection 3.3.4.4.2: scene_assets_hash

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"b7d2e9a1c4f3b8d2e6a1c9f4b3d7e2a1f9c3b8..."`

The SHA-256 fingerprint computed from all the asset files that this scene
uses — images, fonts, or SVG files stored in the `assets/` folder. If an
image used in Scene 3 is replaced, `scene_assets_hash` changes and the
scene must be re-rendered even if the code itself did not change.

#### Subsubsubsection 3.3.4.4.3: scene_audio_hash

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"c1e4f9b2d7a3c8e1f4b9d2a7c3e8f1b4a2d9c7..."`

The SHA-256 fingerprint of the audio clip file linked to this scene
(the file stored in `related_audio_clip_path`). If the audio clip is
re-cut or replaced with a different recording, this hash changes and
the scene video must be re-assembled with the new audio.

#### Subsubsubsection 3.3.4.4.4: final_scene_hash

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"f9a3b7e1d4c2f8a3b7e1d4c9f2a3b7e1d8f4c2..."`

The `final_scene_hash` is the single master combined fingerprint. It is
computed by combining `scene_code_hash`, `scene_assets_hash`, and
`scene_audio_hash` into one final hash.

This is the ONE hash that the render system checks before deciding
whether to render or skip a scene. If ANY of the three component hashes
changed, the `final_scene_hash` will also be different.

```
+-------------------------------------------------------------+
|   HOW THE FOUR HASHES WORK TOGETHER                         |
+-------------------------------------------------------------+
|                                                             |
|   scene_code_hash   ──┐                                     |
|   scene_assets_hash ──┼──→ combine → final_scene_hash       |
|   scene_audio_hash  ──┘                                     |
|                                                             |
|   BEFORE RENDER: compute new final_scene_hash from disk     |
|   COMPARE: new hash vs stored final_scene_hash              |
|                                                             |
|   Equal?  → Nothing changed. SKIP. Save time.              |
|   Differ? → Something changed. RENDER. Produce new video.  |
|                                                             |
|   The individual hashes (code, assets, audio) help debug:   |
|   "The final hash changed. But WHY? Was it the code?        |
|    Was it an image asset? Was it the audio clip?"           |
|   By checking each hash individually, you know exactly.     |
|                                                             |
+-------------------------------------------------------------+
```

### Subsubsection 3.3.4.5: GROUP 5 — Content and Visual Properties

These properties answer the question: "What does this scene show, and
how should it look visually when rendered?"

#### Subsubsubsection 3.3.4.5.1: scene_content

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"Shows how Python variables work using a box diagram animation"`

A plain-English description of what this scene teaches or shows. This is
purely for human documentation. The system does not use this value to make
any decisions. It is simply a note to yourself about what the scene covers.

#### Subsubsubsection 3.3.4.5.2: scene_background_color

**Type:** `str`
**Default:** `"#000000"` (pure black)
**Example value:** `"#000000"`, `"#1a1a2e"`, `"#ffffff"`

The background color of the animation for this scene, stored as a CSS
hex color string. This value is passed to Manim as a rendering argument.

The default is black because Manim's standard educational animation style
uses a black background. You can change it per scene.

```
scene_background_color = "#000000"  →  Pure black (classic Manim style)
scene_background_color = "#ffffff"  →  Pure white background
scene_background_color = "#1a1a2e"  →  Dark navy (popular modern style)
scene_background_color = "#2b2b2b"  →  Dark gray
```

#### Subsubsubsection 3.3.4.5.3: scene_resolution

**Type:** `str`
**Default:** `"1920x1080"`
**Example value:** `"1920x1080"`, `"3840x2160"`, `"1280x720"`

The pixel dimensions of the rendered video for this scene, stored as
`"widthxheight"`. This is passed to Manim as a rendering argument and
tells Manim how many pixels wide and tall each animation frame should be.

Note: This is a per-scene override of the project-level default set in
`render_resolution`. Most scenes should use the same resolution so that
FFmpeg can assemble them cleanly.

#### Subsubsubsection 3.3.4.5.4: scene_fps

**Type:** `int`
**Default:** `60`
**Example value:** `24`, `30`, `60`

The frame rate for this scene's animation — how many frames Manim must
draw per second of animation. Higher frame rates produce smoother motion
but take significantly longer to render.

```
For a 16800ms (16.8-second) scene:
  At 24 fps  →  16.8 × 24  =  403 individual frames to draw
  At 30 fps  →  16.8 × 30  =  504 individual frames to draw
  At 60 fps  →  16.8 × 60  = 1008 individual frames to draw

More frames per second = smoother motion = slower render = bigger file.

24 fps:  Cinema standard. Used in films. Smooth enough for most content.
30 fps:  TV standard. Good choice for educational animations.
60 fps:  Very smooth. Best for fast-moving graphics. Slowest to render.
```

### Subsubsection 3.3.4.6: GROUP 6 — Status and Output Properties

These properties answer the question: "Has this Scene been rendered?
Where is the output video? What happened during the last render attempt?"

#### Subsubsubsection 3.3.4.6.1: scene_status

**Type:** `str`
**Default:** `"pending"`
**Allowed values:** exactly four specific strings: `"pending"`, `"rendered"`,
`"failed"`, `"skipped"`

The `scene_status` is the most important state flag of a Scene. It tells
you at a glance exactly where this scene is in its render lifecycle.

```
+================================================================+
|               THE FOUR POSSIBLE STATUS VALUES                  |
+================================================================+
|                                                                |
|   "pending"                                                    |
|   ──────────────────────────────────────────────────────────  |
|   The scene exists in the project.                             |
|   It has NEVER been successfully rendered.                     |
|   It is waiting to be rendered.                                |
|   Every newly created scene starts as "pending".               |
|                                                                |
|   "rendered"                                                   |
|   ──────────────────────────────────────────────────────────  |
|   The scene was rendered successfully.                         |
|   The video file exists at scene_output_path.                  |
|   scene_rendered_at and scene_render_duration are set.         |
|   The scene is ready to be included in the final export.       |
|                                                                |
|   "failed"                                                     |
|   ──────────────────────────────────────────────────────────  |
|   A render was attempted but Manim returned an error.          |
|   scene_error_message contains the error details.              |
|   The user must fix the code error and re-run the render.      |
|                                                                |
|   "skipped"                                                    |
|   ──────────────────────────────────────────────────────────  |
|   The render command ran for this scene.                       |
|   But the final_scene_hash matched the stored hash.            |
|   Nothing changed since last render. Existing video is valid.  |
|   Manim was NOT called. The saved render was kept as-is.       |
|   This is the efficiency mechanism — the core SuperManim idea. |
|                                                                |
+================================================================+
```

#### Subsubsubsection 3.3.4.6.2: scene_output_path

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"output/scene_03/scene_03.mp4"`

The file path to the final rendered video for this scene. Set
automatically by the render system after Manim finishes successfully.
Stays `None` until the first successful render.

#### Subsubsubsection 3.3.4.6.3: scene_preview_path

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"previews/scene_03_preview.mp4"`

The file path to the low-quality 480p preview video for this scene.
Generated by the `preview scene N` command. Used for quick visual
checking only. Never included in the final export.

#### Subsubsubsection 3.3.4.6.4: scene_error_message

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"NameError: name 'TextMobject' is not defined on line 12"`

When a render attempt fails, the error message returned by Manim is
stored here. This helps the user understand exactly what went wrong
without having to scroll through terminal output. Cleared back to `None`
when the scene is successfully re-rendered.

#### Subsubsubsection 3.3.4.6.5: scene_rendered_at

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"2024-11-12 14:22:30"`

The exact date and time when the last **successful** render finished.
Stored as an ISO-format string. Only written when `scene_status` becomes
`"rendered"`. If a render fails, this field is NOT updated — it keeps
the timestamp of the last successful render, or stays `None` if there
has never been a successful render.

The timestamp is obtained by calling Python's `datetime.now()` at the
exact moment Manim finishes:

```python
from datetime import datetime

render_finished_at = datetime.now()
scene.scene_rendered_at = render_finished_at.strftime("%Y-%m-%d %H:%M:%S")
# Stored as: "2024-11-12 14:22:30"
```

#### Subsubsubsection 3.3.4.6.6: scene_render_duration

**Type:** `Optional[float]`
**Default:** `None`
**Example value:** `252.7` (meaning 252.7 seconds = about 4 minutes 12 seconds)

Records how many seconds the last successful render took, from the moment
Manim started to the moment it finished. Computed by reading the clock
twice and subtracting:

```python
render_started_at  = datetime.now()
# ... Manim runs for several minutes ...
render_finished_at = datetime.now()

elapsed = (render_finished_at - render_started_at).total_seconds()
scene.scene_render_duration = elapsed  # e.g. 252.7
```

Used to show the user statistics like "Last render: 4m 12s" and to
estimate total re-render time for all scenes.

### Subsubsection 3.3.4.7: GROUP 7 — Audio Properties

These properties answer the question: "Is this Scene connected to an
audio clip, and is that connection confirmed and ready for rendering?"

#### Subsubsubsection 3.3.4.7.1: related_audio_clip_path

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"audio_clips/clip_003.mp3"`

The file path to the audio clip that belongs to this scene. When you
split the project's master audio file into pieces (one per scene), each
piece is stored in the `audio_clips/` folder and its path is stored here.

```
+-------------------------------------------------------------+
|   THE THREE AUDIO STATES OF A SCENE                         |
+-------------------------------------------------------------+
|                                                             |
|   STATE 1: No audio assigned                                |
|   related_audio_clip_path = None                            |
|   synced_with_audio       = False                           |
|   → Scene renders as a silent video. No audio.             |
|                                                             |
|   STATE 2: Audio assigned but not confirmed                 |
|   related_audio_clip_path = "audio_clips/clip_003.mp3"     |
|   synced_with_audio       = False                           |
|   → Audio clip is assigned but NOT yet activated.          |
|     Durations have not been verified to match yet.          |
|     Scene still renders as a silent video.                  |
|                                                             |
|   STATE 3: Audio assigned and confirmed (SYNCED)            |
|   related_audio_clip_path = "audio_clips/clip_003.mp3"     |
|   synced_with_audio       = True                            |
|   → Audio clip is assigned AND durations are verified.     |
|     Scene renders WITH audio baked into the video file.     |
|                                                             |
+-------------------------------------------------------------+
```

#### Subsubsubsection 3.3.4.7.2: synced_with_audio

**Type:** `bool`
**Default:** `False`

The `synced_with_audio` flag is a deliberate, confirmed signal that:

1. An audio clip path has been assigned (`related_audio_clip_path` is set)
2. The audio clip's duration has been verified to exactly match `scene_duration`
3. The scene is ready and safe to render with audio included

This flag can ONLY be set to `True` by running the `sync scene` command.
That command performs the duration check first. If the check fails (durations
do not match), the flag stays `False`.

```
+================================================================+
|   THE COMPLETE SYNC FLOW                                       |
+================================================================+
|                                                                |
|   STEP 1: Assign the audio clip path                           |
|   scene.related_audio_clip_path = "audio_clips/clip_003.mp3"  |
|   scene.synced_with_audio       = False  (not yet confirmed)   |
|                                                                |
|   STEP 2: User runs "sync scene 3"                             |
|   System checks:  scene_duration == clip_duration?             |
|   16800 ms == 16800 ms?    YES → MATCH                         |
|   scene.synced_with_audio = True  (confirmed!)                 |
|                                                                |
|   STEP 3: Render scene 3                                       |
|   System sees synced_with_audio = True                         |
|   System mixes audio into the rendered video.                  |
|   Output: scene_03.mp4 with voice narration baked in.         |
|                                                                |
|   IF durations did NOT match:                                  |
|   16800 ms != 17200 ms   → MISMATCH                            |
|   scene.synced_with_audio stays False                          |
|   Error shown: "Duration mismatch: 400ms difference"          |
|                                                                |
+================================================================+
```

### Subsubsection 3.3.4.8: GROUP 8 — SubScene Map

#### Subsubsubsection 3.3.4.8.1: scene_map

**Type:** `List[SubScene]`
**Default:** `[]` (a fresh empty list is created for every new Scene instance)

The `scene_map` is a list of `SubScene` objects. Each `SubScene`
represents one animation block inside this Scene. It is the internal
map of what happens within the Scene — what blocks play, in what order,
and at what timestamps.

When a Scene is first created, `scene_map` is empty. You add SubScenes
to it as you plan the animation in detail.

Not all projects need SubScenes. If your Manim code for Scene 3 is one
continuous animation with no meaningful internal divisions, you can leave
`scene_map` empty and everything works perfectly.

But if your Scene 3 has distinct phases — a title appears, then a diagram
draws itself, then a summary fades in — then SubScenes let you model each
phase as a separate tracked entity with its own timing and status.

**Why use `field(default_factory=list)` instead of just `= []`?**

```python
# WRONG — this is a Python trap:
@dataclass
class Scene:
    scene_map: list = []
    # This creates ONE list that is SHARED between ALL Scene instances!
    # Modifying scene_1.scene_map would also change scene_2.scene_map!

# CORRECT — each instance gets its own fresh list:
@dataclass
class Scene:
    scene_map: list = field(default_factory=list)
    # Each new Scene() call creates a brand new empty list for that instance.
```

## Subsection 3.3.5: A Real, Fully Populated Scene Object

Here is what a complete Scene object looks like for Scene 3 of a real
SuperManim project. Every single field is shown with a real value.

```python
# This is what Scene 3 looks like in memory after being fully set up.

scene_3 = Scene(
    # ── GROUP 1 — IDENTITY ──────────────────────────────────────────
    scene_id               = 3,
    scene_name             = "Example: Python Variables",
    scene_index            = 2,                     # 0-based → 3rd scene
    previous_scene_id      = 2,
    next_scene_id          = 4,

    # ── GROUP 2 — TIMING (all in milliseconds) ───────────────────────
    scene_duration         = 16800,                 # 16.8 seconds
    scene_start_time       = 31000,                 # starts at second 31.0
    scene_end_time         = 47800,                 # ends at second 47.8
    scene_start_marker     = "[CHAPTER 3 BEGIN]",
    scene_end_marker       = "[CHAPTER 3 END]",

    # ── GROUP 3 — CODE ──────────────────────────────────────────────
    scene_code_path        = "my_scenes/example.py",
    scene_code_content     = "from manim import *\nclass Example(Scene):\n    ...",

    # ── GROUP 4 — HASH FINGERPRINTS ──────────────────────────────────
    scene_code_hash        = "a3f8c2d1e4b9ff37c128a6d9e0b45721...",
    scene_assets_hash      = "b7d2e9a1c4f3b8d2e6a1c9f4b3d7e2a1...",
    scene_audio_hash       = "c1e4f9b2d7a3c8e1f4b9d2a7c3e8f1b4...",
    final_scene_hash       = "f9a3b7e1d4c2f8a3b7e1d4c9f2a3b7e1...",

    # ── GROUP 5 — CONTENT AND VISUAL ─────────────────────────────────
    scene_content          = "Shows how Python variables work with a box diagram",
    scene_background_color = "#000000",
    scene_resolution       = "1920x1080",
    scene_fps              = 60,

    # ── GROUP 6 — STATUS AND OUTPUT ──────────────────────────────────
    scene_status           = "rendered",
    scene_output_path      = "output/scene_03/scene_03.mp4",
    scene_preview_path     = "previews/scene_03_preview.mp4",
    scene_error_message    = None,
    scene_rendered_at      = "2024-11-12 14:22:30",
    scene_render_duration  = 252.7,                 # 4 minutes 12 seconds

    # ── GROUP 7 — AUDIO ─────────────────────────────────────────────
    related_audio_clip_path = "audio_clips/clip_003.mp3",
    synced_with_audio       = True,

    # ── GROUP 8 — SUBSCENES ──────────────────────────────────────────
    scene_map = [
        SubScene(
            subscene_id         = 1,
            subscene_name       = "Title Card",
            subscene_index      = 0,
            parent_scene_id     = 3,
            subscene_duration   = 5500,          # 5.5 seconds
            subscene_start_time = 0,
            subscene_end_time   = 5500,
            subscene_content    = "Title 'Python Variables' fades in",
            subscene_status     = "rendered",
        ),
        SubScene(
            subscene_id         = 2,
            subscene_name       = "Variable Diagram",
            subscene_index      = 1,
            parent_scene_id     = 3,
            subscene_duration   = 5700,          # 5.7 seconds
            subscene_start_time = 5500,
            subscene_end_time   = 11200,
            subscene_content    = "Box diagram animates: x = 5 assignment",
            subscene_status     = "rendered",
        ),
        SubScene(
            subscene_id         = 3,
            subscene_name       = "Summary Text",
            subscene_index      = 2,
            parent_scene_id     = 3,
            subscene_duration   = 5600,          # 5.6 seconds
            subscene_start_time = 11200,
            subscene_end_time   = 16800,
            subscene_content    = "Three variable examples fade in one by one",
            subscene_status     = "rendered",
        ),
    ]
)
```

---

# Section 3.4: Entity 2 — SubScene

## Subsection 3.4.1: What Is a SubScene?

A SubScene is a mini-scene inside a Scene. It represents one specific,
distinct animation block — one phase or moment within the larger Scene.

Think of a Scene like a chapter in a book. A SubScene is like a paragraph
inside that chapter. The chapter is the big container. The paragraphs are
the smaller, ordered pieces of content inside it.

```
+=====================================================================+
|                  THE SUBSCENE INSIDE A SCENE                        |
+=====================================================================+
|                                                                     |
|   SCENE 3 — "Python Variables" (16800 ms total)                     |
|   ─────────────────────────────────────────────────────────────    |
|   |                                                               | |
|   |  SubScene 1          SubScene 2          SubScene 3           | |
|   |  scene_map[0]        scene_map[1]        scene_map[2]         | |
|   |                                                               | |
|   |  start: 0 ms         start: 5500 ms      start: 11200 ms     | |
|   |  end:   5500 ms      end:   11200 ms     end:   16800 ms     | |
|   |  dur:   5500 ms      dur:   5700 ms      dur:   5600 ms      | |
|   |                                                               | |
|   |  "Title card         "Variable           "Summary fades      | |
|   |   animates in"        diagram draws"      in line by line"   | |
|   |                                                               | |
|   ─────────────────────────────────────────────────────────────    |
|                                                                     |
|   Total: 5500 + 5700 + 5600 = 16800 ms  ← MUST equal scene_duration|
|                                                                     |
+=====================================================================+
```

### Subsubsection 3.4.1.1: Where Is the SubScene Class Defined on Disk?

The `SubScene` class is defined in the same file as the `Scene` class,
directly below it:

```
/home/mina/SuperManim/core/entities/scenes.py
```

Both classes live in the same file because SubScene is always used as a
component of Scene — it is part of the same domain concept. They are
defined in the same file to make this relationship obvious and to keep
related code together.

## Subsection 3.4.2: The Full Python Class of the SubScene Entity

```python
# File location: /home/mina/SuperManim/core/entities/scenes.py
# (This class is defined BELOW the Scene class in the same file)

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


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
```

## Subsection 3.4.3: Every Property of the SubScene Entity Explained

Here is a quick reference table for all SubScene properties:

```
+================================================================+
|       SUBSCENE ENTITY — COMPLETE PROPERTY REFERENCE           |
+================================================================+
|                                                                |
|  GROUP 1 — IDENTITY                                            |
|  ──────────────────────────────────────────────────────────── |
|  subscene_id          int           Unique ID within scene.    |
|  subscene_name        str | None    Human label. Optional.     |
|  subscene_index       int           Position within scene.     |
|  parent_scene_id      int           Which scene owns this.     |
|                                                                |
|  GROUP 2 — TIMING (milliseconds, relative to parent Scene)    |
|  ──────────────────────────────────────────────────────────── |
|  subscene_duration    int | None    Length in ms.              |
|  subscene_start_time  int | None    Start offset in ms.        |
|  subscene_end_time    int | None    End offset in ms.          |
|                                                                |
|  GROUP 3 — CONTENT                                             |
|  ──────────────────────────────────────────────────────────── |
|  subscene_content     str | None    Plain-text description.    |
|  subscene_code_path   str | None    Optional separate .py file.|
|  subscene_hash        str | None    SHA-256 of separate code.  |
|                                                                |
|  GROUP 4 — STATUS                                              |
|  ──────────────────────────────────────────────────────────── |
|  subscene_status      str           pending/rendered/failed.   |
|  subscene_output_path str | None    Path to clip if rendered.  |
|                                                                |
+================================================================+
```

### Subsubsection 3.4.3.1: GROUP 1 — Identity Properties

#### Subsubsubsection 3.4.3.1.1: subscene_id

**Type:** `int`
**Default:** Required — no default. Must be provided.
**Example:** `1`, `2`, `3`

The unique identifier for this SubScene within its parent Scene.
`subscene_id = 1` means this is the first block. `subscene_id = 2`
means this is the second block, and so on.

Note: `subscene_id` is only unique WITHIN the parent scene. Two different
Scenes can each have a SubScene with `subscene_id = 1`. They are
different objects belonging to different parents.

#### Subsubsubsection 3.4.3.1.2: subscene_name

**Type:** `Optional[str]`
**Default:** `None`
**Example:** `"Title Card"`, `"Diagram Block"`, `"Summary Text"`

A human-readable name for this animation block. Purely for documentation.
The system does not use this to make any processing decisions.

#### Subsubsubsection 3.4.3.1.3: subscene_index

**Type:** `int`
**Default:** `0`
**Example value:** `1` (meaning this is the second block, 0-based)

The playback order position of this SubScene within its parent Scene.
The first SubScene has `subscene_index = 0`, the second has `1`, and so
on. This determines the order in which animation blocks play within the
parent Scene.

#### Subsubsubsection 3.4.3.1.4: parent_scene_id

**Type:** `int`
**Default:** `0`
**Example value:** `3`

The `scene_id` of the Scene that this SubScene belongs to. This is the
back-link that connects the SubScene to its parent.

```
+-------------------------------------------------------------+
|   HOW parent_scene_id LINKS SUBSCENES TO THEIR PARENT       |
+-------------------------------------------------------------+
|                                                             |
|   Scene 3  (scene_id = 3)                                   |
|   │                                                         |
|   ├── scene_map = [                                         |
|   │       SubScene(subscene_id=1, parent_scene_id=3, ...),  |
|   │       SubScene(subscene_id=2, parent_scene_id=3, ...),  |
|   │       SubScene(subscene_id=3, parent_scene_id=3, ...),  |
|   │   ]                                                     |
|   │                                                         |
|   Every SubScene in Scene 3 points back to it               |
|   via parent_scene_id = 3.                                   |
|                                                             |
|   If you find a SubScene in the database and want to know   |
|   which scene it belongs to, just read parent_scene_id.     |
+-------------------------------------------------------------+
```

### Subsubsection 3.4.3.2: GROUP 2 — Timing Properties

**CRITICAL NOTE:** All timing values here are in **milliseconds** and are
measured relative to the **start of the parent Scene**, NOT relative to
the start of the full video.

So `subscene_start_time = 5500` means this block starts 5.5 seconds into
Scene 3. It does NOT mean 5.5 seconds into the overall video.

```
+-------------------------------------------------------------+
|   SUBSCENE TIMING IS RELATIVE TO THE PARENT SCENE           |
+-------------------------------------------------------------+
|                                                             |
|   Scene 3 starts at 31000ms in the full video               |
|   Scene 3 is 16800ms long                                   |
|                                                             |
|   SubScene 2 inside Scene 3:                                |
|     subscene_start_time = 5500   ← 5.5 sec into SCENE 3    |
|     (NOT 5.5 sec into the full video)                       |
|                                                             |
|   Position in full video = 31000 + 5500 = 36500ms           |
|   (This calculation is done by TimelineService, not here)   |
|                                                             |
+-------------------------------------------------------------+
```

#### Subsubsubsection 3.4.3.2.1: subscene_duration

**Type:** `Optional[int]`
**Default:** `None`
**Example:** `5700` (meaning 5.7 seconds)

How many milliseconds this animation block lasts. All SubScene durations
inside one Scene must add up exactly to the parent Scene's `scene_duration`.
This is a data integrity rule enforced by the ValidationService.

```
Scene 3  →  scene_duration = 16800 ms

  SubScene 1:  subscene_duration = 5500
  SubScene 2:  subscene_duration = 5700
  SubScene 3:  subscene_duration = 5600
               ────────────────────────
  Total:                        = 16800  ← must equal scene_duration
```

#### Subsubsubsection 3.4.3.2.2: subscene_start_time

**Type:** `Optional[int]`
**Default:** `None`
**Example:** `5500` (meaning 5500 ms into the parent Scene)

The millisecond offset from the start of the parent Scene when this
animation block begins.

#### Subsubsubsection 3.4.3.2.3: subscene_end_time

**Type:** `Optional[int]`
**Default:** `None`
**Example:** `11200` (meaning 11200 ms into the parent Scene)

The millisecond offset from the start of the parent Scene when this
animation block ends. Always computed as:
```
subscene_end_time = subscene_start_time + subscene_duration
Example: 5500 + 5700 = 11200
```

### Subsubsection 3.4.3.3: GROUP 3 — Content Properties

#### Subsubsubsection 3.4.3.3.1: subscene_content

**Type:** `Optional[str]`
**Default:** `None`
**Example:** `"Animated title: Python Variables appear with FadeIn effect"`

A plain-English description of what happens in this animation block.
Purely for human documentation and reference.

#### Subsubsubsection 3.4.3.3.2: subscene_code_path

**Type:** `Optional[str]`
**Default:** `None`
**Example:** `"my_scenes/example_block_02.py"`

If this SubScene has its own separate Python code file (instead of being
part of the parent Scene's single code file), the path to that file is
stored here. This is optional. Most SubScenes are just sections within
the parent Scene's code and do not have their own separate file.

#### Subsubsubsection 3.4.3.3.3: subscene_hash

**Type:** `Optional[str]`
**Default:** `None`
**Example:** `"d4e9a1b3f7c2e9a1b3f7c2e9a1b3f7c2..."`

The SHA-256 fingerprint of this SubScene's separate code file (only
applicable when `subscene_code_path` is set). Used for change detection
at the SubScene level, following the same principle as `scene_code_hash`
on the parent Scene.

### Subsubsection 3.4.3.4: GROUP 4 — Status Properties

#### Subsubsubsection 3.4.3.4.1: subscene_status

**Type:** `str`
**Default:** `"pending"`
**Allowed values:** `"pending"`, `"rendered"`, `"failed"`, `"skipped"`

The processing status of this SubScene. Uses the same four-value system
as `scene_status` on the parent Scene. Each value means the same thing
but applies to this specific SubScene animation block rather than the
whole scene.

#### Subsubsubsection 3.4.3.4.2: subscene_output_path

**Type:** `Optional[str]`
**Default:** `None`
**Example:** `"output/scene_03/subscene_02.mp4"`

If this SubScene was rendered as its own separate video clip (rather than
being part of the parent scene's single render output), this field stores
the path to that clip on disk.

---


# Section 3.5: Entity 3 — Project

## Subsection 3.5.1: What Is a Project?

A Project is the top-level workspace for one complete video production.
It is the container that holds absolutely everything related to that
production — every Scene, every audio file, every rendered video,
every setting, every fingerprint, and every piece of history.

Think of a Project like a physical desk in a studio. On that desk you have:
a folder for each scene's code files, a drawer for your audio recordings,
a shelf for your rendered video clips, a notepad where you wrote your
settings, and a filing cabinet that remembers everything you have done
so far. The desk itself is the Project. Without the desk, all those things
would be scattered on the floor with no organization and no connection
to each other.

Every single command you type in SuperManim operates on a Project. There
is no work without a Project. The Golden Rule of SuperManim is:
**no command can run unless a Project is currently open.**

### Subsubsection 3.5.1.1: Where Is the Project File on Disk?

```
/home/mina/SuperManim/core/entities/project.py
```

## Subsection 3.5.2: The Three Roles of a Project

A Project plays three roles at the same time:

```
+=====================================================================+
|                   THE THREE ROLES OF A PROJECT                      |
+=====================================================================+
|                                                                     |
|   ROLE 1 — THE WORKSPACE                                            |
|   ─────────────────────────────────────────────────────────────    |
|   A Project is a physical folder on your computer's disk.           |
|   This folder contains every file that belongs to this project.     |
|   Audio clips, rendered videos, preview files, code copies,         |
|   the database — all of them live inside the project folder.        |
|                                                                     |
|   ROLE 2 — THE MEMORY                                               |
|   ─────────────────────────────────────────────────────────────    |
|   A Project contains a database file (project_data.db).             |
|   This database is the project's long-term memory.                  |
|   It remembers: how many scenes exist, their durations,             |
|   which ones were rendered, what the fingerprints are,              |
|   what the export settings are, and everything else.                |
|   Without this database the project is just an empty folder.        |
|                                                                     |
|   ROLE 3 — THE IDENTITY                                             |
|   ─────────────────────────────────────────────────────────────    |
|   A Project has a name, a creation timestamp, and a location.       |
|   These identify it among all other projects.                       |
|   When you type "list projects", SuperManim reads the identity      |
|   fields of all projects and shows them to you.                     |
|                                                                     |
+=====================================================================+
```

## Subsection 3.5.3: The Physical Folder Structure of a Project

When you type `new project MyAnimation` and press Enter, SuperManim does
not just create a record in a database. It creates a real folder on your
computer's disk with a specific structure inside it:

```
+=====================================================================+
|             THE FULL PROJECT FOLDER STRUCTURE ON DISK               |
+=====================================================================+
|                                                                     |
|   /projects/MyAnimation/                                            |
|   |                                                                 |
|   +-- project_data.db          THE BRAIN                           |
|   |                            SQLite database. Stores all settings,|
|   |                            scene records, hashes, audio records.|
|   |                            Without this, project cannot open.  |
|   |                                                                 |
|   +-- audio_clips/             THE SOUND ROOM                       |
|   |   +-- original_audio.mp3   The master audio file.              |
|   |   +-- clip_001.mp3         Cut piece for Scene 1.              |
|   |   +-- clip_002.mp3         Cut piece for Scene 2.              |
|   |   +-- clip_003.mp3         Cut piece for Scene 3.              |
|   |                                                                 |
|   +-- scenes/                  THE WORKSHOP                         |
|   |   +-- scene_01/            Folder for Scene 1's files.         |
|   |   +-- scene_02/            Folder for Scene 2's files.         |
|   |   +-- scene_03/            Folder for Scene 3's files.         |
|   |                                                                 |
|   +-- output/                  THE CINEMA                           |
|   |   +-- scene_01/            Rendered .mp4 for Scene 1.          |
|   |   |   +-- scene_01.mp4                                          |
|   |   +-- scene_02/            Rendered .mp4 for Scene 2.          |
|   |   |   +-- scene_02.mp4                                          |
|   |   +-- scene_03/            Rendered .mp4 for Scene 3.          |
|   |       +-- scene_03.mp4                                          |
|   |                                                                 |
|   +-- previews/                THE DRAFT ROOM                       |
|   |   +-- scene_01_preview.mp4  Low-quality 480p draft.            |
|   |   +-- scene_02_preview.mp4                                      |
|   |                                                                 |
|   +-- exports/                 THE DELIVERY ROOM                    |
|   |   +-- MyAnimation_final.mp4  The assembled final video.        |
|   |                                                                 |
|   +-- assets/                  THE LIBRARY                          |
|   |   +-- images/              User-provided images (.png, .jpg)   |
|   |   +-- fonts/               Custom fonts (.ttf, .otf)           |
|   |   +-- videos/              Embedded video clips                 |
|   |                                                                 |
|   +-- cache/                   THE FINGERPRINT VAULT                |
|   |                            SHA-256 hash files for change detect.|
|   |                                                                 |
|   +-- temp/                    THE TRASH BIN                        |
|                                Temporary files. Auto-cleaned.       |
|                                                                     |
+=====================================================================+
```


### Subsection 3.5.4 The Full Python Class

A Project Entity is a `@dataclass`. It is a pure data container.
It holds all the information about one project. It does not create folders.
It does not open databases. It does not print anything.
The `ProjectService` does those things by reading and writing
the fields of this Entity.

Here is the complete Project Entity with every property:

```python
# core/entities/project.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, TYPE_CHECKING

# Using TYPE_CHECKING to avoid circular imports during type hinting
if TYPE_CHECKING:
    from .media_unit import MediaUnit
    from .render_settings import RenderSettings
    from .audio_settings import AudioSettings
    from .video_settings import VideoSettings
    from .export_settings import ExportSettings

@dataclass
class Project:
    """
    The Project Entity represents one complete video production workspace.
    It is a pure data container holding identifying info, location data, 
    settings, and the list of media items.
    """

    # -- IDENTITY --
    project_name: str

    # -- LOCATION --
    # Paths for project folders and database storage
    project_folder_path: Optional[str] = None
    project_db_path: Optional[str] = None

    # -- TIMESTAMPS --
    # ISO formatted strings for creation and last update
    project_created_at: Optional[str] = None
    
    # -- CONTENT --
    # List of MediaUnit objects (audio clips, video clips, or Manim scenes)
    # Using field(default_factory=list) ensures a fresh list for every new project
    project_items: List[MediaUnit] = field(default_factory=list)

    # -- SETTINGS (Optional components) --
    project_render_settings:   Optional[RenderSettings]  = None
    project_audio_settings:    Optional[AudioSettings]   = None
    project_video_settings:    Optional[VideoSettings]   = None
    project_export_settings:   Optional[ExportSettings]  = None
    project_preview_settings:  Optional[PreviewSettings] = None
    # -- STATE --
    # 1 = Open (Active in memory), 0 = Closed
    project_state: int = 0
```

-


## Subsection 3.5.5: Every Property of the Project Entity Explained

### Subsubsection 3.5.5.1: GROUP 1 — Identity Properties

#### Subsubsubsection 3.5.5.1.1: project_name

**Type:** `str`
**Default:** Required — no default. Must be provided.
**Example value:** `"MyAnimation"`, `"Chapter1_Intro"`, `"PythonTutorial"`

The `project_name` is the human-readable name for this project. It is
the name the user gave when they typed `new project MyAnimation`. It is
also the name of the folder created on disk. The name cannot contain spaces.

```
+-------------------------------------------------------------+
|   VALID vs INVALID PROJECT NAMES                            |
+-------------------------------------------------------------+
|                                                             |
|   VALID names:                                              |
|   MyAnimation                                               |
|   Chapter1_Video                                            |
|   lecture-intro                                             |
|   PythonTutorial_v2                                         |
|                                                             |
|   INVALID names:                                            |
|   My Animation        <- has a space — REFUSED              |
|   my video project    <- has spaces — REFUSED               |
|                                                             |
+-------------------------------------------------------------+
```

### Subsubsection 3.5.5.2: GROUP 2 — Location Properties

#### Subsubsubsection 3.5.5.2.1: project_folder_path

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"/home/user/projects/MyAnimation"`

The full absolute path to the root folder of this project on your
computer's file system. Every other file path in the system (scene output,
audio clips, etc.) lives inside this root folder.

```
project_folder_path = "/home/user/projects/MyAnimation"

All paths derived from this root:
  audio_clips/ = project_folder_path + "/audio_clips/"
  scenes/      = project_folder_path + "/scenes/"
  output/      = project_folder_path + "/output/"
  database     = project_folder_path + "/project_data.db"
```

#### Subsubsubsection 3.5.5.2.2: project_db_path

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"/home/user/projects/MyAnimation/project_data.db"`

The full path to the SQLite database file for this project. This is the
brain of the project — the file that remembers everything across sessions.
When you type `open project MyAnimation`, the very first thing the system
does is locate this file and open it. If this file is missing or corrupted,
the project cannot be opened.

### Subsubsection 3.5.5.3: GROUP 3 — Timestamp Properties

#### Subsubsubsection 3.5.5.3.1: project_created_at

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"2024-11-10 09:00:15"`

The exact date and time when this project was first created. Written
once at creation time and never changed again for the life of the project.
It is the project's birth certificate.


### Subsubsection 3.5.5.4: GROUP 4 — State Properties

#### Subsubsubsection 3.5.5.4.1: project_state

**Type:** `int`
**Default:** `0`
**Allowed values:** `0` or `1`

`project_state = 1` means the project is currently open and active in
memory. `project_state = 0` means the project is closed. This field is
stored in the database so that if SuperManim crashes or is force-closed,
the next session can detect that a project was previously open and offer
to re-open it.

### Subsubsection 3.5.5.5: GROUP 5 — Render Settings Properties

Theis is  the project-level property for how scenes are rendered.
This property is an optional property which means the project can have it or
it can be None if the tool is used only to edits some audio files or even
video files such as splitting them , change the audio formats of them
in this case the project doesn't need this property but when dealing with
redering manim code then you need it.The RenderSettings is an entity and
it will be defined in the following section 




### Subsubsection 3.5.5.6: GROUP 6 — Preview Settings Properties

Theis is  the project-level property for how scenes are previewed.
This property is an optional property which means the project can have it or
it can be None if the tool is used only to edits some audio files or even
video files such as splitting them , change the audio formats of them
in this case the project doesn't need this property but when dealing with
redering manim code and want ot preview them then you need it.The PreviewSettings is an entity and
it will be defined in the following section `Section `



### Subsubsection 3.5.5.7: GROUP 7 — Audio Settings Properties

Theis is  the project-level property for the audio settings these
all the settings related to the audio this property is needed when the
tool is used to edit audio file and also when dealing with audio file related
to the manim code rednered video explained AudioSettings in section ..

### Subsubsection 3.5.5.8: GROUP 8 — Export Settings Properties

Theis is  the project-level property for the export settings these

### Subsubsection 3.5.5.9: GROUP 9 — Project Items Statistics Properties

this the propert of the list of all items the project have this list can be
a list of audio clips
a list of video clips
a list of rendered manim code



### Subsection 3.5.6 HOW A PROJECT IS BORN — THE COMPLETE CREATION FLOW

When the user types `new project MyAnimation` and presses Enter, here
is the complete step-by-step sequence of everything that happens from
that moment until the project is ready to use:

```
+=====================================================================+
|              PROJECT CREATION — COMPLETE FLOW                       |
+=====================================================================+
|                                                                     |
|   USER TYPES:  new project MyAnimation                              |
|                                                                     |
|   STEP 1: Shell receives the command.                               |
|   SuperManimShell.do_new("project MyAnimation")                     |
|   Parses: command="new", keyword="project", name="MyAnimation"      |
|   Calls: project_service.create_project("MyAnimation")              |
|                                                                     |
|   STEP 2: Validate the name.                                        |
|   ValidationService.project_name_is_valid("MyAnimation")            |
|   Checks: contains spaces? NO. Empty? NO. Valid chars? YES.         |
|   Result: VALID. Continue.                                          |
|                                                                     |
|   STEP 3: Check it does not already exist.                          |
|   ProjectRepositoryPort.project_exists("MyAnimation") -> False      |
|   No existing project with this name. No conflict. Continue.        |
|                                                                     |
|                         |
|                            |
|                                                                     |
|   STEP 4: Create the Project Entity in memory.                      |
|   project = Project(                                                |
|       project_id   = 1,                                             |
|       project_name = "MyAnimation",                                 |
|       project_mode = "supermanim",                                  |
|   )                                                                 |
|   (all other fields start at their defaults)                        |
|                                                                     |
|   STEP 5: Set the folder and database paths.                        |
|   project.project_folder_path = "/projects/MyAnimation"             |
|   project.project_db_path     = "/projects/MyAnimation/            |
|                                   project_data.db"                  |
|                                                                     |
|   STEP 6: Create all folders on disk.                               |
|   FileStoragePort.create_folder("/projects/MyAnimation/")           |
|   FileStoragePort.create_folder(".../audio_clips/")                 |
|   FileStoragePort.create_folder(".../scenes/")                      |
|   FileStoragePort.create_folder(".../output/")                      |
|   FileStoragePort.create_folder(".../previews/")                    |
|   FileStoragePort.create_folder(".../exports/")                     |
|   FileStoragePort.create_folder(".../assets/")                      |
|   FileStoragePort.create_folder(".../cache/")                       |
|   FileStoragePort.create_folder(".../temp/")                        |
|                                                                     |
|   STEP 7: Record the creation timestamp.                            |
|   now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")                |
|   project.project_created_at  = now                                 |
|                                  |
|                                                                     |
|   STEP 8: Save the Project Entity to the database.                  |
|   ProjectRepositoryPort.save_project(project)                       |
|   -> SqliteProjectRepository writes the record to                   |
|      /projects/MyAnimation/project_data.db                          |
|                                                                     |
|                          |
|                                                                     |
|   STEP 11: Tell the user everything that was done.                  |
|   NotificationPort.send_success(                                    |
|       "Creating project: MyAnimation\n"                             |
|       "Creating folder: /projects/MyAnimation/\n"                  |
|       "Creating folder: /projects/MyAnimation/scenes/\n"           |
|       "...all other folders...\n"                                   |
|       "Creating database: /projects/MyAnimation/project_data.db\n" |
|       "Project MyAnimation created successfully.\n"                 |
|       "You are now working inside this project."                    |
|   )                                                                 |
|                                                                     |
+=====================================================================+
```





# Section 3.6: Entity 4 — MediaUnit

## Subsection 3.6.1: What Is MediaUnit?

`MediaUnit` is the **abstract base class** for all media items that can
appear on a SuperManim project timeline. It is NOT a concrete thing you
create directly — you can never write `MediaUnit(...)` in your code.
Instead, it is the shared parent class that concrete media types
(`AudioClip`, `VideoClip`, and `Scene`) all inherit from.

Think of it like this: in the real world, you might have audio clips,
video clips, and Manim animation scenes. They are all very different
things. But they all share one fundamental characteristic — they occupy
a stretch of time. They have a start point, an end point, and a duration.
`MediaUnit` is the concept that captures this shared characteristic.

```
+=====================================================================+
|              THE MEDIAUNIT INHERITANCE HIERARCHY                     |
+=====================================================================+
|                                                                     |
|                      MediaUnit  (Abstract)                           |
|                      ─────────────────────                          |
|                       unit_type: str                                |
|                       file_path: Optional[str]                      |
|                       start_time: Optional[int]                     |
|                       end_time: Optional[int]                       |
|                       duration: Optional[int]                       |
|                                                                     |
|         ┌────────────────┬─────────────────┬───────────────┐        |
|         │                │                 │               │        |
|     AudioClip        VideoClip           Scene         (future)     |
|     ──────────       ──────────         ──────                      |
|     + audio_clip_id  + video_clip_id   + scene_id                   |
|     + audio_format   + video_format    + scene_code_path            |
|     + sample_rate    + fps             + scene_fps                  |
|     + channels       + resolution      + scene_map                  |
|     + is_synced      + has_audio        + hashes                    |
|                                                                     |
|   All three inherit start_time, end_time, duration, file_path       |
|   from MediaUnit. They just add their own specific fields.          |
|                                                                     |
+=====================================================================+
```

### Subsubsection 3.6.1.1: Where Is the MediaUnit Class Defined on Disk?

```
/home/mina/SuperManim/core/entities/media_unit.py
```

## Subsection 3.6.2: The Full Python Class of MediaUnit

```python
# File location: /home/mina/SuperManim/core/entities/media_unit.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from abc import ABC, abstractmethod


@dataclass
class MediaUnit(ABC):
    """
    MediaUnit is the abstract base class for all media items that
    can appear on a SuperManim project timeline.

    Every concrete media type (AudioClip, VideoClip, Scene) inherits
    from this class. By inheriting, each subclass is GUARANTEED to
    have a unit_type, a file_path, and timing properties (start_time,
    end_time, duration). The Project entity can then hold a single
    list[MediaUnit] and work with all types uniformly.

    This class is abstract — you CANNOT instantiate it directly:
        unit = MediaUnit(...)     ← This will raise a TypeError.

    You CAN instantiate its concrete subclasses:
        clip = AudioClip(...)     ← This works fine.
        clip = VideoClip(...)     ← This works fine.
        scene = Scene(...)        ← This works fine.

    All timing values are integers in MILLISECONDS.
    """

    # ── CORE IDENTITY ─────────────────────────────────────────────────
    # unit_type tells the system what kind of media item this is.
    # Allowed values: "audio_clip", "video_clip", "scene"
    unit_type:      str

    # ── FILE LOCATION ─────────────────────────────────────────────────
    # The path to the media file on disk that this unit represents.
    file_path:      Optional[str]   = None

    # ── TIMING (in milliseconds) ───────────────────────────────────────
    # These represent where this media unit sits in the timeline.
    # start_time and end_time are positions in the OVERALL project video.
    # duration is the length of this media unit itself.
    start_time:     Optional[int]   = None
    end_time:       Optional[int]   = None
    duration:       Optional[int]   = None
```

## Subsection 3.6.3: Why Does MediaUnit Exist?

Without `MediaUnit`, the `Project` entity would need a separate list for
each media type:

```python
# WITHOUT MediaUnit (fragile, closed design):
@dataclass
class Project:
    audio_clips: list = field(default_factory=list)   # List[AudioClip]
    video_clips: list = field(default_factory=list)   # List[VideoClip]
    scenes:      list = field(default_factory=list)   # List[Scene]
    # Problem 1: Every time you add a new media type (e.g., ImageSlide),
    #            you must add a new list HERE and update EVERY service
    #            that iterates over project items.
    # Problem 2: You cannot treat all items as one unified timeline.
```

With `MediaUnit`, the `Project` entity has ONE unified list:

```python
# WITH MediaUnit (open, extensible design):
@dataclass
class Project:
    project_items: list = field(default_factory=list)   # List[MediaUnit]
    # AudioClip, VideoClip, and Scene ALL go into this same list.
    # Adding a brand new media type (e.g., ImageSlide) requires:
    #   - Creating the new class that inherits from MediaUnit
    #   - That's it. No changes to Project needed.
```

This is called the **Open/Closed Principle** — the system is open for
extension (add new types) but closed for modification (existing code does
not change when you add new types).

## Subsection 3.6.4: How Subclasses Use MediaUnit

When you define `AudioClip(MediaUnit)`, Python copies all of MediaUnit's
fields into `AudioClip` automatically. You just add the AudioClip-specific
fields on top:

```python
# AudioClip inherits from MediaUnit:
@dataclass
class AudioClip(MediaUnit):
    # These fields come from MediaUnit (inherited automatically):
    #   unit_type, file_path, start_time, end_time, duration

    # These fields are AudioClip-specific (defined here):
    audio_clip_id:      int        = 0
    audio_clip_format:  str        = "mp3"
    audio_clip_channels: int       = 1
    audio_clip_is_synced: bool     = False
    # ... and more
```

When the system iterates over `project.project_items` to build the
timeline, it can treat every item identically because they all have
`start_time`, `end_time`, and `duration`. When the audio sync service
needs to check if an item is an audio clip, it checks `unit.unit_type`.

---

# Section 3.7: Entity 5 — AudioClip

## Subsection 3.7.1: What Is an AudioClip?

An `AudioClip` is one cut piece of the master audio file. It is a specific
time segment of the original full-length recording — the piece that belongs
to and will play alongside a single specific Scene.

When the user runs `split audio 4` (split the master audio into 4 pieces,
one for each scene), the system uses FFmpeg to cut the audio file into
pieces. Each piece is saved to disk, and an `AudioClip` Entity is created
to record all the metadata about that piece.

```
+=====================================================================+
|          THE MASTER AUDIO BECOMES INDIVIDUAL AUDIOCLIPS             |
+=====================================================================+
|                                                                     |
|   MASTER AUDIO FILE                                                 |
|   original_audio.mp3  (60000 ms = 60.0 seconds total)              |
|   ─────────────────────────────────────────────────────────────    |
|   │                                                               | |
|   │  0ms ────── 12500ms ────── 31000ms ──── 47800ms ──── 60000ms | |
|   │                                                               | |
|   ────────────────────────────────────────────────────────────     |
|         ↓              ↓              ↓              ↓              |
|   AudioClip 1    AudioClip 2    AudioClip 3    AudioClip 4          |
|   clip_001.mp3   clip_002.mp3   clip_003.mp3   clip_004.mp3         |
|   (0-12500ms)    (12500-31000ms)(31000-47800ms)(47800-60000ms)      |
|   12.5 seconds   18.5 seconds   16.8 seconds   12.2 seconds         |
|                                                                     |
|   Scene 1 ────↑  Scene 2 ────↑  Scene 3 ────↑  Scene 4 ────↑       |
|   (each clip is linked to the scene it plays with)                  |
|                                                                     |
+=====================================================================+
```

### Subsubsection 3.7.1.1: Where Is the AudioClip Class Defined on Disk?

```
/home/mina/SuperManim/core/entities/audio_clip.py
```

## Subsection 3.7.2: The Full Python Class of the AudioClip Entity

```python
# File location: /home/mina/SuperManim/core/entities/audio_clip.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from core.entities.media_unit import MediaUnit


@dataclass
class AudioClip(MediaUnit):
    """
    The AudioClip Entity represents one cut section of the master audio file.

    It is a pure data container. It holds information about a specific
    audio clip file on disk — its path, its timing, its format, and its
    relationship to a Scene.

    It does NOT call FFmpeg. It does NOT read audio files from disk.
    It does NOT play audio. It does NOT call print(). It is just data.

    TIMING NOTE:
    The timing fields inherited from MediaUnit (start_time, end_time,
    duration) use milliseconds like all other entities.

    The AudioClip-specific timing fields (audio_clip_duration,
    audio_clip_start_time, audio_clip_end_time) store values in
    SECONDS as floats — because this is the native unit used by audio
    file metadata and audio analysis tools like librosa and FFprobe.
    """

    # ── GROUP 1 — IDENTITY ────────────────────────────────────────────
    audio_clip_id:              int             = 0
    audio_file_id:              int             = 0

    # ── GROUP 2 — ORDERING AND LINKING ───────────────────────────────
    audio_clip_index:           int             = 0
    scene_id:                   Optional[int]   = None

    # ── GROUP 3 — LOCATION ────────────────────────────────────────────
    audio_clip_path:            Optional[str]   = None

    # ── GROUP 4 — FORMAT ──────────────────────────────────────────────
    audio_clip_format:          str             = "mp3"

    # ── GROUP 5 — TIMING (in SECONDS as floats — audio convention) ────
    audio_clip_duration:        Optional[float] = None
    audio_clip_start_time:      Optional[float] = None
    audio_clip_end_time:        Optional[float] = None

    # ── GROUP 6 — TECHNICAL PROPERTIES ───────────────────────────────
    audio_clip_sample_rate:     Optional[int]   = None
    audio_clip_channels:        int             = 1
    audio_clip_file_size_bytes: Optional[int]   = None

    # ── GROUP 7 — STATE ───────────────────────────────────────────────
    audio_clip_is_synced:       bool            = False
    audio_clip_created_at:      Optional[str]   = None

    # NOTE: The unit_type field (inherited from MediaUnit) is always
    # set to "audio_clip" for AudioClip instances. It tells the system
    # what type of MediaUnit this is when iterating over project_items.
    # Set it explicitly when creating an AudioClip:
    #   AudioClip(unit_type="audio_clip", audio_clip_id=3, ...)
```

## Subsection 3.7.3: Every Property of the AudioClip Entity Explained

### Subsubsection 3.7.3.1: GROUP 1 — Identity Properties

#### Subsubsubsection 3.7.3.1.1: audio_clip_id

**Type:** `int`
**Default:** `0` (should always be set to a real value when creating)
**Example value:** `3`

The unique identifier for this AudioClip within the project. No two
AudioClips in the same project share the same `audio_clip_id`. Used as
the primary key in the database.

#### Subsubsubsection 3.7.3.1.2: audio_file_id

**Type:** `int`
**Default:** `0`
**Example value:** `1`

The `audio_file_id` of the master `AudioFile` that this clip was cut
from. This is the back-link that connects the AudioClip to its parent
AudioFile entity.

A project typically has one master `AudioFile` with `audio_file_id = 1`.
All the AudioClips produced by splitting it will have `audio_file_id = 1`.
If a project ever has two separate master audio files, this field tells
you which master each clip came from.

### Subsubsection 3.7.3.2: GROUP 2 — Ordering and Linking Properties

#### Subsubsubsection 3.7.3.2.1: audio_clip_index

**Type:** `int`
**Default:** `0`
**Example value:** `2` (third clip, 0-based)

The position of this clip in the sequence of clips cut from the master
audio file. Zero-based: the first clip has `audio_clip_index = 0`, the
second has `1`, and so on. Used for ordering clips in display and export.

#### Subsubsubsection 3.7.3.2.2: scene_id

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `3`

The `scene_id` of the Scene that this audio clip is linked to and will
play alongside. When the user runs `sync scene 3`, the system links
AudioClip 3 to Scene 3 by setting `scene_id = 3` on the AudioClip.

`None` means this clip has not been linked to any scene yet.

### Subsubsection 3.7.3.3: GROUP 3 — Location Properties

#### Subsubsubsection 3.7.3.3.1: audio_clip_path

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"audio_clips/clip_003.mp3"`

The file path to this audio clip on disk. FFmpeg saved the cut audio
file here when the `split audio` command ran. The render system reads
this path when it needs to mix this audio into the rendered video.

### Subsubsection 3.7.3.4: GROUP 4 — Format Properties

#### Subsubsubsection 3.7.3.4.1: audio_clip_format

**Type:** `str`
**Default:** `"mp3"`
**Example value:** `"mp3"`, `"wav"`, `"ogg"`, `"aac"`

The file format of this audio clip. AudioClips automatically inherit
the format of the master AudioFile they were cut from, because FFmpeg
preserves the original format when cutting a section of audio (unless
you explicitly request a conversion).

### Subsubsection 3.7.3.5: GROUP 5 — Timing Properties

**IMPORTANT NOTE ON UNITS:** The timing fields in this group are stored
in **SECONDS as float values**, not in milliseconds. This is different
from all other timing in the system. The reason is that audio file
metadata and audio analysis libraries (like FFprobe, librosa) all work
natively in seconds. Storing audio timing in seconds avoids unnecessary
conversions when reading/writing audio metadata.

When comparing with Scene timing (which is in milliseconds), the
`ValidationService` does the conversion: `audio_seconds × 1000 == scene_ms`.

#### Subsubsubsection 3.7.3.5.1: audio_clip_duration

**Type:** `Optional[float]`
**Default:** `None`
**Example value:** `16.8` (meaning 16.8 seconds)

The length of this audio clip in seconds. This is the value that gets
compared to the Scene's `scene_duration` (after unit conversion) during
the `sync scene` command.

```
AudioClip 3:  audio_clip_duration = 16.8 seconds
Scene 3:      scene_duration      = 16800 milliseconds

Sync check conversion:
  16.8 seconds × 1000 = 16800 ms
  16800 ms == 16800 ms  →  MATCH  →  sync approved
```

#### Subsubsubsection 3.7.3.5.2: audio_clip_start_time

**Type:** `Optional[float]`
**Default:** `None`
**Example value:** `31.0`

The exact second in the MASTER AudioFile where this clip begins. This is
a reference back to the original uncut recording, not a property of the
clip file itself.

For AudioClip 3, `audio_clip_start_time = 31.0` means: "This clip
represents the portion of original_audio.mp3 that starts at the
31.0-second mark."

This value is essential for:
- Displaying the audio timeline (`show audio info` command)
- Re-cutting the clips if needed (the system knows exactly where to cut)
- Debugging timing problems

#### Subsubsubsection 3.7.3.5.3: audio_clip_end_time

**Type:** `Optional[float]`
**Default:** `None`
**Example value:** `47.8`

The exact second in the MASTER AudioFile where this clip ends. Together
with `audio_clip_start_time`, this precisely defines which portion of the
original recording this clip represents.

```
AudioClip 3 — complete timing picture:
  audio_clip_start_time = 31.0  (starts at second 31.0 of original)
  audio_clip_end_time   = 47.8  (ends at second 47.8 of original)
  audio_clip_duration   = 16.8  (= 47.8 - 31.0 seconds long)

Terminal display in "show audio info":
  ┌─────────┬───────────┬───────────┬───────────┬─────────────────┐
  │ Scene   │ Start     │ End       │ Duration  │ Clip File       │
  ├─────────┼───────────┼───────────┼───────────┼─────────────────┤
  │   3     │  31.0s    │  47.8s    │  16.8s    │ clip_003.mp3   │
  └─────────┴───────────┴───────────┴───────────┴─────────────────┘
```

### Subsubsection 3.7.3.6: GROUP 6 — Technical Properties

These properties store the raw technical metadata of the audio file.
They are read automatically from the file using FFprobe or librosa when
the clip is created.

#### Subsubsubsection 3.7.3.6.1: audio_clip_sample_rate

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `44100`

The sample rate of this clip's audio file in Hz (samples per second).
AudioClips inherit this value from the parent AudioFile. Standard values:
- `44100` Hz — CD quality. Most common for music and narration.
- `48000` Hz — Professional/broadcast standard. Used in video production.

FFmpeg preserves the sample rate when cutting sections of audio.

#### Subsubsubsection 3.7.3.6.2: audio_clip_channels

**Type:** `int`
**Default:** `1`
**Example value:** `1` (mono), `2` (stereo)

The number of audio channels in this clip. Voice narration is almost
always mono (1 channel) because human speech does not benefit from stereo
separation. Background music is typically stereo (2 channels).

#### Subsubsubsection 3.7.3.6.3: audio_clip_file_size_bytes

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `1410048` (approximately 1.3 MB)

The size of this clip file on disk in bytes. Proportional to the clip's
duration and the compression level of the audio format (MP3 is compressed;
WAV is uncompressed and much larger).

### Subsubsection 3.7.3.7: GROUP 7 — State Properties

#### Subsubsubsection 3.7.3.7.1: audio_clip_is_synced

**Type:** `bool`
**Default:** `False`

`True` when this clip has been successfully linked to a Scene through the
`sync scene` command AND the duration check has passed. When `True`, this
clip will be mixed into the video when the linked scene is rendered.
When `False`, the clip exists on disk but is not active in any render.

#### Subsubsubsection 3.7.3.7.2: audio_clip_created_at

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"2024-11-10 09:10:45"`

The timestamp of when this clip file was created on disk — specifically,
the moment when FFmpeg finished cutting this section from the master
AudioFile during the `split audio N` command.

## Subsection 3.7.4: A Real AudioClip Object in Full

```python
# AudioClip 3 — fully populated example

AudioClip(
    # Inherited from MediaUnit:
    unit_type               = "audio_clip",
    file_path               = "audio_clips/clip_003.mp3",
    start_time              = 31000,   # ms position in project timeline
    end_time                = 47800,   # ms position in project timeline
    duration                = 16800,   # ms length

    # ── GROUP 1 — IDENTITY ──────────────────────────────────────────
    audio_clip_id           = 3,
    audio_file_id           = 1,

    # ── GROUP 2 — ORDERING AND LINKING ──────────────────────────────
    audio_clip_index        = 2,       # 0-based, so this is the 3rd clip
    scene_id                = 3,       # linked to Scene 3

    # ── GROUP 3 — LOCATION ──────────────────────────────────────────
    audio_clip_path         = "audio_clips/clip_003.mp3",

    # ── GROUP 4 — FORMAT ────────────────────────────────────────────
    audio_clip_format       = "mp3",

    # ── GROUP 5 — TIMING (in seconds as floats) ─────────────────────
    audio_clip_duration     = 16.8,    # 16.8 seconds
    audio_clip_start_time   = 31.0,    # starts at 31.0s in original
    audio_clip_end_time     = 47.8,    # ends at 47.8s in original

    # ── GROUP 6 — TECHNICAL PROPERTIES ──────────────────────────────
    audio_clip_sample_rate          = 44100,
    audio_clip_channels             = 1,       # mono voice narration
    audio_clip_file_size_bytes      = 1410048, # ~1.3 MB

    # ── GROUP 7 — STATE ─────────────────────────────────────────────
    audio_clip_is_synced    = True,    # linked and duration verified
    audio_clip_created_at   = "2024-11-10 09:10:45",
)
```

---

# Section 3.8: Entity 6 — VideoClip

## Subsection 3.8.1: What Is a VideoClip?

A `VideoClip` is one cut section of a master video file. It is the video
equivalent of an `AudioClip`. When the user has a video file and wants to
split it into pieces for the timeline, each piece is represented as a
`VideoClip` entity.

```
+=====================================================================+
|          THE MASTER VIDEO BECOMES INDIVIDUAL VIDEOCLIPS             |
+=====================================================================+
|                                                                     |
|   MASTER VIDEO FILE                                                 |
|   screen_record.mp4  (60000 ms = 60.0 seconds total)               |
|   ─────────────────────────────────────────────────────────────    |
|   │                                                               | |
|   │  0ms ─────────── 20000ms ──────────── 45000ms ─── 60000ms   | |
|   │                                                               | |
|   ────────────────────────────────────────────────────────────     |
|         ↓                       ↓                    ↓              |
|   VideoClip 1            VideoClip 2           VideoClip 3          |
|   (0-20000ms)            (20000-45000ms)        (45000-60000ms)     |
|   20.0 seconds           25.0 seconds           15.0 seconds        |
|                                                                     |
+=====================================================================+
```

### Subsubsection 3.8.1.1: Where Is the VideoClip Class Defined on Disk?

```
/home/mina/SuperManim/core/entities/video_clip.py
```

## Subsection 3.8.2: The Full Python Class of the VideoClip Entity

```python
# File location: /home/mina/SuperManim/core/entities/video_clip.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from core.entities.media_unit import MediaUnit


@dataclass
class VideoClip(MediaUnit):
    """
    The VideoClip Entity represents one cut section of a master video file.

    It is a pure data container. It holds all the information about a
    specific video clip file on disk — its path, its timing, its
    visual dimensions, its codec, and its link to a Scene.

    It does NOT call FFmpeg. It does NOT read video files.
    It does NOT decode frames. It is just structured data.

    All timing values (video_clip_duration, video_clip_start_time,
    video_clip_end_time) are stored as integers in MILLISECONDS,
    consistent with the rest of the system.
    """

    # ── GROUP 1 — IDENTITY ────────────────────────────────────────────
    video_clip_id:              int             = 0
    video_file_id:              int             = 0

    # ── GROUP 2 — ORDERING AND LINKING ───────────────────────────────
    video_clip_index:           int             = 0
    scene_id:                   Optional[int]   = None

    # ── GROUP 3 — LOCATION ────────────────────────────────────────────
    video_clip_path:            Optional[str]   = None

    # ── GROUP 4 — FORMAT ──────────────────────────────────────────────
    video_clip_format:          str             = "mp4"

    # ── GROUP 5 — TIMING (in milliseconds) ────────────────────────────
    video_clip_duration:        Optional[int]   = None
    video_clip_start_time:      Optional[int]   = None
    video_clip_end_time:        Optional[int]   = None

    # ── GROUP 6 — VISUAL PROPERTIES ───────────────────────────────────
    video_clip_resolution:      Optional[str]   = None
    video_clip_fps:             Optional[int]   = None
    video_clip_has_audio:       bool            = False

    # ── GROUP 7 — TECHNICAL PROPERTIES ───────────────────────────────
    video_clip_file_size_bytes: Optional[int]   = None
    video_clip_codec:           Optional[str]   = None

    # ── GROUP 8 — STATE ───────────────────────────────────────────────
    video_clip_status:          str             = "pending"
    video_clip_created_at:      Optional[str]   = None
```

## Subsection 3.8.3: Every Property of the VideoClip Entity Explained

### Subsubsection 3.8.3.1: GROUP 1 — Identity Properties

#### Subsubsubsection 3.8.3.1.1: video_clip_id

**Type:** `int`
**Default:** `0`
**Example value:** `2`

The unique identifier for this VideoClip within the project. Used as the
primary key in the database.

#### Subsubsubsection 3.8.3.1.2: video_file_id

**Type:** `int`
**Default:** `0`
**Example value:** `1`

The ID of the master `VideoFile` entity that this clip was cut from.
Links the VideoClip back to its parent VideoFile.

### Subsubsection 3.8.3.2: GROUP 2 — Ordering and Linking Properties

#### Subsubsubsection 3.8.3.2.1: video_clip_index

**Type:** `int`
**Default:** `0`
**Example value:** `1` (second clip, 0-based)

The position of this clip in the sequence of clips cut from the master
video file. Zero-based counting, same as `audio_clip_index`.

#### Subsubsubsection 3.8.3.2.2: scene_id

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `3`

The `scene_id` of the Scene this video clip is linked to. When set,
this clip will be used when rendering or assembling Scene 3.
`None` means not yet linked to any scene.

### Subsubsection 3.8.3.3: GROUP 3 — Location Properties

#### Subsubsubsection 3.8.3.3.1: video_clip_path

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"video_clips/clip_002.mp4"`

The file path to this video clip on disk.

### Subsubsection 3.8.3.4: GROUP 4 — Format Properties

#### Subsubsubsection 3.8.3.4.1: video_clip_format

**Type:** `str`
**Default:** `"mp4"`
**Example value:** `"mp4"`, `"webm"`, `"mov"`, `"avi"`, `"mkv"`

The container format of this video clip file.

### Subsubsection 3.8.3.5: GROUP 5 — Timing Properties

All values are **integers in milliseconds**.

#### Subsubsubsection 3.8.3.5.1: video_clip_duration

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `25000` (meaning 25.0 seconds)

The length of this video clip in milliseconds.

#### Subsubsubsection 3.8.3.5.2: video_clip_start_time

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `20000` (meaning 20.0 seconds into the master video)

The millisecond mark in the master VideoFile where this clip begins.

#### Subsubsubsection 3.8.3.5.3: video_clip_end_time

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `45000` (meaning 45.0 seconds into the master video)

The millisecond mark in the master VideoFile where this clip ends.
Always: `video_clip_end_time = video_clip_start_time + video_clip_duration`
(`20000 + 25000 = 45000`)

### Subsubsection 3.8.3.6: GROUP 6 — Visual Properties

#### Subsubsubsection 3.8.3.6.1: video_clip_resolution

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"1920x1080"`

The pixel dimensions of this video clip. Read from the video file's
metadata when the clip is created. Important for ensuring compatibility
when assembling clips in the final export step.

#### Subsubsubsection 3.8.3.6.2: video_clip_fps

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `30`, `60`

The frame rate of this video clip. Read from the file metadata.
All clips in a project should have the same fps to assemble cleanly.

#### Subsubsubsection 3.8.3.6.3: video_clip_has_audio

**Type:** `bool`
**Default:** `False`

`True` if this video clip contains an embedded audio track.
`False` if it is a silent (video-only) clip. The export system uses
this flag to decide whether to extract and include the audio from this
clip during the final video assembly.

### Subsubsection 3.8.3.7: GROUP 7 — Technical Properties

#### Subsubsubsection 3.8.3.7.1: video_clip_file_size_bytes

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `52428800` (approximately 50 MB)

The size of this video clip file on disk in bytes.

#### Subsubsubsection 3.8.3.7.2: video_clip_codec

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"h264"`, `"h265"`, `"vp9"`, `"av1"`

The video compression codec used to encode this clip. Different codecs
produce different quality-vs-file-size trade-offs. When assembling
multiple clips with different codecs, FFmpeg may need to re-encode some
of them to produce a consistent final output.

### Subsubsection 3.8.3.8: GROUP 8 — State Properties

#### Subsubsubsection 3.8.3.8.1: video_clip_status

**Type:** `str`
**Default:** `"pending"`
**Allowed values:** `"pending"`, `"ready"`, `"failed"`

The processing status of this video clip.
- `"pending"` — clip was just created, not yet fully processed
- `"ready"` — clip has been processed and is available for use
- `"failed"` — processing encountered an error

#### Subsubsubsection 3.8.3.8.2: video_clip_created_at

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"2024-11-10 09:30:00"`

The timestamp when this video clip was cut from the master video file
by FFmpeg.

---

# Section 3.9: Entity 7 — AudioFile

## Subsection 3.9.1: What Is an AudioFile?

An `AudioFile` is the master audio recording for a project. It represents
the complete, uncut audio file — the full-length narration or music track
that the user adds to the project with the `add audio voice.mp3` command.

The relationship between `AudioFile` and `AudioClip` is exactly like a
whole pizza and its individual slices. The `AudioFile` is the whole pizza.
Each `AudioClip` is one slice. You cut the pizza into slices (one per
scene), but the whole pizza still exists and is tracked as an `AudioFile`.

`AudioFile` is flexible — it is also used when a user simply wants to
process a standalone audio file without any Manim animation involved.
For example: splitting a podcast recording into separate clips, or
converting an audio file from one format to another.

```
+=====================================================================+
|          AUDIOFILE AND AUDIOCLIPS — THE PIZZA METAPHOR              |
+=====================================================================+
|                                                                     |
|   AudioFile                                                         |
|   (the whole pizza = original_audio.mp3 = 60.0 seconds)            |
|                                                                     |
|   ─────────────────────────────────────────────────────────────    |
|   │           │              │              │          │            |
|   AudioClip1  AudioClip2     AudioClip3     AudioClip4              |
|   12.5s       18.5s          16.8s          12.2s                   |
|   (slice 1)   (slice 2)      (slice 3)      (slice 4)               |
|                                                                     |
|   5500 + 18500 + 16800 + 12200 = 60000 ms                           |
|   (the slices add up to exactly the whole pizza's duration)         |
|                                                                     |
+=====================================================================+
```

### Subsubsection 3.9.1.1: Where Is the AudioFile Class Defined on Disk?

```
/home/mina/SuperManim/core/entities/audio_file.py
```

## Subsection 3.9.2: The Full Python Class of the AudioFile Entity

```python
# File location: /home/mina/SuperManim/core/entities/audio_file.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class AudioFile:
    """
    The AudioFile Entity represents the master audio file added to the project.

    It is a pure data container. It holds all the metadata about the
    original full-length audio file — its path, format, duration, and
    technical properties. It also contains a list of all AudioClip
    objects that were produced by cutting this master file.

    It does NOT read audio files from disk.
    It does NOT call FFmpeg or librosa.
    It does NOT play or process audio.
    It is just structured data.
    """

    # ── GROUP 1 — IDENTITY ────────────────────────────────────────────
    audio_file_id:              int

    # ── GROUP 2 — LOCATION ────────────────────────────────────────────
    audio_file_path:            Optional[str]   = None
    audio_file_original_name:   Optional[str]   = None

    # ── GROUP 3 — FORMAT ──────────────────────────────────────────────
    audio_file_format:          str             = "mp3"

    # ── GROUP 4 — TIMING (in seconds as float — audio convention) ─────
    audio_file_duration:        Optional[float] = None

    # ── GROUP 5 — TECHNICAL PROPERTIES ───────────────────────────────
    audio_file_sample_rate:     Optional[int]   = None
    audio_file_channels:        int             = 1
    audio_file_bitrate:         Optional[int]   = None
    audio_file_size_bytes:      Optional[int]   = None

    # ── GROUP 6 — CLIPS ───────────────────────────────────────────────
    # The list of AudioClip objects cut from this master AudioFile.
    # Populated when the user runs "split audio N".
    audio_clips:                List            = field(default_factory=list)

    # ── GROUP 7 — STATE ───────────────────────────────────────────────
    audio_file_is_split:        bool            = False
    audio_file_added_at:        Optional[str]   = None
```

## Subsection 3.9.3: Every Property of the AudioFile Entity Explained

### Subsubsection 3.9.3.1: GROUP 1 — Identity Properties

#### Subsubsubsection 3.9.3.1.1: audio_file_id

**Type:** `int`
**Default:** Required.
**Example value:** `1`

The unique identifier for this master audio file within the project.
A typical SuperManim project has exactly one AudioFile with
`audio_file_id = 1`. If a project ever has multiple master audio files
(e.g., one narration track and one background music track), they would
have `audio_file_id = 1` and `audio_file_id = 2`.

### Subsubsection 3.9.3.2: GROUP 2 — Location Properties

#### Subsubsubsection 3.9.3.2.1: audio_file_path

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"audio_clips/original_audio.mp3"`

The path to the master audio file inside the project folder. When the
user runs `add audio voice.mp3`, the system copies `voice.mp3` into the
project's `audio_clips/` directory and stores the internal path here.

`None` means no audio file has been added to this project yet.

#### Subsubsubsection 3.9.3.2.2: audio_file_original_name

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"voice.mp3"`

The original filename as the user provided it, before it was copied into
the project folder (and possibly renamed). Stored for reference so the
user can always see what file they originally added to the project.

### Subsubsection 3.9.3.3: GROUP 3 — Format Properties

#### Subsubsubsection 3.9.3.3.1: audio_file_format

**Type:** `str`
**Default:** `"mp3"`
**Example value:** `"mp3"`, `"wav"`, `"ogg"`, `"aac"`, `"flac"`, `"m4a"`

The file format of the master audio file. Determines which FFmpeg codec
flags are used during audio processing and splitting operations.

### Subsubsection 3.9.3.4: GROUP 4 — Timing Properties

#### Subsubsubsection 3.9.3.4.1: audio_file_duration

**Type:** `Optional[float]`
**Default:** `None`
**Example value:** `60.3` (seconds)

The total duration of the master audio file in seconds. Measured
automatically by the `AudioAnalyzerPort` (using FFprobe or librosa) when
the user adds the file. This is the source of truth for the total audio
duration that the video must match.

### Subsubsection 3.9.3.5: GROUP 5 — Technical Properties

#### Subsubsubsection 3.9.3.5.1: audio_file_sample_rate

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `44100`

The sample rate of the audio file in Hz. All AudioClips cut from this
master inherit this sample rate. Standard values: `44100` Hz (CD quality)
or `48000` Hz (professional broadcast standard).

#### Subsubsubsection 3.9.3.5.2: audio_file_channels

**Type:** `int`
**Default:** `1`
**Example value:** `1` (mono), `2` (stereo)

The number of audio channels. Voice narration is typically `1` (mono).
Background music is typically `2` (stereo).

#### Subsubsubsection 3.9.3.5.3: audio_file_bitrate

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `128000` (meaning 128 kbps)

The bitrate of the audio file in bits per second. Higher bitrate = better
audio quality but larger file size. Common values: `128000` (128 kbps,
standard), `192000` (192 kbps, good quality), `320000` (320 kbps, high quality).

#### Subsubsubsection 3.9.3.5.4: audio_file_size_bytes

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `5292640` (approximately 5 MB for a 60-second mp3)

The size of the master audio file on disk in bytes.

### Subsubsection 3.9.3.6: GROUP 6 — Clips Properties

#### Subsubsubsection 3.9.3.6.1: audio_clips

**Type:** `List[AudioClip]`
**Default:** `[]` (empty list per instance)

The list of all `AudioClip` objects that were produced by cutting this
master AudioFile. When the user runs `split audio 4`, this list is
populated with 4 AudioClip objects, one for each scene.

```python
# After running "split audio 4":
audio_file.audio_clips = [
    AudioClip(audio_clip_id=1, audio_clip_duration=12.5, scene_id=None, ...),
    AudioClip(audio_clip_id=2, audio_clip_duration=18.5, scene_id=None, ...),
    AudioClip(audio_clip_id=3, audio_clip_duration=16.8, scene_id=None, ...),
    AudioClip(audio_clip_id=4, audio_clip_duration=12.2, scene_id=None, ...),
]
# All clips start with scene_id=None until the user runs "sync scene"
```

### Subsubsection 3.9.3.7: GROUP 7 — State Properties

#### Subsubsubsection 3.9.3.7.1: audio_file_is_split

**Type:** `bool`
**Default:** `False`

`True` when the master audio file has already been split into individual
AudioClips. `False` when the file was just added and splitting has not
run yet.

This flag prevents the user from accidentally running `split audio` twice
on the same file, which would produce a second set of duplicate clips.
If the user tries to split an already-split file, the system checks this
flag and refuses with a warning.

#### Subsubsubsection 3.9.3.7.2: audio_file_added_at

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"2024-11-10 09:05:00"`

The timestamp of when this audio file was added to the project — when
the user ran `add audio voice.mp3` and the system copied the file into
the project directory.

---

# Section 3.10: Entity 8 — VideoFile

## Subsection 3.10.1: What Is a VideoFile?

A `VideoFile` is the master video recording that a user adds to a
SuperManim project. It is the complete, uncut video file before it is
split into individual `VideoClip` pieces. It is the video equivalent of
the `AudioFile` entity — the same concept but for video.

Like `AudioFile`, `VideoFile` is flexible. It is used both in `supermanim`
mode (to embed external video content inside Manim scenes) and when the
project is used purely to process a standalone video file (splitting it,
changing its format, extracting audio from it, and so on).

### Subsubsection 3.10.1.1: Where Is the VideoFile Class Defined on Disk?

```
/home/mina/SuperManim/core/entities/video_file.py
```

## Subsection 3.10.2: The Full Python Class of the VideoFile Entity

```python
# File location: /home/mina/SuperManim/core/entities/video_file.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class VideoFile:
    """
    The VideoFile Entity represents a master video file added to the project.

    It is a pure data container. It holds all the metadata about the
    original full-length video file — its path, format, duration, and
    visual/technical properties. It also contains a list of all VideoClip
    objects produced by cutting this master file.

    It does NOT read video files from disk.
    It does NOT call FFmpeg or decode any frames.
    It is just structured data.
    """

    # ── GROUP 1 — IDENTITY ────────────────────────────────────────────
    video_file_id:              int

    # ── GROUP 2 — LOCATION ────────────────────────────────────────────
    video_file_path:            Optional[str]   = None
    video_file_original_name:   Optional[str]   = None

    # ── GROUP 3 — FORMAT ──────────────────────────────────────────────
    video_file_format:          str             = "mp4"
    video_file_codec:           Optional[str]   = None

    # ── GROUP 4 — TIMING (in milliseconds) ────────────────────────────
    video_file_duration:        Optional[int]   = None

    # ── GROUP 5 — VISUAL PROPERTIES ───────────────────────────────────
    video_file_resolution:      Optional[str]   = None
    video_file_fps:             Optional[int]   = None
    video_file_has_audio:       bool            = False

    # ── GROUP 6 — TECHNICAL PROPERTIES ───────────────────────────────
    video_file_size_bytes:      Optional[int]   = None
    video_file_bitrate:         Optional[int]   = None

    # ── GROUP 7 — CLIPS ───────────────────────────────────────────────
    video_clips:                List            = field(default_factory=list)

    # ── GROUP 8 — STATE ───────────────────────────────────────────────
    video_file_is_split:        bool            = False
    video_file_added_at:        Optional[str]   = None
```

## Subsection 3.10.3: Every Property of the VideoFile Entity Explained

### Subsubsection 3.10.3.1: GROUP 1 — Identity Properties

#### Subsubsubsection 3.10.3.1.1: video_file_id

**Type:** `int`
**Default:** Required.
**Example value:** `1`

The unique identifier for this master video file within the project.

### Subsubsection 3.10.3.2: GROUP 2 — Location Properties

#### Subsubsubsection 3.10.3.2.1: video_file_path

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"assets/videos/screen_record.mp4"`

The path to the master video file inside the project folder. When a user
adds a video file, the system copies it into the project and stores the
internal path here.

#### Subsubsubsection 3.10.3.2.2: video_file_original_name

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"screen_record.mp4"`

The original filename as given by the user, before any copying or
renaming. Stored for reference and display purposes.

### Subsubsection 3.10.3.3: GROUP 3 — Format Properties

#### Subsubsubsection 3.10.3.3.1: video_file_format

**Type:** `str`
**Default:** `"mp4"`
**Example value:** `"mp4"`, `"webm"`, `"mov"`, `"avi"`, `"mkv"`

The container format of this video file.

#### Subsubsubsection 3.10.3.3.2: video_file_codec

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"h264"`, `"h265"`, `"vp9"`, `"av1"`

The video codec used to encode this file. Different codecs have different
quality-vs-file-size trade-offs:
- `"h264"` — Most compatible. Works everywhere. Medium compression.
- `"h265"` — Better compression than h264. Same quality at ~half the size.
  Slightly slower to encode/decode.
- `"vp9"` — Google's open codec. Good for web streaming.
- `"av1"` — Newest. Best compression. Slowest to encode.

### Subsubsection 3.10.3.4: GROUP 4 — Timing Properties

#### Subsubsubsection 3.10.3.4.1: video_file_duration

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `60000` (meaning 60.0 seconds)

The total duration of the master video file in milliseconds.

### Subsubsection 3.10.3.5: GROUP 5 — Visual Properties

#### Subsubsubsection 3.10.3.5.1: video_file_resolution

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"1920x1080"`

The pixel dimensions of this video file, read from the file's metadata.

#### Subsubsubsection 3.10.3.5.2: video_file_fps

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `30`, `60`

The frame rate of this video file, read from the file's metadata. All
video clips in a project should have the same fps for smooth assembly.

#### Subsubsubsection 3.10.3.5.3: video_file_has_audio

**Type:** `bool`
**Default:** `False`

`True` if this video file contains an embedded audio track alongside the
video. Used by the export system to decide whether to extract the audio.

### Subsubsection 3.10.3.6: GROUP 6 — Technical Properties

#### Subsubsubsection 3.10.3.6.1: video_file_size_bytes

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `209715200` (approximately 200 MB)

The size of the master video file on disk in bytes.

#### Subsubsubsection 3.10.3.6.2: video_file_bitrate

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `8000000` (meaning 8 Mbps)

The overall bitrate of the video file in bits per second. Higher bitrate
= better quality but larger file size. Typical values: `4000000` (4 Mbps,
standard web), `8000000` (8 Mbps, good quality), `16000000` (16 Mbps, high quality).

### Subsubsection 3.10.3.7: GROUP 7 — Clips Properties

#### Subsubsubsection 3.10.3.7.1: video_clips

**Type:** `List[VideoClip]`
**Default:** `[]` (empty list per instance)

The list of all `VideoClip` objects cut from this master VideoFile.
Populated when the user runs `split video N`. Follows the exact same
pattern as `AudioFile.audio_clips`.

### Subsubsection 3.10.3.8: GROUP 8 — State Properties

#### Subsubsubsection 3.10.3.8.1: video_file_is_split

**Type:** `bool`
**Default:** `False`

`True` when the master video has been split into VideoClips. Prevents
accidental double-splitting, just like `audio_file_is_split`.

#### Subsubsubsection 3.10.3.8.2: video_file_added_at

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"2024-11-10 10:00:00"`

Timestamp of when this video file was added to the project.

---

# Section 3.11: Entity 9 — AssetFile

## Subsection 3.11.1: What Is an AssetFile?

An `AssetFile` is any supporting file that a Manim animation scene uses
but that is not itself the animation code, audio, or video. Think of
asset files as the props and resources that appear inside the animation.

Examples of what counts as an asset file:
- A **PNG or JPG image** file that appears inside a Manim scene using `ImageMobject()`
- A **custom font** file (`.ttf`, `.otf`) used by Manim's `Text()` or `MathTex()`
- An **SVG vector graphic** file imported using `SVGMobject()`

When Manim renders a scene that uses an image, that image must be present
on disk at exactly the path the code expects. The system tracks every such
file as an `AssetFile` entity so it knows all the dependencies of each
scene. This is crucial for the hash fingerprint system — if an image changes,
the `scene_assets_hash` changes, which changes the `final_scene_hash`,
which causes the scene to be re-rendered.

```
+=====================================================================+
|           WHAT COUNTS AS AN ASSET FILE                              |
+=====================================================================+
|                                                                     |
|   TYPE: image                                                       |
|   diagram.png   → used with ImageMobject("assets/images/diagram.png")|
|   logo.svg      → used with SVGMobject("assets/images/logo.svg")    |
|   background.jpg → background image                                  |
|                                                                     |
|   TYPE: font                                                        |
|   MyFont.ttf    → used with Text("Hello", font="MyFont")            |
|   MathFont.otf  → used for custom mathematical rendering            |
|                                                                     |
|   TYPE: svg                                                         |
|   diagram.svg   → used with SVGMobject(...)                         |
|                                                                     |
|   ALL STORED IN THE PROJECT ASSETS FOLDER:                          |
|   /projects/MyAnimation/assets/images/diagram.png                   |
|   /projects/MyAnimation/assets/images/logo.svg                      |
|   /projects/MyAnimation/assets/fonts/MyFont.ttf                     |
|                                                                     |
+=====================================================================+
```

### Subsubsection 3.11.1.1: Where Is the AssetFile Class Defined on Disk?

```
/home/mina/SuperManim/core/entities/asset_file.py
```

## Subsection 3.11.2: The Full Python Class of the AssetFile Entity

```python
# File location: /home/mina/SuperManim/core/entities/asset_file.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class AssetFile:
    """
    The AssetFile Entity represents one supporting file used by a Manim
    animation scene — such as an image, SVG graphic, or font file.

    It is a pure data container. It holds the path, type, and metadata
    of the asset file, and links it to the scene that uses it.

    This entity is critical for the hash fingerprint system. If any
    asset file linked to a scene changes (a different image is placed
    in the assets folder), the scene_assets_hash on the parent Scene
    changes, which triggers a re-render of that scene.

    It does NOT read files from disk.
    It does NOT load or process images or fonts.
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

    # ── GROUP 7 — STATE ───────────────────────────────────────────────
    asset_file_added_at:        Optional[str]   = None

    # ALLOWED VALUES FOR asset_file_type:
    # "image"  → .png, .jpg, .jpeg raster image
    # "svg"    → .svg vector graphic
    # "font"   → .ttf, .otf font file
    # "video"  → .mp4 or other video embedded inside a scene
```

## Subsection 3.11.3: Every Property of the AssetFile Entity Explained

### Subsubsection 3.11.3.1: GROUP 1 — Identity Properties

#### Subsubsubsection 3.11.3.1.1: asset_file_id

**Type:** `int`
**Default:** Required.
**Example value:** `5`

The unique identifier for this asset file within the project. Used as
the primary key in the database.

### Subsubsection 3.11.3.2: GROUP 2 — Linking Properties

#### Subsubsubsection 3.11.3.2.1: scene_id

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `3`

The `scene_id` of the Scene that uses this asset file. This back-link
is what allows the hash system to compute `scene_assets_hash` correctly.
The system finds all AssetFiles with `scene_id = 3`, reads their
`asset_file_hash` values, combines them, and produces the
`scene_assets_hash` for Scene 3.

```
scene_assets_hash for Scene 3 is computed from:
  AssetFile(asset_file_id=5, scene_id=3, asset_file_hash="e3b0...")
  AssetFile(asset_file_id=6, scene_id=3, asset_file_hash="f8a1...")
  AssetFile(asset_file_id=7, scene_id=3, asset_file_hash="9c4d...")
  ─────────────────────────────────────────────────────────────────
  Combined → scene_assets_hash = "a9f3b2c1..."
```

### Subsubsection 3.11.3.3: GROUP 3 — Location Properties

#### Subsubsubsection 3.11.3.3.1: asset_file_path

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"assets/images/diagram.png"`

The path to the asset file inside the project folder.

#### Subsubsubsection 3.11.3.3.2: asset_file_original_name

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"diagram.png"`

The original filename as provided by the user.

### Subsubsection 3.11.3.4: GROUP 4 — Type and Format Properties

#### Subsubsubsection 3.11.3.4.1: asset_file_type

**Type:** `str`
**Default:** `"image"`
**Allowed values:** `"image"`, `"svg"`, `"font"`, `"video"`

The category of this asset. Determines how it is used in Manim code
and how it is processed by the system.

```
"image"  → ImageMobject("assets/images/diagram.png")
"svg"    → SVGMobject("assets/images/logo.svg")
"font"   → Text("Hello World", font="MyFont")
"video"  → (embedded video clips inside a Manim scene)
```

#### Subsubsubsection 3.11.3.4.2: asset_file_format

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"png"`, `"jpg"`, `"svg"`, `"ttf"`, `"otf"`

The file extension/format of this asset.

### Subsubsection 3.11.3.5: GROUP 5 — Technical Properties

#### Subsubsubsection 3.11.3.5.1: asset_file_size_bytes

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `245760` (approximately 240 KB for a medium-resolution PNG)

The size of this asset file on disk in bytes.

### Subsubsection 3.11.3.6: GROUP 6 — Hash Properties

#### Subsubsubsection 3.11.3.6.1: asset_file_hash

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"e3b0c44298fc1c149afb4c8996fb92427ae41e4649b934ca495991b7852b855"`

The SHA-256 fingerprint of this asset file's content. If the user
replaces `diagram.png` with a different image (even if it has the same
filename), this hash changes. That change then propagates:

```
asset_file_hash changes
      ↓
scene_assets_hash on the parent Scene changes
      ↓
final_scene_hash on the parent Scene changes
      ↓
Scene must be re-rendered (hash no longer matches stored hash)
```

### Subsubsection 3.11.3.7: GROUP 7 — State Properties

#### Subsubsubsection 3.11.3.7.1: asset_file_added_at

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"2024-11-10 09:15:00"`

The timestamp when this asset file was registered in the project. Set
when the user runs `add asset diagram.png scene 3`.

---


# Section 3.12: Entity 10 — Timeline

## Subsection 3.12.1: What Is a Timeline?

The Timeline is the entity that represents the ordered sequence of all
media units in a project and the calculated total duration of the
entire video. Think of it like a spreadsheet row that says:
"This project has 5 scenes, they play in this order, and together they
last exactly 60300 milliseconds."

The Timeline does not store scenes itself — the Scenes are stored
separately. The Timeline is a calculated summary of how all scenes
connect into a continuous video.

```
+=====================================================================+
|                    THE TIMELINE CONCEPT                             |
+=====================================================================+
|                                                                     |
|   0ms     12500ms    31000ms    47800ms    60000ms                  |
|   |────────|──────────|──────────|──────────|                      |
|   Scene 1   Scene 2    Scene 3    Scene 4                           |
|   12500ms   18500ms    16800ms    12200ms                           |
|                                                                     |
|   Timeline:                                                         |
|     total_duration  = 60000ms                                       |
|     scene_count     = 4                                             |
|     is_complete     = True  (no gaps between scenes)               |
|                                                                     |
+=====================================================================+
```

### Subsubsection 3.12.1.1: Where Is the Timeline File on Disk?

```
/home/mina/SuperManim/core/entities/timeline.py
```

## Subsection 3.12.2: The Full Python Class of the Timeline Entity

```python
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

    # ── GROUP 6 — STATE ───────────────────────────────────────────────
    last_calculated_at:     Optional[str]   = None
```

## Subsection 3.12.3: Every Property of the Timeline Entity Explained
### Subsubsection 3.12.3.2: GROUP 2 — Summary Properties

#### Subsubsubsection 3.12.3.2.1: total_duration

**Type:** `int`
**Default:** `0`
**Example value:** `60000` (60 seconds in milliseconds)

The sum of all scene durations in the project. Recomputed automatically
by `TimelineService` every time a scene is added, removed, or its
duration changes.

```
Scene 1: 12500ms
Scene 2: 18500ms
Scene 3: 16800ms
Scene 4: 12200ms
─────────────────
Total:   60000ms  ← stored in timeline.total_duration
```

#### Subsubsubsection 3.12.3.2.2: scene_count

**Type:** `int`
**Default:** `0`
**Example value:** `4`

The total number of scenes currently in the timeline.

### Subsubsection 3.12.3.3: GROUP 3 — Ordered Scene IDs

#### Subsubsubsection 3.12.3.3.1: ordered_scene_ids

**Type:** `List[int]`
**Default:** `[]`
**Example value:** `[1, 2, 3, 4]`

An ordered list of `scene_id` values representing the sequence in which
scenes will play. The first ID in the list is the first scene to play.
When the user runs `move scene 4 to 1`, this list is reordered:
 `[4, 1, 2, 3]`.

The scene_index is the order of the scene in the timeline but the scene_id is the uniqe identifier of
 the scene
if the list is 
`[4, 1, 2, 3]`.
Then the scene_id = 4 is placed in scene_index = 0  
     the scene_id = 3 is placed in scene_index = 3 in the list   
### Subsubsection 3.12.3.4: GROUP 4 — Synchronization Properties

#### Subsubsubsection 3.12.3.4.1: audio_total_duration

**Type:** `Optional[float]`
**Default:** `None`
**Example value:** `60.0` (seconds)

The total duration of the master audio file (mirrored from
`Project.audio_total_duration`). Stored here for quick comparison
with `total_duration` during the sync validation check.
for sync the total duration (sums of all scenes durations) must be equal the audio total duration 
#### Subsubsubsection 3.12.3.4.2: is_synced_with_audio

**Type:** `bool`
**Default:** `False`

`True` when `total_duration` (converted to seconds) equals
`audio_total_duration`. Meaning: the total video duration matches the
total audio duration exactly. The video will play in perfect sync with
the audio from start to finish.

### Subsubsection 3.12.3.5: GROUP 5 — Validation Properties

#### Subsubsubsection 3.12.3.5.1: has_gaps

**Type:** `bool`
**Default:** `False`

`True` if there are gaps between scenes — places where one scene ends
and the next scene does not begin immediately. A gap means the final
video will have a blank/silent section. This is usually a mistake and
the system warns the user.

#### Subsubsubsection 3.12.3.5.2: is_complete

**Type:** `bool`
**Default:** `False`

`True` when:
1. `scene_count > 0` (at least one scene exists)
2. `has_gaps = False` (no empty spaces between scenes)
3. `total_duration > 0` (the timeline has actual content)

A complete timeline means the scenes connect seamlessly from start to
finish with no holes.

# SuperManim Settings Entities — Full Reference

> **What this document covers:**
> The five settings entities used in every SuperManim project:
> `AudioSettings`, `VideoSettings`, `RenderSettings`, `PreviewSettings`, and `ExportSettings`.
>
> Each section explains what the entity IS, what it DOES, where it LIVES, all its PROPERTIES
> (with types, defaults, and examples), and how it CONNECTS to other parts of the system.

---

---

# Section 3.13 Entity 11  — AudioSettings

---

##  Subsection 3.13.1  What Is AudioSettings?

`AudioSettings` is the entity that stores all information about the
**project-level audio file** — the single audio recording (narration or
background music) that plays behind the entire animation from start to finish.

Think of it like a **cassette tape label**. The label does not contain the
actual audio. It just describes the tape:

- What format is it? (MP3? WAV?)
- Where is the file stored on disk?
- How long is it?

`AudioSettings` is that label. It is a pure data container — it does not
play audio, convert audio, or read audio bytes. It just holds three pieces
of information about the audio file.

```
+=====================================================================+
|              THE THREE QUESTIONS AUDIOSETTINGS ANSWERS              |
+=====================================================================+
|                                                                     |
|   1.  WHAT FORMAT is the audio file?                                |
|       Is it MP3? WAV? OGG? AAC? FLAC? M4A?                         |
|       → Stored in:  audio_format                                    |
|                                                                     |
|   2.  WHERE is the audio file on disk?                              |
|       What is the full path to the master audio file?               |
|       → Stored in:  audio_file_path                                 |
|                                                                     |
|   3.  HOW LONG is the audio file?                                   |
|       How many total seconds of audio are there?                    |
|       → Stored in:  audio_total_duration                            |
|                                                                     |
+=====================================================================+
```

---

##  Subsection 3.13.2  Where Does AudioSettings Live?

`AudioSettings` is a **nested field inside the `Project` entity**.
Every project holds exactly one `AudioSettings` object. If no audio has
been added to the project yet, the field is `None`.

```
Project
├── project_name:            "My Math Video"
├── project_total_duration:  60.3
├── project_items:           [Scene 1, Scene 2, Scene 3, Scene 4]
└── project_audio_settings:  AudioSettings   ← lives here
                                 ├── audio_format:          "mp3"
                                 ├── audio_file_path:       "audio_clips/original_audio.mp3"
                                 └── audio_total_duration:  60.3

When no audio has been added yet:
└── project_audio_settings:  None
```

---

##  Subsection 3.13.3  File Location on Disk

```
/home/mina/SuperManim/core/entities/audio_settings.py
```

It is imported inside `project.py` like this:

```python
from .audio_settings import AudioSettings

@dataclass
class Project:
    ...
    project_audio_settings: Optional[AudioSettings] = None
```

---

##  Subsection 3.13.4  All Properties inside AudioSettings entity

---

### Subsubsection 3.13.4.1  `audio_format`

+------------------+------------------------------------------------------+
| Field            | Value                                                |
+------------------+------------------------------------------------------+
| Type             | str                                                  |
| Default          | "mp3"                                                |
| Example values   | "mp3", "wav", "ogg", "aac", "flac", "m4a"            |
+------------------+------------------------------------------------------+
 
The `audio_format` field stores the file format of the master audio file
as a lowercase string.

This value is used by `AudioService` when the system needs to
convert the audio to a different format (for example, converting MP3 to WAV
before high-quality export). It is also used when the system needs to pass
the correct FFmpeg codec flags during the final video assembly step.

```
Supported format values and what they mean:

"mp3"   → MPEG Audio Layer III. Most common. Works everywhere.
           Smaller file size. Slight quality loss (lossy compression).
           Best for: general use, narration, background music.

"wav"   → Waveform Audio File Format. Uncompressed.
           Very large file sizes. Perfect audio quality (lossless).
           Best for: professional audio workflows, studio-quality output.

"ogg"   → Ogg Vorbis. Open format. Smaller than MP3 at same quality.
           Not supported by all players. Best for: web use, open-source projects.

"aac"   → Advanced Audio Coding. Better quality than MP3 at same file size.
           Widely supported. Used by YouTube, Apple devices.
           Best for: modern web and mobile delivery.

"flac"  → Free Lossless Audio Codec. Lossless but compressed.
           Much smaller than WAV. Still perfect quality.
           Best for: archival, high-quality editing workflows.

"m4a"   → MPEG-4 Audio. AAC inside an MP4 container.
           Used by Apple ecosystem (iTunes, iPhones).
           Best for: Apple-targeted workflows.
```

---

 ### Subsubsection 3.13.4.2  `audio_file_path`

+------------------+---------------------------------------------+
| Field            | Value                                       |
+------------------+---------------------------------------------+
| Type             | str                                         |
| Default          | "" (empty string)                           |
| Example values   | "audio_clips/original_audio.mp3"            |
|                  | "/home/mina/projects/narration.wav"         |
+------------------+---------------------------------------------+

The `audio_file_path` field stores the path to the master audio file on disk.
This is the single long audio recording that covers the entire project.

This path can be either:
- A **relative path** from the project root directory: `"audio_clips/narration.mp3"`
- An **absolute path** from the filesystem root: `"/home/mina/audio/narration.mp3"`

The `AudioService` reads this path to locate the file before
any cutting, converting, or processing operation. The `AudioService`
uses this path as the source when it cuts smaller `AudioClip` pieces for
each scene.

```
IMPORTANT RULES about audio_file_path:
─────────────────────────────────────────────────────────────
  1.  The file must exist at this path when any service tries to use it.
      If the file is moved or deleted after being registered, all
      audio-related operations will fail with a FileNotFoundError.

  2.  The path should be consistent across machines if the project
      is shared. Relative paths are safer for shared projects.

  3.  This field is NEVER None. If no audio has been added,
      the entire project_audio_settings field is None.
      Once AudioSettings exists, it always has a valid path.
```

---
 ### Subsubsection 3.13.4.3 `audio_total_duration`
+------------------+-----------------------------+
| Field            | Value                       |
+------------------+-----------------------------+
| Type             | int                         |
| Default          | 0                           |
| Example values   | 60000, 3000                 |
|                  |                             |
+------------------+-----------------------------+

 The `audio_total_duration` field stores the total length of the master
audio file in **milliseconds**, as a integer  number.

This value is critical for **timeline synchronization**. The
`TimelineService` compares `audio_total_duration` against
`project_total_duration`. If they do not match, it means the audio and
the animation are different lengths, and the final video will either
have silence at the end or cut off before the audio finishes.

```
TIMELINE SYNC CHECK (performed by TimelineService):

   project_total_duration  =  60.3 seconds
   audio_total_duration    =  60.3 seconds
   → MATCH. Timeline is synchronized. Export is safe.

   project_total_duration  =  65.0 seconds
   audio_total_duration    =  60.3 seconds
   → MISMATCH. WARNING: "Audio is 4.7 seconds shorter than the project.
     The last 4.7 seconds of the video will have no audio."

   project_total_duration  =  55.0 seconds
   audio_total_duration    =  60.3 seconds
   → MISMATCH. WARNING: "Audio is 5.3 seconds longer than the project.
     The last 5.3 seconds of the audio will be cut off during export."
```

The value is set automatically by `AudioService` when the
user adds an audio file. It uses FFmpeg to probe the file and measure
the exact duration. You never set this manually.

### Subsubsection 3.13.4.4  `audio_sample_rate`

+------------------+------------------------------------------------------+
| Field            | Value                                                |
+------------------+------------------------------------------------------+
| Type             | int                                                  |
| Default          | 44100                                                |
| Example values   | 44100, 48000, 96000                                 |
+------------------+------------------------------------------------------+

The `audio_sample_rate` field stores the number of
audio samples per second (in Hertz) in the master audio file.

* A sample is a tiny measurement of the sound wave at a single point in time.
* The more samples per second, the better the audio can represent the original sound.
* Common values:

  * 44100 Hz → standard for music and narration
  * 48000 Hz → standard for video production
  * 96000 Hz → high-quality professional audio

`AudioService` uses this value to make sure the audio plays at the correct speed
and matches the video timeline.

---

### Subsubsection 3.13.4.5  `audio_channels`

+------------------+------------------------------------------------------+
| Field            | Value                                                |
+------------------+------------------------------------------------------+
| Type             | int                                                  |
| Default          | 1                                                    |
| Example values   | 1, 2                                                |
+------------------+------------------------------------------------------+

The `audio_channels` field stores the number of channels in the audio file.

* 1 → Mono (single channel, same sound in both ears)
* 2 → Stereo (two channels, left and right for directional sound)

This helps the system know how to mix or export audio correctly.
For example, stereo music in a video needs two channels, while a simple narration may only need one.

---

### Subsubsection 3.13.4.6  `audio_bit_depth`

+------------------+------------------------------------------------------+
| Field            | Value                                                |
+------------------+------------------------------------------------------+
| Type             | int                                                  |
| Default          | 16                                                   |
| Example values   | 16, 24, 32                                         |
+------------------+------------------------------------------------------+

The `audio_bit_depth` field shows how many bits are used to store each audio sample.

* More bits → more detail in the sound → clearer audio
* Example:

  * 16-bit → CD quality
  * 24-bit → professional recording
  * 32-bit → very high quality, used in mastering

This is important for maintaining good audio quality,
especially if the file will be edited or exported multiple times.

---

### Subsubsection 3.13.4.7  `audio_bitrate`

+------------------+------------------------------------------------------+
| Field            | Value                                                |
+------------------+------------------------------------------------------+
| Type             | Optional[int]                                       |
| Default          | None                                                 |
| Example values   | 128000, 192000, 320000                              |
+------------------+------------------------------------------------------+

The `audio_bitrate` field stores how many bits per second are used to encode the audio.

* Higher bitrate → better quality, larger file
* Lower bitrate → smaller file, lower quality
* Only applies to compressed formats like MP3 or AAC
* `AudioService` may use this when converting the audio to a different format or compressing it.

---
### Subsubsection 3.13.4.8  `is_audio_exist`

+------------------+------------------------------------------------------+
| Field            | Value                                                |
+------------------+------------------------------------------------------+
| Type             | bool                                                 |
| Default          | False                                                 |
| Example values   | True, False                                         |
+------------------+------------------------------------------------------+

The `audio_exists` field indicates if the master audio file has been added to the project.

* True → audio is present and ready for processing
* False → no audio is assigned yet

This helps avoid errors when services try to access audio that doesn’t exist.

---

### Subsubsection 3.13.4.9  `audio_file_size_byte`

+------------------+------------------------------------------------------+
| Field            | Value                                                |
+------------------+------------------------------------------------------+
| Type             | int                                                 |
| Default          | 0                                                    |
| Example values   | 1234567, 98765432                                   |
+------------------+------------------------------------------------------+

The `audio_file_size_byte` field stores the size of the master audio file in bytes.

* Used for validation and debugging
* Ensures that the audio file is fully downloaded or copied correctly
---

## Subsection 3.13. 5 Full Python Class (Reference)

```python
# File location: /home/mina/SuperManim/core/entities/audio_settings.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class AudioSettings:
    """
    AudioSettings stores all metadata about the project-level audio file.

    This is a pure data container (entity). It does NOT play, read, or convert
    audio. It only describes the master audio file (narration or background music)
    that spans the entire project.

    Main fields:
        - audio_format: format of the audio file (mp3, wav, etc.)
        - audio_file_path: path to the audio file on disk
        - audio_total_duration: total duration in milliseconds

    Optional fields (enhanced metadata):
        - audio_sample_rate: samples per second (Hz)
        - audio_channels: number of audio channels (mono/stereo)
        - audio_bit_depth: bits per audio sample
        - audio_bitrate: bits per second for compressed audio
        - is_audio_exist: whether audio is present
        - audio_file_size_byte: size of the audio file in bytes
    """

    # === MAIN PROPERTIES ===
    # The audio file format (lowercase string)
    # Examples: "mp3", "wav", "ogg", "aac", "flac", "m4a"
    audio_format: str = "mp3"

    # Full path to the master audio file (relative or absolute)
    audio_file_path: str = ""

    # Total duration of the audio in milliseconds
    audio_total_duration: int = 0

    # True if the audio file exists in the project
    is_audio_exist: bool = False

    # Size of the audio file in bytes
    audio_file_size_byte: int = 0

    # === OPTIONAL PROPERTIES ===
    # Number of audio samples per second in Hertz
    # Common: 44100, 48000, 96000
    audio_sample_rate: Optional[int] = 44100

    # Number of channels: 1 = mono, 2 = stereo
    audio_channels: Optional[int] = 1

    # Bits per audio sample: 16, 24, 32
    audio_bit_depth: Optional[int] = 16

    # Audio bitrate (optional, only for compressed formats like mp3 or aac)
    # Example: 128000, 192000, 320000
    audio_bitrate: Optional[int] = None
```

# Section 3.14 Entitiy 12 VideoSettings
## Subsection 3.14.1  What Is VideoSettings?

`VideoSettings` is the entity that stores the **core identity of the
project as a video** — the properties that define what kind of video
the project is, who created it, and what its natural dimensions and
aspect ratio are.

While `RenderSettings` controls *how* scenes are rendered (resolution,
frame rate), `VideoSettings` answers the more fundamental question:
*what is this video?* It holds the project's metadata for the final
assembled video output, including the visual canvas size and the
author/creator information that may be embedded in the exported file.

Think of `VideoSettings` as the **identity card** for the video project.

---

## Subsection 3.14.2  Where Does VideoSettings Live?

`VideoSettings` is a **nested field inside the `Project` entity**.

```
Project
├── project_name:             "My Math Video"
├── project_total_duration:   60.3
└── project_video_settings:   VideoSettings   ← lives here
                                  ├── video_width:        1920
                                  ├── video_height:       1080
                                  ├── video_aspect_ratio: "16:9"
                                  └── video_author:       "Mina"
```

---

## Subsection 3.14.3  All Properties inside VideoSettings

Got it! I can rewrite the **VideoSettings properties** fully in **paragraph form**, simple English, in-depth explanations, no “Definition / Why it matters / Explanation” labels. I’ll keep it comprehensive and beginner-friendly with examples and ASCII tables. Here’s the full rewrite:

---

# Section 3.14 Entity 12 — VideoSettings

---

## Subsection 3.14.3  All Properties inside VideoSettings entity

`VideoSettings` stores all configuration and metadata for the video output of a project.
It describes the canvas size, aspect ratio, frame rate, background color, codec,
file paths, duration, and other key properties needed for rendering animations.

This entity does not hold video frames or render anything itself;
it is purely a **data container** that tells the system how the video should be created and stored.
Think of it like a blueprint for the video.

---

### Subsubsection 3.14.3.1  `video_width`

```
+------------------+---------------------------+
| Field            | Value                     |
+------------------+---------------------------+
| Type             | int                       |
| Default          | 1920                      |
| Example values   | 854, 1280, 1920, 3840     |
+------------------+---------------------------+
```

The `video_width` specifies how many horizontal pixels the video canvas has.
A larger width results in higher resolution, sharper images, and bigger file sizes,
while smaller widths allow faster previews and smaller output files.

For example, 854 pixels is common for 480p preview, 1280 for 720p HD,
1920 for 1080p Full HD (default), and 3840 for 4K Ultra HD.
`video_width` always works together with `video_height` to define
the complete canvas dimensions.

---

### Subsubsection 3.14.3.2  `video_height`

```
+------------------+---------------------------+
| Field            | Value                     |
+------------------+---------------------------+
| Type             | int                       |
| Default          | 1080                      |
| Example values   | 480, 720, 1080, 2160      |
+------------------+---------------------------+
```

The `video_height` sets the vertical pixel count of the canvas. Together with `video_width`,
it determines the resolution of the video. For instance,
a video of 1920x1080 pixels is 1080p Full HD,
while 1280x720 produces 720p HD.

Using standard dimensions ensures the video displays correctly on most screens,
avoiding stretched or squashed images.

---

### Subsubsection 3.14.3.3  `video_aspect_ratio`

```
+------------------+--------------------------------------+
| Field            | Value                                |
+------------------+--------------------------------------+
| Type             | str                                  |
| Default          | "16:9"                               |
| Example values   | "16:9", "4:3", "1:1", "9:16", "21:9"|
+------------------+--------------------------------------+
```

The `video_aspect_ratio` stores the ratio of width to height in a human-readable string.
Common ratios include 16:9 for widescreen videos like YouTube,
4:3 for older monitors or slides, 1:1 for square social media content,
9:16 for vertical videos on mobile platforms like TikTok, and 21:9 for cinematic ultra-wide formats.

Even if `video_width` and `video_height` already determine the ratio mathematically,
storing it explicitly allows other services to quickly access the ratio without calculations.

---

### Subsubsection 3.14.3.4  `video_frame_rate`

```
+------------------+---------------------------+
| Field            | Value                     |
+------------------+---------------------------+
| Type             | int                       |
| Default          | 30                        |
| Example values   | 24, 30, 60                |
+------------------+---------------------------+
```

The `video_frame_rate` defines how many frames per second (FPS) the video will contain.
Higher FPS produces smoother motion but increases file size and processing requirements.
Common frame rates include 24 FPS for a cinematic feel, 30 FPS for standard animations (default),
and 60 FPS for very smooth video, often used in fast-paced or gaming content.

---

### Subsubsection 3.14.3.5  `video_background_color`

```
+------------------+---------------------------+
| Field            | Value                     |
+------------------+---------------------------+
| Type             | str                       |
| Default          | "#000000"                 |
| Example values   | "#000000", "#ffffff", "#ff0000" |
+------------------+---------------------------+
```

The `video_background_color` specifies the background color of the canvas in hexadecimal format.
It is the color visible in areas where no visual layers exist. Black (`#000000`) is the default,
white (`#ffffff`) is common for presentations, and any other color like red (`#ff0000`)
can be chosen for stylistic effects. Some formats also support transparency, allowing overlays
to appear on other backgrounds.

---

### Subsubsection 3.14.3.6  `video_total_duration`

```
+------------------+---------------------------+
| Field            | Value                     |
+------------------+---------------------------+
| Type             | float                     |
| Default          | 0.0                       |
| Example values   | 60.3, 120.0, 45.75        |
+------------------+---------------------------+
```

The `video_total_duration` stores the total length of the video in seconds.
This property is essential for synchronizing video with audio and scene timelines.
If `video_total_duration` and the total audio duration do not match,
the final video may have silent sections or be cut short at the end.

---

### Subsubsection 3.14.3.7  `video_file_path`

```
+------------------+------------------------------------------+
| Field            | Value                                    |
+------------------+------------------------------------------+
| Type             | str                                      |
| Default          | ""                                       |
| Example values   | "videos/final_render.mp4", "/home/user/project/video.mp4" |
+------------------+------------------------------------------+
```

The `video_file_path` indicates where the rendered video file will be saved.
This path can be relative to the project directory or absolute on the system.

It is used by the rendering service to write the final output and must exist or be creatable.
Using relative paths ensures portability when sharing the project.

---

### Subsubsection 3.14.3.8  `video_codec`

```
+------------------+---------------------------+
| Field            | Value                     |
+------------------+---------------------------+
| Type             | str                       |
| Default          | "h264"                    |
| Example values   | "h264", "hevc", "vp9", "av1" |
+------------------+---------------------------+
```

The `video_codec` defines the format used to compress and encode the video file.
H264 is widely compatible and used by default. HEVC provides better compression,
VP9 is web-friendly, and AV1 is a next-generation codec designed for future-proofing.
The codec affects both video quality and file size.

---

### Subsubsection 3.14.3.9  `is_video_exist`

```
+------------------+---------------------------+
| Field            | Value                     |
+------------------+---------------------------+
| Type             | bool                      |
| Default          | False                     |
| Example values   | True, False               |
+------------------+---------------------------+
```

The `is_video_exist` property indicates whether the rendered video file currently exists on disk.
It prevents errors when the system or services attempt to access the video before it has been generated.

---

### Subsubsection 3.14.3.10  `video_file_size_byte`

```
+------------------+---------------------------+
| Field            | Value                     |
+------------------+---------------------------+
| Type             | int                       |
| Default          | 0                         |
| Example values   | 1234567, 98765432         |
+------------------+---------------------------+
```

The `video_file_size_byte` stores the size of the final video file in bytes.
It is used for validation, storage tracking, and to ensure that the export completed successfully.
Large videos will naturally have bigger sizes, especially at higher resolutions and frame rates.


## Subsection 3.14.4 Full Python Class (Reference)

```python 
# File location: /home/mina/SuperManim/core/entities/video_settings.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class VideoSettings:
    """
    VideoSettings stores all configuration and metadata for video output.
    It describes canvas size, aspect ratio, frame rate, background color, codec,
    file paths, duration, and other key properties needed for rendering animations.

    This entity does not hold video frames or perform rendering.
    It is a pure data container (blueprint) for video creation.
    """

    # === Video Dimensions ===
    video_width: int = 1920
    video_height: int = 1080
    video_aspect_ratio: str = "16:9"

    # === Frame Rate ===
    video_frame_rate: int = 30

    # === Visual Appearance ===
    video_background_color: Optional[str] = "#000000"

    # === Timing ===
    video_total_duration: int = 0.0  # in seconds

    # === Output File ===
    video_file_path: str = None
    video_codec: Optional[str] = "h264"

    # === File Status ===
    is_video_exist: bool = False
    video_file_size_byte: int = 0

```


---
# Section 3.15 Entity 13 — RenderSettings

## Subsection 3.15.1  What Is RenderSettings?

`RenderSettings` is the entity that stores the **visual quality defaults
for rendering all animation scenes** in a project. It controls how Manim
draws each scene — how many pixels per frame, how many frames per second,
and what background color to paint behind every animation.

Think of `RenderSettings` as the **camera settings** for the entire project.
Just like a camera operator chooses the resolution and frame rate before
pressing record, `RenderSettings` defines those values before Manim renders
your animations. Every scene in the project inherits these defaults
unless it explicitly overrides them with its own values.

While `VideoSettings` answers the question *what is this video?* by storing
the project's identity and output metadata, `RenderSettings` answers a
different question: *how should every frame be drawn?* It is the technical
blueprint that Manim reads to know the resolution, smoothness, color,
and output format for each rendered scene.

An important distinction to understand is that these are **project-level
defaults**. Individual `Scene` entities have their own `scene_resolution`,
`scene_fps`, and `scene_background_color` fields that can override these
defaults for specific scenes. If a scene does not specify its own values,
it falls back to whatever `RenderSettings` provides.

Beyond the rendering configuration, `RenderSettings` also holds four
**cached statistics counters** that track the current state of all scenes
in the project. These counters are updated automatically whenever a scene's
status changes, giving the system instant access to progress information
without needing to query the database every time.

Think of `RenderSettings` as the **master control panel** that sets the
baseline quality for the entire production, with per-scene overrides
available when needed, and a built-in dashboard that always shows how
many scenes are done, pending, or failed.

---

## Subsection 3.15.2  Where Does RenderSettings Live?

`RenderSettings` is a **nested field inside the `Project` entity**.

```
Project
├── project_name:              "My Math Video"
├── project_total_duration:    60.3
└── project_render_settings:   RenderSettings   ← lives here
                                  ├── render_resolution:       "1920x1080"
                                  ├── render_fps:              60
                                  ├── render_background_color: "#000000"
                                  ├── render_quality:          "high"
                                  ├── render_output_dir:       "output/"
                                  ├── project_total_scenes:    5
                                  ├── project_rendered_scenes: 3
                                  ├── project_pending_scenes:  1
                                  └── project_failed_scenes:   1
```

When the user creates a new project, `RenderSettings` is automatically
created with sensible defaults — 1080p resolution, 60 FPS, a black
background, and all four statistics counters set to zero. As scenes are
added and their statuses change, the counters update automatically. The
user can change any of the rendering values at any time, and the next
render will use the updated settings.

---

## Subsection 3.15.3  All Properties inside RenderSettings

`RenderSettings` stores all configuration for how Manim renders animation
scenes in a project, along with cached counters that track the progress
of all scenes. It describes the pixel resolution, frame rate, background
appearance, quality presets, output directory, and scene-level statistics.

This entity does not draw anything itself, does not invoke Manim, and
does not manage files on disk. It is purely a **data container** — a set
of instructions that other services read when they need to know how a
scene should be rendered and how far along the project is. Think of it
like a photographer's settings card that gets handed to the lab, combined
with a progress checklist that says how many shots are developed, how
many are waiting, and how many had errors.

---

### Subsubsection 3.15.3.1  `render_resolution`

```
+------------------+------------------------------------------+
| Field            | Value                                    |
+------------------+------------------------------------------+
| Type             | str                                      |
| Default          | "1920x1080"                              |
| Example values   | "854x480", "1280x720", "1920x1080", "3840x2160" |
+------------------+------------------------------------------+
```

The `render_resolution` specifies the default pixel dimensions for every
rendered scene, stored as a single string in the format `"widthxheight"`.
This value is passed directly to Manim as a command-line argument when
rendering each scene, telling Manim how large to make every single frame
of the animation.

All scenes in a project should ideally use the same resolution. When FFmpeg
assembles the final video by concatenating individual scene clips, every
clip must have identical pixel dimensions. Mixing different resolutions
across scenes — for example, rendering Scene 1 at 720p and Scene 2 at
1080p — will cause FFmpeg to fail or produce a broken video with
mismatched frame sizes. For this reason, `RenderSettings` provides a
single shared resolution that all scenes inherit by default.

```
+-------------------------------------------------------------+
|   COMMON RENDER RESOLUTIONS                                  |
+-------------------------------------------------------------+
|                                                             |
|   "854x480"    →  480p    Fast. Low quality. Testing only.  |
|   "1280x720"   →  720p    HD. Good balance of speed/quality |
|   "1920x1080"  →  1080p   Full HD. DEFAULT. Best for most.  |
|   "3840x2160"  →  4K      Ultra HD. Very slow render.       |
|                                                             |
+-------------------------------------------------------------+
```

A larger resolution produces sharper, more detailed video but
dramatically increases render time because Manim must calculate and draw
many more pixels per frame. For example, a 1080p frame has over two
million pixels, while a 480p frame has only about four hundred thousand —
roughly five times fewer pixels to compute. During development and testing,
lowering the resolution to 480p or 720p can save significant time, then
switching back to 1080p for the final production render.

---

### Subsubsection 3.15.3.2  `render_fps`

```
+------------------+---------------------------+
| Field            | Value                     |
+------------------+---------------------------+
| Type             | int                       |
| Default          | 60                        |
| Example values   | 15, 24, 30, 60            |
+------------------+---------------------------+
```

The `render_fps` defines the default frame rate for all rendered scenes —
how many individual still images Manim must draw for every one second of
animation. Higher frame rates produce noticeably smoother motion, because
there are more individual frames bridging each second of movement, but the
trade-off is that significantly more frames must be computed and stored.

```
+-------------------------------------------------------------+
|   WHAT FRAME RATE MEANS FOR RENDER TIME                     |
+-------------------------------------------------------------+
|                                                             |
|   For a 16.8-second scene:                                  |
|                                                             |
|   At 15 fps  →  16.8 × 15  =   252 frames to draw          |
|   At 24 fps  →  16.8 × 24  =   403 frames to draw          |
|   At 30 fps  →  16.8 × 30  =   504 frames to draw          |
|   At 60 fps  →  16.8 × 60  =  1008 frames to draw          |
|                                                             |
|   Higher fps = smoother motion = more frames = slower render|
|                                                             |
|   15 fps:  Rough. Good for quick testing only.              |
|   24 fps:  Cinema standard. Smooth enough for most video.   |
|   30 fps:  TV standard. Good for educational animations.    |
|   60 fps:  Very smooth. DEFAULT. Best for detailed motion.  |
|                                                             |
+-------------------------------------------------------------+
```

A scene rendered at 60 FPS takes roughly four times as long to render as
the same scene at 15 FPS, because Manim must draw four times as many
individual frames. During early development, when you are primarily
checking layout and logic rather than visual smoothness, dropping the
frame rate to 15 or 24 can dramatically speed up your iteration cycle.
The default of 60 FPS is chosen because it produces the smoothest
possible output for educational and mathematical animations where precise
motion matters.

---

### Subsubsection 3.15.3.3  `render_background_color`

```
+------------------+------------------------------------------+
| Field            | Value                                    |
+------------------+------------------------------------------+
| Type             | str                                      |
| Default          | "#000000"                                |
| Example values   | "#000000", "#FFFFFF", "#1a1a2e", "#f5f5f5" |
+------------------+------------------------------------------+
```

The `render_background_color` sets the default background fill color for
all rendered scenes, specified as a hexadecimal color code. Before Manim
draws any animation objects — shapes, text, graphs, or equations — it
first paints the entire frame with this color. Every pixel that is not
covered by an animation object will display this background color.

Individual scenes can override this value with their own
`scene_background_color` field, allowing some scenes to have a dark
background and others to have a light one within the same project.
However, if a scene does not specify its own background color, it
automatically inherits the color stored here.

```
Common background color choices:

  "#000000"  → Pure black.    DEFAULT. Classic math/science video look.
  "#FFFFFF"  → Pure white.    Clean, bright, whiteboard style.
  "#1a1a2e"  → Deep navy.     Modern, polished, professional dark theme.
  "#f5f5f5"  → Off-white.     Softer than pure white. Easy on the eyes.
  "#0d1117"  → GitHub dark.   Very popular for coding/programming videos.
  "#fdf6e3"  → Solarized.     Warm cream tone. Readable and calm.
```

The choice of background color is mostly an aesthetic decision, but it
can affect readability. Light text on a dark background or dark text on
a light background are the two standard approaches. The default black
background is traditional for mathematical animations because it makes
colored shapes and white text stand out clearly.

---

### Subsubsection 3.15.3.4  `render_quality`

```
+------------------+------------------------------------------+
| Field            | Value                                    |
+------------------+------------------------------------------+
| Type             | str                                      |
| Default          | "high"                                   |
| Example values   | "low", "medium", "high", "ultra"         |
+------------------+------------------------------------------+
```

The `render_quality` is a convenience shorthand that maps to a
predefined combination of resolution and frame rate. Instead of manually
setting `render_resolution` and `render_fps` separately, you can set
`render_quality` to one of four preset levels, and the corresponding
resolution and frame rate values are applied automatically.

```
Quality preset mappings:

  "low"    → render_resolution = "854x480",   render_fps = 15
  "medium" → render_resolution = "1280x720",  render_fps = 30
  "high"   → render_resolution = "1920x1080", render_fps = 60  ← DEFAULT
  "ultra"  → render_resolution = "3840x2160", render_fps = 60
```

Using the quality shorthand is faster and less error-prone than setting
resolution and frame rate independently, especially when switching between
testing and production modes. During development, you might set the quality
to `"low"` for fast iteration, then switch to `"high"` for the final
render. Both approaches — setting individual fields or using the shorthand —
result in exactly the same configuration values being passed to Manim.

---

### Subsubsection 3.15.3.5  `render_output_dir`

```
+------------------+----------------------------------------------+
| Field            | Value                                        |
+------------------+----------------------------------------------+
| Type             | str                                          |
| Default          | "output/"                                    |
| Example values   | "output/", "rendered_scenes/", "/tmp/manim/" |
+------------------+----------------------------------------------+
```

The `render_output_dir` specifies the folder where Manim saves the rendered
video file for each scene after a successful render. After Manim finishes
drawing all frames for a scene and encoding them into a video clip, the
resulting `.mp4` file is written to this directory.

The `ProjectExportService` later reads all scene clips from this directory
when assembling the final exported video with FFmpeg. Every rendered scene
is stored here as a separate file, typically named by its scene index.

```
Typical output directory layout after rendering 4 scenes:

  output/
  ├── scene_001.mp4
  ├── scene_002.mp4
  ├── scene_003.mp4
  └── scene_004.mp4

The ProjectExportService reads all .mp4 files from this directory
and concatenates them in order to produce the final video.
```

This path can be relative to the project root directory or an absolute
path on the system. Using a relative path like `"output/"` ensures that
the project remains portable when moved or shared between machines, because
the output folder will always be created inside the project directory
rather than at some arbitrary location on the file system.

---

### Subsubsection 3.15.3.6  `project_total_scenes`

```
+------------------+---------------------------+
| Field            | Value                     |
+------------------+---------------------------+
| Type             | int                       |
| Default          | 0                         |
| Example values   | 0, 4, 10, 25             |
+------------------+---------------------------+
```

The `project_total_scenes` counter stores the total number of `Scene`
objects that belong to this project. Every time a new scene is added to
the project, this counter increases by one. Every time a scene is deleted,
it decreases by one. This counter always reflects the absolute total —
it does not care whether a scene is rendered, pending, or failed; it
simply counts how many scenes exist in the project at any given moment.

This counter is important because many parts of the system need to know
how large the project is. The timeline service uses it to validate that
scene indices are within range. The export service uses it to know how
many clips to expect in the output directory. The progress display uses
it to calculate completion percentages. Without this cached counter, the
system would have to query the database and count rows every time it needs
this information, which would be slow and unnecessary for such a simple
number.

The counter is automatically maintained by the scene management service.
When the user runs `add scene` or `delete scene`, the service updates
this value as part of the same operation, ensuring it stays perfectly
synchronized with the actual number of scenes in the database.

---

### Subsubsection 3.15.3.7  `project_rendered_scenes`

```
+------------------+---------------------------+
| Field            | Value                     |
+------------------+---------------------------+
| Type             | int                       |
| Default          | 0                         |
| Example values   | 0, 3, 10, 25             |
+------------------+---------------------------+
```

The `project_rendered_scenes` counter tracks how many scenes in the
project currently have a status of `"rendered"`. A scene becomes rendered
when Manim successfully finishes drawing all its frames and encoding
the output video file. This counter goes up by one every time a render
succeeds, and goes down by one if a previously rendered scene is reset
back to pending status.

This is the number that tells the user (and the system) how much of the
project is actually finished. When `project_rendered_scenes` equals
`project_total_scenes`, every scene in the project has been rendered
and the project is ready for export. The progress bar in the terminal
uses these two numbers to calculate the completion percentage.

```
SCENES
──────────────────
Total:      5    ← project_total_scenes
Rendered:   3    ← project_rendered_scenes
Pending:    1    ← project_pending_scenes
Failed:     1    ← project_failed_scenes

Progress:   3/5  =  60% complete
```

When the user re-renders a scene that was already in the `"rendered"`
state — for example, after changing the animation code — the counter
does not double-count. The scene was already counted as rendered, so
the number stays the same. The counter only changes when a scene's
status actually transitions between states.

---

### Subsubsection 3.15.3.8  `project_pending_scenes`

```
+------------------+---------------------------+
| Field            | Value                     |
+------------------+---------------------------+
| Type             | int                       |
| Default          | 0                         |
| Example values   | 0, 1, 4, 10              |
+------------------+---------------------------+
```

The `project_pending_scenes` counter tracks how many scenes in the
project currently have a status of `"pending"`. A pending scene is one
that has been created and added to the project but has never been
successfully rendered. Every newly created scene starts its life with
the status `"pending"`, so this counter increases by one whenever a new
scene is added, and decreases by one when that scene is rendered for the
first time.

Pending scenes represent the remaining work. If a project has five scenes
and three are rendered, the two pending scenes are the ones that still
need to be rendered before the project can be fully exported. When the
user runs `render all`, the system can use this counter to know exactly
how many scenes need processing, and can skip scenes that are already
rendered or failed, focusing only on the pending ones.

```
Status transitions that affect project_pending_scenes:

  +1  when:  a new scene is created (status → "pending")
  -1  when:  a pending scene is successfully rendered (status → "rendered")
  -1  when:  a pending scene fails during render    (status → "failed")
  +1  when:  a rendered scene is reset               (status → "pending")
  +1  when:  a failed scene is reset                 (status → "pending")
```

This counter is always automatically updated by the scene management
service whenever a scene's status changes. The system never requires
manual updates to these counters — they are maintained as part of the
same atomic operation that changes the scene's status in the database.

---

### Subsubsection 3.15.3.9  `project_failed_scenes`

```
+------------------+---------------------------+
| Field            | Value                     |
+------------------+---------------------------+
| Type             | int                       |
| Default          | 0                         |
| Example values   | 0, 1, 2, 5               |
+------------------+---------------------------+
```

The `project_failed_scenes` counter tracks how many scenes in the
project currently have a status of `"failed"`. A scene enters the failed
state when a render was attempted but Manim returned an error — for
example, a syntax error in the animation code, a missing import, or an
invalid Manim command. The counter goes up by one when a render fails,
and goes down by one when the user fixes the problem and successfully
re-renders the scene.

Failed scenes are the ones that need attention from the developer. They
represent code that has a bug or a configuration problem that prevented
Manim from completing the render. The system can use this counter to
display a clear warning: "1 scene failed — check scene errors before
exporting." If the user tries to export a project while failed scenes
exist, the system can warn them that the export will be incomplete.

```
Status transitions that affect project_failed_scenes:

  +1  when:  a render attempt fails             (status → "failed")
  -1  when:  a failed scene is fixed and rendered (status → "rendered")
  -1  when:  a failed scene is reset to pending   (status → "pending")

Example lifecycle of a problematic scene:

  Created       → status = "pending"    (pending_scenes: +1)
  Render fails  → status = "failed"     (pending_scenes: -1, failed_scenes: +1)
  Code fixed, re-render succeeds
                → status = "rendered"   (failed_scenes: -1, rendered_scenes: +1)
```

The four counters — `project_total_scenes`, `project_rendered_scenes`,
`project_pending_scenes`, and `project_failed_scenes` — must always add up
correctly. At any moment in time, the following equation must hold true:

```
project_total_scenes = project_rendered_scenes
                     + project_pending_scenes
                     + project_failed_scenes

Example:  5 = 3 + 1 + 1  ← 5 scenes total, 3 rendered, 1 pending, 1 failed
```

If this equation ever breaks, it means there is a bug in the scene
management service that updated the counters incorrectly. The system can
use this equation as a validation check during startup or before exports
to catch any counter synchronization issues early.

---

## Subsection 3.15.4  Full Python Class (Reference)

```python
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

    # === Visual Quality ===
    render_resolution:            str   = "1920x1080"
    render_fps:                   int   = 60
    render_background_color:      str   = "#000000"
    render_quality:               str   = "high"

    # === Output Location ===
    render_output_dir:            str   = "output/"

    # === Scene Statistics (cached counters) ===
    project_total_scenes:         int   = 0
    project_rendered_scenes:      int   = 0
    project_pending_scenes:       int   = 0
    project_failed_scenes:        int   = 0
```


---
# Section 3.16 Entity 14 — PreviewSettings

## Subsection 3.16.1  What Is PreviewSettings?

`PreviewSettings` is the entity that stores the **configuration for
generating quick preview videos** of individual scenes. A preview is a
rough, low-quality draft that the user can watch in a few seconds to
check whether an animation looks correct, without waiting the minutes
that a full render would take.

The entire purpose of the preview system is **speed over quality**. Every
setting inside `PreviewSettings` is chosen to make the preview generate
as fast as possible. Users check previews to catch layout errors, wrong
colors, or timing problems. They do not need full quality for that. They
just need to see: are the objects in the right place? Is the text readable?
Does the animation run in the correct order?

Think of it like a **pencil sketch** before painting the final canvas.
The sketch is fast to draw, easy to erase and redraw, and tells you
everything you need to know about the composition. Only when the sketch
looks right do you commit to the slow, detailed final painting — which
in this case is the full render controlled by `RenderSettings`.

While `RenderSettings` is designed for maximum quality and visual fidelity,
`PreviewSettings` is the exact opposite: it trades quality for speed at
every single opportunity. Lower resolution, lower frame rate, separate
output folder — every decision is made to get the preview into the user's
hands as quickly as possible.

---

## Subsection 3.16.2  Where Does PreviewSettings Live?

`PreviewSettings` is a **nested field inside the `Project` entity**.

```
Project
├── project_name:              "My Math Video"
├── project_total_duration:    60.3
├── project_render_settings:   RenderSettings   ← full quality settings
└── project_preview_settings:  PreviewSettings  ← lives here
                                  ├── preview_resolution:  "854x480"
                                  ├── preview_fps:         30
                                  └── preview_output_dir:  "previews/"
```

Notice that the `Project` entity has **both** `RenderSettings` and
`PreviewSettings`. They live side by side. One controls the final
production quality, and the other controls the quick draft quality.
They are independent of each other — changing the preview settings
does not affect the render settings, and vice versa.

When the user creates a new project, `PreviewSettings` is automatically
created with its fixed defaults. The user does not need to configure
anything — the system already knows the fastest possible settings for
previews and locks them in.

---

## Subsection 3.16.3  All Properties inside PreviewSettings

`PreviewSettings` stores the configuration for generating quick preview
videos. It describes the preview resolution, frame rate, and the folder
where preview files are saved.

This entity does not render anything itself, does not call Manim, and
does not play video files. It is purely a **data container** that tells
the preview service how to configure Manim when generating a draft. Think
of it like a sticky note on your desk that says "drafts go in this
folder, at this size, at this speed" — the note does not do any work,
but the person who reads it knows exactly what to do.

An important thing to understand is that the values in `PreviewSettings`
are **system constants**. They are not meant to be changed by the user.
The entire preview system is built around the assumption that previews
always use 480p resolution and 30 FPS. These values are locked in place
to guarantee that previews are always fast, every single time.

---

### Subsubsection 3.16.3.1  `preview_resolution`

```
+------------------+---------------------------+
| Field            | Value                     |
+------------------+---------------------------+
| Type             | str                       |
| Default          | "854x480"                 |
| Example values   | "854x480"                 |
+------------------+---------------------------+
```

The `preview_resolution` is fixed at `"854x480"` (480p). This is not a
user-configurable setting — it is a system constant that never changes,
regardless of what `render_resolution` is set to in `RenderSettings`.

The entire point of the preview system is speed. If the preview used the
same resolution as the full render (1080p by default), it would take just
as long to generate and the whole concept of a "quick preview" would be
pointless. By locking the resolution at 480p, the system guarantees that
previews are always fast.

```
+-------------------------------------------------------------+
|   WHY 480p IS LOCKED FOR PREVIEWS                           |
+-------------------------------------------------------------+
|                                                             |
|   "854x480"    →  480p  →  409,920 pixels per frame        |
|   "1920x1080"  →  1080p →  2,073,600 pixels per frame      |
|                                                             |
|   1080p has roughly FIVE TIMES more pixels than 480p.       |
|   This means a 480p preview renders approximately 5x faster |
|   than a full 1080p render.                                 |
|                                                             |
|   Example:                                                  |
|     Full render at 1080p takes ~3 minutes                   |
|     Preview at 480p takes    ~35 seconds                    |
|                                                             |
|   Same scene. Same animation. 5x faster.                    |
|                                                             |
+-------------------------------------------------------------+
```

At 480p, the video looks noticeably less sharp than the final output, but
that is perfectly fine for a preview. The user is not watching the preview
for visual beauty — they are watching it to verify that objects are in the
right position, text is spelled correctly, and the animation sequence makes
sense. None of those things require high resolution to check.

---

### Subsubsection 3.16.3.2  `preview_fps`

```
+------------------+---------------------------+
| Field            | Value                     |
+------------------+---------------------------+
| Type             | int                       |
| Default          | 30                        |
| Example values   | 30                        |
+------------------+---------------------------+
```

The `preview_fps` is fixed at `30` frames per second. Just like
`preview_resolution`, this is a system constant — it is not meant to be
changed. The full render uses 60 FPS by default, but the preview cuts
that in half to 30 FPS. Fewer frames per second means fewer frames for
Manim to draw, which directly translates to faster generation.

```
+-------------------------------------------------------------+
|   WHY 30 FPS IS LOCKED FOR PREVIEWS                         |
+-------------------------------------------------------------+
|                                                             |
|   Frame count for a 16.8-second scene:                      |
|                                                             |
|   At 60 fps (full render) →  16.8 × 60 = 1,008 frames      |
|   At 30 fps (preview)     →  16.8 × 30 =   504 frames      |
|                                                             |
|   The preview draws HALF the frames of the full render.     |
|   Motion will look slightly less smooth, but still very     |
|   watchable — perfectly fine for checking layout and logic. |
|                                                             |
+-------------------------------------------------------------+
```

When you combine the lower resolution (5x fewer pixels) with the lower
frame rate (2x fewer frames), a preview can be generated approximately
**10 times faster** than a full render. That is the real power of the
preview system — a scene that takes 3 minutes to fully render will have
its preview ready in about 18 seconds.

At 30 FPS, motion is still smooth enough to follow what is happening in
the animation. The human eye can detect choppiness below about 24 FPS,
so 30 FPS provides a comfortable viewing experience even though it is
half the full render's frame rate. The slight reduction in smoothness
is an acceptable trade-off for the massive speed gain.

---

### Subsubsection 3.16.3.3  `preview_output_dir`

```
+------------------+------------------------------------------+
| Field            | Value                                    |
+------------------+------------------------------------------+
| Type             | str                                      |
| Default          | "previews/"                              |
| Example values   | "previews/", "/tmp/manim_previews/"      |
+------------------+------------------------------------------+
```

The `preview_output_dir` is the folder where Manim saves the preview video
file for each scene after a preview render completes. Preview files are
stored in a completely separate directory from full render output files,
which prevents any possibility of mixing up draft files with final
production files.

This separation matters because the file names can look similar — a
full render might be called `scene_003.mp4` and a preview might be called
`scene_003_preview.mp4`. If they were stored in the same folder, it would
be easy to accidentally use the low-quality preview clip when assembling
the final video. Keeping them in different folders eliminates this risk
entirely.

```
+-------------------------------------------------------------+
|   SEPARATE FOLDERS KEEP THINGS CLEAN                        |
+-------------------------------------------------------------+
|                                                             |
|   previews/              output/                            |
|   ├── scene_001_preview.mp4    ├── scene_001.mp4            |
|   ├── scene_002_preview.mp4    ├── scene_002.mp4            |
|   └── scene_003_preview.mp4    ├── scene_003.mp4            |
|                                                             |
|   LEFT:  low quality drafts (480p, 30 fps)                  |
|   RIGHT: full quality renders (1080p, 60 fps)               |
|                                                             |
|   The export service reads ONLY from output/                |
|   The preview service writes ONLY to previews/              |
|   They never cross paths.                                   |
|                                                             |
+-------------------------------------------------------------+
```

This path can be relative to the project root or an absolute path on the
system. The default `"previews/"` is a relative path, which means the
previews folder is created inside the project directory. This keeps
everything self-contained and makes the project portable — if you copy
the project folder to another machine, the previews go with it.

---

## Subsection 3.16.4  How PreviewSettings Compares to RenderSettings

Because `PreviewSettings` and `RenderSettings` live side by side inside
the same `Project` entity and both control how scenes are rendered, it is
helpful to see them compared directly. The table below shows how every
corresponding property differs between the two entities.

```
+-------------------------------------------------------------+
|   PREVIEW SETTINGS  vs  RENDER SETTINGS                     |
+-------------------------------------------------------------+
|                                                             |
|   Property              Preview    Render                   |
|   ────────────────────────────────────────────────────────  |
|   resolution            854x480    1920x1080                |
|   frame rate            30 fps     60 fps                   |
|   output folder         previews/  output/                  |
|   purpose               quick check final production        |
|   speed                 ~10x faster baseline                |
|   user configurable?    NO         YES                      |
|                                                             |
+-------------------------------------------------------------+
```

The key takeaway is that `PreviewSettings` is designed for one thing
and one thing only: **getting a draft on screen as fast as possible**.
Every value is chosen to minimize generation time. The user does not
configure these values because there is no benefit to changing them —
a preview at 720p would be slower without being meaningfully more useful
than one at 480p. The system makes the optimal choice and locks it in.

---

## Subsection 3.16.5  Full Python Class (Reference)

```python
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
```

# Section 3.17 Entity 15 — ExportSettings

## Subsection 3.17.1  What Is ExportSettings?

`ExportSettings` is the entity that stores the **configuration for the
final video export step** — the step where all individually rendered
scene clips are assembled into one complete, finished video file that
the user can share, upload, or deliver.

Think of the entire SuperManim workflow as a factory assembly line. The
user writes animation code (Scene), renders each scene into a video clip
(RenderSettings), and checks drafts along the way (PreviewSettings).
`ExportSettings` is the **shipping department** at the very end of the
line. It answers the question: "When all scenes are done and I type
`export`, what should the final product look like, what format should
it be in, and where should it be saved?"

While `RenderSettings` controls how each individual scene is drawn by
Manim, and `VideoSettings` stores the identity of the video project
itself, `ExportSettings` is concerned only with the very last step —
taking all the finished scene clips and stitching them together into a
single video file. It does not care about how scenes were rendered or
what code produced them. It only cares about the output: format, quality,
filename, audio, and readiness.

These settings persist between sessions because they are stored as part
of the `Project` entity in the database. The user configures them once
and they stay until deliberately changed. This means the user can set up
their preferred export format and quality at the start of a project and
never think about it again until they are ready to export.

Think of `ExportSettings` as the **delivery label** on a package — it
tells the system exactly how to wrap up and ship the finished product.

---

## Subsection 3.17.2  Where Does ExportSettings Live?

`ExportSettings` is a **nested field inside the `Project` entity**.

```
Project
├── project_name:              "My Math Video"
├── project_total_duration:    60.3
├── project_render_settings:   RenderSettings
├── project_preview_settings:  PreviewSettings
└── project_export_settings:   ExportSettings   ← lives here
                                  ├── export_format:           "mp4"
                                  ├── export_quality:          "high"
                                  ├── export_name:             None
                                  ├── export_output_dir:       "exports/"
                                  ├── export_output_path:      None
                                  ├── export_include_audio:    True
                                  ├── export_codec:            "libx264"
                                  ├── project_is_export_ready: False
                                  └── export_watermark_text:   None
```

When the user creates a new project, `ExportSettings` is automatically
created with sensible defaults — MP4 format, high quality, H.264 codec,
audio enabled, and the readiness flag set to `False` because no scenes
have been rendered yet. As the project progresses and scenes get rendered,
the readiness flag updates automatically. The user can change any of the
configuration values at any time, and the next export will use the updated
settings.

---

## Subsection 3.17.3  All Properties inside ExportSettings

`ExportSettings` stores all configuration for the final video assembly
step, along with a readiness flag and a watermark option. It describes
the output format, quality level, filename, output folder, codec, audio
inclusion, whether the project is ready to export, and an optional
watermark text overlay.

This entity does not assemble video files, does not invoke FFmpeg, and
does not manage any rendering process. It is purely a **data container** —
a set of instructions that the export service reads when it is time to
stitch all the scene clips together into one final video. Think of it
like a recipe card that tells the chef exactly how to plate and package
the dish, but the actual cooking happened earlier in the kitchen.

---

### Subsubsection 3.17.3.1  `export_format`

```
+------------------+------------------------------------------+
| Field            | Value                                    |
+------------------+------------------------------------------+
| Type             | str                                      |
| Default          | "mp4"                                    |
| Example values   | "mp4", "webm", "mov", "avi"              |
+------------------+------------------------------------------+
```

The `export_format` determines the container format of the final assembled
video file. A container format is like the type of box that holds the
video data — it decides what file extension the video gets, what players
can open it, and how the video and audio data are packaged together inside
the file.

MP4 is the default and by far the most widely supported video format in
the world. It works on every operating system, every browser, every phone,
and every video platform. For almost every project, MP4 is the right
choice and the user never needs to change this setting.

```
+-------------------------------------------------------------+
|   THE FOUR EXPORT FORMATS                                     |
+-------------------------------------------------------------+
|                                                             |
|   "mp4"                                            DEFAULT  |
|   Works everywhere. Windows, macOS, Linux, Android, iOS,   |
|   all browsers, YouTube, every video player ever made.     |
|   Best choice for: almost every project.                    |
|   File extension: .mp4                                      |
|                                                             |
|   "webm"                                                   |
|   Designed for the web. Slightly smaller files than MP4.   |
|   Not supported by all desktop players.                     |
|   Best choice for: embedding in websites.                   |
|   File extension: .webm                                     |
|                                                             |
|   "mov"                                                    |
|   Apple QuickTime format. Used in professional editing      |
|   tools like Final Cut Pro and DaVinci Resolve on macOS.   |
|   Larger file sizes than MP4.                               |
|   Best choice for: professional editing on macOS.           |
|   File extension: .mov                                      |
|                                                             |
|   "avi"                                                    |
|   An older Microsoft format. Very large files. Limited      |
|   modern support. Only use if a specific tool needs it.     |
|   File extension: .avi                                      |
|                                                             |
+-------------------------------------------------------------+
```

The choice of format mainly depends on where the video will end up. If
the video is going to YouTube, social media, or a website, MP4 is almost
always the best choice. If the video needs to be imported into a
professional editing tool on macOS, MOV might be preferred. If the video
will be embedded directly in a web page and file size matters more than
compatibility, WebM can be a good option.

---

### Subsubsection 3.17.3.2  `export_quality`

```
+------------------+------------------------------------------+
| Field            | Value                                    |
+------------------+------------------------------------------+
| Type             | str                                      |
| Default          | "high"                                   |
| Example values   | "low", "medium", "high", "ultra"         |
+------------------+------------------------------------------+
```

The `export_quality` determines the resolution and bitrate of the final
assembled video. This setting only affects the very last step where all
the scene clips get stitched together into one file. It does not affect
how individual scenes were rendered — those are always produced at full
resolution in the `output/` folder.

This separation means the user can render all scenes once at full quality,
and then export multiple times at different quality levels without ever
re-rendering a single scene. For example, they could export a quick 480p
version to send to a colleague for review, and then later export a full
1080p version for the final delivery — all from the same set of rendered
clips.

```
+-------------------------------------------------------------+
|   THE FOUR EXPORT QUALITY LEVELS                             |
+-------------------------------------------------------------+
|                                                             |
|   "low"     →  480p   (854 x 480 pixels)                    |
|   File size (~60s video):  ≈  40 MB                         |
|   Export speed:           fastest                           |
|   Best for: quick sharing, internal drafts, testing only.   |
|                                                             |
|   "medium"  →  720p   (1280 x 720 pixels)                   |
|   File size (~60s video):  ≈  90 MB                         |
|   Best for: web uploads, acceptable YouTube quality,         |
|   general-purpose sharing.                                  |
|                                                             |
|   "high"    →  1080p  (1920 x 1080 pixels)        DEFAULT  |
|   File size (~60s video):  ≈  214 MB                        |
|   Best for: most projects. Sharp on all modern screens.     |
|   Standard for YouTube HD uploads and professional content. |
|                                                             |
|   "ultra"   →  4K     (3840 x 2160 pixels)                 |
|   File size (~60s video):  ≈  850 MB                        |
|   Best for: professional publishing, large screens,          |
|   archival quality. Slow to export.                         |
|                                                             |
+-------------------------------------------------------------+
```

Higher quality means more pixels, larger file sizes, and longer export
times. But because the export step only re-encodes video that has already
been rendered, even the "ultra" quality export is much faster than
re-rendering all scenes from scratch.

---

### Subsubsection 3.17.3.3  `export_name`

```
+------------------+------------------------------------------+
| Field            | Value                                    |
+------------------+------------------------------------------+
| Type             | Optional[str]                            |
| Default          | None                                     |
| Example values   | "IntroToCalculus_Ep1", "FinalVersion_v3" |
+------------------+------------------------------------------+
```

The `export_name` is the custom filename the user wants for the final
exported video, **without the file extension**. The file extension is
always added automatically from the `export_format` field, so the user
never needs to type `.mp4` or `.webm` as part of the name.

When `export_name` is `None`, the system falls back to using
`project_name + "_final"` as the filename. This means that if the user
never sets a custom name, the exported file will be named after the
project with `_final` appended to it.

```
export_name = None
project_name = "MyAnimation"
→ exported file:  exports/MyAnimation_final.mp4

export_name = "IntroToCalculus_Ep1"
export_format = "mp4"
→ exported file:  exports/IntroToCalculus_Ep1.mp4

If the user later changes the format to "webm" (name stays the same):
→ exported file:  exports/IntroToCalculus_Ep1.webm
```

The extension is always derived automatically from `export_format`. This
design means the user can change the video format without having to
rename the file — the system handles it. The user only needs to provide
the base name once, and the correct extension is always applied.

---

### Subsubsection 3.17.3.4  `export_output_dir`

```
+------------------+----------------------------------------------+
| Field            | Value                                        |
+------------------+----------------------------------------------+
| Type             | str                                          |
| Default          | "exports/"                                   |
| Example values   | "exports/", "/home/mina/videos/", "output/"  |
+------------------+----------------------------------------------+
```

The `export_output_dir` is the folder where the final assembled video
file will be saved when the export command runs. This is the destination
folder — the place where the finished product lands after all the scene
clips have been stitched together.

```
exports/
└── IntroToCalculus_Ep1.mp4   ← the final finished video lives here
```

This path can be relative to the project root directory or an absolute
path on the system. Using a relative path like `"exports/"` keeps
everything self-contained inside the project folder, which makes the
project portable. Using an absolute path like `"/home/mina/videos/"`
saves the file to a specific location on the computer, which is useful
if the user wants all exported videos from all projects to go to one
central folder.

The export folder is separate from both the render output folder
(`output/`) and the preview folder (`previews/`). This three-folder
structure keeps things organized — drafts in one place, renders in
another, and the final finished product in a third.

---

### Subsubsection 3.17.3.5  `export_output_path`

```
+------------------+----------------------------------------------+
| Field            | Value                                        |
+------------------+----------------------------------------------+
| Type             | Optional[str]                                |
| Default          | None                                         |
| Example value    | "exports/IntroToCalculus_Ep1.mp4"            |
+------------------+----------------------------------------------+
```

The `export_output_path` stores the **full path** to the final exported
video file after it has been successfully created. Before any export has
happened, this field is `None`. After a successful export, the system
writes the complete file path here automatically.

This is a **result value**, not a configuration value. The user never
sets this field manually. It is filled in by the export service after
FFmpeg finishes assembling the video. The system then uses this path
to tell the user where to find the finished file, or to open it
directly in a video player.

```
Before export:  export_output_path = None
After export:   export_output_path = "exports/IntroToCalculus_Ep1.mp4"
```

Think of it like a delivery confirmation number. You do not write it
yourself — the shipping company fills it in after the package has been
delivered, and then you can use it to track down exactly where the
package is.

---

### Subsubsection 3.17.3.6  `export_include_audio`

```
+------------------+---------------------------+
| Field            | Value                     |
+------------------+---------------------------+
| Type             | bool                      |
| Default          | True                      |
| Example values   | True, False               |
+------------------+---------------------------+
```

The `export_include_audio` controls whether the final exported video
includes sound or not. When set to `True` (the default), the export
service mixes the audio from each scene's audio clip into the final
video during assembly. The exported video will have narration, music,
or whatever audio was recorded for the project.

When set to `False`, the export service assembles only the video
clips without any audio track. The exported video will be completely
silent. This is useful in post-production workflows where the user
wants to do the audio mixing separately in a professional audio or
video editor.

```
export_include_audio = True   → final video has sound
                             → narration, music, sound effects included
                             → ready to upload and share as-is

export_include_audio = False  → final video is silent
                             → video-only, no audio track
                             → useful for external editing workflows
```

The audio for each scene comes from the `AudioClip` entity that was
synced to that scene. If a scene does not have an audio clip, that
portion of the final video simply has no sound, even when this setting
is `True`.

---

### Subsubsection 3.17.3.7  `export_codec`

```
+------------------+----------------------------------------------+
| Field            | Value                                        |
+------------------+----------------------------------------------+
| Type             | str                                          |
| Default          | "libx264"                                    |
| Example values   | "libx264", "libx265", "libvpx-vp9", "prores" |
+------------------+----------------------------------------------+
```

The `export_codec` is the video compression codec used when encoding
the final assembled video. A codec is the algorithm that squeezes the
raw video data into a smaller file. Different codecs make different
trade-offs between file size, encoding speed, video quality, and
compatibility with different devices and players.

H.264 (`libx264`) is the default and the safest choice. It has been
the industry standard for over a decade and works on virtually every
device and platform in existence. For most users and most projects,
there is no reason to change this setting.

```
+-------------------------------------------------------------+
|   THE FOUR EXPORT CODECS                                      |
+-------------------------------------------------------------+
|                                                             |
|   "libx264"  →  H.264 codec. DEFAULT.                       |
|   Best compatibility. Works everywhere.                     |
|   Good balance of file size and quality.                    |
|   Best for: general delivery, YouTube, web sharing.         |
|                                                             |
|   "libx265"  →  H.265 / HEVC codec.                         |
|   Roughly HALF the file size of H.264 at same quality.      |
|   Slower to encode. Needs a newer player to play.           |
|   Best for: archival storage, reducing disk usage.          |
|                                                             |
|   "libvpx-vp9"  →  VP9 codec. Used with WebM format.       |
|   Efficient open-source codec. Good web support.            |
|   Best for: web video without licensing concerns.           |
|                                                             |
|   "prores"  →  Apple ProRes codec. Used with MOV format.   |
|   Very large files. Designed for professional editing.      |
|   Best for: macOS post-production workflows.                |
|                                                             |
+-------------------------------------------------------------+
```

The codec choice should match the format choice. Using `"prores"` with
the `"webm"` format would not make sense, because ProRes is designed for
the MOV container. In practice, the system handles these pairings
automatically, but understanding which codecs go with which formats
helps the user make informed decisions.

---

### Subsubsection 3.17.3.8  `project_is_export_ready`

```
+------------------+---------------------------+
| Field            | Value                     |
+------------------+---------------------------+
| Type             | bool                      |
| Default          | False                     |
| Example values   | True, False               |
+------------------+---------------------------+
```

The `project_is_export_ready` flag is the **most important readiness
signal** in the entire project. It tells the system and the user whether
the project is complete enough to be exported into a final video. This
flag is `True` only when every single scene in the project has been
successfully rendered. Even one pending scene or one failed scene will
keep this flag at `False`.

For the flag to become `True`, all three of these conditions must be
met at the same time:

```
project_is_export_ready = True   ONLY when ALL of these are true:

  project_total_scenes    >  0     (the project has at least one scene)
  project_pending_scenes  == 0     (no scenes are waiting to be rendered)
  project_failed_scenes   == 0     (no scenes have errors)
```

The export command checks this flag before doing anything. If it is
`False`, the export is refused and the user is told exactly what is
missing — which scenes are still pending or which ones have failed. This
prevents the user from accidentally exporting an incomplete video where
some scenes are missing or broken.

```
+-------------------------------------------------------------+
|   project_is_export_ready — FULL LIFECYCLE                   |
+-------------------------------------------------------------+
|                                                             |
|   PROJECT CREATED (5 scenes, none rendered):                |
|   total=5  rendered=0  pending=5  failed=0                  |
|   project_is_export_ready = False  ← cannot export yet      |
|                                                             |
|   AFTER RENDERING SCENES 1, 2, 3:                           |
|   total=5  rendered=3  pending=2  failed=0                  |
|   project_is_export_ready = False  ← 2 scenes still waiting |
|                                                             |
|   SCENE 4 RENDERS WITH AN ERROR:                            |
|   total=5  rendered=3  pending=1  failed=1                  |
|   project_is_export_ready = False  ← one scene has an error |
|                                                             |
|   USER FIXES SCENE 4 AND RE-RENDERS. SCENE 5 ALSO RENDERS: |
|   total=5  rendered=5  pending=0  failed=0                  |
|   project_is_export_ready = True   ← ALL DONE. READY!       |
|                                                             |
+-------------------------------------------------------------+
```

This flag is automatically maintained by the scene management service.
Every time a scene's status changes — from pending to rendered, from
rendered to failed, or from failed back to rendered — the service
recalculates whether the project is fully ready. The user never has to
set this flag manually.

---

### Subsubsection 3.17.3.9  `export_watermark_text`

```
+------------------+----------------------------------------------+
| Field            | Value                                        |
+------------------+----------------------------------------------+
| Type             | Optional[str]                                |
| Default          | None                                         |
| Example values   | "Math With Mina", "© 2025 SuperManim"        |
+------------------+----------------------------------------------+
```

The `export_watermark_text` is an optional text string that gets burned
into the video frames during export. It appears as a visible text overlay
in a corner of every frame in the final video, like a channel logo or a
copyright notice that you see on television broadcasts.

When this field is `None` (the default), no watermark is added and the
video frames are left untouched. The user only needs to set this field
if they want a visible brand or notice on their exported video.

```
export_watermark_text = None   → no watermark, clean video frames

export_watermark_text = "Math With Mina"
→ every frame in the exported video shows "Math With Mina"
  in the bottom corner, overlaid on top of the animation
```

It is important to understand the difference between this watermark
and the `video_author` field in `VideoSettings`. The `video_author`
field is invisible metadata — it is embedded inside the video file's
data but nobody can see it while watching the video. The
`export_watermark_text` is a visible, permanent text overlay that is
literally painted onto every frame. Once exported with a watermark, it
cannot be removed without re-exporting.

---

## Subsection 3.17.4  Full Python Class (Reference)

```python
# File location: /home/mina/SuperManim/core/entities/export_settings.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class ExportSettings:
    """
    ExportSettings stores all configuration for the final video
    assembly step — where rendered scene clips are stitched together
    into one complete output file.

    It describes the output format, quality level, filename, folder,
    codec, audio inclusion, export readiness, and optional watermark.

    This entity does not assemble video, invoke FFmpeg, or encode
    anything. It is a pure data container — a set of instructions
    that the export service reads to know how to package the final
    video.

    The project_is_export_ready flag is automatically maintained by
    the scene management service. It is True only when all scenes
    are rendered with zero pending and zero failed.
    """

    # === Output Format ===
    export_format:           str           = "mp4"

    # === Output Quality ===
    export_quality:          str           = "high"

    # === Output Naming ===
    export_name:             Optional[str] = None
    export_output_dir:       str           = "exports/"

    # === Export Result (set automatically after export) ===
    export_output_path:      Optional[str] = None

    # === Audio ===
    export_include_audio:    bool          = True

    # === Codec ===
    export_codec:            str           = "libx264"

    # === Readiness ===
    project_is_export_ready: bool          = False

    # === Watermark ===
    export_watermark_text:   Optional[str] = None
```



---
# Section 3.18  Quick Reference Summary

| Entity | Purpose | Key Properties |
|---|---|---|
| **AudioSettings** | Describes the master audio file | `audio_format`, `audio_file_path`, `audio_total_duration` |
| **VideoSettings** | Identity card of the video | `video_width`, `video_height`, `video_aspect_ratio`, `video_author`, `video_language` |
| **RenderSettings** | Manim rendering defaults | `render_resolution`, `render_fps`, `render_background_color`, `render_quality` |
| **PreviewSettings** | Fast draft preview config | `preview_resolution` (fixed 480p), `preview_fps` (fixed 30), `preview_auto_open` |
| **ExportSettings** | Final video delivery config | `export_format`, `export_quality`, `export_name`, `project_is_export_ready` |

---

```
Where each entity lives inside Project:

Project
├── project_audio_settings:    AudioSettings
├── project_video_settings:    VideoSettings
├── project_render_settings:   RenderSettings
├── project_preview_settings:  PreviewSettings
└── project_export_settings:   ExportSettings
```



# Section 3.19: How All the Entities Relate to Each Other

## Subsection 3.19.1: The Complete Entity Relationship Map

Here is the complete picture of how all ten entities connect to each
other in the SuperManim data model:

```
+=====================================================================+
|              COMPLETE ENTITY RELATIONSHIP DIAGRAM                    |
+=====================================================================+
|                                                                     |
|   Project                                                           |
|   ─────────────────────────────────────────────────────────────    |
|   │ Has one  → Timeline      (one ordered view of all scenes)       |
|   │ Has many → Scene         (via project_items or DB)              |
|   │ Has one  → AudioFile     (the master audio recording)           |
|   │ Has one  → VideoFile     (the master video, if used)            |
|   │                                                                 |
|   Timeline                                                          |
|   ─────────────────────────────────────────────────────────────    |
|   │ References many → Scene  (via ordered_scene_ids list)           |
|   │                                                                 |
|   AudioFile                                                         |
|   ─────────────────────────────────────────────────────────────    |
|   │ Has many → AudioClip     (one clip per scene, via audio_clips)  |
|   │                                                                 |
|   VideoFile                                                         |
|   ─────────────────────────────────────────────────────────────    |
|   │ Has many → VideoClip     (one clip per scene, via video_clips)  |
|   │                                                                 |
|   Scene                                                             |
|   ─────────────────────────────────────────────────────────────    |
|   │ Is linked to ← AudioClip (via AudioClip.scene_id)              |
|   │ Has many → SubScene      (via scene_map list)                   |
|   │ Has many → AssetFile     (via AssetFile.scene_id)              |
|   │ Inherits from → MediaUnit                                       |
|   │                                                                 |
|   SubScene                                                          |
|   ─────────────────────────────────────────────────────────────    |
|   │ Belongs to → Scene       (via parent_scene_id)                  |
|   │                                                                 |
|   AudioClip                                                         |
|   ─────────────────────────────────────────────────────────────    |
|   │ Belongs to → AudioFile   (via audio_file_id)                    |
|   │ Is linked to → Scene     (via scene_id)                         |
|   │ Inherits from → MediaUnit                                       |
|   │                                                                 |
|   AssetFile                                                         |
|   ─────────────────────────────────────────────────────────────    |
|      Belongs to → Scene      (via scene_id)                         |
|      Contributes to → scene_assets_hash on parent Scene             |
|                                                                     |
+=====================================================================+
```

## Subsection 3.19.2: A Complete Real-World Data Flow Example

Here is a step-by-step example showing how all the entities work together
when a user creates and renders a complete 4-scene synchronized video.

```
+=====================================================================+
|   COMPLETE DATA FLOW: 4-SCENE SYNCHRONIZED VIDEO                    |
+=====================================================================+
|                                                                     |
|   COMMAND: new project MyAnimation                                  |
|   ENTITIES INVOLVED:                                                |
|     → Project entity created in memory                              |
|     → project_name = "MyAnimation"                                  |
|     → All folders created on disk                                   |
|     → Timeline entity created (empty, total_duration = 0)          |
|     → Saved to database                                             |
|                                                                     |
|   ─────────────────────────────────────────────────────────────    |
|                                                                     |
|   COMMAND: set scenes_number 4                                      |
|   ENTITIES INVOLVED:                                                |
|     → 4 Scene entities created:                                     |
|         Scene(scene_id=1, status="pending", duration=None)          |
|         Scene(scene_id=2, status="pending", duration=None)          |
|         Scene(scene_id=3, status="pending", duration=None)          |
|         Scene(scene_id=4, status="pending", duration=None)          |
|     → Timeline updated:                                             |
|         ordered_scene_ids = [1, 2, 3, 4]                            |
|         scene_count       = 4                                       |
|     → Project.project_total_scenes = 4                              |
|     → Project.project_pending_scenes = 4                            |
|                                                                     |
|   ─────────────────────────────────────────────────────────────    |
|                                                                     |
|   COMMAND: set scene 3 duration 16.8                                |
|   ENTITIES INVOLVED:                                                |
|     → Scene 3 updated: scene_duration = 16800                       |
|     → TimelineService recomputes all start/end times:               |
|         (assumes scenes 1 and 2 already had durations set)          |
|         Scene 3: scene_start_time = 31000, scene_end_time = 47800   |
|     → Timeline updated: total_duration = sum of all scene durations |
|                                                                     |
|   ─────────────────────────────────────────────────────────────    |
|                                                                     |
|   COMMAND: add audio voice.mp3                                      |
|   ENTITIES INVOLVED:                                                |
|     → AudioFile entity created:                                     |
|         AudioFile(audio_file_id=1, audio_file_duration=60.0, ...)   |
|     → Project.audio_total_duration = 60.0                           |
|     → Project.audio_file_path = "audio_clips/original_audio.mp3"   |
|     → Timeline.audio_total_duration = 60.0                          |
|                                                                     |
|   ─────────────────────────────────────────────────────────────    |
|                                                                     |
|   COMMAND: split audio 4                                            |
|   ENTITIES INVOLVED:                                                |
|     → FFmpeg cuts voice.mp3 into 4 pieces (handled by Adapter)      |
|     → 4 AudioClip entities created:                                  |
|         AudioClip(id=1, duration=12.5, start=0.0,  end=12.5)        |
|         AudioClip(id=2, duration=18.5, start=12.5, end=31.0)        |
|         AudioClip(id=3, duration=16.8, start=31.0, end=47.8)        |
|         AudioClip(id=4, duration=12.2, start=47.8, end=60.0)        |
|     → AudioFile.audio_clips = [clip1, clip2, clip3, clip4]          |
|     → AudioFile.audio_file_is_split = True                          |
|                                                                     |
|   ─────────────────────────────────────────────────────────────    |
|                                                                     |
|   COMMAND: set scene 3 code my_scenes/example.py                   |
|   ENTITIES INVOLVED:                                                |
|     → Scene 3 updated:                                              |
|         scene_code_path = "my_scenes/example.py"                   |
|         scene_code_hash = SHA256("my_scenes/example.py" content)   |
|         final_scene_hash recomputed                                  |
|                                                                     |
|   ─────────────────────────────────────────────────────────────    |
|                                                                     |
|   COMMAND: sync scene 3                                             |
|   ENTITIES INVOLVED:                                                |
|     → ValidationService checks:                                     |
|         scene_duration (16800 ms) == clip_duration (16.8s × 1000)?  |
|         16800 == 16800  →  MATCH                                    |
|     → Scene 3 updated: related_audio_clip_path = "clip_003.mp3"    |
|                          synced_with_audio = True                   |
|     → AudioClip 3 updated: scene_id = 3                             |
|                              audio_clip_is_synced = True             |
|                                                                     |
|   ─────────────────────────────────────────────────────────────    |
|                                                                     |
|   COMMAND: render scene 3                                           |
|   ENTITIES INVOLVED:                                                |
|     → RenderService reads Scene 3 entity                            |
|     → Computes fresh final_scene_hash from disk files               |
|     → fresh hash ≠ stored hash  →  RENDER (something changed)       |
|     → ManimAdapter runs Manim on "my_scenes/example.py"             |
|     → Manim produces output/scene_03/scene_03.mp4                  |
|     → Scene 3 updated:                                              |
|         scene_status = "rendered"                                    |
|         scene_output_path = "output/scene_03/scene_03.mp4"          |
|         scene_rendered_at = "2024-11-12 14:22:30"                   |
|         scene_render_duration = 252.7                               |
|         final_scene_hash = (new hash stored)                        |
|     → Project.project_rendered_scenes += 1                          |
|     → Project.project_pending_scenes -= 1                           |
|                                                                     |
|   ─────────────────────────────────────────────────────────────    |
|                                                                     |
|   COMMAND: render scene 3  (run AGAIN, no code changes)             |
|   ENTITIES INVOLVED:                                                |
|     → RenderService reads Scene 3 entity                            |
|     → Computes fresh final_scene_hash from disk files               |
|     → fresh hash == stored hash  →  SKIP (nothing changed!)         |
|     → Scene 3 updated:  scene_status = "skipped"                    |
|     → Manim is NOT called. No waiting. Instant result.              |
|                                                                     |
|   ─────────────────────────────────────────────────────────────    |
|                                                                     |
|   COMMAND: export  (after ALL 4 scenes are rendered)                |
|   ENTITIES INVOLVED:                                                |
|     → Project.project_is_export_ready checked                       |
|     → total=4, rendered=4, pending=0, failed=0  →  True. Proceed.  |
|     → FFmpegAdapter assembles all 4 scene_output_path files         |
|     → Project.export_output_path = "exports/MyAnimation_final.mp4"  |
|                                                                     |
+=====================================================================+
```

## Subsection 3.19.3: The Entity Dependency Graph

This diagram shows which entities depend on other entities — meaning
which entities store IDs or references to other entities:

```
+=====================================================================+
|                ENTITY DEPENDENCY GRAPH                              |
+=====================================================================+
|                                                                     |
|                        Project                                      |
|                      /    |    \                                    |
|                     /     |     \                                   |
|              AudioFile  Timeline  VideoFile                         |
|                 │                    │                              |
|          (audio_file_id)      (video_file_id)                       |
|                 │                    │                              |
|             AudioClip            VideoClip                          |
|                 │ (scene_id)                                         |
|                 │                                                   |
|               Scene ──────────────────────────────────             |
|             /   |   \                                               |
|    (parent_  (scene_  (scene_                                       |
|    scene_id)  id)      id)                                          |
|       │         │          │                                        |
|    SubScene  AssetFile   (many                                      |
|              (contrib.  properties                                  |
|              to hash)   about this                                  |
|                          scene)                                     |
|                                                                     |
|   All of AudioClip, VideoClip, Scene inherit from → MediaUnit       |
|                                                                     |
+=====================================================================+
```

---

# Section 3.20: The `__init__.py` File — Making Imports Clean

## Subsection 3.20.1: What Is `__init__.py`?

The `core/entities/` directory contains a special file called
`__init__.py`. This file makes the directory a Python **package**. It
also serves as a central place to list all the entity classes so that
other modules can import them easily.

### Subsubsection 3.20.1.1: Where Is the __init__.py File?

```
/home/mina/SuperManim/core/entities/__init__.py
```

## Subsection 3.20.2: The Full `__init__.py` File

```python
# File location: /home/mina/SuperManim/core/entities/__init__.py

"""
SuperManim Core Entities Package

This package contains all the Entity classes — pure data containers
that represent the real-world objects that SuperManim works with.

All entities are pure data containers:
  - No database calls
  - No file system calls
  - No subprocess calls
  - No print() calls
  - Only @dataclass fields with types and default values

Import any entity directly from this package:
  from core.entities import Scene, SubScene, Project
  from core.entities import AudioClip, AudioFile
  from core.entities import VideoClip, VideoFile
  from core.entities import AssetFile, Timeline, MediaUnit
"""

from core.entities.scenes import Scene, SubScene
from core.entities.project import Project
from core.entities.media_unit import MediaUnit
from core.entities.audio_clip import AudioClip
from core.entities.audio_file import AudioFile
from core.entities.video_clip import VideoClip
from core.entities.video_file import VideoFile
from core.entities.asset_file import AssetFile
from core.entities.timeline import Timeline

__all__ = [
    "Scene",
    "SubScene",
    "Project",
    "MediaUnit",
    "AudioClip",
    "AudioFile",
    "VideoClip",
    "VideoFile",
    "AssetFile",
    "Timeline",
]
```

With this `__init__.py` in place, any other module in SuperManim can
import entities like this:

```python
# Clean import (using the package):
from core.entities import Scene, Project, AudioClip

# Instead of the verbose per-file import:
from core.entities.scenes import Scene
from core.entities.project import Project
from core.entities.audio_clip import AudioClip
```

---
