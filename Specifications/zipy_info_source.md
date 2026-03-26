@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Module 3 The core of the SuperManim  tool:

###### The fist component is the Core of the tool(The Brain):

WHAT IS "THE CORE"?
---------------------
Before we talk about what is inside the Core, we need to deeply understand
what the Core actually IS as a concept. Most people hear the word "Core"
and think it just means "the important code." That is not precise enough.
Let's build the understanding from the ground up.

The World Is Full of External Things

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

The Core is the answer to this question.The Core Is a Protected Island

Imagine the external world as an ocean. The ocean is noisy, unpredictable,
and full of things that can change at any time. SQLite might be upgraded.
Manim might change its command-line arguments. FFmpeg might change its flags.

The Core is an island in the middle of that ocean.

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
import subprocess to run Manim. It does not call print() to talk to the
terminal. It does not use os.path to touch the file system.

If you open any Python file inside the Core folder and see any of these:

```python
import sqlite3          # NO. This belongs in an Adapter.
import subprocess       # NO. This belongs in an Adapter.
import os               # NO. This belongs in an Adapter.
from manim import *     # NO. This belongs in an Adapter.
print("something")      # NO. This belongs in an Adapter.
```

Something is wrong. That code does not belong in the Core.

So What DOES the Core Know About:
--------------------------------------------------------
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
|   2. ITS OWN RULES (Business Rules)                                 |
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
are the three components of the Core. They are what this document
is going to explain in complete depth.

---
COMPONENT 1: ENTITIES
-----------------------------

What Is an Entity?
=====================
An Entity is a data object. It is a Python class that represents one
real "thing" that SuperManim works with. Think of it as a container
that holds all the information about that thing.

An Entity does not DO anything complex. It does not talk to databases.
It does not run Manim. It does not print anything. It is just a
structured collection of related data fields, grouped together
under a meaningful name.

The word "Entity" comes from the word "thing that exists."
A Scene exists. A Project exists. An AudioClip exists.
These are real things in the world of SuperManim, and each one
is represented in code as an Entity.

Why Do We Need Entities?
=======================
Without Entities, data floats around as loose variables everywhere.
You would have `scene_id`, `scene_duration`, `scene_code_path`,
`scene_status`, `scene_hash` all scattered throughout the code.
When you need to pass a scene to a function, you would have to pass
five separate arguments. When you want to check something about a scene,
you have to remember what the variable was called.

With Entities, all of that information lives together in one object.
You pass ONE Scene object to a function. Inside that function,
you access `scene.duration`, `scene.code_path`, `scene.status`.
Everything about a scene is in one place, under one name.

The Entities in SuperManim
=========================================================
SuperManim has four main Entities. Let us go through each one completely.

---

**Entity 1 — Scene**
=======================
========================
**WHAT IS A SCENE, REALLY?**

Before we look at any code or any property names, let us build a completely
clear picture of what a Scene actually IS inside SuperManim.

A Scene is one section of your video. Think of your final video like a book.
Your book has chapters. Each chapter is one Scene. Chapter 1 plays first,
Chapter 2 plays after it, Chapter 3 plays after that, all the way to the end.

If your video is 60 seconds long and has 5 sections, you have 5 Scenes.

```
+=====================================================================+
|                 YOUR 60-SECOND VIDEO — 5 SCENES                     |
+=====================================================================+
|                                                                     |
|  0s ─────────── 12.5s ─────────── 31.0s ─────── 47.8s ──── 60.0s  |
|  |              |                 |              |          |       |
|  |  SCENE 1     |    SCENE 2      |   SCENE 3    | SCENE 4  |       |
|  | Introduction | Main Concept    |   Example    |Conclusion|       |
|  |  12.5 sec    |   18.5 sec      |  16.8 sec    |  5.5 sec |       |
|  |              |                 |              |          |       |
|                                                                     |
+=====================================================================+
```

Now here is the important thing to understand: a Scene is NOT the video file.
A Scene is NOT the Python animation code.
A Scene is the RECORD that SuperManim keeps about all the information
surrounding one section of the video.

Think of a Scene like a filing card in a cabinet. The filing card says:
"Scene 3. Duration: 16.8 seconds. Code file: example.py.
Status: rendered. Audio: clip_003.mp3. Synced: yes.
Video at: output/scene_03/scene_03.mp4."

The filing card itself is just information. The actual video, audio,
and code files are stored separately on disk. The Scene Entity is that
filing card — the central record that knows where everything is and
what state everything is in.

---

**THE TWO LEVELS OF A SCENE**

A Scene in SuperManim has two levels inside it.

**Level 1** is the Scene itself — one section of the video.

**Level 2** is the SubScene — one block or moment inside that section.

A single Scene can be divided into multiple SubScenes. Each SubScene
is a mini-scene — a smaller piece of animation within the bigger Scene.

Think of it like this:

```
+=====================================================================+
|                      SCENE  AND  SUBSCENES                          |
+=====================================================================+
|                                                                     |
|   SCENE 3 (16.8 seconds total)                                      |
|   ─────────────────────────────────────────────────────────────    |
|   |                                                               | |
|   |  SubScene A       SubScene B        SubScene C                | |
|   |  (0.0 → 5.5s)     (5.5 → 11.2s)    (11.2 → 16.8s)           | |
|   |  "Title appears"  "Graph draws"     "Conclusion fades in"     | |
|   |                                                               | |
|   ─────────────────────────────────────────────────────────────    |
|                                                                     |
|   The Scene is the container.                                       |
|   The SubScenes are the blocks inside that container.               |
|                                                                     |
+=====================================================================+
```

When you write Manim code for Scene 3, you might have multiple animation
blocks: first a title animates in, then a graph draws itself, then a
text conclusion fades in. Each of those blocks is a SubScene.

The SubScene allows SuperManim to track these individual animation blocks
separately — their timing, their content, their order within the Scene.

We will define the SubScene fully after we finish the main Scene properties.

---
**The Full Python Class of scene entitiy**
An Entity is a Python data class. It is a container that holds
all the information about one thing. It does not run Manim.
It does not talk to SQLite. It does not call print().
It is pure data — fields with types and default values.
That is all. That is exactly what makes it clean and safe.

The Scene Entity is the most important Entity in all of SuperManim
because almost every command, every service, every rule, and every
workflow in the entire system reads or updates a Scene object.



Here is the complete Scene Entity with every property:

```python
# core/entities/scene.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Scene:
    """
    The Scene Entity represents one section of the animation video.

    This is a pure data container — a filing card that holds
    all information about one scene. It does not call any
    external tools, does not open databases, does not run Manim.
    It is just structured data.

    A Scene can contain zero or more SubScene objects inside
    its scene_map list. SubScenes are the individual animation
    blocks that make up this scene.
    """

    # ── IDENTITY ──────────────────────────────────────────────────────
    scene_id:               int
    scene_name:             Optional[str]   = None
    scene_index:            int             = 0
    previous_scene_id:      Optional[int]   = None
    next_scene_id:          Optional[int]   = None

    # ── TIMING ────────────────────────────────────────────────────────
    scene_duration:         Optional[float] = None
    scene_start_time:       Optional[float] = None
    scene_end_time:         Optional[float] = None
    scene_start_marker:     Optional[str]   = None
    scene_end_marker:       Optional[str]   = None

    # ── CODE ──────────────────────────────────────────────────────────
    scene_code_path:        Optional[str]   = None
    scene_code_content:     Optional[str]   = None
    scene_hash:             Optional[str]   = None

    # ── CONTENT AND METADATA ──────────────────────────────────────────
    scene_content:          Optional[str]   = None
    scene_background_color: str             = "#000000"
    scene_resolution:       str             = "1920x1080"
    scene_fps:              int             = 60

    # ── STATUS AND OUTPUT ─────────────────────────────────────────────
    scene_status:           str             = "pending"
    scene_output_path:      Optional[str]   = None
    scene_preview_path:     Optional[str]   = None
    scene_error_message:    Optional[str]   = None
    scene_rendered_at:      Optional[str]   = None
    scene_render_duration:  Optional[float] = None

    # ── AUDIO ─────────────────────────────────────────────────────────
    audio_clip_path:        Optional[str]   = None
    synced_with_audio:      bool            = False

    # ── SUBSCENES ─────────────────────────────────────────────────────
    scene_map:              list[SubScene]  = field(default_factory=list)

    # ── ALLOWED STATUS VALUES ─────────────────────────────────────────
    # "pending"   → scene exists but has never been rendered
    # "rendered"  → scene was rendered successfully
    # "failed"    → render was attempted but failed with an error
    # "skipped"   → render was skipped because code did not change
```

---

**EVERY PROPERTY EXPLAINED IN DEPTH**

The properties are grouped into 7 groups. Each group handles one
aspect of what the Scene needs to know about itself.

A quick reference table for every property in the Scene Entity.

```
+================================================================+
|         SCENE ENTITY — COMPLETE PROPERTY REFERENCE            |
+================================================================+
|                                                                |
|  GROUP 1 — IDENTITY                                            |
|  ──────────────────────────────────────────────────────────── |
|  scene_id            int           Required. The unique ID.   |
|  scene_name          str | None    Human label. Optional.     |
|  scene_index         int           Position in sequence.      |
|  previous_scene_id   int | None    ID of preceding scene.     |
|  next_scene_id       int | None    ID of following scene.     |
|                                                                |
|  GROUP 2 — TIMING                                              |
|  ──────────────────────────────────────────────────────────── |
|  scene_duration      float | None  Length in seconds.         |
|  scene_start_time    float | None  Computed: when it starts.  |
|  scene_end_time      float | None  Computed: when it ends.    |
|  scene_start_marker  str | None    Audio label at start.      |
|  scene_end_marker    str | None    Audio label at end.        |
|                                                                |
|  GROUP 3 — CODE                                                |
|  ──────────────────────────────────────────────────────────── |
|  scene_code_path     str | None    Path to the .py file.      |
|  scene_code_content  str | None    Full text of the file.     |
|  scene_hash          str | None    SHA-256 of code file.      |
|                                                                |
|  GROUP 4 — CONTENT AND VISUAL                                  |
|  ──────────────────────────────────────────────────────────── |
|  scene_content       str | None    Description of scene.      |
|  scene_background_color  str       Hex color. Default black.  |
|  scene_resolution    str           e.g. "1920x1080".          |
|  scene_fps           int           Frames per second. Def 60. |
|                                                                |
|  GROUP 5 — STATUS AND OUTPUT                                   |
|  ──────────────────────────────────────────────────────────── |
|  scene_status        str           pending/rendered/failed/   |
|                                    skipped                     |
|  scene_output_path   str | None    Path to final .mp4.        |
|  scene_preview_path  str | None    Path to preview .mp4.      |
|  scene_error_message str | None    Error text if failed.      |
|  scene_rendered_at   str | None    Timestamp of last render.  |
|  scene_render_duration float|None  How long render took (s).  |
|                                                                |
|  GROUP 6 — AUDIO                                               |
|  ──────────────────────────────────────────────────────────── |
|  audio_clip_path     str | None    Path to audio clip file.   |
|  synced_with_audio   bool          True = render with audio.  |
|                                    Default: False.             |
|                                                                |
|  GROUP 7 — SUBSCENES                                           |
|  ──────────────────────────────────────────────────────────── |
|  scene_map           list[SubScene] Animation blocks inside.  |
|                                     Default: empty list.       |
|                                                                |
+================================================================+
```

**GROUP 1 — IDENTITY PROPERTIES**

These properties answer the question: "Which Scene is this and how
does it sit among the other Scenes in the project?"

---

**scene_id**

**Type:** `int`
**Default:** Required (no default — you must provide it)
**Example value:** `3`

The `scene_id` is the unique number that identifies this specific Scene
within the project. No two Scenes in the same project can share the same `scene_id`.
This number is used everywhere in the system — when you type `render scene 3`,
the system loads the Scene whose `scene_id` is 3. When the database stores a Scene,
it uses `scene_id` as the primary key. When the audio clip is named `clip_003.mp3`,
the `003` comes from the `scene_id`.

```
scene_id is the fingerprint of identity.
Everything that references a scene uses scene_id.

render scene 3          → loads scene where scene_id = 3
clip_003.mp3            → audio for scene where scene_id = 3
output/scene_03/...     → video for scene where scene_id = 3
```

---

**scene_name**

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"Introduction"` or `"Main Concept"` or `"Conclusion"`

The `scene_name` is a human-readable label for the scene. While `scene_id` is
a number used by the computer, `scene_name` is a word used by the human.

The `scene_name` is optional. The system works perfectly without it.
But it makes your project much easier to understand. Instead of looking
at a table and seeing "Scene 3 | rendered", you see
"Scene 3 (Example) | rendered". That immediately tells you what the scene is about.

```
WITHOUT scene_name:               WITH scene_name:
  Scene 1 | rendered                Scene 1 (Introduction)    | rendered
  Scene 2 | rendered                Scene 2 (Main Concept)    | rendered
  Scene 3 | rendered                Scene 3 (Example)         | rendered
  Scene 4 | pending                 Scene 4 (Practice)        | pending
  Scene 5 | failed                  Scene 5 (Conclusion)      | FAILED
```

---

**scene_index**

**Type:** `int`
**Default:** `0`
**Example value:** `2` (meaning this is the third scene, 0-indexed)

The `scene_index` is the position of the Scene in the project's sequence.
It uses zero-based counting: the first scene has index 0, the second has index 1,
the third has index 2, and so on.

You might wonder: if we already have `scene_id`, why do we also need `scene_index`?
The reason is that `scene_id` is a permanent identity — it never changes.
Scene 3 always has `scene_id = 3` for the life of the project.
But `scene_index` is the current ORDER position, and that CAN change.

When you run `move scene 5 to 2`, the scene that was Scene 5 keeps its `scene_id`
but its `scene_index` changes from 4 to 1. The order in the video changed,
but the identity of the scene is still the same.

```
+-------------------------------------------------------------+
|   scene_id  vs  scene_index                                 |
+-------------------------------------------------------------+
|                                                             |
|   scene_id     = permanent identity. Never changes.        |
|                  Used for: database lookup, file naming     |
|                                                             |
|   scene_index  = current position in the video sequence.   |
|                  Changes when you move scenes around.       |
|                  Used for: ordering, timeline calculation   |
|                                                             |
|   Example after "move scene 5 to 2":                        |
|                                                             |
|   scene_index 0  →  scene_id=1  (Scene 1, unchanged)       |
|   scene_index 1  →  scene_id=5  (was last, now second)     |
|   scene_index 2  →  scene_id=2  (shifted right)            |
|   scene_index 3  →  scene_id=3  (shifted right)            |
|   scene_index 4  →  scene_id=4  (shifted right)            |
|                                                             |
+-------------------------------------------------------------+
```

---

**previous_scene_id**

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `2` (the scene that plays before this one)

The `previous_scene_id` stores the `scene_id` of the Scene that comes
just before this Scene in the video. For Scene 3, `previous_scene_id` is `2`.
For Scene 1 (the very first scene), `previous_scene_id` is `None` because
there is no scene before it.

This property makes it easy to navigate backward through the sequence.
If you have a Scene object and you want to know what came before it,
you do not have to calculate or search — you just read `scene.previous_scene_id`.

```
Scene 1  →  previous_scene_id = None   (nothing before it)
Scene 2  →  previous_scene_id = 1
Scene 3  →  previous_scene_id = 2
Scene 4  →  previous_scene_id = 3
Scene 5  →  previous_scene_id = 4
```

---

**next_scene_id**

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `4` (the scene that plays after this one)

The `next_scene_id` stores the `scene_id` of the Scene that comes just
after this Scene. For Scene 3, `next_scene_id` is `4`. For Scene 5
(the very last scene), `next_scene_id` is `None` because there is
nothing after it.

Together, `previous_scene_id` and `next_scene_id` form a doubly-linked list
structure. You can start at any scene and navigate in either direction.

```
Scene 1  →  next_scene_id = 2
Scene 2  →  next_scene_id = 3
Scene 3  →  next_scene_id = 4
Scene 4  →  next_scene_id = 5
Scene 5  →  next_scene_id = None   (nothing after it)
```

---

**GROUP 2 — TIMING PROPERTIES**

These properties answer the question: "When does this Scene happen
in the video timeline and exactly how long does it last?"

This group is critically important in SuperManim because audio sync
depends entirely on getting the timing exactly right.

---

**scene_duration**

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `16000`

The `scene_duration` is the length of this Scene in milile seconds. It is the most
important timing property. It tells the animation engine exactly how long to
run the animation for this scene. It tells the audio system exactly how long
the audio clip for this scene must be. It tells the timeline engine how much
space this scene occupies in the full video.

When you type `set scene 3 duration 16.8`, you are setting `scene_duration = 16.8`
for Scene 3. Everything else — audio sync validation, timeline calculation,
assembly — is built on top of this value.

Why `None` by default? Because when a scene is first created (when you type
`set scenes_number 5`), the system creates the Scene object but you have not
told it the duration yet. The `None` value signals "duration not set yet."
The system will refuse to render a scene whose `scene_duration` is `None`.

```
+-------------------------------------------------------------+
|   scene_duration drives everything timing-related           |
+-------------------------------------------------------------+
|                                                             |
|   The animation engine uses it:                             |
|   → "Run Manim for exactly 16.8 seconds"                   |
|                                                             |
|   The audio system uses it:                                 |
|   → "The audio clip must also be 16.8 seconds"             |
|     (Rule 4.1: duration mismatch = sync refused)            |
|                                                             |
|   The timeline uses it:                                     |
|   → scene_end_time = scene_start_time + scene_duration      |
|   → total video length = sum of all scene_durations         |
|                                                             |
+-------------------------------------------------------------+
```

**scene_start_time**

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `31`

The `scene_start_time` is the exact second in the full video when this Scene
begins playing. Scene 1 always starts at `0.0`. Scene 2 starts at the
moment Scene 1 ends. Scene 3 starts at the moment Scene 2 ends, and so on.

This is a computed value — you do not set it manually. The `TimelineService`
calculates it automatically by adding up all the durations of the scenes
that come before this one.

```
For a project with 5 scenes:

  Scene 1: duration=12.5  →  start_time = 0.0
  Scene 2: duration=18.5  →  start_time = 0.0 + 12.5 = 12.5
  Scene 3: duration=16.8  →  start_time = 12.5 + 18.5 = 31.0
  Scene 4: duration= 7.0  →  start_time = 31.0 + 16.8 = 47.8
  Scene 5: duration= 5.5  →  start_time = 47.8 +  7.0 = 54.8
```

The `scene_start_time` is important for audio work because if you are
cutting the audio file manually into clips, you need to know exactly
at what second each scene starts in the original audio file.

---

**scene_end_time**

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `47000`

The `scene_end_time` is the exact second in the full video when this Scene
stops playing. It is always computed as:

```
scene_end_time = scene_start_time + scene_duration
```

For Scene 3 in the example above: `31.0 + 16.8 = 47.8`.

This means Scene 3 occupies the video from 31.0 seconds to 47.8 seconds.

Like `scene_start_time`, this is a computed value. The `TimelineService`
calculates it. You do not set it manually.

---

**scene_start_marker**

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"[INTRO END]"` or `"[CHAPTER 2 BEGIN]"`

The `scene_start_marker` is a human-readable label that marks the beginning
of this scene in the audio file. When you listen to your narration audio,
you might say at second 31.0: "Alright, now let's look at an example."
That phrase is the audio marker for Scene 3.

The marker is stored as a text string. It is purely for reference — so
that when you are working on the project days or weeks later, you can
look at a scene and immediately understand where it starts in your narration
without having to re-listen to the audio file.

---

**scene_end_marker**

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"[CHAPTER 3 END]"` or `"[PAUSE]"`

The `scene_end_marker` is the same idea as `scene_start_marker` but for
the point where the scene ends in the audio. Together, `scene_start_marker`
and `scene_end_marker` give you a human-readable description of the
audio section that corresponds to this scene.

---

**GROUP 3 — CODE PROPERTIES**
These properties answer the question: "What code file draws this
Scene's animation, and has that code changed since the last render?"

This group is the foundation of SuperManim's incremental rendering superpower.

---

**scene_code_path**

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"my_scenes/example.py"`

The `scene_code_path` is the file path to the Python file that contains
the Manim animation code for this scene. This is the file that Manim will
execute to produce the animation video for this scene.

When you type `set scene 3 code my_scenes/example.py`, you are setting
`scene_code_path = "my_scenes/example.py"` for Scene 3.

The path can be relative (starting from the current directory) or absolute
(the full path from the root of your file system). SuperManim validates
that the file actually exists at this path before saving it. If the file
does not exist, the assignment is refused.

The `scene_code_path` is the first thing the render checklist looks at.
If it is `None`, the render is immediately refused — you cannot render
a scene with no code.

---

**scene_code_content**

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** The full text content of the Python file as a string

The `scene_code_content` stores the actual TEXT of the Python code file
inside the database. This is optional but very useful for two reasons.

First, it gives you a snapshot of exactly what code was used in the last
render. Even if you later change or delete the file on disk, the database
still has a record of what the code looked like when it was rendered.

Second, it can be used for debugging. If a render failed, you can look
at the code content that was used and understand why it failed.

This field is populated automatically when the code file is assigned
to the scene, by reading the file and storing its contents.

---

**scene_hash**

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"a3f8c2d1e4b9ff37c128a6d9e0b45721..."`

The `scene_hash` is the SHA-256 fingerprint of the code file at the time
it was last rendered. This is the most important property for SuperManim's
incremental rendering feature.

A SHA-256 hash is a 64-character string that is calculated from the contents
of a file. If you change even ONE character in the file, the hash changes
completely. If the file stays exactly the same, the hash stays exactly the same.

```
+================================================================+
|         HOW scene_hash ENABLES SMART RENDERING                 |
+================================================================+
|                                                                |
|   FIRST RENDER:                                                |
|   You assign example.py to Scene 3.                            |
|   The system reads the file.                                   |
|   Computes SHA-256: "a3f8c2d1e4b9..."                          |
|   Stores it: scene_hash = "a3f8c2d1e4b9..."                   |
|   Renders Scene 3. Produces scene_03.mp4.                      |
|                                                                |
|   SECOND RENDER (you changed nothing):                         |
|   System reads example.py again.                               |
|   Computes SHA-256: "a3f8c2d1e4b9..."   ← same!               |
|   Compares to stored hash: same.                               |
|   Decision: SKIP. Use the existing scene_03.mp4.              |
|   Time saved: 4 minutes.                                       |
|                                                                |
|   THIRD RENDER (you changed one line):                         |
|   System reads example.py again.                               |
|   Computes SHA-256: "f7c3a9e1b2d8..."   ← DIFFERENT!          |
|   Compares to stored hash: different.                          |
|   Decision: RENDER. Produce a new scene_03.mp4.                |
|   Time taken: 4 minutes.                                       |
|                                                                |
+================================================================+
```

When a scene has never been rendered, `scene_hash` is `None`. This `None`
value is treated as "always changed" — meaning the scene will always be
rendered if it has no stored hash.

---

**GROUP 4 — CONTENT AND VISUAL PROPERTIES**

These properties answer the question: "What does this Scene look like
visually? What are its visual settings?"

---

**scene_content**

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"Introduction to Python variables with animated text"`

The `scene_content` is a text description of what this scene is about —
what the animation shows, what the narration covers, what the viewer
will see and hear. It is a human-written note for documentation purposes.

It is purely for reference. The system never reads this field for any
computation. It is there to help you and other developers understand
what each scene is meant to contain.

---

**scene_resolution**

**Type:** `str`
**Default:** `"1920x1080"` (Full HD, 1080p)
**Example value:** `"1920x1080"`, `"3840x2160"`, `"1280x720"`, `"854x480"`

The `scene_resolution` defines the pixel dimensions of the output video
for this scene. It is stored as `"widthxheight"`.

```
+-------------------------------------------------------------+
|   COMMON RESOLUTIONS                                        |
+-------------------------------------------------------------+
|                                                             |
|   "854x480"    →  480p   (low quality, fast render)        |
|   "1280x720"   →  720p   (HD)                              |
|   "1920x1080"  →  1080p  (Full HD — the default)           |
|   "3840x2160"  →  4K     (Ultra HD, very slow render)      |
|                                                             |
+-------------------------------------------------------------+
```

All scenes in a project should use the same resolution, because when
FFmpeg stitches them together into the final video, they must all
have matching dimensions. If Scene 1 is 1080p and Scene 2 is 720p,
the assembly will fail or produce a broken video.

Note that the `scene_resolution` applies to the FINAL render only.
Preview renders always use `"854x480"` regardless of this setting,
to keep previews fast and small.

---

**scene_fps**

**Type:** `int`
**Default:** `60`
**Example value:** `24`, `30`, `60`

The `scene_fps` is the frame rate — how many individual frames
(still images) are drawn per second of video.

```
+-------------------------------------------------------------+
|   WHAT FRAME RATE MEANS                                     |
+-------------------------------------------------------------+
|                                                             |
|   fps = "frames per second"                                 |
|                                                             |
|   24 fps:  cinema standard. Smooth enough for film.         |
|   30 fps:  TV standard. Good for most educational videos.   |
|   60 fps:  very smooth. Best for fast animations.           |
|                                                             |
|   For a 16.8 second scene:                                  |
|   At 24 fps → 16.8 × 24 = 403 frames to render             |
|   At 30 fps → 16.8 × 30 = 504 frames to render             |
|   At 60 fps → 16.8 × 60 = 1008 frames to render            |
|                                                             |
|   Higher fps = smoother video = more frames = slower render |
|                                                             |
+-------------------------------------------------------------+
```

---

**GROUP 5 — STATUS AND OUTPUT PROPERTIES**

These properties answer the question: "What happened when this Scene
was rendered? Was it successful? Where is the output?"

---

**scene_status**

**Type:** `str`
**Default:** `"pending"`

The `scene_status` is the most checked property in the entire Scene Entity.
Every render checklist, every export check, every status display reads this field.

It tells you the current state of the scene with respect to rendering.
There are exactly four allowed values:

```
+================================================================+
|                  THE FOUR STATUS VALUES                        |
+================================================================+
|                                                                |
|   "pending"                                                    |
|   ─────────────────────────────────────────────────────────── |
|   The scene exists but has never been successfully rendered.   |
|   This is the default for every newly created scene.           |
|   Also set when you reset a scene to force re-render.          |
|                                                                |
|   "rendered"                                                   |
|   ─────────────────────────────────────────────────────────── |
|   The scene was rendered successfully.                         |
|   A video file exists at scene_output_path.                    |
|   The scene_hash is stored and up to date.                     |
|   This is the status you want all scenes to have               |
|   before you can export the final video.                       |
|                                                                |
|   "failed"                                                     |
|   ─────────────────────────────────────────────────────────── |
|   A render was attempted but Manim returned an error.          |
|   The scene_error_message field contains the error details.    |
|   The user must fix the code and then retry.                   |
|                                                                |
|   "skipped"                                                    |
|   ─────────────────────────────────────────────────────────── |
|   The render was not attempted because the scene_hash          |
|   matches the stored hash — the code did not change.           |
|   The existing rendered video is still valid and usable.       |
|   This status is set during a "render all" run for scenes      |
|   that were unchanged.                                         |
|                                                                |
+================================================================+
```

The `scene_status` drives the export readiness check. The project cannot
be exported until every Scene has `scene_status = "rendered"`. A single
scene with `"pending"` or `"failed"` status blocks the entire export.

---

**scene_output_path**

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"output/scene_03/scene_03.mp4"`

The `scene_output_path` is the file path where the rendered video file
for this Scene is stored on disk. This is the video clip that will be
stitched together with the other scenes during export to produce the
final video.

This field is set automatically by the render system after a successful
render. You never set it manually.

Before rendering, `scene_output_path` is `None`. After a successful render,
it holds the path like `"output/scene_03/scene_03.mp4"`.

The export system checks that this file actually exists on disk before
starting assembly. If the file was accidentally deleted, the export
will detect this and report the specific scene as missing.

---

**scene_preview_path**

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"previews/scene_03_preview.mp4"`

The `scene_preview_path` is the file path for the low-quality preview
video of this scene. This is completely separate from `scene_output_path`.

Preview videos are:
- Low resolution (always 480p, regardless of scene_resolution)
- Generated quickly (seconds instead of minutes)
- Never used in the final exported video
- Stored in the `previews/` folder, not `output/`
- Used only by the user to check their work

When you type `preview scene 3`, the system generates a quick
480p video and stores its path in `scene_preview_path`.
When you type `clear preview scene 3`, it deletes the file and
sets `scene_preview_path = None`.

---

**scene_error_message**

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"NameError: name 'Circle' is not defined on line 12"`

The `scene_error_message` stores the error text when a render fails.
If Manim crashes or returns an error while rendering this scene,
the error message from Manim is captured and stored here.

When `scene_status = "failed"`, `scene_error_message` will contain
the reason. When `scene_status = "rendered"`, `scene_error_message`
will be `None`.

This field is what the tool shows when you type `show scene 5 info`
and Scene 5 has failed — it displays the exact error so you know
what to fix in your Manim code.

---

**scene_rendered_at**

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"2024-11-12 14:22:30"`

The `scene_rendered_at` stores the timestamp of when this scene was
last successfully rendered. It is stored as a string in ISO format.

This is useful for knowing how fresh your renders are. If you look at
a scene and see it was rendered two weeks ago and you have made many
changes since then, you know it might be stale.


When you type `render scene 3` and Manim finishes successfully, the system does not ask anyone for the time.
It asks the **operating system** directly. Python has a built-in module called `datetime` that talks
to the operating system clock and returns the current date and time at that exact moment.

Here is the complete sequence of what happens, from the moment you press Enter to the moment the timestamp
is stored:

```
YOU PRESS ENTER after typing: render scene 3
          |
          v
+------------------------------------------------------------------+
|  STEP 1: The Shell receives the command                          |
|                                                                  |
|  SuperManimShell.do_render("scene 3")                            |
|  It calls: render_service.render_scene(scene_id=3)               |
+------------------------------------------------------------------+
          |
          v
+------------------------------------------------------------------+
|  STEP 2: RenderService runs all the checks                       |
|                                                                  |
|  - Is project open?          YES                                 |
|  - Does scene have code?     YES                                 |
|  - Has code changed?         YES                                 |
|  - Do durations match?       YES (if synced)                     |
|                                                                  |
|  All checks passed. Proceed to render.                           |
+------------------------------------------------------------------+
          |
          v
+------------------------------------------------------------------+
|  STEP 3: The system reads the clock BEFORE calling Manim         |
|                                                                  |
|  from datetime import datetime                                   |
|                                                                  |
|  render_started_at = datetime.now()                              |
|                                                                  |
|  At this exact moment the OS clock is read.                      |
|  render_started_at = datetime(2024, 11, 12, 14, 18, 5)          |
|  meaning: 12 November 2024, at 14:18:05 (2:18 PM and 5 seconds) |
+------------------------------------------------------------------+
          |
          v
+------------------------------------------------------------------+
|  STEP 4: Manim runs (this takes several minutes)                 |
|                                                                  |
|  result = RenderRunnerPort.render(scene)                         |
|                                                                  |
|  Inside the ManimSubprocessRenderer Adapter:                     |
|  subprocess.run(["manim", "--quality", "high", "example.py"])   |
|                                                                  |
|  The program STOPS HERE and WAITS.                               |
|  Python is blocked. It does nothing until Manim finishes.        |
|  Manim draws every frame. This takes 4 minutes 22 seconds.       |
|                                                                  |
|  Manim finishes. Returns exit code 0. (0 = success)             |
+------------------------------------------------------------------+
          |
          v
+------------------------------------------------------------------+
|  STEP 5: Manim is done. The system reads the clock AGAIN.       |
|                                                                  |
|  render_finished_at = datetime.now()                             |
|                                                                  |
|  render_finished_at = datetime(2024, 11, 12, 14, 22, 27)        |
|  meaning: 14:22:27 (2:22 PM and 27 seconds)                     |
+------------------------------------------------------------------+
          |
          v
+------------------------------------------------------------------+
|  STEP 6: The system checks if Manim succeeded or failed          |
|                                                                  |
|  result.succeeded == True?    YES                                |
|                                                                  |
|  The render worked. Now we calculate and store the data.         |
+------------------------------------------------------------------+
          |
          v
+------------------------------------------------------------------+
|  STEP 7: Calculate the elapsed time                              |
|                                                                  |
|  elapsed = render_finished_at - render_started_at               |
|                                                                  |
|  datetime(14, 22, 27) - datetime(14, 18, 5)                     |
|  = 4 minutes and 22 seconds                                      |
|  = 262 seconds                                                   |
|                                                                  |
|  This becomes: scene.scene_render_duration = 262.0              |
+------------------------------------------------------------------+
          |
          v
+------------------------------------------------------------------+
|  STEP 8: Format the timestamp as a string and store it           |
|                                                                  |
|  scene.scene_rendered_at = render_finished_at.strftime(         |
|      "%Y-%m-%d %H:%M:%S"                                        |
|  )                                                               |
|                                                                  |
|  result: scene.scene_rendered_at = "2024-11-12 14:22:27"        |
|                                                                  |
|  This is the moment Manim finished successfully.                 |
+------------------------------------------------------------------+
          |
          v
+------------------------------------------------------------------+
|  STEP 9: Save everything to the database                         |
|                                                                  |
|  scene.scene_status         = "rendered"                         |
|  scene.scene_rendered_at    = "2024-11-12 14:22:27"             |
|  scene.scene_render_duration = 262.0                             |
|  scene.scene_output_path    = "output/scene_03/scene_03.mp4"    |
|  scene.scene_hash           = current_hash                       |
|                                                                  |
|  SceneRepositoryPort.save_scene(scene)                           |
|  → SqliteSceneRepository writes all fields to the database      |
+------------------------------------------------------------------+
          |
          v
+------------------------------------------------------------------+
|  STEP 10: Tell the user                                          |
|                                                                  |
|  NotificationPort.send_success(                                  |
|      "Scene 3 rendered successfully.\n"                          |
|      "Output:   output/scene_03/scene_03.mp4\n"                  |
|      "Duration: 16.8 seconds\n"                                  |
|      "Rendered in: 4m 22s"                                       |
|  )                                                               |
+------------------------------------------------------------------+
```
The Key Insight — Two Clock Reads, One Subtraction

The whole mechanism rests on one simple idea:

```
+================================================================+
|                                                                |
|   BEFORE Manim starts  →  read the clock  →  time A           |
|                                                                |
|   [Manim runs for several minutes]                             |
|                                                                |
|   AFTER Manim finishes →  read the clock  →  time B           |
|                                                                |
|   scene_rendered_at    =  time B  (when it finished)           |
|   scene_render_duration = time B - time A  (how long it took)  |
|                                                                |
+================================================================+
```

`datetime.now()` is the Python call that reads the operating system clock.
It returns the current date and time at that exact nanosecond.
You call it twice — once before, once after — and the difference is the duration.
The finish time is the timestamp that gets stored.

---

**Why `strftime("%Y-%m-%d %H:%M:%S")` Converts It to a String**

`datetime.now()` returns a Python `datetime` object. SQLite cannot store
a Python object directly — it stores text, numbers, and blobs.
So we convert the datetime to a string using `strftime`, which means
"string format time." The format `"%Y-%m-%d %H:%M:%S"` produces:

```
%Y   = 4-digit year    → 2024
%m   = 2-digit month   → 11
%d   = 2-digit day     → 12
%H   = 2-digit hour    → 14   (24-hour format)
%M   = 2-digit minute  → 22
%S   = 2-digit second  → 27

Result: "2024-11-12 14:22:27"
```

When you later need to read it back as a real datetime object (to do
calculations like "how many days ago was this rendered?"), you convert
it back with `datetime.strptime("2024-11-12 14:22:27", "%Y-%m-%d %H:%M:%S")`.

---
Notice that `scene_rendered_at` is only written when `result.succeeded == True`.

If Manim crashes and returns an error:
- `scene_status` becomes `"failed"`
- `scene_error_message` gets the error text
- `scene_rendered_at` stays `None` — because the scene was NOT successfully rendered

This means `scene_rendered_at` always tells you the last time the scene was **successfully** rendered.
A `None` value means it has never succeeded.

---    

**scene_render_duration**

**Type:** `Optional[float]`
**Default:** `None`
**Example value:** `252.7` (meaning 252.7 seconds = about 4 minutes 12 seconds)

The `scene_render_duration` records how long the last successful render
took, in seconds. This is the elapsed time from when Manim started to
when it finished.

This is purely informational — the system uses it to show you statistics
like "Rendered in 4m 12s" and to estimate how long a full re-render
of all scenes would take.

---

**GROUP 6 — AUDIO PROPERTIES**

These properties answer the question: "Is this Scene linked to an audio
clip, and does it need to play in sync with that audio?"

---

**audio_clip_path**

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"audio_clips/clip_003.mp3"`

The `audio_clip_path` is the file path to the audio clip that belongs
to this scene. When you split the project's audio file into pieces
(one piece per scene), each piece gets stored in the `audio_clips/`
folder and the path to that piece is stored here.

When `audio_clip_path` is `None`, this scene has no audio assigned to it.
If you render it, the rendered video will be a silent video.

When `audio_clip_path` is set, the scene has an audio clip. But the clip
is not yet "active" until `synced_with_audio` is also set to `True`.

```
+-------------------------------------------------------------+
|   THE AUDIO STATES OF A SCENE                               |
+-------------------------------------------------------------+
|                                                             |
|   audio_clip_path = None,  synced_with_audio = False        |
|   → No audio. Scene renders as silent video.               |
|                                                             |
|   audio_clip_path = "clip_003.mp3",  synced_with_audio = False
|   → Audio clip is assigned but NOT yet activated.          |
|     Durations may or may not match yet.                     |
|     Scene still renders as silent video.                    |
|                                                             |
|   audio_clip_path = "clip_003.mp3",  synced_with_audio = True
|   → Audio clip is assigned AND activated.                  |
|     Durations have been verified to match.                  |
|     Scene renders WITH audio included in the video.         |
|                                                             |
+-------------------------------------------------------------+
```

---

**synced_with_audio**

**Type:** `bool`
**Default:** `False`

The `synced_with_audio` flag is a deliberate confirmation by the user that:
1. An audio clip has been assigned to this scene (`audio_clip_path` is set)
2. The audio clip's duration has been verified to match `scene_duration`
3. The scene is ready to render with audio included

This flag is `False` for every newly created scene. It can only be set
to `True` by running the `sync scene` command. And that command will only
set it to `True` if the duration check passes — the scene duration and
the audio clip duration must be identical (within 1 millisecond).

```
+================================================================+
|   THE SYNC FLOW                                                |
+================================================================+
|                                                                |
|   STEP 1: Assign audio clip                                    |
|   scene.audio_clip_path   = "audio_clips/clip_003.mp3"        |
|   scene.synced_with_audio = False   (not yet confirmed)        |
|                                                                |
|   STEP 2: User runs "sync scene 3 audio_clip 3"               |
|   System checks: scene_duration == clip_duration?              |
|   16.8 == 16.8?  YES                                           |
|   scene.synced_with_audio = True   (confirmed!)                |
|                                                                |
|   STEP 3: Render scene 3                                       |
|   System sees synced_with_audio = True                         |
|   System includes audio in the rendered video.                 |
|   Output: scene_03.mp4 with voice narration baked in.         |
|                                                                |
+================================================================+
```

---

**GROUP 7 — THE SUBSCENE MAP**

This is the most advanced property of the Scene Entity.

---

**scene_map**

**Type:** `list[SubScene]`
**Default:** `[]` (empty list)

The `scene_map` is a list of `SubScene` objects. Each `SubScene` represents
one animation block inside this Scene. It is the internal structure of the Scene —
the map of what happens inside the Scene, in what order, and at what times.

When a Scene is first created, `scene_map` is empty. You can add SubScenes
to it as you design the animation in detail.

Not all projects need SubScenes. If your Manim code for Scene 3 is a single
animation sequence with no meaningful internal blocks, you can leave
`scene_map` empty and the system works perfectly.

But if your Scene 3 has distinct phases — a title appears, then a diagram draws,
then a summary text fades in — then SubScenes let you model each of those
phases as a separate tracked entity.

---


**A REAL SCENE OBJECT IN FULL**

Here is what a fully populated Scene object looks like for Scene 3
of a real SuperManim project. Every field is shown with a real value.

```python
Scene(
    # ── IDENTITY ────────────────────────────────────────────────
    scene_id               = 3,
    scene_name             = "Example: Python Variables",
    scene_index            = 2,                  # 0-based, so 3rd scene
    previous_scene_id      = 2,
    next_scene_id          = 4,

    # ── TIMING ──────────────────────────────────────────────────
    scene_duration         = 16.8,
    scene_start_time       = 31.0,               # starts at 31 seconds
    scene_end_time         = 47.8,               # ends at 47.8 seconds
    scene_start_marker     = "[CHAPTER 3 BEGIN]",
    scene_end_marker       = "[CHAPTER 3 END]",

    # ── CODE ────────────────────────────────────────────────────
    scene_code_path        = "my_scenes/example.py",
    scene_code_content     = "from manim import *\nclass Example(Scene):\n ...",
    scene_hash             = "c9a1b3e7f2d4a8b1c3e7f9a2b4d6e8f0...",

    # ── CONTENT AND VISUAL ──────────────────────────────────────
    scene_content          = "Shows how Python variables work with animation",
    scene_background_color = "#000000",
    scene_resolution       = "1920x1080",
    scene_fps              = 60,

    # ── STATUS AND OUTPUT ───────────────────────────────────────
    scene_status           = "rendered",
    scene_output_path      = "output/scene_03/scene_03.mp4",
    scene_preview_path     = "previews/scene_03_preview.mp4",
    scene_error_message    = None,
    scene_rendered_at      = "2024-11-12 14:22:30",
    scene_render_duration  = 252.7,              # 4 minutes 12 seconds

    # ── AUDIO ───────────────────────────────────────────────────
    audio_clip_path        = "audio_clips/clip_003.mp3",
    synced_with_audio      = True,

    # ── SUBSCENES ───────────────────────────────────────────────
    scene_map = [
        SubScene(
            subscene_id          = 1,
            subscene_name        = "Title Card",
            subscene_index       = 0,
            parent_scene_id      = 3,
            subscene_duration    = 5.5,
            subscene_start_time  = 0.0,
            subscene_end_time    = 5.5,
            subscene_content     = "Title appears with FadeIn animation",
            subscene_status      = "rendered",
        ),
        SubScene(
            subscene_id          = 2,
            subscene_name        = "Variable Diagram",
            subscene_index       = 1,
            parent_scene_id      = 3,
            subscene_duration    = 5.7,
            subscene_start_time  = 5.5,
            subscene_end_time    = 11.2,
            subscene_content     = "Box diagram shows variable assignment x = 5",
            subscene_status      = "rendered",
        ),
        SubScene(
            subscene_id          = 3,
            subscene_name        = "Summary Text",
            subscene_index       = 2,
            parent_scene_id      = 3,
            subscene_duration    = 5.6,
            subscene_start_time  = 11.2,
            subscene_end_time    = 16.8,
            subscene_content     = "Three example variable names fade in one by one",
            subscene_status      = "rendered",
        ),
    ]
)
```

---



**Entity-3 SubScene**
=======================
=======================


A SubScene is a mini-scene inside a Scene. It represents one specific
animation block — one moment or sequence within the larger Scene.

```
+=====================================================================+
|                  THE SUBSCENE INSIDE A SCENE                        |
+=====================================================================+
|                                                                     |
|   SCENE 3 — "Python Variables" (16.8 seconds)                       |
|   ─────────────────────────────────────────────────────────────    |
|   |                                                               | |
|   |  SubScene 1        SubScene 2        SubScene 3               | |
|   |  scene_map[0]      scene_map[1]      scene_map[2]             | |
|   |                                                               | |
|   |  start: 0.0s       start: 5.5s       start: 11.2s            | |
|   |  end:   5.5s       end:  11.2s       end:   16.8s            | |
|   |  duration: 5.5s    duration: 5.7s    duration: 5.6s          | |
|   |                                                               | |
|   |  "Title card       "Variable         "Summary with          | |
|   |   animates in"      assignment        three examples"        | |
|   |                     diagram draws"                            | |
|   |                                                               | |
|   ─────────────────────────────────────────────────────────────    |
|                                                                     |
+=====================================================================+
```

**The Full SubScene Entity**

```python
# core/entities/subscene.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class SubScene:
    """
    A SubScene is one animation block inside a Scene.
    It represents a distinct phase or moment within the Scene's animation.
    Like the Scene Entity, it is a pure data container.
    It holds information only. It does not call any external tools.
    """

    # ── IDENTITY ──────────────────────────────────────────────────────
    subscene_id:            int
    subscene_name:          Optional[str]   = None
    subscene_index:         int             = 0
    parent_scene_id:        int             = 0

    # ── TIMING (relative to the START of the parent Scene) ────────────
    subscene_duration:      Optional[float] = None
    subscene_start_time:    Optional[float] = None
    subscene_end_time:      Optional[float] = None

    # ── CONTENT ───────────────────────────────────────────────────────
    subscene_content:       Optional[str]   = None
    subscene_code_path:     Optional[str]   = None
    subscene_hash:          Optional[str]   = None

    # ── STATUS ────────────────────────────────────────────────────────
    subscene_status:        str             = "pending"
    subscene_output_path:   Optional[str]   = None
```

**Every SubScene Property Explained**

```
+================================================================+
|       SUBSCENE ENTITY — COMPLETE PROPERTY REFERENCE           |
+================================================================+
|                                                                |
|  subscene_id         int           Unique ID within scene.    |
|  subscene_name       str | None    Human label. Optional.     |
|  subscene_index      int           Position within scene.     |
|  parent_scene_id     int           Which scene owns this.     |
|  subscene_duration   float | None  Length in seconds.         |
|  subscene_start_time float | None  Start within parent scene. |
|  subscene_end_time   float | None  End within parent scene.   |
|  subscene_content    str | None    Description.               |
|  subscene_code_path  str | None    Optional separate code.    |
|  subscene_hash       str | None    Hash of subscene code.     |
|  subscene_status     str           pending/rendered/failed.   |
|  subscene_output_path str|None     Path to clip if rendered.  |
|                                                                |
+================================================================+
```

---

**subscene_id**

**Type:** `int`
**Example:** `1`, `2`, `3`

The unique identifier for this SubScene within its parent Scene.
`subscene_id = 1` means this is the first block in the scene.

---

 **subscene_name**

**Type:** `Optional[str]`
**Example:** `"Title Card"`, `"Diagram Block"`, `"Summary Text"`

A human-readable name for this animation block.
Purely for documentation and reference.

---

 **subscene_index**

**Type:** `int`
**Default:** `0`

The order position of this SubScene within its parent Scene.
The first SubScene has `subscene_index = 0`, the second has `1`, and so on.
This determines the order in which the animation blocks play.

---

**parent_scene_id**

**Type:** `int`
**Default:** `0`

The `scene_id` of the Scene that this SubScene belongs to.
This links the SubScene back to its parent. If `parent_scene_id = 3`,
this SubScene is a block inside Scene 3.

---

**subscene_duration**

**Type:** `Optional[float]`
**Example:** `5.5`

How many seconds this animation block lasts.
All SubScene durations inside one Scene must add up exactly to the
parent Scene's `scene_duration`.

```
Scene 3 scene_duration = 16.8 seconds
  SubScene 1: subscene_duration = 5.5
  SubScene 2: subscene_duration = 5.7
  SubScene 3: subscene_duration = 5.6
  ─────────────────────────────────────
  Total:                          16.8  ← must match scene_duration
```

---

**subscene_start_time**

**Type:** `Optional[float]`
**Example:** `5.5`

The second within the parent Scene when this animation block begins.
This is measured from the START of the Scene (not from the start of the video).
So `subscene_start_time = 5.5` means this block starts 5.5 seconds into Scene 3.

---

 **subscene_end_time**

**Type:** `Optional[float]`
**Example:** `11.2`

The second within the parent Scene when this animation block ends.
Always computed as: `subscene_end_time = subscene_start_time + subscene_duration`.

---

**subscene_content**

**Type:** `Optional[str]`
**Example:** `"Animated title: Python Variables appear with a FadeIn effect"`

A text description of what happens in this animation block.
Purely for documentation.

---

**subscene_code_path**

**Type:** `Optional[str]`
**Example:** `"my_scenes/example_block_01.py"`

If this SubScene has its own separate code file (rather than being part
of the parent Scene's code file), this stores the path to that file.
This is optional — many SubScenes are just sections of the parent
Scene's code and do not have their own separate file.

---

**subscene_hash**

**Type:** `Optional[str]`
**Example:** `"d4e9a1b3f7c2..."`

The SHA-256 fingerprint of the SubScene's code file (if it has its own
separate file). Used for change detection at the SubScene level.

---

**subscene_status**

**Type:** `str`
**Default:** `"pending"`
**Allowed values:** `"pending"`, `"rendered"`, `"failed"`, `"skipped"`

The render status of this specific SubScene.
Follows the same four-value system as the parent Scene's `scene_status`.

---

**subscene_output_path**

**Type:** `Optional[str]`
**Example:** `"output/scene_03/subscene_01.mp4"`

If this SubScene was rendered separately (as its own video clip),
this stores the path to that clip.

---

**Entity 3 — Project**
=======================
=======================


**WHAT IS A PROJECT, REALLY?**

Before we look at any code or any property names, let us build a completely
clear picture of what a Project actually IS inside SuperManim.

A Project is the top-level workspace for one complete video production.
It is the container that holds absolutely everything related to that
production — every Scene, every audio file, every rendered video,
every setting, every fingerprint, and every piece of history.

Think of a Project like a physical desk in a studio. On that desk you have:
a folder for each scene's code files, a drawer for your audio recordings,
a shelf for your rendered video clips, a notepad where you wrote your settings,
and a filing cabinet that remembers everything you have done so far.
The desk itself is the Project. Without the desk, all those things would
be scattered on the floor with no organization and no connection to each other.

Every single command you type in SuperManim operates on a Project.
When you type `set scene 3 duration 16.8`, that duration is stored in
the current Project's database. When you type `render all`, the render
system reads from the current Project to know what to render.
When you type `export`, the export system reads the current Project's
settings to know what format and quality to use.

There is no work without a Project. The Golden Rule of SuperManim is:
**no command can run unless a Project is currently open.**

---

**THE THREE ROLES OF A PROJECT**

A Project plays three roles at the same time.

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
|   It remembers: how many scenes exist, what their durations are,    |
|   which ones were rendered, what the fingerprints are,              |
|   what the export settings are, and everything else.                |
|   Without this database the project is just an empty folder.        |
|                                                                     |
|   ROLE 3 — THE IDENTITY                                             |
|   ─────────────────────────────────────────────────────────────    |
|   A Project has a name, a creation timestamp, and a         |
|   location. These identify it among all other projects.             |
|   When you type "list projects", SuperManim reads the identity      |
|   fields of all projects and shows them to you.                     |
|                                                                     |
+=====================================================================+
```

---

**THE PHYSICAL FOLDER STRUCTURE OF A PROJECT**

When you type `new project MyAnimation` and press Enter, SuperManim
does not just create a record in a database. It creates a real folder
on your computer's disk with a specific structure inside it.

Every subfolder inside the project has a specific purpose and is managed
by a specific Service. Let us look at the complete structure:

```
+=====================================================================+
|             THE FULL PROJECT FOLDER STRUCTURE ON DISK               |
+=====================================================================+
|                                                                     |
|   /projects/MyAnimation/                                            |
|   |                                                                 |
|   +-- project_data.db         THE BRAIN                            |
|   |                           The SQLite database. Stores all       |
|   |                           settings, scene records, hashes,      |
|   |                           audio records, and history.           |
|   |                           Without this file, the project        |
|   |                           cannot be opened.                     |
|   |                                                                 |
|   +-- audio_clips/            THE SOUND ROOM                        |
|   |   +-- original_audio.mp3  The master audio file. Copied here   |
|   |   |                       when user runs "add audio".           |
|   |   +-- clip_001.mp3        Cut piece for Scene 1.               |
|   |   +-- clip_002.mp3        Cut piece for Scene 2.               |
|   |   +-- clip_003.mp3        Cut piece for Scene 3.               |
|   |                           Managed by:   |
|   |                                                                 |
|   +-- scenes/                 THE WORKSHOP                          |
|   |   +-- scene_01/           Folder for Scene 1's files.          |
|   |   +-- scene_02/           Folder for Scene 2's files.          |
|   |   +-- scene_03/           Folder for Scene 3's files.          |
|   |                           Each scene_XX/ folder holds the       |
|   |                           Python code and any related files     |
|   |                           for that specific scene.              |
|   |                           Managed by:     |
|   |                                                                 |
|   +-- output/                 THE CINEMA                            |
|   |   +-- scene_01/           Rendered .mp4 for Scene 1.           |
|   |   |   +-- scene_01.mp4                                          |
|   |   +-- scene_02/           Rendered .mp4 for Scene 2.           |
|   |   |   +-- scene_02.mp4                                          |
|   |   +-- scene_03/           Rendered .mp4 for Scene 3.           |
|   |       +-- scene_03.mp4                                          |
|   |                           This is where the final high-quality  |
|   |                           video clips appear after rendering.   |
|   |                           Managed by:    |
|   |                                                                 |
|   +-- previews/               THE DRAFT ROOM                        |
|   |   +-- scene_01_preview.mp4  Low-quality 480p draft video.      |
|   |   +-- scene_02_preview.mp4  Generated by "preview scene N".    |
|   |                           Never used in the final export.       |
|   |                           Managed by:  |
|   |                                                                 |
|   +-- exports/                THE DELIVERY ROOM                     |
|   |   +-- MyAnimation_final.mp4  The final assembled video.        |
|   |                           This is the finished product:         |
|   |                           all scenes stitched together.         |
|   |                           Managed by:      |
|   |                                                                 |
|   +-- assets/                 THE LIBRARY                           |
|   |   +-- images/             User-provided images (.png, .jpg)    |
|   |   +-- fonts/              Custom fonts (.ttf, .otf)            |
|   |   +-- videos/             Embedded video clips                  |
|   |                           When Manim code needs an image or    |
|   |                           font, it looks in assets/.            |
|   |                                                                 |
|   +-- cache/                  THE FINGERPRINT VAULT                 |
|   |                           Stores SHA-256 hash fingerprints      |
|   |                           for each scene's code file.           |
|   |                           Used by the incremental render system |
|   |                           to detect what changed.               |
|   |                           Managed by:        |
|   |                                                                 |
|   +-- temp/                   THE TRASH BIN                         |
|                               Temporary files created during        |
|                               processing (audio conversion,         |
|                               video assembly, etc.).                |
|                               Automatically cleaned up after use.   |
|                               You never need to look here.          |
|                                                                     |
+=====================================================================+
```

 **THE FULL PYTHON CLASS**

A Project Entity is a `@dataclass`. It is a pure data container.
It holds all the information about one project. It does not create folders.
It does not open databases. It does not print anything.
The `ProjectLifecycleService` does those things by reading and writing
the fields of this Entity.

Here is the complete Project Entity with every property:

```python
# core/entities/project.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class Project:
    """
    The Project Entity represents one complete video production workspace.

    This is a pure data container — the filing card for the whole project.
    It holds all identifying information, location data, timestamps,
    mode settings, export settings, render settings, and project-level
    statistics.

    It does not create folders, does not open databases, does not call
    Manim or FFmpeg. It is just structured data.
    """

    # ── IDENTITY ──────────────────────────────────────────────────────
    project_name:               str
   
    # ── LOCATION ──────────────────────────────────────────────────────
    project_folder_path:        Optional[str]       = None
    project_db_path:            Optional[str]       = None

    # ── TIMESTAMPS ────────────────────────────────────────────────────
    project_created_at:         Optional[str]       = None
   
    # ── STATE ─────────────────────────────────────────────────────────
     project_total_scenes:       int                 = 0
    project_total_duration:     float               = 0.0

    # ── EXPORT SETTINGS ───────────────────────────────────────────────
    export_format:              Optional[str]       = "mp4"
    export_quality:             Optional[str]       = "high"
    export_name:                Optional[str]       = None
    export_output_path:         Optional[str]       = None

    # ── RENDER SETTINGS ───────────────────────────────────────────────
    render_resolution:          str                 = "1920x1080"
    render_fps:                 int                 = 60
    render_background_color:    str                 = "#000000"

    # ── PREVIEW SETTINGS ──────────────────────────────────────────────
    preview_resolution:         str                 = "854x480"
    preview_fps:                int                 = 30

    # ── AUDIO SETTINGS ────────────────────────────────────────────────
    audio_format:               str                 = "mp3"
    audio_file_path:            Optional[str]       = None
    audio_total_duration:       Optional[float]     = None

    # ── STATISTICS ────────────────────────────────────────────────────
    project_rendered_scenes:    int                 = 0
    project_pending_scenes:     int                 = 0
    project_failed_scenes:      int                 = 0
    project_is_export_ready:    bool                = False

   ```

---

**EVERY PROPERTY EXPLAINED IN DEPTH**

The properties are grouped into 9 groups. Each group handles one
aspect of what the Project needs to know about itself.

A quick reference table for every property in the Project Entity:

```
+================================================================+
|         PROJECT ENTITY — COMPLETE PROPERTY REFERENCE          |
+================================================================+
|                                                                |
|  GROUP 1 — IDENTITY                                            |
|  ──────────────────────────────────────────────────────────── |
|   |
|  project_name         str         Required. Human name.       |
|                                                               |
|  GROUP 2 — LOCATION                                            |
|  ──────────────────────────────────────────────────────────── |
|  project_folder_path  str | None  Path to project root folder.|
|  project_db_path      str | None  Path to project_data.db.   |
|                                                                |
|  GROUP 3 — TIMESTAMPS                                          |
|  ──────────────────────────────────────────────────────────── |
|  project_created_at      str|None When project was created.   |
|  project_updated_at      str|None When last modified.         |
|           |
|                                                                |
|  GROUP 4 — STATE                                               |
|  ──────────────────────────────────────────────────────────── |
|                                                               |
|  project_total_scenes    int      How many scenes exist.      |
|  project_total_duration  float    Sum of all scene durations. |
|                                                                |
|  GROUP 5 — EXPORT SETTINGS                                     |
|  ──────────────────────────────────────────────────────────── |
|  export_format        str         mp4/webm/mov/avi.           |
|  export_quality       str         low/medium/high/ultra.      |
|  export_name          str | None  Custom output filename.     |
|  export_output_path   str | None  Full path to final video.   |
|                                                                |
|  GROUP 6 — RENDER SETTINGS                                     |
|  ──────────────────────────────────────────────────────────── |
|  render_resolution       str      e.g. "1920x1080". Def 1080p.|
|  render_fps              int      Frames per second. Def 60.  |
|  render_background_color str      Hex color. Default black.   |
|                                                                |
|  GROUP 7 — PREVIEW SETTINGS                                    |
|  ──────────────────────────────────────────────────────────── |
|  preview_resolution   str         Always "854x480".           |
|  preview_fps          int         Default 30.                  |
|                                                                |
|  GROUP 8 — AUDIO SETTINGS                                      |
|  ──────────────────────────────────────────────────────────── |
|  audio_format         str         mp3/wav/ogg/aac. Def "mp3". |
|  audio_file_path      str | None  Path to original audio.     |
|  audio_total_duration float|None  Total seconds of audio.     |
|                                                                |
|  GROUP 9 — STATISTICS                                          |
|  ──────────────────────────────────────────────────────────── |
|  project_rendered_scenes  int     Count of rendered scenes.   |
|  project_pending_scenes   int     Count of pending scenes.    |
|  project_failed_scenes    int     Count of failed scenes.     |
|  project_is_export_ready  bool    True only if all rendered.  |
|                                                                |
+================================================================+
```

---

**GROUP 1 — IDENTITY PROPERTIES**

These properties answer the question: "Which Project is this and what
kind of work does it do?"

---
**project_name**

**Type:** `str`
**Default:** Required (no default — you must provide it)
**Example value:** `"MyAnimation"`, `"Chapter1_Intro"`, `"PythonTutorial"`

The `project_name` is the human-readable name for this project. It is the
name the user gave when they typed `new project MyAnimation`. It is also
the name of the folder created on disk.

The name is case-sensitive. `MyAnimation` and `myanimation` are two
different projects. The `project_name` is used everywhere in the system:
in terminal output, in folder creation, in the database filename, and in
the default export filename.

```
project_name = "MyAnimation"

Folder created:
  /projects/MyAnimation/

Database created:
  /projects/MyAnimation/project_data.db

Default export file produced:
  /projects/MyAnimation/exports/MyAnimation_final.mp4

Every status display shows it:
  Project Status — MyAnimation
  ==============================
  Project: MyAnimation
```

The name cannot contain spaces. If a user tries to create a project with
a space in the name, the `ValidationService.project_name_is_valid()`
method refuses it immediately and explains why.

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

---
**GROUP 2 — LOCATION PROPERTIES**

These properties answer the question: "Where does this Project live
on the computer's disk?"

---

**project_folder_path**

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"/home/user/projects/MyAnimation"`

The `project_folder_path` is the full absolute path to the root folder
of this project on your computer's file system. This is the top-level
folder that contains all subfolders and the database file.

When the `ProjectLifecycleService` creates a new project, it:
1. Determines the path (the global projects directory plus the project name)
2. Creates the folder using the `FileStoragePort`
3. Stores the full path in this field

Every file path stored elsewhere in the system — `scene_output_path`,
`audio_clip_path`, `scene_code_path` — is either an absolute path or
a path relative to `project_folder_path`.

```
project_folder_path = "/home/user/projects/MyAnimation"

All subfolders are inside this root:
  audio_clips/  =  project_folder_path + "/audio_clips/"
  scenes/       =  project_folder_path + "/scenes/"
  output/       =  project_folder_path + "/output/"
  database      =  project_folder_path + "/project_data.db"
```

---

**project_db_path**

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"/home/user/projects/MyAnimation/project_data.db"`

The `project_db_path` is the full path to the SQLite database file for
this project. This is the brain of the project — the file that remembers
everything about it across sessions.

When you type `open project MyAnimation`, the very first thing the system
does is locate this file and open it. If this file is missing or corrupted,
the project cannot be opened.

The database file is always named `project_data.db` and always lives
directly inside `project_folder_path`. The `project_db_path` stores the
full path as a convenience so that any code that needs the database can
read this one field instead of constructing the path from parts every time.

```
project_db_path = project_folder_path + "/project_data.db"
               = "/home/user/projects/MyAnimation/project_data.db"
```

---

**GROUP 3 — TIMESTAMP PROPERTIES**

These properties answer the question: "When was this Project created,
when was it last changed, and when was it last used?"

All three are strings in the format `"YYYY-MM-DD HH:MM:SS"`, set
automatically by the system using `datetime.now()` — the exact same
mechanism explained in the Scene Entity's `scene_rendered_at` field.
The system reads the operating system clock, formats it as a string,
and stores it.

---

**project_created_at**

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"2024-11-10 09:00:15"`

The `project_created_at` stores the exact date and time when this project
was first created — when the user ran `new project MyAnimation` and
the `ProjectLifecycleService` created all the folders and the database.

This timestamp is written exactly once — at creation time — and never
changed again for the life of the project. It is the project's birth certificate.

You see it in the `project info` output:

```
supermanim> project info

  ==========================================
  Project: MyAnimation
  ==========================================
  Mode:          supermanim
  Created:       2024-11-10 09:00      <- project_created_at
  Last modified: 2024-11-12 14:30
  Location:      /projects/MyAnimation/
```

**project_total_scenes**

**Type:** `int`
**Default:** `0`
**Example value:** `5`

The `project_total_scenes` stores the count of how many Scene records
currently exist in this project. This is a cached counter that is
updated automatically whenever a scene is added or deleted:

```
User types: set scenes_number 5
  → 5 scenes created
  → project_total_scenes = 5

User types: add scene
  → 1 more scene added
  → project_total_scenes = 6

User types: delete scene 6
  → 1 scene removed
  → project_total_scenes = 5
```

Caching this count means the status display can show the total instantly
without running a SQL `COUNT` query every time.

---

**project_total_duration**

**Type:** `float`
**Default:** `0.0`
**Example value:** `60.3`

The `project_total_duration` stores the sum of all scene durations in
seconds. It is a cached computed value updated whenever any scene's
duration changes.

```
If your project has 5 scenes with these durations:
  Scene 1: 12.5s
  Scene 2: 18.5s
  Scene 3: 16.8s
  Scene 4:  7.0s
  Scene 5:  5.5s
  ─────────────
  project_total_duration = 60.3 seconds
```

This value is critical in `supermanim` mode. The `TimelineService`
compares `project_total_duration` to `audio_total_duration`. If they
are not equal, the audio cannot be perfectly synchronized with the video.
This is the core requirement of the duration-matching rule.

---

**GROUP 5 — EXPORT SETTINGS PROPERTIES**

These properties answer the question: "When the user types `export`,
what format, quality, and filename should the final video have?"

Export settings persist between sessions because they are stored as
part of the Project Entity in the database. You set them once and they
stay until you deliberately change them.

---

**export_format**

**Type:** `str`
**Default:** `"mp4"`
**Example value:** `"mp4"`, `"webm"`, `"mov"`, `"avi"`

The `export_format` determines the container format of the final assembled
video file. The user sets this with `set export format mp4`.

```
+================================================================+
|                  THE FOUR EXPORT FORMATS                       |
+================================================================+
|                                                                |
|   "mp4"   <- THE DEFAULT                                       |
|   ─────────────────────────────────────────────────────────── |
|   The most widely supported video format in the world.         |
|   Works on Windows, macOS, Linux, Android, iOS,                |
|   all web browsers, YouTube, and every video player.           |
|   Best choice for almost every project.                        |
|   File extension: .mp4                                         |
|                                                                |
|   "webm"                                                       |
|   ─────────────────────────────────────────────────────────── |
|   An open format designed for web use.                         |
|   Good for embedding videos directly in websites.              |
|   Slightly smaller file sizes than mp4 at the same quality.    |
|   Not supported by all desktop video players.                  |
|   File extension: .webm                                        |
|                                                                |
|   "mov"                                                        |
|   ─────────────────────────────────────────────────────────── |
|   Apple QuickTime format.                                      |
|   Used in professional editing tools on macOS                  |
|   such as Final Cut Pro and Adobe Premiere.                    |
|   Larger file sizes. Use only if your workflow requires it.    |
|   File extension: .mov                                         |
|                                                                |
|   "avi"                                                        |
|   ─────────────────────────────────────────────────────────── |
|   An older Microsoft format.                                   |
|   Very large file sizes. Limited modern support.               |
|   Only use this if a specific tool specifically requires it.   |
|   File extension: .avi                                         |
|                                                                |
+================================================================+
```

---

**export_quality**

**Type:** `str`
**Default:** `"high"`
**Example value:** `"low"`, `"medium"`, `"high"`, `"ultra"`

The `export_quality` determines the video resolution and bitrate of the
final assembled video. The user sets this with `set export quality high`.

```
+================================================================+
|                  THE FOUR EXPORT QUALITY LEVELS                |
+================================================================+
|                                                                |
|   "low"     ->  480p   (854 x 480 pixels)                      |
|   ─────────────────────────────────────────────────────────── |
|   File size for a 60-second video:  approximately 40 MB        |
|   Render and export time:           fastest                    |
|   When to use:  quick sharing, internal drafts, testing only.  |
|   Not suitable for public publishing.                          |
|                                                                |
|   "medium"  ->  720p   (1280 x 720 pixels)                     |
|   ─────────────────────────────────────────────────────────── |
|   File size for a 60-second video:  approximately 90 MB        |
|   When to use:  web uploads, YouTube (acceptable quality),     |
|   general-purpose sharing and distribution.                    |
|                                                                |
|   "high"    ->  1080p  (1920 x 1080 pixels)   <- DEFAULT       |
|   ─────────────────────────────────────────────────────────── |
|   File size for a 60-second video:  approximately 214 MB       |
|   When to use:  the standard for most projects. Looks sharp    |
|   on most screens. The right choice for YouTube HD uploads     |
|   and professional educational content.                        |
|                                                                |
|   "ultra"   ->  4K     (3840 x 2160 pixels)                    |
|   ─────────────────────────────────────────────────────────── |
|   File size for a 60-second video:  approximately 850 MB       |
|   When to use:  professional publishing, large-screen          |
|   displays, archival quality. Very slow to export.             |
|                                                                |
+================================================================+
```

An important note: `export_quality` only affects the final assembly step
where FFmpeg stitches all clips together. The individual scene renders
in the `output/` folder are always produced at full resolution (controlled
by `render_resolution`). This means you can render all scenes once at
full quality and then export multiple times at different quality levels
without re-rendering a single scene.

---

**export_name**

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"IntroductionToCalculus_Episode1"`, `"FinalVersion_v3"`

The `export_name` is the custom filename the user wants for the final
exported video, without the file extension.

When `export_name` is `None`, the system uses the `project_name` followed
by `_final` as the default filename. For a project named `MyAnimation`,
the default exported file is `MyAnimation_final.mp4`.

When the user types `set export name IntroductionToCalculus_Episode1`,
the system stores that name here. The next export command produces a
file named `IntroductionToCalculus_Episode1.mp4`.

The file extension is never stored in `export_name` — the system always
adds it automatically based on `export_format`. This means if you change
the format from `mp4` to `webm`, the file name automatically becomes
`IntroductionToCalculus_Episode1.webm` without you needing to change
the name setting.

```
export_name   = "IntroductionToCalculus_Episode1"
export_format = "mp4"
Result:  exports/IntroductionToCalculus_Episode1.mp4

If format changes to "webm":
Result:  exports/IntroductionToCalculus_Episode1.webm
(name setting unchanged, extension updates automatically)
```

---

**export_output_path**

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"exports/MyAnimation_final.mp4"`

The `export_output_path` stores the full path to the final exported video
after it has been successfully assembled by FFmpeg. It is `None` until
the `export` command runs and completes without errors.

After a successful export, this field tells the system (and the user)
exactly where to find the finished video. The system uses it in the
`open output` command to navigate directly to the file.

This field is set automatically by `ProjectExportService`. You never
set it manually.

---

**GROUP 6 — RENDER SETTINGS PROPERTIES**

These properties define the visual quality and appearance defaults for
all rendered animation scenes in this project. They are the project-level
defaults. Individual Scene objects have their own corresponding fields
(`scene_resolution`, `scene_fps`, `scene_background_color`) that can
override these project defaults for specific scenes.

---

**render_resolution**

**Type:** `str`
**Default:** `"1920x1080"`
**Example value:** `"1920x1080"`, `"3840x2160"`, `"1280x720"`, `"854x480"`

The `render_resolution` is the default pixel dimensions for all rendered
scenes in this project, stored as `"widthxheight"`.

This value is passed to Manim as a command-line argument when rendering
each scene. It tells Manim how large to make each frame of the animation.

All scenes in a project should use the same resolution because when FFmpeg
assembles them into the final video, every clip must have identical
dimensions. Mixing resolutions will cause FFmpeg to fail or produce a
broken video with mismatched frames.

```
+-------------------------------------------------------------+
|   COMMON RENDER RESOLUTIONS                                 |
+-------------------------------------------------------------+
|                                                             |
|   "854x480"    ->  480p   Fast. Low quality. Testing only.  |
|   "1280x720"   ->  720p   HD. Good balance.                 |
|   "1920x1080"  ->  1080p  Full HD. DEFAULT. Best for most.  |
|   "3840x2160"  ->  4K.    Ultra HD. Very slow render.       |
|                                                             |
+-------------------------------------------------------------+
```

---

**render_fps**

**Type:** `int`
**Default:** `60`
**Example value:** `24`, `30`, `60`

The `render_fps` is the default frame rate for all rendered scenes in this
project — how many frames Manim draws per second of animation.

```
+-------------------------------------------------------------+
|   WHAT FRAME RATE MEANS FOR RENDER TIME                     |
+-------------------------------------------------------------+
|                                                             |
|   For a 16.8-second scene:                                  |
|   At 24 fps  ->  16.8 x 24  =  403 frames to draw          |
|   At 30 fps  ->  16.8 x 30  =  504 frames to draw          |
|   At 60 fps  ->  16.8 x 60  = 1008 frames to draw          |
|                                                             |
|   Higher fps = smoother motion = more frames = slower render|
|                                                             |
|   24 fps:  Cinema standard. Smooth enough for most video.   |
|   30 fps:  TV standard. Good for educational animations.    |
|   60 fps:  Very smooth. Best for fast-moving animations.    |
|                                                             |
+-------------------------------------------------------------+
```
---

**GROUP 7 — PREVIEW SETTINGS PROPERTIES**

These properties define how preview videos are generated for scenes in
this project. They are intentionally separate from and lower-quality than
the render settings because the preview system's entire purpose is speed.

---

**preview_resolution**

**Type:** `str`
**Default:** `"854x480"`

The `preview_resolution` is fixed at `"854x480"` (480p) regardless of
what `render_resolution` is set to. This is not a user-configurable setting.
It is a system constant.

The reason it is fixed: the entire purpose of the preview system is to
generate a quick, rough draft that the user can check visually in seconds
instead of minutes. Making the preview the same resolution as the final
render would completely defeat that purpose.

A 480p frame has roughly 410,000 pixels. A 1080p frame has roughly
2,070,000 pixels — five times more pixels. This means a preview renders
approximately five times faster than a full render.

---

**preview_fps**

**Type:** `int`
**Default:** `30`

The `preview_fps` is the frame rate used for preview videos. It defaults
to 30fps rather than the 60fps used for full renders. Fewer frames per
second means fewer frames to draw, which means faster generation.

A 30fps preview takes half the time of a 60fps full render, on top of
the speed savings already gained from the lower resolution. Together,
a preview can be ready in seconds where a full render takes minutes.

---

**GROUP 8 — AUDIO SETTINGS PROPERTIES**

These properties are primarily used in `supermanim` . They store the
project-level audio configuration — what audio file the user added and
what its properties are.

---

audio_format

**Type:** `str`
**Default:** `"mp3"`
**Example value:** `"mp3"`, `"wav"`, `"ogg"`, `"aac"`, `"flac"`, `"m4a"`

The `audio_format` stores the file format of the original audio file
that was added to the project. When the user runs `add audio voice.mp3`,
the system reads the `.mp3` extension and stores `"mp3"` here.

When the user runs `change audio_format wav`, the `AudioPreparationService`
converts the file using FFmpeg and updates this field to `"wav"`.
---

**audio_file_path**

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"audio_clips/original_audio.mp3"`

The `audio_file_path` stores the path to the original full-length audio
file that was copied into the project when the user ran `add audio voice.mp3`.

This is the master audio file — the complete, uncut narration or music
track. All `AudioClip` objects (the smaller pieces for individual scenes)
are derived from this file .

---

**audio_total_duration**

**Type:** `Optional[float]`
**Default:** `None`
**Example value:** `60.3`

The `audio_total_duration` stores the total length of the original audio
file in seconds. It is read automatically from the audio file when the
user runs `add audio voice.mp3` — the system uses the `AudioAnalyzerPort`
to measure the file and stores the result here.

The core synchronization rule of SuperManim is:

```
+-------------------------------------------------------------+
|   THE SYNCHRONIZATION RULE                                  |
+-------------------------------------------------------------+
|                                                             |
|   project_total_duration  ==  audio_total_duration          |
|                                                             |
|   Example (PASS):                                           |
|   project_total_duration  =  60.3 seconds                   |
|   audio_total_duration    =  60.3 seconds                   |
|   Result: MATCH. The video will sync perfectly.             |
|                                                             |
|   Example (FAIL):                                           |
|   project_total_duration  =  58.0 seconds                   |
|   audio_total_duration    =  60.3 seconds                   |
|   Result: MISMATCH. 2.3 seconds of audio will have          |
|   no matching video. WARNING is shown.                      |
|                                                             |
+-------------------------------------------------------------+
```

The `TimelineService.total_matches_audio()` domain service method
compares these two values to check this rule.

---

**GROUP 9 — STATISTICS PROPERTIES**

These properties answer the question: "Right now, how many scenes are
rendered, how many are still waiting, and is the project ready to export?"

These are all cached counters. They are updated automatically whenever
a scene's status changes, so the system can read them instantly without
running a database count query.

---

**project_rendered_scenes**

**Type:** `int`
**Default:** `0`
**Example value:** `3`

The count of scenes currently with `scene_status = "rendered"`. Updated
automatically whenever a scene render succeeds (count goes up by 1) or
whenever a rendered scene is reset to pending for any reason (count goes down).

Shown in the project info:

```
  SCENES
  ------
  Total:         5
  Rendered:      3    <- project_rendered_scenes
  Pending:       1
  Failed:        1
```

---

**project_pending_scenes**

**Type:** `int`
**Default:** `0`
**Example value:** `1`

The count of scenes currently with `scene_status = "pending"` — scenes
that have been created and configured but have never been successfully rendered.
Every newly created scene starts as pending and increments this counter.

When a pending scene is successfully rendered, this counter decreases
by 1 and `project_rendered_scenes` increases by 1.

---

**project_failed_scenes**

**Type:** `int`
**Default:** `0`
**Example value:** `1`

The count of scenes currently with `scene_status = "failed"` — scenes
where a render attempt was made but Manim returned an error. When the user
fixes the code error and successfully re-renders the scene, the count
decreases and `project_rendered_scenes` increases.

---

**project_is_export_ready**

**Type:** `bool`
**Default:** `False`

The `project_is_export_ready` flag is the single most important readiness
signal for the entire project. It is `True` only when all of the following
conditions are true at the same time:

```
project_is_export_ready = True   when:
  project_total_scenes    > 0    (the project is not empty)
  project_pending_scenes == 0    (nothing is waiting to be rendered)
  project_failed_scenes  == 0    (nothing has failed)
```

In other words: only when every single scene in the project has been
successfully rendered does this flag become `True`.

The `export` command checks this flag first. If it is `False`, the export
is refused before anything else happens, and the user is shown exactly
which scenes need fixing.

```
+================================================================+
|   project_is_export_ready — FULL LIFECYCLE                     |
+================================================================+
|                                                                |
|   PROJECT CREATED (5 scenes, none rendered):                   |
|   total=5  rendered=0  pending=5  failed=0                     |
|   project_is_export_ready = False   <- cannot export yet       |
|                                                                |
|   AFTER RENDERING SCENES 1, 2, 3:                              |
|   total=5  rendered=3  pending=2  failed=0                     |
|   project_is_export_ready = False   <- still not ready         |
|                                                                |
|   SCENE 4 RENDERS WITH AN ERROR:                               |
|   total=5  rendered=3  pending=1  failed=1                     |
|   project_is_export_ready = False   <- one scene failed        |
|                                                                |
|   USER FIXES SCENE 4 AND RE-RENDERS. SCENE 5 ALSO RENDERS:    |
|   total=5  rendered=5  pending=0  failed=0                     |
|   project_is_export_ready = True    <- ALL RENDERED. EXPORT!   |
|                                                                |
+================================================================+
```

---

**A REAL PROJECT OBJECT IN FULL**

Here is what a fully populated Project object looks like for a real
SuperManim project called `MyAnimation` — after the user has set
everything up, rendered all five scenes, and is ready to export.

```python
Project(
    # ── IDENTITY ────────────────────────────────────────────────
       project_name             = "MyAnimation",
       # ── LOCATION ────────────────────────────────────────────────
    project_folder_path      = "/home/user/projects/MyAnimation",
    project_db_path          = "/home/user/projects/MyAnimation/project_data.db",

    # ── TIMESTAMPS ──────────────────────────────────────────────
    project_created_at       = "2024-11-10 09:00:15",
   
    # ── STATE ───────────────────────────────────────────────────
       project_total_scenes     = 5,
    project_total_duration   = 60.3,

    # ── EXPORT SETTINGS ─────────────────────────────────────────
    export_format            = "mp4",
    export_quality           = "high",
    export_name              = "IntroductionToCalculus_Episode1",
    export_output_path       = None,        # not yet exported

    # ── RENDER SETTINGS ─────────────────────────────────────────
    render_resolution        = "1920x1080",
    render_fps               = 60,
   
    # ── PREVIEW SETTINGS ────────────────────────────────────────
    preview_resolution       = "854x480",
    preview_fps              = 30,

    # ── AUDIO SETTINGS ──────────────────────────────────────────
    audio_format             = "mp3",
    audio_file_path          = "audio_clips/original_audio.mp3",
    audio_total_duration     = 60.3,        # matches project_total_duration

    # ── STATISTICS ──────────────────────────────────────────────
    project_rendered_scenes  = 5,
    project_pending_scenes   = 0,
    project_failed_scenes    = 0,
    project_is_export_ready  = True,        # ready — all 5 scenes rendered
)
```

Just by reading this object you know everything about the project:
it has 5 scenes totalling 60.3 seconds,the audio file is also 60.3 seconds
so durations match, all 5 scenes are rendered, the export settings are
configured for a high-quality mp4 named `IntroductionToCalculus_Episode1.mp4`,
and it is ready to export right now with a single `export` command.

---

**HOW A PROJECT IS BORN — THE COMPLETE CREATION FLOW**

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

---


**Entity 4 — AudioFile**
=======================
=======================

**WHAT IS AN AUDIOFILE, REALLY?**

Before we look at any code or any property names, let us build a completely
clear picture of what an AudioFile actually IS inside SuperManim.

An AudioFile represents the original, complete, uncut audio recording
that the user adds to a project. When you record yourself explaining
a concept for 60 seconds and save it as `voice.mp3`, that entire recording
is the AudioFile. It is the master — the source of everything audio-related
in the project.

Think of the AudioFile like the original master tape in a recording studio.
When a musician records an album, they first make one complete master recording.
Everything else — the individual song tracks, the mixed versions, the radio edits
— comes from that master. The master itself is never modified.
In SuperManim, the AudioFile is that master tape.

```
+=====================================================================+
|                WHAT HAPPENS TO AN AUDIOFILE                         |
+=====================================================================+
|                                                                     |
|   User records voice.mp3 (60.3 seconds of narration)               |
|                                                                     |
|   User types: add audio voice.mp3                                   |
|                                                                     |
|   SuperManim copies it to the project:                              |
|   audio_clips/original_audio.mp3                                    |
|                                                                     |
|   This copy becomes the AudioFile Entity.                           |
|   The AudioFile is NEVER cut, NEVER modified directly.              |
|   It is the read-only source.                                       |
|                                                                     |
|   Later, SuperManim cuts it into AudioClips:                        |
|   audio_clips/clip_001.mp3   (12.5 seconds, for Scene 1)           |
|   audio_clips/clip_002.mp3   (18.5 seconds, for Scene 2)           |
|   audio_clips/clip_003.mp3   (16.8 seconds, for Scene 3)           |
|   audio_clips/clip_004.mp3   ( 7.0 seconds, for Scene 4)           |
|   audio_clips/clip_005.mp3   ( 5.5 seconds, for Scene 5)           |
|                                                                     |
|   The AudioFile is Entity 4.                                        |
|   The AudioClips are Entity 5.                                      |
|   They are completely separate things.                              |
|                                                                     |
+=====================================================================+
```

An AudioFile is different from an AudioClip in two key ways.
First, there is only ever ONE AudioFile per project. A project has one
master recording. But a project can have many AudioClips — one for each scene.
Second, the AudioFile is the source that AudioClips are derived from.
You never modify the AudioFile directly. You only read from it and cut pieces out of it.

---

**THE TWO THINGS AN AUDIOFILE KNOWS**

An AudioFile Entity knows two categories of things about itself.

The first category is what the file IS — its identity and location.
What is its name? Where is it stored? What format is it in?

The second category is what the file SOUNDS like — its technical properties.
How long is it in seconds? What is its sample rate? How many audio channels does it have?
What is its file size on disk?

```
+=====================================================================+
|              TWO CATEGORIES OF AUDIOFILE KNOWLEDGE                  |
+=====================================================================+
|                                                                     |
|   CATEGORY 1 — IDENTITY AND LOCATION                                |
|   What is this file? Where is it?                                   |
|                                                                     |
|   audio_file_id         The unique database ID.                     |
|                                                                     |
|   original_path         Where the user's file came from on disk.    |
|   stored_path           Where the copy lives in the project folder. |
|   original_filename     The original name (e.g. "voice.mp3")        |
|   audio_format          The file format: mp3, wav, ogg, etc.        |
|   audio_added_at        When the user ran "add audio".              |
|                                                                     |
|   CATEGORY 2 — TECHNICAL AUDIO PROPERTIES                           |
|   What does this file sound like?                                   |
|                                                                     |
|   audio_total_duration  Total length in seconds (e.g. 60.3)        |
|   audio_sample_rate     Samples per second (e.g. 44100 Hz)         |
|   audio_channels        1 = mono, 2 = stereo                        |
|   audio_bit_rate        Bits per second of audio data               |
|   audio_file_size_bytes File size on disk in bytes                  |
|   audio_is_split        Has it been cut into clips yet?             |
|   audio_clip_count      How many clips were cut from it             |
|                                                                     |
+=====================================================================+
```

---

## THE FULL PYTHON CLASS

```python
# core/entities/audio_file.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class AudioFile:
    """
    The AudioFile Entity represents the original, complete audio recording
    that the user adds to the project.

    This is a pure data container. It holds all information about the master
    audio file — its location on disk, its format, its duration, and its
    technical properties.

    There is exactly ONE AudioFile per project.
    All AudioClips (the cut pieces) are derived from this AudioFile.

    It does not play audio, does not call FFmpeg, does not open files.
    It is just structured data.
    """

    # ── IDENTITY ──────────────────────────────────────────────────────
    audio_file_id:          int
   
    # ── LOCATION ──────────────────────────────────────────────────────
    original_path:          Optional[str]   = None
    stored_path:            Optional[str]   = None
    original_filename:      Optional[str]   = None

    # ── FORMAT ────────────────────────────────────────────────────────
    audio_format:           str             = "mp3"

    # ── DURATION AND TECHNICAL PROPERTIES ─────────────────────────────
    audio_total_duration:   Optional[float] = None
    audio_sample_rate:      Optional[int]   = None
    audio_channels:         int             = 1
    audio_bit_rate:         Optional[int]   = None
    audio_file_size_bytes:  Optional[int]   = None

    # ── STATE ─────────────────────────────────────────────────────────
    audio_is_split:         bool            = False
    audio_clip_count:       int             = 0
    audio_added_at:         Optional[str]   = None

   ```

---

**EVERY PROPERTY EXPLAINED IN DEPTH**

```
+================================================================+
|         AUDIOFILE ENTITY — COMPLETE PROPERTY REFERENCE        |
+================================================================+
|                                                                |
|  GROUP 1 — IDENTITY                                            |
|  ──────────────────────────────────────────────────────────── |
|  audio_file_id        int         Required. Unique DB key.    |
|  |                                                                |
|  GROUP 2 — LOCATION                                            |
|  ──────────────────────────────────────────────────────────── |
|  original_path        str | None  Where the user's file was.  |
|  stored_path          str | None  Where the copy lives.       |
|  original_filename    str | None  The original file name.     |
|                                                                |
|  GROUP 3 — FORMAT                                              |
|  ──────────────────────────────────────────────────────────── |
|  audio_format         str         mp3/wav/ogg/aac/flac/m4a.  |
|                                   Default: "mp3".              |
|                                                                |
|  GROUP 4 — TECHNICAL PROPERTIES                                |
|  ──────────────────────────────────────────────────────────── |
|  audio_total_duration float|None  Total length in seconds.    |
|  audio_sample_rate    int | None  Hz. Usually 44100 or 48000. |
|  audio_channels       int         1=mono, 2=stereo. Def: 1.  |
|  audio_bit_rate       int | None  Bits per second.            |
|  audio_file_size_bytes int|None   File size in bytes.         |
|                                                                |
|  GROUP 5 — STATE                                               |
|  ──────────────────────────────────────────────────────────── |
|  audio_is_split       bool        Has it been cut yet?        |
|                                   Default: False.              |
|  audio_clip_count     int         How many clips were cut.    |
|                                   Default: 0.                  |
|  audio_added_at       str | None  Timestamp of "add audio".   |
|                                                                |
+================================================================+
```

---

GROUP 1 — IDENTITY PROPERTIES

---

audio_file_id

**Type:** `int`
**Default:** Required
**Example value:** `1`

The `audio_file_id` is the unique number that identifies this AudioFile
in the database. Since there is only ONE AudioFile per project, this will
almost always be `1`. The database uses this as the primary key when
storing or loading the AudioFile record.

---
GROUP 2 — LOCATION PROPERTIES

---

audio_file_original_path

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"/home/user/recordings/voice.mp3"` or `"C:/Users/Ahmed/Desktop/lecture.mp3"`

The `original_path` stores the full path to the audio file on the user's
computer BEFORE it was copied into the project. This is where the user's
file lived before SuperManim touched it.

When the user types `add audio /home/user/recordings/voice.mp3`, that
path is stored in `original_path`. This is purely for reference — so that
if the user ever needs to find their original file again, the project record
remembers where it came from.

The original file is never modified. SuperManim makes a copy of it.

---

audio_file_stored_path

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"audio_clips/original_audio.mp3"`

The `stored_path` is the path to the copy of the audio file that SuperManim
made inside the project's `audio_clips/` folder. This is the file the
system actually reads and works with.

When you type `add audio voice.mp3`, SuperManim:
1. Reads the file from `original_path`
2. Makes a copy in the project's `audio_clips/` folder
3. Names the copy `original_audio.mp3` (keeping the original extension)
4. Stores the new location in `stored_path`

From that moment on, all operations — format conversion, silence detection,
splitting into clips — are done on the file at `stored_path`. The original
at `original_path` is never touched again.

```
What the terminal shows when you run "add audio":

  Audio file added successfully.
  Copied to:   audio_clips/original_audio.mp3    <- this is stored_path
  Format:      mp3
  Duration:    60.3 seconds
```

---

audio_file_original_filename

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"voice.mp3"`, `"lecture_recording.wav"`

The `original_filename` stores just the filename part (not the full path)
of the user's original audio file. If the user added `/home/user/recordings/voice.mp3`,
then `original_filename = "voice.mp3"`.

This is stored for display purposes — so the user interface can say
"Original file: voice.mp3" in the audio info display without showing
the entire long path.

---

GROUP 3 — FORMAT PROPERTIES

---

audio_file_format

**Type:** `str`
**Default:** `"mp3"`
**Example value:** `"mp3"`, `"wav"`, `"ogg"`, `"aac"`, `"flac"`, `"m4a"`

The `audio_format` stores the file format of the audio file. When the
user first adds an audio file, the format is read from the file extension.
If the user adds `voice.mp3`, the format is `"mp3"`.

When the user runs `change audio_format wav`, the `AudioPreparationService`
converts the file using FFmpeg and updates this field to `"wav"`.

```
+-------------------------------------------------------------+
|   THE SIX SUPPORTED AUDIO FORMATS                           |
+-------------------------------------------------------------+
|                                                             |
|   "mp3"   Most common. Lossy compression.                   |
|            Small files. Slight quality loss at low bitrates.|
|            Good for voice recordings.                       |
|                                                             |
|   "wav"   Lossless. No compression. Maximum quality.        |
|            Files are large (about 10x larger than mp3).     |
|            Best if you want to preserve every detail.       |
|                                                             |
|   "ogg"   Open format. Good lossy compression.              |
|            Better quality than mp3 at the same file size.  |
|            Good web and gaming standard.                    |
|                                                             |
|   "aac"   Apple format. Lossy compression.                  |
|            Better quality than mp3 at the same bitrate.    |
|            Default on iPhone and iTunes.                    |
|                                                             |
|   "flac"  Lossless compression. Smaller than wav.           |
|            Perfect quality with smaller files than wav.     |
|            Best of both: quality + size.                    |
|                                                             |
|   "m4a"   Apple container format. Usually contains AAC.     |
|            Used by iTunes, Apple Music, and iOS.            |
|                                                             |
+-------------------------------------------------------------+
```

---

GROUP 4 — TECHNICAL PROPERTIES

These properties are read automatically from the audio file when
the user runs `add audio`. The user never sets them manually.
They are measured and stored by the `AudioAnalyzerPort` (which uses
the librosa library internally).

---

**audio_file_total_duration**

**Type:** `Optional[float]`
**Default:** `None`
**Example value:** `60.3`

The `audio_total_duration` stores the total length of the audio file
in seconds. This is the most important technical property.

When you type `add audio voice.mp3`, SuperManim immediately measures
the duration and stores it here. Everything that comes after — setting
scene durations, splitting into clips, checking sync — depends on this value.

In supermanim mode, the sum of all scene durations must equal `audio_total_duration`
exactly. If they do not match, the audio cannot be synchronized perfectly
with the video. The `TimelineService` compares these values constantly.

```
audio_total_duration = 60.3 seconds

This becomes the target for all scene durations:
  Scene 1: 12.5s
  Scene 2: 18.5s
  Scene 3: 16.8s
  Scene 4:  7.0s
  Scene 5:  5.5s
  ─────────────
  Total:   60.3s   <- must equal audio_total_duration
```

---

**audio_sample_rate**

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `44100`, `48000`, `22050`

The `audio_sample_rate` is how many times per second the audio is measured
(sampled) when it is recorded. It is measured in Hertz (Hz).

A sample rate of 44100 Hz means the audio was measured 44,100 times every
single second. Higher sample rates capture more detail in the sound.

```
+-------------------------------------------------------------+
|   COMMON SAMPLE RATES                                       |
+-------------------------------------------------------------+
|                                                             |
|   22050 Hz   Low quality. Old telephone standard.           |
|   44100 Hz   CD quality. Standard for most music and voice. |
|   48000 Hz   Professional/broadcast standard.               |
|              Used in film, TV, and professional recordings. |
|   96000 Hz   High-resolution audio. Studio use only.        |
|                                                             |
|   For voice recordings (narration): 44100 Hz is perfect.   |
|   For professional productions: 48000 Hz is recommended.   |
|                                                             |
+-------------------------------------------------------------+
```

SuperManim stores this information for reference. FFmpeg uses it
when converting the format or when mixing audio into the final video.

---

**audio_channels**

**Type:** `int`
**Default:** `1` (mono)
**Example value:** `1`, `2`

The `audio_channels` field stores how many independent audio streams
the file contains.

```
+-------------------------------------------------------------+
|   MONO vs STEREO                                            |
+-------------------------------------------------------------+
|                                                             |
|   1 = MONO                                                  |
|   One single audio stream.                                  |
|   Plays the same sound in both the left and right speaker.  |
|   Voice recordings and narration are almost always mono.   |
|   Smaller file size than stereo.                            |
|                                                             |
|   2 = STEREO                                                |
|   Two separate audio streams (left and right).              |
|   Different sound can come from each speaker.               |
|   Music is usually stereo.                                  |
|   Larger file size than mono.                               |
|                                                             |
|   For SuperManim narration: mono is the right choice.       |
|   One person speaking does not need a left and right track. |
|                                                             |
+-------------------------------------------------------------+
```

---

**audio_bit_rate**

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `128000`, `192000`, `320000`

The `audio_bit_rate` is how many bits of audio data are used per second
of sound. It is measured in bits per second (bps). Higher bit rates
mean better audio quality but larger file sizes.

Common MP3 bit rates: 128 kbps (128,000 bps) is basic quality,
192 kbps is good quality, 320 kbps is the highest MP3 quality.

For voice narration, 128 kbps is usually sufficient because the human
voice does not require the same detail as music.

---

**audio_file_size_bytes**

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `4404019` (approximately 4.2 MB)

The `audio_file_size_bytes` stores the size of the stored audio file
in bytes. This is useful for:
- Showing the user how much disk space the audio is using
- Comparing file sizes before and after format conversion
- Estimating how much space the project will need

The terminal shows a human-readable version of this when you change format:

```
supermanim> change audio_format wav

  Converting: original_audio.mp3  -->  original_audio.wav
  Old size:   4.2 MB     <- audio_file_size_bytes before
  New size:   31.8 MB    <- audio_file_size_bytes after
```

---

**GROUP 5 — STATE PROPERTIES**

---

**audio_is_split**

**Type:** `bool`
**Default:** `False`

The `audio_is_split` flag tracks whether the AudioFile has been cut
into AudioClip pieces yet. It starts as `False` when the audio is
first added. It becomes `True` after any split command runs successfully
(`split audio auto`, `split audio half`, or `split audio duration`).

This flag is useful for validation. Before splitting, the system can check
if the audio has already been split. If `audio_is_split = True` and the
user tries to split again, the system can warn them that cutting again
will replace all existing clips and break any existing sync links.

```
+-------------------------------------------------------------+
|   audio_is_split — THE LIFECYCLE                            |
+-------------------------------------------------------------+
|                                                             |
|   add audio voice.mp3                                       |
|   -> audio_is_split = False                                 |
|      audio_clip_count = 0                                   |
|                                                             |
|   split audio auto   (finds 5 segments)                     |
|   -> audio_is_split = True                                  |
|      audio_clip_count = 5                                   |
|                                                             |
|   split audio duration 12.5 18.5 16.8   (re-split)         |
|   -> audio_is_split = True   (still True)                   |
|      audio_clip_count = 3   (updated to new count)          |
|                                                             |
+-------------------------------------------------------------+
```

---

**audio_clip_count**

**Type:** `int`
**Default:** `0`

The `audio_clip_count` stores how many AudioClip pieces were cut from
this AudioFile the last time a split command ran. It starts at 0 and
is updated every time the audio is split.

This number is shown in the audio info display and in the project status
output so the user can quickly see how many clips were generated.

---

**audio_added_at**

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"2024-11-10 09:05:30"`

The `audio_added_at` timestamp records the exact date and time when the
user ran `add audio` and the file was copied into the project.
It is set once using `datetime.now()` and never changed again.

---

**A REAL AUDIOFILE OBJECT IN FULL**

```python
AudioFile(
    # ── IDENTITY ────────────────────────────────────────────────
    audio_file_id          = 1,
   
    # ── LOCATION ────────────────────────────────────────────────
    original_path          = "/home/user/recordings/voice.mp3",
    stored_path            = "audio_clips/original_audio.mp3",
    original_filename      = "voice.mp3",

    # ── FORMAT ──────────────────────────────────────────────────
    audio_format           = "mp3",

    # ── TECHNICAL PROPERTIES ────────────────────────────────────
    audio_total_duration   = 60.3,
    audio_sample_rate      = 44100,
    audio_channels         = 1,              # mono voice recording
    audio_bit_rate         = 192000,         # 192 kbps
    audio_file_size_bytes  = 4404019,        # about 4.2 MB

    # ── STATE ───────────────────────────────────────────────────
    audio_is_split         = True,           # has been cut into clips
    audio_clip_count       = 5,              # 5 clips were generated
    audio_added_at         = "2024-11-10 09:05:30",
)
```

---

---

**Entity 5 — AudioClip**
=======================
=======================


**WHAT IS AN AUDIOCLIP, REALLY?**

An AudioClip represents one piece of audio. It is always derived from an
AudioFile — it is one cut section of the master recording.

Think of the AudioFile as a long roll of film. The AudioClips are the
individual frames you cut out of that roll. Each cut piece is an AudioClip.
The roll itself is the AudioFile and it never changes.

There are two completely different situations when an AudioClip Entity exists:

```
+=====================================================================+
|             THE TWO KINDS OF AUDIOCLIP                             |
+=====================================================================+
|                                                                     |
|   KIND 1 — SCENE CLIP                                               |
|   ─────────────────────────────────────────────────────────────    |
|   A piece of audio that was cut from the master AudioFile           |
|   to match one specific scene.                                      |
|                                                                     |
|   Example:                                                          |
|   clip_001.mp3 — the first 12.5 seconds of voice.mp3               |
|   This clip belongs to Scene 1.                                     |
|   It plays while Scene 1's animation is on screen.                  |
|   It is exactly 12.5 seconds long — same as Scene 1's duration.    |
|                                                                     |
|   clip_002.mp3 — seconds 12.5 to 31.0 of voice.mp3                |
|   This clip belongs to Scene 2.                                     |
|   It is exactly 18.5 seconds long — same as Scene 2's duration.    |
|                                                                     |
|   KIND 2 — STANDALONE EDITED CLIP                  |
|   ─────────────────────────────────────────────────────────────    |
|   In "normal" mode, the user edits audio files without animation.   |
|   An AudioClip here is any piece of audio the user creates by       |
|   cutting, splitting, or converting the original audio file.        |
|   It does not necessarily link to any Scene.                        |
|                                                                     |
+=====================================================================+
```

The most important kind — the one that powers supermanim mode — is Kind 1.
This is the clip that gets attached to a Scene and synchronized with it,
so that when the scene is rendered, the audio and animation play together
at exactly the right time.

---

**THE RELATIONSHIP BETWEEN AUDIOFILE AND AUDIOCLIP**

```
+=====================================================================+
|              AUDIOFILE  ->  AUDIOCLIPS  ->  SCENES                  |
+=====================================================================+
|                                                                     |
|   AudioFile (audio_file_id=1)                                       |
|   original_audio.mp3                                                |
|   Total duration: 60.3 seconds                                      |
|   |                                                                 |
|   | split audio duration 12.5 18.5 16.8 7.0 5.5                    |
|   |                                                                 |
|   +-- AudioClip (clip_id=1, clip_index=1)                           |
|   |   clip_001.mp3   (0.0s to 12.5s)   duration: 12.5s             |
|   |   linked to Scene 1 (scene_id=1)                                |
|   |                                                                 |
|   +-- AudioClip (clip_id=2, clip_index=2)                           |
|   |   clip_002.mp3   (12.5s to 31.0s)  duration: 18.5s             |
|   |   linked to Scene 2 (scene_id=2)                                |
|   |                                                                 |
|   +-- AudioClip (clip_id=3, clip_index=3)                           |
|   |   clip_003.mp3   (31.0s to 47.8s)  duration: 16.8s             |
|   |   linked to Scene 3 (scene_id=3)                                |
|   |                                                                 |
|   +-- AudioClip (clip_id=4, clip_index=4)                           |
|   |   clip_004.mp3   (47.8s to 54.8s)  duration:  7.0s             |
|   |   linked to Scene 4 (scene_id=4)                                |
|   |                                                                 |
|   +-- AudioClip (clip_id=5, clip_index=5)                           |
|       clip_005.mp3   (54.8s to 60.3s)  duration:  5.5s             |
|       linked to Scene 5 (scene_id=5)                                |
|                                                                     |
+=====================================================================+
```

Each AudioClip knows three time-related things:
- Its own duration (how long it is)
- Where it started in the original AudioFile (`audio_clip_start_time`)
- Where it ended in the original AudioFile (`audio_clip_end_time`)

These three values together mean you can always reconstruct exactly which
part of the master recording this clip came from.

---

**THE FULL PYTHON CLASS**

```python
# core/entities/audio_clip.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class AudioClip:
    """
    The AudioClip Entity represents one piece of audio — a cut section
    of the master AudioFile that belongs to one specific scene.

    This is a pure data container. It holds all information about one
    audio clip: where it lives on disk, how long it is, which part of
    the original audio it came from, and which scene it belongs to.

    It does NOT play audio, does NOT call FFmpeg.
    It is just structured data.
    """

    # ── IDENTITY ──────────────────────────────────────────────────────
    audio_clip_id:                    int
    audio_file_id:              int

    # ── ORDERING AND LINKING ──────────────────────────────────────────
    audio_clip_index:                 Optional[int]   = None
    scene_id:                   Optional[int]   = None

    # ── LOCATION ──────────────────────────────────────────────────────
    audio_clip_path:                  Optional[str]   = None

    # ── FORMAT ────────────────────────────────────────────────────────
    audio_clip_format:                str             = "mp3"

    # ── TIMING — OWN DURATION ─────────────────────────────────────────
    audio_clip_duration:              Optional[float] = None

    # ── TIMING — POSITION IN THE ORIGINAL AUDIOFILE ───────────────────
    audio_clip_start_time:     Optional[float] = None
    audio_clip_end_time  :     Optional[float] = None

    # ── TECHNICAL PROPERTIES ──────────────────────────────────────────
    audio_clip_sample_rate:           Optional[int]   = None
    audio_clip_channels:              int             = 1
    audio_clip_file_size_bytes:       Optional[int]   = None

    # ── STATE ─────────────────────────────────────────────────────────
    audio_clip_is_synced:             bool            = False
    audio_clip_created_at:            Optional[str]   = None
```

---

**EVERY PROPERTY EXPLAINED IN DEPTH**

```
+================================================================+
|         AUDIOCLIP ENTITY — COMPLETE PROPERTY REFERENCE        |
+================================================================+
|                                                                |
|  GROUP 1 — IDENTITY                                            |
|  ──────────────────────────────────────────────────────────── |
|  clip_id              int         Required. Unique DB key.    |
|  project_id           int         Required. Owner project.    |
|  audio_file_id        int         Required. Source AudioFile. |
|                                                                |
|  GROUP 2 — ORDERING AND LINKING                                |
|  ──────────────────────────────────────────────────────────── |
|  clip_index           int | None  Position in clip sequence.  |
|                                   1=first, 2=second, etc.     |
|  scene_id             int | None  Which scene owns this clip. |
|                                   None = not assigned yet.    |
|                                                                |
|  GROUP 3 — LOCATION                                            |
|  ──────────────────────────────────────────────────────────── |
|  clip_path            str | None  Path to clip file on disk.  |
|                                                                |
|  GROUP 4 — FORMAT                                              |
|  ──────────────────────────────────────────────────────────── |
|  clip_format          str         mp3/wav/ogg/aac. Def "mp3". |
|                                                                |
|  GROUP 5 — TIMING                                              |
|  ──────────────────────────────────────────────────────────── |
|  clip_duration           float|None Own length in seconds.    |
|  clip_start_in_original  float|None Start second in master.   |
|  clip_end_in_original    float|None End second in master.     |
|                                                                |
|  GROUP 6 — TECHNICAL PROPERTIES                                |
|  ──────────────────────────────────────────────────────────── |
|  clip_sample_rate     int | None  Hz. Usually 44100 or 48000. |
|  clip_channels        int         1=mono, 2=stereo. Def: 1.  |
|  clip_file_size_bytes int | None  File size in bytes.         |
|                                                                |
|  GROUP 7 — STATE                                               |
|  ──────────────────────────────────────────────────────────── |
|  clip_is_synced       bool        True if Scene is synced.    |
|                                   Default: False.              |
|  clip_created_at      str | None  When clip was cut.          |
|                                                                |
+================================================================+
```

---

GROUP 1 — IDENTITY PROPERTIES

---

audio_clip_id

**Type:** `int`
**Default:** Required
**Example value:** `3`

The `clip_id` is the unique number that identifies this AudioClip in the
database. For a project with 5 clips, the IDs are 1, 2, 3, 4, and 5.

---
audio_file_id

**Type:** `int`
**Default:** Required
**Example value:** `1`

Links this AudioClip back to the specific AudioFile it was cut from.
This is the foreign key relationship: the clip knows which master file
it came from. If you ever need to re-cut the clips from the original
(for example, if the split was wrong), the system can find the master
by reading `audio_file_id`.

---

GROUP 2 — ORDERING AND LINKING PROPERTIES

---

audio_clip_index

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `1`, `2`, `3`, `4`, `5`

The `clip_index` is the position number of this clip in the sequence of
all clips generated from the AudioFile. The first clip has index 1, the
second has index 2, and so on.

This is used to name the clip files on disk. Clip 1 becomes `clip_001.mp3`,
clip 2 becomes `clip_002.mp3`, and so on. The naming is always zero-padded
to three digits so that clips sort alphabetically in the correct order in
the file explorer.

```
clip_index = 1  ->  filename: clip_001.mp3
clip_index = 2  ->  filename: clip_002.mp3
clip_index = 3  ->  filename: clip_003.mp3
...
clip_index = 10 ->  filename: clip_010.mp3
```

`clip_index` is `None` only in "normal" mode when a clip is created
as a standalone edited piece that does not belong to a numbered sequence.

---

**scene_id**

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `3`

The `scene_id` stores which Scene this AudioClip belongs to. When the
clip has been linked to a scene, this field holds the `scene_id` of
that scene.

When `scene_id` is `None`, this clip has not been linked to any scene
yet. When the user runs `sync scene 3 audio_clip 3`, the `AudioPreparationService`
sets `scene_id = 3` on AudioClip 3 and also sets `synced_with_audio = True`
on Scene 3. Both sides of the link are updated at the same time.

```
Before sync:
  AudioClip 3: scene_id = None, clip_is_synced = False
  Scene 3: synced_with_audio = False, audio_clip_path = None

After "sync scene 3 audio_clip 3":
  AudioClip 3: scene_id = 3,    clip_is_synced = True
  Scene 3: synced_with_audio = True, audio_clip_path = "audio_clips/clip_003.mp3"
```

---

**GROUP 3 — LOCATION PROPERTIES**

---

**audio_clip_path**

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"audio_clips/clip_003.mp3"`

The `clip_path` is the file path where this AudioClip's audio file is
stored on disk inside the project folder. It is set automatically when
the clip is created by the split command.

The render system reads this path when it needs to include audio in a
rendered video. FFmpeg receives this path as the audio input when baking
audio into the scene's video file.

---

**GROUP 4 — FORMAT PROPERTIES**

---

**audio_clip_format**

**Type:** `str`
**Default:** `"mp3"`
**Example value:** `"mp3"`, `"wav"`, `"ogg"`

The format of this specific clip file. AudioClips inherit the format
of the AudioFile they were cut from. If the master AudioFile is in
`"mp3"` format, all the clips cut from it will also be `"mp3"`.

If the user runs `change audio_format wav` before splitting, the new
clips will be in `"wav"` format. If they run the format change after
splitting, the system also converts all the existing clips.

---

**GROUP 5 — TIMING PROPERTIES**

This is the most important group for understanding what an AudioClip IS.
The three timing properties together tell the complete story of this clip:
how long it is, where it started in the original audio, and where it ended.

---

**clip_duration**

**Type:** `Optional[float]`
**Default:** `None`
**Example value:** `16.8`

The `clip_duration` is the length of this specific AudioClip in seconds.
This is the most critical value for synchronization because it must
exactly equal the duration of the Scene it is linked to.

```
The Duration Matching Rule:

audio_clip_duration  ==  scene_duration

AudioClip 3: audio_clip_duration = 16.8 seconds
Scene 3:     scene_duration = 16.8 seconds
Match: YES  ->  can sync.

AudioClip 4: audio_clip_duration = 9.3 seconds
Scene 4:     scene_duration = 7.0 seconds
Difference:  2.3 seconds  ->  CANNOT sync. Will be refused.
```

This is the value that `ValidationService.sync_is_valid()` compares
against the scene's `scene_duration` when the user runs `sync scene`.

---

**audio_clip_start_time**
**Type:** `Optional[float]`
**Default:** `None`
**Example value:** `31.0`

The `clip_start_in_original` stores the exact second in the MASTER
AudioFile where this clip begins. This is a reference to the original,
not a property of the clip itself.

For AudioClip 3 (which covers the third section of the narration),
`clip_start_in_original = 31.0` means: "This clip is the section of the
original audio that starts at the 31.0-second mark."

This value is essential for:
- Showing the user the audio timeline in `show audio info`
- Re-cutting the clips if needed (the system knows exactly where to cut)
- Debugging timing problems

---
Here’s the corrected and consistent version with all references renamed to `audio_clip_start_time`:

---

**audio_clip_end_time**
**Type:** `Optional[float]`
**Default:** `None`
**Example value:** `47.8`

The `audio_clip_end_time` stores the exact second in the MASTER AudioFile
where this clip ends.

Together with `audio_clip_start_time`, this tells you exactly which
portion of the master recording this clip represents:

```
AudioClip 3:
  audio_clip_start_time = 31.0
  audio_clip_end_time   = 47.8
  clip_duration         = 16.8  (= 47.8 - 31.0)

  This clip is the section from second 31.0 to second 47.8
  of the original voice.mp3 recording.
```

The terminal shows this information in the `show audio info` command:

```
SCENE AUDIO MAP
+---------+-----------+-----------+-----------+-----------------+
| Scene   | Start     | End       | Duration  | Clip File       |
+---------+-----------+-----------+-----------+-----------------+
|   3     |  31.0s    |  47.8s    |  16.8s    | clip_003.mp3    |
+---------+-----------+-----------+-----------+-----------------+
```

Those Start and End columns come directly from `audio_clip_start_time`
and `audio_clip_end_time`.

---


**GROUP 6 — TECHNICAL PROPERTIES**

These properties mirror the same fields in the AudioFile Entity but
apply to this specific clip file rather than the master.

---
Here is the same content with only the `clip_` prefix changed to `audio_`:

---
Got it — using `audio_clip_` and keeping the `**    **` style exactly:

---

**audio_clip_sample_rate**

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `44100`

The sample rate of this clip's audio file in Hz. AudioClips inherit
the sample rate of the AudioFile they were cut from. FFmpeg preserves
the sample rate when it cuts a section of audio.

---

 **audio_clip_channels**

**Type:** `int`
**Default:** `1`
**Example value:** `1`, `2`

The number of audio channels in this clip. Same as in AudioFile —
1 means mono, 2 means stereo. Voice narration clips are typically mono.

---

 **audio_clip_file_size_bytes**

**Type:** `Optional[int]`
**Default:** `None`
**Example value:** `880804` (approximately 0.84 MB for a 12.5-second mp3 clip)

The size of this clip file on disk in bytes. Proportional to the clip's
duration and the format's compression level.

---

---

**GROUP 7 — STATE PROPERTIES**

 **audio_clip_is_synced**

**Type:** `bool`
**Default:** `False`

The `audio_clip_is_synced` flag mirrors the `synced_with_audio` flag on the
Scene. It is `True` when this clip has been successfully linked to a Scene
through the `sync scene` command and the duration check has passed.

When `audio_clip_is_synced = True`, this clip will be baked into the video when
the linked scene is rendered. When `audio_clip_is_synced = False`, the clip exists
on disk but is not currently active in any render workflow.

---

 **audio_clip_created_at**

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"2024-11-10 09:10:45"`

The timestamp when this clip file was created — when the split command
ran and FFmpeg cut this specific section from the master AudioFile.

---

---

**A REAL AUDIOCLIP OBJECT IN FULL**

```
AudioClip(
    # ── IDENTITY ────────────────────────────────────────────────
    audio_clip_id                  = 3,
    audio_file_id                  = 1,        # comes from AudioFile 1

    # ── ORDERING AND LINKING ────────────────────────────────────
    audio_clip_index               = 3,        # third clip in the sequence
    scene_id                       = 3,        # linked to Scene 3

    # ── LOCATION ────────────────────────────────────────────────
    audio_clip_path                = "audio_clips/clip_003.mp3",

    # ── FORMAT ──────────────────────────────────────────────────
    audio_clip_format              = "mp3",

    # ── TIMING ──────────────────────────────────────────────────
    audio_clip_duration            = 16.8,
    audio_clip_start_time          = 31.0,    # starts at second 31.0 of voice.mp3
    audio_clip_end_time            = 47.8,    # ends at second 47.8 of voice.mp3

    # ── TECHNICAL PROPERTIES ────────────────────────────────────
    audio_clip_sample_rate         = 44100,
    audio_clip_channels            = 1,       # mono
    audio_clip_file_size_bytes     = 1410048, # about 1.3 MB

    # ── STATE ───────────────────────────────────────────────────
    audio_clip_is_synced           = True,    # linked and duration verified
    audio_clip_created_at          = "2024-11-10 09:10:45",
)
```


**Entity 6 — ProjectSettings**
===============================
===============================

**WHAT IS PROJECTSETTINGS, REALLY?**

ProjectSettings is a data container that holds all the configurable
preferences for one specific project. These are the settings that
control how the project behaves — what export format it uses, what quality
it renders at, what background color scenes use, and so on.

You might ask: why is this separate from the Project Entity? Why not
put all settings directly on the Project?

The reason is the read-only rule. When a project is created, some information
is locked forever — the project's name,  its creation timestamp,
and its folder location. These never change. But the settings — export format,
quality, resolution — change frequently as the user adjusts them.

By separating settings into their own Entity, we make this distinction
explicit and clear in the code. The Project Entity holds identity and
state. The ProjectSettings Entity holds preferences. They are different
kinds of data and they deserve to be in different places.

```
+=====================================================================+
|         WHY PROJECTSETTINGS IS SEPARATE FROM PROJECT                |
+=====================================================================+
|                                                                     |
|   Project Entity holds:                                             |
|   - Identity ( project_name,)              |
|   - Location (folder_path, db_path)                                 |
|   - Timestamps (created_at, updated_at)                             |
|   - Statistics (total_scenes, rendered_count, etc.)                 |
|                                                                     |
|   These are FACTS. They describe what the project IS.               |
|   project_name never changes. Mode never changes.                   |
|   created_at is locked the moment the project is born.              |
|                                                                     |
|   ProjectSettings Entity holds:                                     |
|   - Export preferences (format, quality, output name)               |
|   - Render preferences (resolution, fps, background color)          |
|   - Preview preferences (resolution, fps)                           |
|   - Audio preferences (default format)                              |
|                                                                     |
|   These are CHOICES. They describe how the project BEHAVES.         |
|   The user changes export_format from mp4 to webm.                  |
|   The user changes export_quality from high to ultra.               |
|   The user changes render_fps from 60 to 30.                        |
|   All of these are frequent, normal changes.                        |
|                                                                     |
+=====================================================================+
```

---

**WHERE PROJECTSETTINGS LIVES**

ProjectSettings is stored as a table called `project_settings` inside
the project's `project_data.db` file. It is not a separate file.

```
/projects/MyAnimation/
└── project_data.db
    ├── table: scenes
    ├── table: audio_clips
    └── table: project_settings   <- ProjectSettings lives here
```

There is exactly ONE row in the `project_settings` table per project.
When the project is created, that one row is written with all the default
values. After that, only the mutable columns are ever updated.

---

**THE LOCKED FIELDS vs THE MUTABLE FIELDS**

This is the most important concept about ProjectSettings.
Some fields are written ONCE at creation and NEVER changed again.
Other fields are changed by the user through commands.

```
+=====================================================================+
|           LOCKED FIELDS vs MUTABLE FIELDS                           |
+=====================================================================+
|                                                                     |
|   LOCKED AT CREATION (written once, never changed):                 |
|   ─────────────────────────────────────────────────────────────    |
|   project_name          The name given at creation.                 |
|   project_folder_path   Where the project lives on disk.            |
|   project_db_path       Path to this database file.                 |
|   settings_created_at   Timestamp of when the project was created.  |
|                                                                     |
|   If you try to change these through any command or any port,       |
|   the system refuses. The adapter has no method to change them.     |
|                                                                     |
|   MUTABLE — CHANGE AS NEEDED:                                       |
|   ─────────────────────────────────────────────────────────────    |
|   export_format         "set export format webm"                    |
|   export_quality        "set export quality ultra"                  |
|   export_name           "set export name MyVideo_v2"               |
|   render_resolution     (changed through settings commands)         |
|   render_fps            (changed through settings commands)         |
|   render_background_color (changed through settings commands)       |
|   preview_resolution    (internal — always 854x480)                 |
|   preview_fps           (internal — default 30)                     |
|   audio_default_format  (changed through settings commands)         |
|   settings_updated_at   (auto-updated whenever any field changes)   |
|                                                                     |
+=====================================================================+
```

---

**THE FULL PYTHON CLASS**

```python
# core/entities/project_settings.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class ProjectSettings:
    """
    The ProjectSettings Entity holds all configurable preferences for
    one specific project.

    It is stored as a table inside project_data.db.
    There is exactly ONE row per project.

    LOCKED FIELDS are written at project creation and never changed.
    MUTABLE FIELDS are changed by the user through settings commands.

    Only ProjectLifecycleService is allowed to update the mutable fields.
    The locked fields have no update method — they cannot be changed.

    This is a pure data container. It holds structured preferences.
    It does not call Manim, FFmpeg, or SQLite.
    """
    # ── LOCKED FIELDS (written once at creation, never changed) ───────
    project_name:               str                 = ""
    project_folder_path:        Optional[str]       = None
    project_db_path:            Optional[str]       = None
    
    # ── MUTABLE — EXPORT SETTINGS ─────────────────────────────────────
    export_format:              str                 = "mp4"
    export_quality:             str                 = "high"
    export_name:                Optional[str]       = None

    # ── MUTABLE — RENDER SETTINGS ─────────────────────────────────────
    render_resolution:          str                 = "1920x1080"
    render_fps:                 int                 = 60
    render_background_color:    str                 = "#000000"

    # ── MUTABLE — PREVIEW SETTINGS ────────────────────────────────────
    preview_resolution:         str                 = "854x480"
    preview_fps:                int                 = 30

    # ── MUTABLE — AUDIO SETTINGS ──────────────────────────────────────
    audio_format:               str                 = "mp3"
```

---

## EVERY PROPERTY EXPLAINED IN DEPTH

```
+================================================================+
|      PROJECTSETTINGS ENTITY — COMPLETE PROPERTY REFERENCE     |
+================================================================+
|                                                                |
|  GROUP 1 — IDENTITY                                            |
|  ──────────────────────────────────────────────────────────── |
|  settings_id          int         Required. Unique DB key.    |
|  project_id           int         Required. Owner project.    |
|                                                                |
|  GROUP 2 — LOCKED FIELDS (written once, never changed)         |
|  ──────────────────────────────────────────────────────────── |
|  project_name         str         The project's name.         |
|  project_mode         str         normal/simplemanim/super.   |
|  project_folder_path  str | None  Root folder on disk.        |
|  project_db_path      str | None  Database file path.         |
|  settings_created_at  str | None  Creation timestamp.         |
|                                                                |
|  GROUP 3 — MUTABLE EXPORT SETTINGS                             |
|  ──────────────────────────────────────────────────────────── |
|  export_format        str         mp4/webm/mov/avi. Def: mp4. |
|  export_quality       str         low/medium/high/ultra.      |
|                                   Default: "high".             |
|  export_name          str | None  Custom output filename.     |
|                                   Default: None (uses project  |
|                                   name + "_final").            |
|                                                                |
|  GROUP 4 — MUTABLE RENDER SETTINGS                             |
|  ──────────────────────────────────────────────────────────── |
|  render_resolution    str         Default: "1920x1080".        |
|  render_fps           int         Default: 60.                 |
|  render_background_color str      Hex. Default: "#000000".    |
|                                                                |
|  GROUP 5 — MUTABLE PREVIEW SETTINGS                            |
|  ──────────────────────────────────────────────────────────── |
|  preview_resolution   str         Always "854x480".           |
|  preview_fps          int         Default: 30.                 |
|                                                                |
|  GROUP 6 — MUTABLE AUDIO SETTINGS                              |
|  ──────────────────────────────────────────────────────────── |
|  audio_default_format str         Default: "mp3".              |
|                                                                |
|  GROUP 7 — AUTO-UPDATED                                        |
|  ──────────────────────────────────────────────────────────── |
|  settings_updated_at  str | None  Set by system on any change.|
|                                                                |
+================================================================+
```

GROUP 2 — LOCKED FIELDS

These fields are written exactly once — when the project is created —
and can never be changed through any command, any service, or any port.
The `SqliteProjectSettingsRepository` adapter literally has no method
to update these columns. They are read-only from the moment of creation.

---

project_name

**Type:** `str`
**Default:** `""` (empty, but always set at creation)
**Example value:** `"MyAnimation"`

A copy of the project's name, stored in the settings table for fast
access. Having it here means a service can read all project configuration
from one place without needing to join the projects table.

This is a copy — the authoritative source is the Project Entity. If
these ever differ (which they should not), the Project Entity's value
is the truth.

---

project_folder_path

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"/home/user/projects/MyAnimation"`

The full path to the project's root folder. Locked because if the project
folder moves, the project must be re-opened pointing at the new location
rather than updated in the database.

---

project_db_path

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"/home/user/projects/MyAnimation/project_data.db"`

The full path to this very database file. Stored here so that any
service reading the settings knows exactly where the database lives
without having to construct the path from parts.

GROUP 3 — MUTABLE EXPORT SETTINGS

These are the settings the user changes most often. They control
what the final exported video looks like.

---

export_format

**Type:** `str`
**Default:** `"mp4"`

The file format of the final exported video. Changed with:
`set export format webm`

```
What happens in the system when the user types "set export format webm":

  1. Shell receives: do_set("export format webm")
  2. ProjectLifecycleService.set_export_format("webm") is called.
  3. ValidationService.export_format_is_supported("webm") -> True
  4. ProjectSettingsRepositoryPort.update_export_format(project_id, "webm")
  5. SqliteProjectSettingsRepository writes to the database:
     UPDATE project_settings SET export_format='webm',
     settings_updated_at='2024-11-12 14:30:55'
     WHERE project_id=1
  6. The in-memory ProjectSettings object is updated.
  7. User sees: "Export format updated. Format: webm"
```

Supported values: `"mp4"`, `"webm"`, `"mov"`, `"avi"`.
Any other value is refused by the `ValidationService` before it reaches
the repository.

---

export_quality

**Type:** `str`
**Default:** `"high"`

The quality level of the final exported video. Changed with:
`set export quality ultra`

```
+-------------------------------------------------------------+
|   EXPORT QUALITY LEVELS AND THEIR MEANINGS                  |
+-------------------------------------------------------------+
|                                                             |
|   "low"    ->  480p   (854x480)    ~40 MB per 60 seconds   |
|   "medium" ->  720p   (1280x720)   ~90 MB per 60 seconds   |
|   "high"   ->  1080p  (1920x1080)  ~214 MB per 60 seconds  |
|   "ultra"  ->  4K     (3840x2160)  ~850 MB per 60 seconds  |
|                                                             |
|   Note: This only affects the EXPORT assembly step.        |
|   Individual scene renders in output/ are always            |
|   produced at render_resolution quality.                    |
|                                                             |
+-------------------------------------------------------------+
```

---

export_name

**Type:** `Optional[str]`
**Default:** `None`
**Example value:** `"IntroductionToCalculus_Episode1"`

The custom filename for the exported video, without extension.
When `None`, the system uses `{project_name}_final` as the default.
Changed with: `set export name MyCustomName`

The extension is added automatically based on `export_format`.
Storing the name without extension means changing the format
automatically updates the file extension without needing to
change the name separately.

```
export_name = "IntroductionToCalculus_Episode1"
export_format = "mp4"   -> IntroductionToCalculus_Episode1.mp4
export_format = "webm"  -> IntroductionToCalculus_Episode1.webm
(name unchanged, only the extension updates)
```

---

GROUP 4 — MUTABLE RENDER SETTINGS

These settings control the visual output of every rendered scene.

---

render_resolution

**Type:** `str`
**Default:** `"1920x1080"`
**Example value:** `"1920x1080"`, `"3840x2160"`, `"1280x720"`

The pixel dimensions used when Manim renders scenes. All scenes in a project
must use the same resolution because FFmpeg requires all input clips to have
identical dimensions when stitching them into the final video.

---

render_fps

**Type:** `int`
**Default:** `60`
**Example value:** `24`, `30`, `60`

How many frames Manim draws per second of animation. 60fps is smooth
but slow to render. 24fps is cinema standard and much faster to render.

```
For a 16.8-second scene:
  24 fps ->  403 frames to draw
  30 fps ->  504 frames to draw
  60 fps -> 1008 frames to draw

Lower fps = fewer frames = faster render = less smooth motion.
```

---

render_background_color

**Type:** `str`
**Default:** `"#000000"` (pure black)
**Example value:** `"#000000"`, `"#FFFFFF"`, `"#1a1a2e"`

The background color of the animation canvas in hex format.
Manim fills the canvas with this color before drawing anything.
Most educational animations use black because shapes and text
stand out clearly against it.

---

GROUP 5 — MUTABLE PREVIEW SETTINGS

---

preview_resolution

**Type:** `str`
**Default:** `"854x480"` (480p)

The resolution used for preview renders. This is always 480p and is not
intended to be changed by the user — it exists as a setting so the system
can read it consistently from one place rather than hardcoding it.

480p is chosen because it is roughly five times fewer pixels than 1080p,
making previews about five times faster to generate than full renders.

---

preview_fps

**Type:** `int`
**Default:** `30`

The frame rate used for preview renders. Lower than the render fps
by default (30 vs 60) to make previews twice as fast. Again, this
is not intended to be changed by the user directly.

---

GROUP 6 — MUTABLE AUDIO SETTINGS

---

audio_format

**Type:** `str`
**Default:** `"mp3"`
**Example value:** `"mp3"`, `"wav"`, `"ogg"`

The default format that will be used when audio files are added to this
project or when audio clips are generated from splitting. Changed with:
`change audio_format wav`

When this setting is changed, the next time audio is added or split,
the clips will be created in the new format.

---

A REAL PROJECTSETTINGS OBJECT IN FULL

```python
ProjectSettings(
    # ── IDENTITY ────────────────────────────────────────────────
    settings_id              = 1,
    project_id               = 1,

    # ── LOCKED FIELDS ───────────────────────────────────────────
    project_name             = "MyAnimation",
    project_mode             = "supermanim",
    project_folder_path      = "/home/user/projects/MyAnimation",
    project_db_path          = "/home/user/projects/MyAnimation/project_data.db",
    settings_created_at      = "2024-11-10 09:00:15",

    # ── MUTABLE EXPORT SETTINGS ──────────────────────────────────
    export_format            = "mp4",
    export_quality           = "high",
    export_name              = "IntroductionToCalculus_Episode1",

    # ── MUTABLE RENDER SETTINGS ──────────────────────────────────
    render_resolution        = "1920x1080",
    render_fps               = 60,
    render_background_color  = "#000000",

    # ── MUTABLE PREVIEW SETTINGS ─────────────────────────────────
    preview_resolution       = "854x480",
    preview_fps              = 30,

    # ── MUTABLE AUDIO SETTINGS ───────────────────────────────────
    audio_default_format     = "mp3",

    # ── AUTO-UPDATED ─────────────────────────────────────────────
    settings_updated_at      = "2024-11-12 14:30:55",
)
```

What you can read from this object in one glance:
the project is named MyAnimation, it is in supermanim mode, it exports
to a 1080p mp4 named IntroductionToCalculus_Episode1, it renders at
60fps on a black background, preview mode uses 480p at 30fps, audio
defaults to mp3, and the settings were last updated on November 12 at 2:30 PM.

---

HOW PROJECTSETTINGS IS SHOWN TO THE USER

When the user types `show export settings`, the system loads the
ProjectSettings Entity and displays the relevant fields:

```
supermanim> show export settings

  Export Settings — MyAnimation
  ================================
  Output filename:    IntroductionToCalculus_Episode1
  Format:             mp4
  Quality:            high (1080p)
  Full output path:   exports/IntroductionToCalculus_Episode1.mp4

  Estimated file size for this project:  ~214 MB
  Total assembled duration:              60.3 seconds

  To change these settings:
    set export name     <filename>
    set export format   <format>
    set export quality  <level>

  To run the export:
    export
```

Every line of this display comes from reading fields of the
ProjectSettings Entity and formatting them for the user.

---

THE THREE ENTITIES WORKING TOGETHER

```
+=====================================================================+
|        HOW AUDIOFILE, AUDIOCLIP, AND PROJECTSETTINGS RELATE         |
+=====================================================================+
|                                                                     |
|   Project (project_id=1, "MyAnimation")                             |
|   |                                                                 |
|   +-- ProjectSettings (project_id=1)                                |
|   |   export_format="mp4", export_quality="high"                    |
|   |   render_resolution="1920x1080", render_fps=60                  |
|   |   <- These settings apply to all renders and exports            |
|   |                                                                 |
|   +-- AudioFile (project_id=1, audio_file_id=1)                     |
|   |   stored_path="audio_clips/original_audio.mp3"                  |
|   |   audio_total_duration=60.3, audio_format="mp3"                 |
|   |   audio_is_split=True, audio_clip_count=5                       |
|   |   <- The master recording. Never cut. Never modified.           |
|   |                                                                 |
|   +-- AudioClip (clip_id=1, audio_file_id=1, scene_id=1)            |
|   |   clip_path="audio_clips/clip_001.mp3"                          |
|   |   clip_duration=12.5                                            |
|   |   clip_start_in_original=0.0, clip_end_in_original=12.5        |
|   |   clip_is_synced=True  <- linked to Scene 1                     |
|   |                                                                 |
|   +-- AudioClip (clip_id=3, audio_file_id=1, scene_id=3)            |
|   |   clip_path="audio_clips/clip_003.mp3"                          |
|   |   clip_duration=16.8                                            |
|   |   clip_start_in_original=31.0, clip_end_in_original=47.8       |
|   |   clip_is_synced=True  <- linked to Scene 3                     |
|   |                                                                 |
|   +-- Scene (scene_id=3)                                            |
|       scene_duration=16.8                                           |
|       audio_clip_path="audio_clips/clip_003.mp3"                    |
|       synced_with_audio=True                                        |
|       <- render uses clip_003.mp3 (duration matches: 16.8==16.8)   |
|                                                                     |
+=====================================================================+
```

COMPONENT 2: BUSINESS RULES
----------------------------
What Is a Business Rule?
===========================
A Business Rule is a law that the system must never break.
It is not about HOW to do something. It is about WHAT is allowed
and WHAT is not allowed.

Business Rules are the constraints — the boundaries — within which
SuperManim operates. If you violate a Business Rule, the system
must stop, refuse to continue, and tell the user what went wrong.

Business Rules answer the question: **"Is this allowed?"**

They are written as checks that return YES or NO, VALID or INVALID,
ALLOWED or REFUSED.

Where Do Business Rules Live?
=================================
Business Rules live in the Domain Services inside the Core.
Specifically in the `ValidationService` and the pure logic methods
of `TimelineService` and `HashService`.

They do NOT live in Adapters. An Adapter never decides if a scene
is valid. It just stores and retrieves data.

They do NOT live in the CLI Shell. The Shell just reads commands.
It does not know the rules of the system.

Only the Core knows the rules. This means the rules are the same
whether you use SuperManim from the terminal, from a GUI, or from
an API — because the rules live in one place and everything goes
through that one place.


Let's go through every single Business Rule in SuperManim, explain
WHY it exists, WHAT happens when it is violated, and WHERE in the
code it is checked.

---

Business Rule Group 1 — The Global Rules
========================================
These rules apply in every mode, at all times, for every command.

---

Rule 1.1 — The Open Project Rule (The Golden Rule)
====================================================
====================================================

**The rule:**
No command can be executed unless a project is currently open.

**Why this rule exists:**
Every command in SuperManim operates ON a project.
Adding a scene — which project? Rendering — which project?
Setting a duration — for which project's scene?
Without an open project, these questions have no answer.
The system would not know where to store data, where to look for files,
or which database to update. So before every command runs, the system
checks: "Is there an open project?" If no, it refuses.

**What happens when it is violated:**
The user types a command without having created or opened a project first.

```
supermanim> set scene 1 duration 12.5

  ERROR: No project is open.
  You must create or open a project before using this command.

  To create a new project:  new project <name>
  To open an existing one:  open project <name>

supermanim>
```

**Where it is checked in the code:**
Every Application Service method checks this at the very start.

---

Rule 1.2 — The Command Case-Insensitivity Rule
====================================================
====================================================


**The rule:**
Command words are case-insensitive. Project names are case-sensitive.

**Why this rule exists:**
Users should not have to remember whether to type `Create` or `create`
or `CREATE`. The command words are just instructions — their meaning
does not change based on capitalization. But project names are
identifiers. `MyAnimation` and `myanimation` are two different projects,
just like two different people can have names that look similar but
are different people.

**What this looks like:**

```
These are all identical commands:
  new project MyAnimation
  New Project MyAnimation
  NEW PROJECT MyAnimation
  nEw pRoJeCt MyAnimation

But these create DIFFERENT projects:
  new project MyAnimation      ← creates "MyAnimation"
  new project myanimation      ← creates "myanimation" (different!)
```

**Where it is checked:**
In the CLI Shell Adapter, before passing the command to a Service:

```python
# In the Shell Adapter:
def do_new(self, args: str) -> None:
    parts = args.strip().split()
    keyword = parts[0].lower()    # <-- command word lowercased
    name    = parts[1]            # <-- project name kept as-is
```

---

Rule 1.3 — The No-Spaces-In-Project-Name Rule
====================================================
====================================================


**The rule:**
Project names cannot contain spaces. They must use underscores or hyphens.

**Why this rule exists:**
Project names become folder names on disk. Most operating systems
handle spaces in folder paths poorly — they cause problems in terminal
commands, in FFmpeg calls, in Manim calls. By forbidding spaces at
the rule level, SuperManim prevents an entire category of file system
bugs before they happen.

**What happens when it is violated:**

```
supermanim> new project My Animation

  ERROR: Project name cannot contain spaces.
  Use underscores or hyphens instead.

  Good names:  My_Animation   my-animation   MyAnimation
  Bad names:   My Animation   my animation

supermanim>
```

**Where it is checked:**
In `ValidationService.project_name_is_valid()`:

```python
# core/domain/validation_service.py

def project_name_is_valid(self, name: str) -> list[str]:
    errors = []
    if " " in name:                          # <-- Rule 1.3 check
        errors.append(
            "Project name cannot contain spaces. "
            "Use underscores or hyphens instead."
        )
    if len(name) == 0:
        errors.append("Project name cannot be empty.")
    return errors
```

---

Business Rule Group 2 — Project Management Rules
================================================
These rules apply when creating, opening, and deleting projects.

---

Rule 2.1 — The Mandatory Folder Structure Rule
====================================================
====================================================


**The rule:**
When a project is created, the full folder structure must be created
immediately and completely. A project cannot exist without all its folders.

**Why this rule exists:**
Every part of SuperManim assumes certain folders exist.
The AudioService copies files into `audio_clips/`.
The RenderService reads from `output/`.
The PreviewService writes to `previews/`.
If any of these folders is missing, operations will fail with
confusing file-not-found errors deep inside the workflow.
By creating all folders at project creation time, this entire
category of errors is prevented.

**The full structure that must be created:**

```
/projects/MyAnimation/
     |
     +-- project_data.db       The brain — stores all settings
     +-- audio_clips/          Where audio files live
     +-- scenes/               Where scene code files are copied
     +-- cache/                Where fingerprints are stored
     +-- output/               Where rendered videos appear
     +-- previews/             Where preview videos appear
     +-- assets/               Where user images/fonts live
     +-- temp/                 Temporary working files
     +-- exports/              Where the final assembled video goes
```

**Where it is checked:**
In `ProjectService.create_project()` — it creates all folders
immediately after validating the project name.

---

Rule 2.2 — The Database Is Mandatory Rule
====================================================
====================================================


**The rule:**
Every project must have its own `project_data.db` file.
No project can operate without this file.

**Why this rule exists:**
The database is the memory of the project. It stores:
- How many scenes there are
- The duration of each scene
- The status of each scene (pending, rendered, failed)
- The fingerprint of each scene's code file
- Which audio clips have been cut
- Which scenes are synced to which clips
- Export settings

Without the database, none of this information survives between
sessions. Every time you close and re-open SuperManim, you would
start from scratch. The database is what makes the project persistent.

---

Rule 2.3 — The Confirm Before Delete Rule
====================================================
====================================================


**The rule:**
A project can only be deleted after the user explicitly types "yes"
to confirm. There is no undo.

**Why this rule exists:**
Deleting a project removes the project folder, all scene files,
all rendered videos, all audio clips, and the database — permanently.
This is an irreversible action. A user who accidentally types
`delete project MyAnimation` when they meant something else
would lose all their work. The confirmation step gives them
one last chance to cancel.

**What it looks like:**

```
supermanim> delete project OldTest

  WARNING: This will permanently delete project "OldTest"
  and all files inside it. This cannot be undone.

  Files that will be deleted:
    /projects/OldTest/  (entire folder and all contents)

  Type "yes" to confirm, or anything else to cancel:
  > yes

  Deleting...
  Project "OldTest" has been permanently deleted.

supermanim>
```

---

Business Rule Group 3 — Scene Rules
====================================================
These rules apply when working with scenes.

---

Rule 3.1 — The Code File Must Exist Rule
====================================================
====================================================


**The rule:**
When assigning a code file to a scene, the file must actually exist
on disk at the path provided. SuperManim will not accept a path
to a file that does not exist.

**Why this rule exists:**
If SuperManim accepted a non-existent file path and stored it in the
database, the error would only appear much later — during rendering,
which might take minutes to start, and then fail with a confusing
Manim error message. By checking at the time of assignment, the user
gets an immediate, clear error message and can fix the problem right away.

**What happens when violated:**

```
supermanim> set scene 1 code wrong_path/intro.py

  ERROR: File not found: wrong_path/intro.py
  The file does not exist at this location.

  Please check the path and try again.
  Current directory: /home/user/my_project/

supermanim>
```

**Where it is checked:**
In `ValidationService.scene_code_path_is_valid()` and checked
by `SceneService.set_scene_code()` before saving.

---

Rule 3.2 — The Fingerprinting Rule (Hash)
====================================================
====================================================


**The rule:**
When a code file is assigned to a scene, its SHA-256 fingerprint
(hash) must be computed and stored. This fingerprint is the basis
for deciding whether to re-render a scene or skip it.

**Why this rule exists:**
This is the core superpower of SuperManim. You have 20 scenes.
You change one line in Scene 14's code file. Without fingerprinting,
SuperManim would have to re-render all 20 scenes because it has
no way to know what changed. With fingerprinting, it computes the
current hash of each code file and compares it to the stored hash
from the last render. Only the scenes whose hash changed get rendered.

**How the hash works:**

```
+=====================================================================+
|               HOW FINGERPRINTING WORKS                              |
+=====================================================================+
|                                                                     |
|   FIRST TIME (scene never rendered before):                         |
|                                                                     |
|   User assigns intro.py to Scene 1.                                 |
|   SuperManim reads intro.py.                                        |
|   Computes SHA-256: "a3f8c2d1e4b9..."                               |
|   Stores this hash in the database next to Scene 1.                 |
|   Renders Scene 1.                                                   |
|                                                                     |
|   ─────────────────────────────────────────────────────────────    |
|                                                                     |
|   NEXT TIME (user runs render again):                               |
|                                                                     |
|   SuperManim reads intro.py again.                                  |
|   Computes SHA-256: "a3f8c2d1e4b9..."  ← same hash                 |
|   Compares to stored: "a3f8c2d1e4b9..."                             |
|   They match. → File has NOT changed. → SKIP. (0 seconds)          |
|                                                                     |
|   ─────────────────────────────────────────────────────────────    |
|                                                                     |
|   AFTER USER EDITS THE FILE:                                        |
|                                                                     |
|   User changes one line in intro.py.                                |
|   SuperManim reads intro.py.                                        |
|   Computes SHA-256: "ff91b3a2c7d8..."  ← DIFFERENT hash            |
|   Compares to stored: "a3f8c2d1e4b9..."                             |
|   They do NOT match. → File HAS changed. → RENDER. (5 minutes)     |
|                                                                     |
+=====================================================================+
```

---

Rule 3.3 — The Auto-Numbering Rule
====================================================
====================================================


**The rule:**
When a new scene is added, it automatically gets the next available
number. When a scene is deleted, the remaining scenes are re-numbered
to fill the gap.

**Why this rule exists:**
Scene numbers must always be a continuous sequence starting from 1.
If you have scenes 1, 2, 3, 4 and you delete Scene 2, you cannot
have scenes 1, 3, 4 — because that would mean Scene 3's audio clip
is clip_003, but it is now the second scene. The timeline would
break. Re-numbering keeps the sequence clean and consistent.

**What it looks like:**

```
Before deleting Scene 2:
  Scene 1 | Scene 2 | Scene 3 | Scene 4

After deleting Scene 2:
  Scene 1 | Scene 2 | Scene 3
  (old Scene 3 becomes new Scene 2, old Scene 4 becomes new Scene 3)
```

---

Business Rule Group 4 — Audio and Synchronization Rules
============================================================
These rules apply only in supermanim mode, where audio sync is active.

---

 Rule 4.1 — The Duration Matching Rule (The Most Critical Rule)
====================================================
====================================================


**The rule:**
When syncing a scene to an audio clip, the scene's duration and the
audio clip's duration must be identical (within 1 millisecond tolerance).
If they do not match, the sync is refused.

**Why this rule exists:**
This is the central promise of SuperManim: the video matches the audio
perfectly. If Scene 3 lasts 16.8 seconds but its audio clip lasts 17.2 seconds,
then when the video plays, the scene will end 0.4 seconds before the
audio finishes — and there will be silence, or the next scene will
start while the audio for the previous scene is still playing.
The user would see a video that is out of sync with the audio.
The rule prevents this from ever happening by refusing to allow
a sync between non-matching durations.

**The tolerance is 0.001 seconds (1 millisecond):**
We do not check for exact equality because of how floating point
numbers work in computers. 16.8 might be stored internally as
16.800000000001. So we check if the difference is smaller than
1 millisecond, which is imperceptibly small to human ears and eyes.

**What happens when violated:**

```
supermanim> sync scene 4 audio_clip 4

  Checking durations:
  Scene 4 duration:       7.0 seconds
  clip_004.mp3 duration:  9.3 seconds
  Difference:             2.3 seconds

  ERROR: Cannot sync. Durations do not match.

  Fix options:
    Option A: Change the scene duration to match the clip:
              set scene 4 duration 9.3

    Option B: Re-cut the audio to match the scene:
              split audio duration ... 7.0 ...

supermanim>
```

**Where it is checked:**
In `ValidationService.sync_is_valid()` and called by
`AudioService.sync_scene()` before setting `synced_with_audio = True`.

```python
# core/domain/validation_service.py

def sync_is_valid(self, scene: Scene, clip: AudioClip) -> list[str]:
    errors = []
    difference = abs(scene.duration - clip.duration)
    if difference >= 0.001:                        # <-- Rule 4.1 check
        errors.append(
            f"Duration mismatch. "
            f"Scene={scene.duration}s, "
            f"Clip={clip.duration}s. "
            f"Difference={difference:.3f}s."
        )
    return errors
```

---

Rule 4.2 — The Total Duration Matching Rule
====================================================
====================================================


**The rule:**
The sum of all scene durations must equal the total duration of the
original audio file. SuperManim warns the user if they don't match,
and refuses the final synchronized render if they still don't match.

**Why this rule exists:**
If your audio is 60.3 seconds but your scenes only add up to 58.0 seconds,
the final video will be 58.0 seconds long — and the last 2.3 seconds
of your audio narration will be cut off. Or worse, if scenes add up
to 62.0 seconds, the video will be longer than the audio and the
last 1.7 seconds of video will play in silence.

**What it looks like:**

```
After setting all 5 scene durations:

  Duration summary:
  Scene 1:  12.5s
  Scene 2:  18.5s
  Scene 3:  16.8s
  Scene 4:   7.0s
  Scene 5:   5.5s
  ──────────────────────────
  Total:    60.3 seconds

  Audio file: voice.mp3 (60.3 seconds)
  Match: YES ✓

  vs.

  Total:    58.0 seconds
  Audio:    60.3 seconds
  Match: NO ✗  (2.3 seconds short)
  WARNING: Your scenes are 2.3 seconds shorter than your audio.
```

---

Rule 4.3 — The synced_with_audio Flag Rule
====================================================
====================================================


**The rule:**
A scene must have `synced_with_audio = True` before it can be rendered
as a synchronized scene (with audio baked into the video). The default
for all new scenes is `False`. Only the `sync scene` command can set
it to `True`.

**Why this rule exists:**
A scene might have an audio clip assigned to it, but the durations
might not match yet, or the user might not have verified the sync yet.
The flag is a deliberate confirmation: "I have checked this, the
durations match, this scene is ready to render with audio."
It prevents half-configured scenes from being rendered incorrectly.

---

Rule 4.4 — The Audio Format Support Rule
====================================================
====================================================


**The rule:**
Only certain audio formats are supported: mp3, wav, ogg, aac, flac, m4a.
Any other format is rejected.

**Why this rule exists:**
FFmpeg can handle many formats, but SuperManim has been tested and
validated only with these specific formats. Accepting unknown formats
could lead to FFmpeg errors that are hard to diagnose. By maintaining
an explicit allowlist, error messages stay clear and predictable.

---

Business Rule Group 5 — Rendering Rules
===================================================
These rules apply during the rendering process.

---

Rule 5.1 — The Incremental Rendering Rule
====================================================
====================================================


**The rule:**
A scene is only rendered (Manim is only called) if the scene's code
file has changed since the last successful render. If the fingerprint
is the same, the scene is skipped — its existing rendered video is
used as-is.

**Why this rule exists:**
This is the entire reason SuperManim exists. Rendering with Manim
takes minutes per scene. A project with 20 scenes takes 100 minutes
to render from scratch. If the user changes one scene, they should
only wait for that one scene — not 100 minutes. This rule is what
makes that possible.

**The decision tree:**

```
+=====================================================================+
|   THE INCREMENTAL RENDERING DECISION                                |
+=====================================================================+
|                                                                     |
|   For each scene, before calling Manim:                             |
|                                                                     |
|   Q1: Has this scene ever been rendered before?                     |
|       NO  → stored hash = None → MUST render.                       |
|       YES → go to Q2.                                               |
|                                                                     |
|   Q2: Has the code file changed since last render?                  |
|       Compute current hash. Compare to stored hash.                 |
|       SAME    → file unchanged → SKIP. Use existing video.          |
|       DIFFERENT → file changed → MUST render.                       |
|                                                                     |
|   Q3: (only if synced with audio) Do durations still match?         |
|       YES → proceed to render.                                      |
|       NO  → REFUSE. Report mismatc. Render the video without audio  |
|                                                                     |
+=====================================================================+
```

---

Rule 5.2 — The Renderable Scene Rule
====================================================
====================================================


**The rule:**
A scene can only be rendered if it has BOTH a code file assigned
AND a duration set. A scene missing either of these cannot be rendered.

**Why this rule exists:**
Without a code file, Manim has nothing to draw. Without a duration,
the animation engine does not know when to stop. Both are required
for a render to be possible. Checking this before calling Manim
prevents Manim from receiving incomplete instructions and crashing.

---

Business Rule Group 6 — Export Rules
====================================
These rules apply when assembling the final video.

---

Rule 6.1 — The All-Rendered-Before-Export Rule
====================================================
====================================================


**The rule:**
The final video cannot be assembled (exported) unless every single
scene has a status of "rendered". If even one scene has status
"pending" or "failed", the export is refused.

**Why this rule exists:**
The export process takes all rendered scene videos and stitches them
together into one final video using FFmpeg. If any scene is missing
its video file (because it was never rendered or because it failed),
FFmpeg would crash or produce a broken video. The rule prevents this
by checking completeness before starting the assembly.

**What happens when violated:**

```
supermanim> export

  Export checklist:
  [OK] Project is open: MyAnimation
  [OK] Project has 5 scenes.
  [!!] Not all scenes are rendered.

  Scene 4 → status: pending   (not yet rendered)
  Scene 5 → status: FAILED    (error on last attempt)

  Cannot export. Fix these scenes first:
    render scene 4
    render failed

supermanim>
```

---

Rule 6.2 — The Supported Export Format Rule
====================================================
====================================================


**The rule:**
The export format must be one of: mp4, webm, mov, avi.
Any other format is rejected.

---

Rule 6.3 — The Preview Quality Rule
====================================================
====================================================


**The rule:**
Preview renders must use low quality (480p). Final renders must use
high quality (1080p or configured quality). These cannot be swapped.

**Why this rule exists:**
The entire purpose of previews is speed — they exist so users can
check their work quickly without waiting minutes. If preview quality
matched final quality, they would take just as long and defeat their purpose.

---
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


# Module 4 Ports (Interfaces):

























 

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# Module 5 Adapters:


@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# Module 6 Services:


@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


# Module  Project State Management:

