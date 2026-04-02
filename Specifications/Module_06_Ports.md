
# Module 6 Ports (Interfaces):

###### The second component is the ports (Interfaces):
What are the ports:
--------------------
A Port is an **interface**. It is a contract. It says: "If you want to give me a service,
you must provide these exact functions. I don't care how you implement them.
Just give me these functions."

The Core defines Ports. The Core says: "I need someone who can save a scene.I need someone
who can run a render. I need someone who can read audio duration." The Core does not care
*how* these things are done. It just defines the shape of what it needs.

In Python, Ports are typically written as Abstract Base Classes (ABCs) or Protocols.

There are two types of Ports:
--------------------------------
Inbound Ports (also called "Driving Ports")  
================================================

What are inbounds ports:
=========================
=========================
These are how the outside world talks TO the Core. The outside world says "do this thing."
The CLI uses an Inbound Port when it sends a command like `render scene 1` to the Core.


Types of INBOUND PORTS (Outside world --> Core)
==============================================
=============================================

ProjectCommandPort      - Accepts project-level commands
                          (create project, open project, close project)

SceneCommandPort        - Accepts scene-level commands
                          (add scene, set scene duration, set scene code)

AudioCommandPort        - Accepts audio-level commands
                          (add audio, auto-split, map scene to audio)

RenderCommandPort       - Accepts render commands
                          (render scene, render all, preview scene)

ExportCommandPort       - Accepts export commands
                          (export project, package project)



Outbound Ports (also called "Driven Ports")
=================================================

What are outbound ports:
==========================
==========================
These are how the Core talks to the outside world to GET things done. The Core says "save this scene"
using an Outbound Port. Someone on the other end of that port fulfills the request
(the database adapter, the file system adapter, etc.).


**Example of a Outbound Port in Python:**

```python
# This is an Outbound Port.
# The Core defines this.
# The Core says: "I need a SceneRepository.
#                 I do not care if it uses SQLite, JSON, or anything else.
#                 Just give me something that has these three methods."

from abc import ABC, abstractmethod

class SceneRepositoryPort(ABC):

    @abstractmethod
    def save_scene(self, scene: Scene) -> None:
        """Save a scene to whatever storage you are using."""
        pass

    @abstractmethod
    def load_scene(self, scene_id: int) -> Scene:
        """Load a scene by its ID."""
        pass

    @abstractmethod
    def all_scenes(self) -> list[Scene]:
        """Return all scenes in this project."""
        pass
```

The Core only ever calls `save_scene()`, `load_scene()`, `all_scenes()`.
It never asks "are you using SQLite?"or "are you using a JSON file?"
It does not know. It does not care.



TYPES OF OUTBOUND PORTS (Core --> Outside world)
===============================================
================================================
SceneRepositoryPort     - Save and load scene data
ProjectRepositoryPort   - Save and load project settings
AudioRepositoryPort     - Save and load audio metadata
RenderRunnerPort        - Actually run a render (calls Manim)
AudioProcessorPort      - Actually process audio (calls FFmpeg or PyDub)
VideoAssemblerPort      - Actually assemble final video (calls FFmpeg)
FileStoragePort         - Read and write files on disk
HashComputerPort        - Compute a hash/fingerprint of a code file
NotificationPort        - Send messages to the user (print to terminal, etc.)
```


Classigications of Ports:
------------------------------
SuperManim's ports are divided into six logical groups based on what they do:

```
+------+----------------------------------+----------------------------+
|  #   |  Group Name                      |  What it Covers            |
+------+----------------------------------+----------------------------+
|  1   |  Repository Ports                |  Saving & Loading Data     |
|  2   |  Media Processing Ports          |  Rendering & Audio & Video |
|  3   |  Infrastructure Ports            |  Files, Hashing, Temp Work |
|  4   |  Driving Ports (Inbound)         |  User Commands (Input)     |
|  5   |  Notification Ports (Outbound)   |  Feedback to User (Output) |
|  6   |  Configuration Ports             |  Settings & Environment    |
+------+----------------------------------+----------------------------+
```
GROUP 1 — Repository Ports (Data Persistence)
======================================================
Think of this group as SuperManim's **long-term memory**. Without this group, every time you close the program,
everything is forgotten — all your scenes, all your audio clips, all your render history. The Repository Ports
make sure that data is saved to disk and can be retrieved later, exactly as you left it.

Every port in this group follows the same idea:
- `save_something(...)` — write data to storage
- `load_something(...)` — read data back
- `delete_something(...)` — remove data
- `list_all(...)` — get everything

The core logic does not know if it is talking to a SQLite file, a JSON file, a YAML file,
or even a remote server.It only talks to the Port.

Port 1.1 — SceneRepositoryPort
================================
================================
**Simple Definition:**
This port is the memory bank for every scene in your project. A "scene" in SuperManim is one section of your
video — for example, Scene 3 might be a 12-second animation showing a mathematical concept.
This port saves everything about that scene so nothing is lost.

**Why It Exists:**
Without this port, if you close SuperManim after creating 10 scenes, all that work disappears.
This port makes sure every scene is saved to disk, including its duration, its Python code file path,
its render status, and its hash fingerprint (used for smart skipping).

**What Data It Saves for Each Scene:**
- Scene id  number (1, 2, 3, ...)
- Duration in mille seconds (e.g., 12000 seconds)
- Path to the Manim Python code file
- Hash fingerprint of the code (used to detect if the code changed)
- Whether the scene has been rendered yet 
- The path to the rendered video clip
- The audio clip path assigned to this scene
- The start time of the audio for this scene (in seconds)
- The end time of the audio for this scene (in seconds)
- Any error message from the last failed render

**Functions the Core Calls Through This Port:**
These function can be categorized into 6 categories:

The Six Function Categories
```
+---+---------------------------+-------+-----------------------------------------+
| # | Category                  | Count | What It Covers                          |
+---+---------------------------+-------+-----------------------------------------+
| 1 | CRUD                      |   5   | Create, read, update, delete one scene  |
| 2 | QUERY                     |   9   | Read many scenes at once, with filters  |
| 3 | STATUS                    |  11   | Update render state and field values    |
| 4 | BULK                      |   5   | Operate on many scenes in one call      |
| 5 | CACHE / HASH              |   5   | Smart skip support via fingerprinting   |
| 6 | UTILITY                   |   8   | Housekeeping and introspection          |
+---+---------------------------+-------+-----------------------------------------+
                                  38
```

These categories include these functions:

```
+---+-------------------------------------+----------------------------------------------------------+
| # | Function Signature                  | One-Line Purpose                                         |
+---+-------------------------------------+----------------------------------------------------------+
|   | --- CRUD ---                         |                                                          |
| 1 | save_scene(scene)                   | Insert or update a scene record                          |
| 2 | load_scene(scene_id)                | Load one scene by ID, raise error if missing             |
| 3 | Is_scene_exist(scene_id)            | Safe check — returns True/False, never raises            |
| 4 | delete_scene(scene_id)              | Remove one scene record from storage                     |
| 5 | delete_all_scenes()                 | Wipe every scene record in the project                   |
+---+-------------------------------------+----------------------------------------------------------+
|   | --- QUERY ---                        |                                                          |
| 6 | load_all_scenes()                   | Return every scene, ordered by ID                        |
| 7 | count_scenes()                      | Count scenes without loading their data                  |
| 8 | get_scenes_by_status(status)        | Filter by "pending", "rendered", or "failed"             |
| 9 | get_rendered_scenes()               | Shortcut for status == "rendered"                        |
|10 | get_pending_scenes()                | Shortcut for status == "pending"                         |
|11 | get_failed_scenes()                 | Shortcut for status == "failed"                          |
|12 | get_scenes_in_range(start, end)     | Return scenes from ID start to ID end                    |
|13 | get_scenes_without_code()           | Find scenes with no code file assigned                   |
|14 | get_scenes_without_audio()          | Find scenes with no audio clip assigned                  |
+---+-------------------------------------+----------------------------------------------------------+
|   | --- STATUS ---                       |                                                          |
|15 | mark_as_rendered(scene_id, path)    | Set status rendered, store video path and timestamp      |
|16 | mark_as_failed(scene_id, message)   | Set status failed, store error message                   |
|17 | mark_as_pending(scene_id)           | Reset one scene to pending, clear video and error        |
|18 | mark_all_as_pending()               | Reset every scene to pending at once                     |
|19 | update_scene_hash(scene_id, hash)   | Store the new code fingerprint after rendering           |
|20 | update_scene_duration(scene_id, s)  | Update only the duration field                           |
|21 | update_scene_code_path(scene_id, p) | Update only the code file path                           |
|22 | update_scene_video_path(scene_id,p) | Update only the output video path                        |
|23 | update_scene_audio_path(scene_id,p) | Assign or update the audio clip path                     |
|24 | update_scene_audio_range(id, s, e)  | Store start and end seconds within the original audio    |
|25 | clear_error(scene_id)               | Erase the stored error message before a retry            |
+---+-------------------------------------+----------------------------------------------------------+
|   | --- BULK ---                         |                                                          |
|26 | save_all_scenes(scenes_list)        | Save many scenes in one atomic transaction               |
|27 | reorder_scenes(new_order_list)      | Reassign all scene positions in one operation            |
|28 | reset_render_status_for_scenes(ids) | Mark a list of specific scenes as pending                |
|29 | get_total_duration()                | Sum all scene durations, return total seconds            |
|30 | get_scenes_changed_since(timestamp) | Return scenes modified after a given datetime            |
+---+-------------------------------------+----------------------------------------------------------+
|   | --- CACHE / HASH ---                 |                                                          |
|31 | get_scene_hash(scene_id)            | Return the stored hash, or None if never rendered        |
|32 | hash_has_changed(scene_id, hash)    | Compare current hash to stored — True means re-render    |
|33 | get_all_hashes()                    | Return dict of all scene hashes in one query             |
|34 | invalidate_scene_cache(scene_id)    | Delete one scene's hash to force re-render               |
|35 | invalidate_all_caches()             | Delete every hash to force full re-render                |
+---+-------------------------------------+----------------------------------------------------------+
|   | --- UTILITY ---                      |                                                          |
|36 | get_last_rendered_scene()           | Find the most recently rendered scene by timestamp       |
|37 | get_next_scene_id()                 | Return the next available ID for a new scene             |
|38 | swap_scenes(scene_id_a, scene_id_b) | Swap the positions of two scenes atomically              |
|39 | duplicate_scene(scene_id)           | Copy a scene with a new ID, status reset to pending      |
|40 | get_render_summary()                | Return counts of rendered / pending / failed scenes      |
|41 | validate_all_video_paths()          | Check which stored video paths still exist on disk       |
|42 | export_to_dict()                    | Serialize all scene data to a Python dict for backup     |
|43 | import_from_dict(data)              | Restore all scene data from a previously exported dict   |
+---+-------------------------------------+----------------------------------------------------------+
```

Every function in this port follows the same four rules:

**Rule 1 — The Core never writes SQL.**
All SQL lives inside the adapter (`SqliteSceneRepository`). The Core only calls port functions by name.

**Rule 2 — The Core never imports database libraries.**
No `import sqlite3`, no `import psycopg2`, no `import json` for storage. All of that is the adapter's job.

**Rule 3 — Specific updates over full saves.**
When only one field changes, call the specific update function (for example, `update_scene_duration()`),
not `save_scene()`. This is faster and prevents accidentally overwriting data.

**Rule 4 — One place to swap everything.**
If you ever want to switch from SQLite to PostgreSQL, or from a database to JSON files,you write a new adapter
class that implements all  functions above. The Core code changes zero lines.

**Dividing the SceneRepository Port into specific ports:**
You have 43 functions that all deal with "scenes."
The question is: should they all live in one giant port, or should you
split them into smaller ports, each with a focused purpose?

**Split them. Do NOT put all 43 functions in one port.**

Here is why. Imagine you are building a house. A house needs a plumber,
an electrician, and a painter. You could hire one person and say
"you do everything." But that one person becomes overloaded, hard to
replace, and impossible to test in parts. Instead you hire three specialists.
Each specialist is small, focused, and replaceable.

Ports work the same way. One giant port with 43 functions has these problems:

```
+=====================================================================+
|        PROBLEMS WITH ONE GIANT SceneRepositoryPort                  |
+=====================================================================+
|                                                                     |
|   PROBLEM 1 — Hard to understand                                    |
|   When a developer opens the file and sees 43 functions,            |
|   they do not know what to focus on. Everything is mixed together.  |
|   CRUD sits next to cache invalidation sits next to export.         |
|   The port tells no story. It is just a pile of functions.         |
|                                                                     |
|   PROBLEM 2 — Impossible to test in isolation                       |
|   If you want to test only the hash/cache logic, you have to        |
|   create a fake object that implements ALL 43 functions.            |
|   Even the 38 functions you don't need for that test.               |
|   This makes test setup painful and fragile.                        |
|                                                                     |
|   PROBLEM 3 — Forces unnecessary dependencies                       |
|   RenderPipelineService only needs cache functions.                 |
|   But if all 43 are in one port, RenderPipelineService receives     |
|   a reference to a port with CRUD, QUERY, STATUS, BULK, UTILITY     |
|   functions it will never use. This is called "interface pollution."|
|                                                                     |
|   PROBLEM 4 — Hard to swap adapters                                 |
|   If you want to replace the cache storage with Redis while         |
|   keeping SQLite for everything else, you cannot. They are all      |
|   welded into one port. You would have to replace everything        |
|   just to change one part.                                          |
|                                                                     |
+=====================================================================+
```

When you split into smaller ports, each service only receives the
port(s) it actually needs. `RenderPipelineService` only receives
`SceneCachePort`. `SceneLifecycleService` only receives
`SceneWritePort` and `SceneReadPort`. This is clean, testable, and clear.

---

# PART 3 — THE SPLIT: HOW MANY PORTS AND HOW TO DIVIDE

The 43 functions divide naturally into 5 ports based on what they do.
Each port has a clear, single responsibility.

```
+=====================================================================+
|                  THE 5 PORTS — OVERVIEW                             |
+=====================================================================+
|                                                                     |
|   PORT 1: SceneWritePort                                            |
|   "I write and change scene records."                               |
|   Functions: save, delete, update fields, bulk saves, reorder       |
|   Used by: SceneLifecycleService, RenderPipelineService             |
|                                                                     |
|   PORT 2: SceneReadPort                                             |
|   "I read and query scene records."                                 |
|   Functions: load, count, filter by status, find missing data       |
|   Used by: SceneLifecycleService, RenderPipelineService,            |
|            TimelineCoordinatorService, ProjectExportService         |
|                                                                     |
|   PORT 3: SceneStatusPort                                           |
|   "I update only the render status and related output fields."      |
|   Functions: mark rendered, mark failed, mark pending, clear error  |
|   Used by: RenderPipelineService, PreviewGenerationService          |
|                                                                     |
|   PORT 4: SceneCachePort                                            |
|   "I manage hash fingerprints for smart rendering."                 |
|   Functions: get hash, compare hash, get all hashes, invalidate     |
|   Used by: RenderPipelineService, RenderCacheService                |
|                                                                     |
|   PORT 5: SceneUtilityPort                                          |
|   "I handle housekeeping — swap, duplicate, summarize, backup."     |
|   Functions: swap, duplicate, summarize, export/import to dict      |
|   Used by: SceneLifecycleService, ProjectExportService              |
|                                                                     |
+=====================================================================+
```

---

# PART 4 — THE ADAPTER: STILL JUST ONE

Even though we have 5 ports, there is still only **ONE adapter**:
`SqliteSceneRepository`.

This single adapter implements all 5 ports. It knows SQLite. It writes SQL.
It is the only piece of code that touches the scenes table in the database.

```
+=====================================================================+
|              5 PORTS — 1 ADAPTER                                    |
+=====================================================================+
|                                                                     |
|   SceneWritePort   ─────────────────────────────┐                  |
|   SceneReadPort    ─────────────────────────────┤                  |
|   SceneStatusPort  ─────────────────────────────┤──► SqliteScene   |
|   SceneCachePort   ─────────────────────────────┤    Repository    |
|   SceneUtilityPort ─────────────────────────────┘                  |
|                                                                     |
|   The adapter inherits from all 5 port interfaces.                  |
|   It implements every function defined across all 5 ports.          |
|   It is the ONLY place in the codebase that writes SQL for scenes.  |
|                                                                     |
|   class SqliteSceneRepository(                                      |
|       SceneWritePort,                                               |
|       SceneReadPort,                                                |
|       SceneStatusPort,                                              |
|       SceneCachePort,                                               |
|       SceneUtilityPort,                                             |
|   ):                                                                |
|       ...all 43+ functions implemented here...                      |
|                                                                     |
+=====================================================================+
```

Why still one adapter? Because the adapter's job is to talk to SQLite.
SQLite does not care about your conceptual divisions. All scene data
lives in the same database table. Splitting the adapter would force you
to open the same database file from multiple places, creating connection
management headaches. One adapter, one connection, one place for all SQL.

---

# PART 5 — PORT 1: SceneWritePort

## What Is It?

`SceneWritePort` is responsible for everything that WRITES or CHANGES scene
records in the database. If you need to create a scene, update it, or delete it —
that goes through this port.

This port answers the question: "How do I change what is stored about scenes?"

```
+=====================================================================+
|                        SceneWritePort                               |
+=====================================================================+
|                                                                     |
|   File:    core/ports/scene_write_port.py                           |
|   Adapter: adapters/repositories/sqlite_scene_repository.py        |
|                                                                     |
|   Services that use this port:                                      |
|     SceneLifecycleService    (add, edit, delete scenes)             |
|     RenderPipelineService    (update after successful render)       |
|     AudioPreparationService  (assign audio path to scene)           |
|     TimelineCoordinatorService (reorder scenes)                     |
|                                                                     |
+=====================================================================+
```

## The Python Interface

```python
# core/ports/scene_write_port.py

from abc import ABC, abstractmethod
from core.entities.scene import Scene


class SceneWritePort(ABC):
    """
    Defines all write operations on scene records.
    Any code that needs to create, update, or delete scene data
    must use this port — never talk to the database directly.
    """

    @abstractmethod
    def save_scene(self, scene: Scene) -> None: ...

    @abstractmethod
    def delete_scene(self, scene_id: int) -> None: ...

    @abstractmethod
    def delete_all_scenes(self) -> None: ...

    @abstractmethod
    def update_scene_duration(self, scene_id: int,
                               duration_ms: int) -> None: ...

    @abstractmethod
    def update_scene_code_path(self, scene_id: int,
                                code_path: str) -> None: ...

    @abstractmethod
    def update_scene_video_path(self, scene_id: int,
                                 video_path: str) -> None: ...

    @abstractmethod
    def update_scene_audio_path(self, scene_id: int,
                                 audio_path: str) -> None: ...

    @abstractmethod
    def update_scene_audio_range(self, scene_id: int,
                                  start_ms: int,
                                  end_ms: int) -> None: ...

    @abstractmethod
    def save_all_scenes(self, scenes: list[Scene]) -> None: ...

    @abstractmethod
    def reorder_scenes(self, new_order: list[int]) -> None: ...
```

## Every Function Explained

---

### save_scene(scene: Scene) -> None

**What it does:**
Takes one complete Scene object and saves it to the database.
If a scene with this `scene_id` already exists, it updates the existing record.
If it does not exist yet, it creates a new record.
This is the INSERT-or-UPDATE operation — also called "upsert."

**When it is called:**
- When `SceneLifecycleService.add_scene()` creates a new scene
- When the user sets a scene name: `set scene 3 name "Introduction"`
- After any field on the Scene object changes and needs to be persisted

**What it takes:**
A complete `Scene` object with all fields populated.

**What it returns:**
Nothing. It either works silently or raises an exception on failure.

**Example:**
```python
scene = Scene(scene_id=3, scene_duration=16800, scene_status="pending")
scene_write_port.save_scene(scene)
```

---

### delete_scene(scene_id: int) -> None

**What it does:**
Permanently removes ONE scene record from the database by its ID.
This removes only the database row. It does NOT delete any files on disk
(code files, video files, audio files). File deletion is the job of
`FileStoragePort`.

**When it is called:**
When the user types `delete scene 3`.
The `SceneLifecycleService` first confirms with the user, then calls this.

**What it takes:**
The integer `scene_id` of the scene to delete.

**What it returns:**
Nothing. Raises `SceneNotFoundError` if the scene does not exist.

**Example:**
```python
scene_write_port.delete_scene(3)
```

---

### delete_all_scenes() -> None

**What it does:**
Wipes every single scene record in the current project from the database.
This is a complete reset of all scene data.

**When it is called:**
When the user chooses to completely restart their scene setup —
for example, re-running `set scenes_number 5` after having already
created scenes will first call this to wipe the old ones.

**WARNING:**
This is irreversible. It deletes all scenes, all their render status,
all their audio links, all their fingerprints. The tool asks the user
to confirm before this is triggered.

---

### update_scene_duration(scene_id: int, duration_ms: int) -> None

**What it does:**
Updates ONLY the `scene_duration` field of one specific scene.
It does not touch any other field.

**Why this exists instead of just calling `save_scene`:**
When you run `save_scene(scene)`, you write ALL fields.
If something else changed `scene.scene_status` between when you loaded
the scene and when you called `save_scene`, you might accidentally
overwrite a status change with stale data.
`update_scene_duration` changes only the one field you intend to change.
Nothing else is touched. This is safer and faster.

**Duration is in MILLISECONDS:**
The duration is stored as an integer in milliseconds, not seconds.
16.8 seconds = 16800 milliseconds.
Using integers avoids floating-point rounding errors in timeline math.

**When it is called:**
When the user types `set scene 3 duration 16.8`.
The command converts 16.8 seconds to 16800 milliseconds and calls this.

**Example:**
```python
scene_write_port.update_scene_duration(3, 16800)  # 16.8 seconds
```

---

### update_scene_code_path(scene_id: int, code_path: str) -> None

**What it does:**
Updates ONLY the `scene_code_path` field of one specific scene.

**When it is called:**
When the user types `set scene 3 code my_scenes/example.py`.
The `SceneLifecycleService` validates the file exists on disk,
computes the hash, then calls this to store the path.

**Example:**
```python
scene_write_port.update_scene_code_path(3, "my_scenes/example.py")
```

---

### update_scene_video_path(scene_id: int, video_path: str) -> None

**What it does:**
Updates ONLY the `scene_output_path` field — the path to the rendered
video file for this scene.

**When it is called:**
By `RenderPipelineService` immediately after a successful render,
to record where the output video was saved.

**Example:**
```python
scene_write_port.update_scene_video_path(3, "output/scene_03/scene_03.mp4")
```

---

### update_scene_audio_path(scene_id: int, audio_path: str) -> None

**What it does:**
Updates ONLY the `audio_clip_path` field — the path to the audio clip
file that belongs to this scene.

**When it is called:**
By `AudioPreparationService` when the user runs `sync scene 3 audio_clip 3`
and the duration check passes.

**Example:**
```python
scene_write_port.update_scene_audio_path(3, "audio_clips/clip_003.mp3")
```

---

### update_scene_audio_range(scene_id: int, start_ms: int, end_ms: int) -> None

**What it does:**
Updates the `scene_start_time` and `scene_end_time` fields of one scene.
These values represent where in the ORIGINAL full audio file this scene's
clip starts and ends, measured in milliseconds.

**Why milliseconds:**
Same reason as duration — integer arithmetic avoids floating-point errors.
31.0 seconds = 31000 milliseconds.

**When it is called:**
By `AudioPreparationService` after audio splitting, to record exactly which
portion of the master audio belongs to each scene.

**Example:**
```python
# Scene 3 starts at 31.0s and ends at 47.8s in the original audio
scene_write_port.update_scene_audio_range(3, 31000, 47800)
```

---

### save_all_scenes(scenes: list[Scene]) -> None

**What it does:**
Saves many scenes in one single database transaction.
All scenes are written atomically — either ALL succeed or NONE of them
are written. If the operation fails halfway through, no partial data
is left in the database.

**Why it exists:**
When the user runs `split audio auto` and SuperManim creates 5 scenes
all at once, calling `save_scene()` five times in a loop creates five
separate database transactions. If the system crashes after the third one,
only 3 scenes are saved and the project is in a broken state.
`save_all_scenes` wraps all five in one transaction — one commit.

**When it is called:**
When creating multiple scenes at once: `set scenes_number 5`.

**Example:**
```python
scenes = [Scene(scene_id=1), Scene(scene_id=2), Scene(scene_id=3)]
scene_write_port.save_all_scenes(scenes)
```

---

### reorder_scenes(new_order: list[int]) -> None

**What it does:**
Reassigns the `scene_index` (the playback order position) for all scenes
in a single atomic operation.

`new_order` is a list of `scene_id` values in the new desired order.
The first ID in the list gets `scene_index = 0`, the second gets `1`, etc.

**When it is called:**
When the user runs `move scene 5 to 2`. The `SceneLifecycleService`
computes the new order and calls this once to update all positions.

**Example:**
```python
# Before: [scene_id=1, scene_id=2, scene_id=3, scene_id=4, scene_id=5]
# After move scene 5 to position 2:
scene_write_port.reorder_scenes([1, 5, 2, 3, 4])
# scene_id=1 -> index=0, scene_id=5 -> index=1, etc.
```

---

# PART 6 — PORT 2: SceneReadPort

## What Is It?

`SceneReadPort` is responsible for everything that READS scene records
from the database. It has no side effects — it never changes anything.
It only fetches data.

This port answers the question: "What do I know about the scenes in this project?"

```
+=====================================================================+
|                        SceneReadPort                                |
+=====================================================================+
|                                                                     |
|   File:    core/ports/scene_read_port.py                            |
|   Adapter: adapters/repositories/sqlite_scene_repository.py        |
|                                                                     |
|   Services that use this port:                                      |
|     SceneLifecycleService         (list scenes, show scene info)    |
|     RenderPipelineService         (load scene before rendering)     |
|     TimelineCoordinatorService    (load all scenes for timeline)    |
|     ProjectExportService          (load all scenes before export)   |
|     AudioPreparationService       (find scenes without audio)       |
|     ValidationService             (check scene exists)              |
|                                                                     |
+=====================================================================+
```

## The Python Interface

```python
# core/ports/scene_read_port.py

from abc import ABC, abstractmethod
from core.entities.scene import Scene


class SceneReadPort(ABC):
    """
    Defines all read operations on scene records.
    Never changes any data. Only returns data.
    """

    @abstractmethod
    def load_scene(self, scene_id: int) -> Scene: ...

    @abstractmethod
    def scene_exists(self, scene_id: int) -> bool: ...

    @abstractmethod
    def load_all_scenes(self) -> list[Scene]: ...

    @abstractmethod
    def count_scenes(self) -> int: ...

    @abstractmethod
    def get_scenes_by_status(self, status: str) -> list[Scene]: ...

    @abstractmethod
    def get_rendered_scenes(self) -> list[Scene]: ...

    @abstractmethod
    def get_pending_scenes(self) -> list[Scene]: ...

    @abstractmethod
    def get_failed_scenes(self) -> list[Scene]: ...

    @abstractmethod
    def get_scenes_in_range(self, start_id: int,
                             end_id: int) -> list[Scene]: ...

    @abstractmethod
    def get_scenes_without_code(self) -> list[Scene]: ...

    @abstractmethod
    def get_scenes_without_audio(self) -> list[Scene]: ...

    @abstractmethod
    def get_total_duration_ms(self) -> int: ...

    @abstractmethod
    def get_scenes_modified_since(self,
                                   timestamp: str) -> list[Scene]: ...
```

## Every Function Explained

---

### load_scene(scene_id: int) -> Scene

**What it does:**
Loads ONE scene from the database by its `scene_id` and returns it as
a complete `Scene` object with all fields populated.

**When it is called:**
- Before rendering: `render scene 3` → load Scene 3
- Before showing info: `show scene 3 info` → load Scene 3
- Before any operation that needs a scene's current data

**What it returns:**
A fully populated `Scene` object.
Raises `SceneNotFoundError` if no scene with this ID exists.

**Example:**
```python
scene = scene_read_port.load_scene(3)
print(scene.scene_duration)   # 16800
print(scene.scene_status)     # "rendered"
```

---

### scene_exists(scene_id: int) -> bool

**What it does:**
Returns `True` if a scene with this ID exists. Returns `False` if it does not.
This NEVER raises an exception. It is a safe check.

**Why this exists separately from `load_scene`:**
If you call `load_scene(7)` on a project with only 5 scenes, you get an
exception. If you call `scene_exists(7)`, you get `False` — clean and safe.
Use this whenever you want to CHECK before you LOAD.

**When it is called:**
Before every operation that targets a specific scene by number.
When the user types `render scene 7` and the project only has 5 scenes,
`scene_exists(7)` returns `False` and the system shows a clear error.

**Example:**
```python
if scene_read_port.scene_exists(7):
    scene = scene_read_port.load_scene(7)
else:
    notifier.send_error("Scene 7 does not exist. This project has 5 scenes.")
```

---

### load_all_scenes() -> list[Scene]

**What it does:**
Loads every scene in the project and returns them as a list of `Scene`
objects, ordered by `scene_index` (their playback position).

**When it is called:**
- `list scenes` → shows all scenes in a table
- `render all` → loops through all scenes to check which ones need rendering
- `export` → needs all scenes to assemble the final video
- `sync all` → checks all scenes for sync status

**What it returns:**
A list of `Scene` objects in the correct playback order.
Returns an empty list if no scenes have been created yet.

---

### count_scenes() -> int

**What it does:**
Returns the total number of scenes in the project as an integer.
This is much faster than loading all scenes and counting them,
because it runs a SQL `COUNT` query instead of fetching all data.

**When it is called:**
When you only need the number, not the actual scene data.
For example: checking whether any scenes exist before attempting export.

**Example:**
```python
total = scene_read_port.count_scenes()  # returns 5
```

---

### get_scenes_by_status(status: str) -> list[Scene]

**What it does:**
Returns all scenes that match a specific status value.
The status can be `"pending"`, `"rendered"`, `"failed"`, or `"skipped"`.

**When it is called:**
When you need scenes filtered by their render state.

**Example:**
```python
failed_scenes = scene_read_port.get_scenes_by_status("failed")
```

---

### get_rendered_scenes() -> list[Scene]

**What it does:**
Returns all scenes with `scene_status = "rendered"`.
This is a shortcut — it calls `get_scenes_by_status("rendered")` internally.
It exists because this query is needed very frequently and having a
named method makes the calling code more readable.

**When it is called:**
During export readiness check: are ALL scenes rendered?

---

### get_pending_scenes() -> list[Scene]

**What it does:**
Returns all scenes with `scene_status = "pending"`.
Shortcut for `get_scenes_by_status("pending")`.

**When it is called:**
By `render_pending` command — render only the scenes that have not been
rendered yet.

---

### get_failed_scenes() -> list[Scene]

**What it does:**
Returns all scenes with `scene_status = "failed"`.
Shortcut for `get_scenes_by_status("failed")`.

**When it is called:**
By `render_failed` command — retry only the scenes that previously crashed.

---

### get_scenes_in_range(start_id: int, end_id: int) -> list[Scene]

**What it does:**
Returns scenes whose `scene_id` falls between `start_id` and `end_id`
(inclusive on both ends).

**When it is called:**
When the user wants to render or preview a specific range of scenes:
`render scenes 3 to 7` → calls `get_scenes_in_range(3, 7)`.

**Example:**
```python
scenes = scene_read_port.get_scenes_in_range(3, 7)
# returns scenes with scene_id = 3, 4, 5, 6, 7
```

---

### get_scenes_without_code() -> list[Scene]

**What it does:**
Returns all scenes that have `scene_code_path = None` — scenes that
exist but have no Python code file assigned to them yet.

**When it is called:**
By `validate project` command to find incomplete scenes.
By the export readiness check — a scene cannot be rendered without code.

**Example output in the terminal:**
```
validate project

  Scene level:
  [!!] Scene 3: NO code file assigned.
  [!!] Scene 5: NO code file assigned.
```

These two scenes were found by `get_scenes_without_code()`.

---

### get_scenes_without_audio() -> list[Scene]

**What it does:**
Returns all scenes that have `audio_clip_path = None` — scenes that
have no audio clip assigned to them.

**When it is called:**
By `show audio info` to display which scenes lack audio.
By `sync all` to identify scenes that cannot be synced.

---

### get_total_duration_ms() -> int

**What it does:**
Adds up the `scene_duration` of every scene and returns the total in
milliseconds.

**Why this exists:**
The total duration of the project must equal the duration of the audio
file in `supermanim` mode. This function provides the "total scenes"
side of that comparison.

**When it is called:**
By `TimelineCoordinatorService` when checking if scene durations match
the audio file's total duration.
By `set scene N duration` to show a running total after every change.

**Example:**
```python
total_ms = scene_read_port.get_total_duration_ms()
# returns 60300 for a project with scenes totaling 60.3 seconds
```

---

### get_scenes_modified_since(timestamp: str) -> list[Scene]

**What it does:**
Returns all scenes that were modified (any field changed) after a given
timestamp. The timestamp is a string in ISO format: `"2024-11-12 14:00:00"`.

**When it is called:**
For incremental backup and sync features — find only what changed since
the last backup. Also useful for showing the user what changed in the
current session.

---

# PART 7 — PORT 3: SceneStatusPort

## What Is It?

`SceneStatusPort` is responsible for updating the render status of scenes
and the output fields that go with that status. This is its own port
because render status changes happen constantly during rendering — they are
the most frequent write operations in the system.

By separating status updates from general writes, the rendering system can
use only this port without needing the full write capability of `SceneWritePort`.

```
+=====================================================================+
|                       SceneStatusPort                               |
+=====================================================================+
|                                                                     |
|   File:    core/ports/scene_status_port.py                          |
|   Adapter: adapters/repositories/sqlite_scene_repository.py        |
|                                                                     |
|   Services that use this port:                                      |
|     RenderPipelineService    (mark scenes after render attempts)    |
|     PreviewGenerationService (mark scenes after preview)            |
|                                                                     |
+=====================================================================+
```

## The Python Interface

```python
# core/ports/scene_status_port.py

from abc import ABC, abstractmethod


class SceneStatusPort(ABC):
    """
    Defines all operations that update the render status of scenes.
    These are called constantly during the render workflow.
    """

    @abstractmethod
    def mark_as_rendered(self, scene_id: int,
                          video_path: str,
                          rendered_at: str,
                          render_duration_s: float) -> None: ...

    @abstractmethod
    def mark_as_failed(self, scene_id: int,
                        error_message: str) -> None: ...

    @abstractmethod
    def mark_as_pending(self, scene_id: int) -> None: ...

    @abstractmethod
    def mark_as_skipped(self, scene_id: int) -> None: ...

    @abstractmethod
    def mark_all_as_pending() -> None: ...

    @abstractmethod
    def reset_render_status_for_scenes(self,
                                        scene_ids: list[int]) -> None: ...

    @abstractmethod
    def clear_error(self, scene_id: int) -> None: ...

    @abstractmethod
    def update_scene_hash(self, scene_id: int,
                           hash_value: str) -> None: ...

    @abstractmethod
    def update_preview_path(self, scene_id: int,
                             preview_path: str) -> None: ...
```

## Every Function Explained

---

### mark_as_rendered(scene_id, video_path, rendered_at, render_duration_s)

**What it does:**
Sets the scene's status to `"rendered"` and saves all the related
output information at the same time:
- `scene_status = "rendered"`
- `scene_output_path = video_path`
- `scene_rendered_at = rendered_at` (the timestamp)
- `scene_render_duration = render_duration_s` (how many seconds it took)
- `scene_error_message = None` (clears any previous error)

All five fields are updated in ONE database call — not five separate calls.

**When it is called:**
By `RenderPipelineService` immediately after Manim finishes successfully.

**Example:**
```python
scene_status_port.mark_as_rendered(
    scene_id          = 3,
    video_path        = "output/scene_03/scene_03.mp4",
    rendered_at       = "2024-11-12 14:22:27",
    render_duration_s = 262.0
)
```

---

### mark_as_failed(scene_id: int, error_message: str) -> None

**What it does:**
Sets the scene's status to `"failed"` and saves the error message.
- `scene_status = "failed"`
- `scene_error_message = error_message`
- `scene_output_path = None` (no video was produced)

**When it is called:**
By `RenderPipelineService` when Manim returns an error or crashes.

**Example:**
```python
scene_status_port.mark_as_failed(
    scene_id      = 5,
    error_message = "NameError: name 'Circle' is not defined on line 12"
)
```

---

### mark_as_pending(scene_id: int) -> None

**What it does:**
Resets one scene back to `"pending"` status and clears all render output:
- `scene_status = "pending"`
- `scene_output_path = None`
- `scene_error_message = None`
- `scene_rendered_at = None`
- `scene_render_duration = None`

**When it is called:**
When `force render scene 3` is used — the scene is reset to pending
before being re-rendered.
Also when the user edits a code file — the scene should be marked
pending again to signal it needs re-rendering.

---

### mark_as_skipped(scene_id: int) -> None

**What it does:**
Sets the scene's status to `"skipped"`.
This means the render was not attempted because the code fingerprint
was unchanged. The existing rendered video is still valid.

**When it is called:**
By `RenderPipelineService` during `render all` when a scene's hash
matches the stored hash — the code has not changed, so skip it.

---

### mark_all_as_pending() -> None

**What it does:**
Resets EVERY scene in the project to `"pending"` in one single
database operation.

**When it is called:**
When the user runs `force render all` — the tool first resets
everything to pending, then re-renders all scenes from scratch.

---

### reset_render_status_for_scenes(scene_ids: list[int]) -> None

**What it does:**
Resets a SPECIFIC LIST of scenes to `"pending"` in one single operation.
Useful when you want to force-re-render a subset of scenes.

**When it is called:**
When the user explicitly selects certain scenes to reset.

**Example:**
```python
# Reset only scenes 2, 4, and 5 to pending
scene_status_port.reset_render_status_for_scenes([2, 4, 5])
```

---

### clear_error(scene_id: int) -> None

**What it does:**
Clears the `scene_error_message` field WITHOUT changing the status.
Sets `scene_error_message = None`.

**When it is called:**
Before re-rendering a failed scene — the old error message is cleared
first, then if the new render also fails, a fresh error message is written.

---

### update_scene_hash(scene_id: int, hash_value: str) -> None

**What it does:**
Updates ONLY the `scene_hash` field — the SHA-256 fingerprint of the
scene's code file.

**When it is called:**
By `RenderPipelineService` immediately after a successful render.
The hash that was used for this render is stored so that next time,
the system can compare and decide whether to skip re-rendering.

**Example:**
```python
scene_status_port.update_scene_hash(3, "c9a1b3e7f2d4a8b1...")
```

---

### update_preview_path(scene_id: int, preview_path: str) -> None

**What it does:**
Updates ONLY the `scene_preview_path` field — the path to the low-quality
preview video for this scene.

**When it is called:**
By `PreviewGenerationService` after generating a preview for a scene.

---

# PART 8 — PORT 4: SceneCachePort

## What Is It?

`SceneCachePort` is entirely dedicated to the hash fingerprint system —
the mechanism that makes SuperManim's incremental rendering possible.

Every time a scene's code file is rendered, the SHA-256 fingerprint of
that file is stored. Before the next render, the current fingerprint is
compared to the stored one. If they match, the code has not changed
and the render is skipped. This is the entire secret behind SuperManim's
speed advantage.

```
+=====================================================================+
|                       SceneCachePort                                |
+=====================================================================+
|                                                                     |
|   File:    core/ports/scene_cache_port.py                           |
|   Adapter: adapters/repositories/sqlite_scene_repository.py        |
|                                                                     |
|   Services that use this port:                                      |
|     RenderPipelineService    (compare hashes before rendering)      |
|     RenderCacheService       (manage and clear cached hashes)       |
|                                                                     |
+=====================================================================+
```

## The Python Interface

```python
# core/ports/scene_cache_port.py

from abc import ABC, abstractmethod


class SceneCachePort(ABC):
    """
    Manages the hash fingerprint cache that powers smart rendering.
    A stored hash tells the system what code was used in the last render.
    If the current hash matches the stored hash, the render can be skipped.
    """

    @abstractmethod
    def get_scene_hash(self, scene_id: int) -> str | None: ...

    @abstractmethod
    def hash_has_changed(self, scene_id: int,
                          current_hash: str) -> bool: ...

    @abstractmethod
    def get_all_hashes(self) -> dict[int, str | None]: ...

    @abstractmethod
    def invalidate_scene_cache(self, scene_id: int) -> None: ...

    @abstractmethod
    def invalidate_all_caches(self) -> None: ...

    @abstractmethod
    def get_scenes_with_changed_hashes(
        self,
        current_hashes: dict[int, str]
    ) -> list[int]: ...
```

## Every Function Explained

---

### get_scene_hash(scene_id: int) -> str | None

**What it does:**
Returns the stored SHA-256 hash for a specific scene.
Returns `None` if the scene has never been rendered (no hash stored yet).

**When it is called:**
By `RenderPipelineService` before rendering a scene, to get the
previously stored fingerprint for comparison.

**What the return value means:**
- Returns a string like `"a3f8c2d1e4b9..."` → scene was rendered before
- Returns `None` → scene was never rendered, so it MUST be rendered

**Example:**
```python
stored_hash = scene_cache_port.get_scene_hash(3)
if stored_hash is None:
    print("Scene 3 has never been rendered. Will render now.")
```

---

### hash_has_changed(scene_id: int, current_hash: str) -> bool

**What it does:**
Compares the `current_hash` you provide to the stored hash for this scene.
Returns `True` if they are DIFFERENT (code changed → must re-render).
Returns `True` if there is NO stored hash (never rendered → must render).
Returns `False` if they are IDENTICAL (code unchanged → can skip).

**This is the single most called function in the rendering workflow.**
Every single scene check in `render all` calls this function.

**When it is called:**
By `RenderPipelineService` in the core decision loop:
"Should I render this scene or skip it?"

**The logic inside:**
```
if stored_hash is None:   return True   (never rendered → render)
if current != stored:     return True   (code changed → render)
if current == stored:     return False  (unchanged → skip)
```

**Example:**
```python
current_hash = hash_computer_port.compute("my_scenes/example.py")
if scene_cache_port.hash_has_changed(3, current_hash):
    # code changed — render scene 3
else:
    # code unchanged — skip scene 3
    notifier.send_info("Scene 3 unchanged. Skipped.")
```

---

### get_all_hashes() -> dict[int, str | None]

**What it does:**
Returns the stored hashes for ALL scenes in the project as one dictionary.
The keys are `scene_id` integers. The values are hash strings or `None`.

**Why it exists:**
When running `render all`, you need to check every scene's hash.
Instead of calling `get_scene_hash()` 20 times (20 database queries),
you call `get_all_hashes()` once (1 database query) and get all hashes
in one operation. This is significantly faster for large projects.

**What it returns:**
```python
{
    1: "a3f8c2d1...",   # Scene 1 hash
    2: "b7c9e1f4...",   # Scene 2 hash
    3: None,            # Scene 3 never rendered
    4: "f2d8a1b3...",   # Scene 4 hash
    5: "c9e7b2d1...",   # Scene 5 hash
}
```

**Example:**
```python
all_hashes = scene_cache_port.get_all_hashes()
for scene_id, stored_hash in all_hashes.items():
    current_hash = compute_current_hash(scene_id)
    if stored_hash != current_hash:
        scenes_to_render.append(scene_id)
```

---

### invalidate_scene_cache(scene_id: int) -> None

**What it does:**
Deletes the stored hash for ONE specific scene.
After this call, `get_scene_hash(scene_id)` returns `None`.
This forces the next render of this scene to actually run Manim,
regardless of whether the code file changed.

**When it is called:**
When the user runs `force render scene 3` — the cache for scene 3
is invalidated first, then the render runs unconditionally.
Also called when an asset file changes (image, font) but the code
file itself did not change. The fingerprint would say "unchanged"
but the output would be different.

---

### invalidate_all_caches() -> None

**What it does:**
Deletes the stored hash for EVERY scene in the project.
After this, every single scene will be rendered on the next `render all`.

**When it is called:**
When the user runs `force render all` — every cache is cleared,
then every scene is rendered from scratch.
Also called when a global setting changes (like resolution or fps)
that would affect the output of every scene.

---

### get_scenes_with_changed_hashes(current_hashes: dict[int, str]) -> list[int]

**What it does:**
Takes a dictionary of CURRENT hashes (just computed from the code files)
and compares them all to the STORED hashes in the database.
Returns a list of `scene_id` values for scenes whose code has changed
(or was never rendered).

**Why it exists:**
This is the "batch comparison" function for `render all`.
Instead of looping through scenes one by one and calling `hash_has_changed`
for each one, you pass all current hashes at once and get back the list
of scenes that need rendering. One database round-trip instead of N.

**What it returns:**
A list of `scene_id` integers for scenes that need re-rendering.

**Example:**
```python
# current_hashes computed by reading all code files
current_hashes = {
    1: "a3f8c2d1...",   # same as stored -> skip
    2: "CHANGED!!!",    # different from stored -> render
    3: "f7c3a9e1...",   # same as stored -> skip
    4: None,            # no code file yet -> skip
    5: "d8b1c4e9...",   # never rendered (no stored hash) -> render
}

scenes_to_render = scene_cache_port.get_scenes_with_changed_hashes(current_hashes)
# returns [2, 5]
```

---

# PART 9 — PORT 5: SceneUtilityPort

## What Is It?

`SceneUtilityPort` handles the housekeeping functions — operations that
do not fit cleanly into reading, writing, or status management.
These are the "miscellaneous but important" functions: swapping scenes,
duplicating scenes, getting summary statistics, and backup/restore.

```
+=====================================================================+
|                      SceneUtilityPort                               |
+=====================================================================+
|                                                                     |
|   File:    core/ports/scene_utility_port.py                         |
|   Adapter: adapters/repositories/sqlite_scene_repository.py        |
|                                                                     |
|   Services that use this port:                                      |
|     SceneLifecycleService    (swap, duplicate, summarize)           |
|     ProjectExportService     (export/import for backup)             |
|     ValidationService        (validate video paths, summarize)      |
|                                                                     |
+=====================================================================+
```

## The Python Interface

```python
# core/ports/scene_utility_port.py

from abc import ABC, abstractmethod
from core.entities.scene import Scene


class SceneUtilityPort(ABC):
    """
    Utility operations on scenes: structural changes, summaries, backup.
    """

    @abstractmethod
    def get_last_rendered_scene(self) -> Scene | None: ...

    @abstractmethod
    def get_next_scene_id(self) -> int: ...

    @abstractmethod
    def swap_scenes(self, scene_id_a: int,
                    scene_id_b: int) -> None: ...

    @abstractmethod
    def duplicate_scene(self, scene_id: int) -> Scene: ...

    @abstractmethod
    def get_render_summary(self) -> dict: ...

    @abstractmethod
    def validate_all_video_paths(self) -> dict[int, bool]: ...

    @abstractmethod
    def export_to_dict(self) -> dict: ...

    @abstractmethod
    def import_from_dict(self, data: dict) -> None: ...
```

## Every Function Explained

---

### get_last_rendered_scene() -> Scene | None

**What it does:**
Finds and returns the scene that was rendered most recently,
based on the `scene_rendered_at` timestamp.
Returns `None` if no scenes have been rendered yet.

**When it is called:**
For informational display — showing the user which scene was
most recently updated. Also useful for resuming work after reopening
a project: "You last rendered Scene 4 on November 12."

---

### get_next_scene_id() -> int

**What it does:**
Returns the integer ID that should be used for the next new scene.
This is always `max(existing_scene_ids) + 1`.
If no scenes exist yet, it returns `1`.

**When it is called:**
By `SceneLifecycleService.add_scene()` to assign a new ID before
creating the scene object.

**Why this matters:**
Scene IDs must be unique. This function ensures the system never
assigns the same ID twice, even if scenes were deleted in between.
If scenes 1, 2, 3, 5 exist (scene 4 was deleted), the next ID is 6
— not 4. Deleted IDs are never reused, because files and folders
on disk were named after those IDs.

**Example:**
```python
new_id = scene_utility_port.get_next_scene_id()
new_scene = Scene(scene_id=new_id)
```

---

### swap_scenes(scene_id_a: int, scene_id_b: int) -> None

**What it does:**
Exchanges the `scene_index` values of two scenes.
Scene A goes to where Scene B was, and Scene B goes to where Scene A was.
No other data changes. The IDs stay the same. Only the position changes.
This is done atomically — both updates happen in one transaction.

**When it is called:**
When the user types `swap scenes 2 4`.

**Example:**
```python
# Before: Scene 2 is at index 1, Scene 4 is at index 3
scene_utility_port.swap_scenes(2, 4)
# After: Scene 2 is at index 3, Scene 4 is at index 1
```

---

### duplicate_scene(scene_id: int) -> Scene

**What it does:**
Creates a complete copy of the specified scene and inserts it as a
new scene at the end of the project.

The copy gets:
- A new `scene_id` (the next available ID)
- The same `scene_code_path` as the original
- The same `scene_duration` as the original
- `scene_status = "pending"` (reset — it has never been rendered)
- `audio_clip_path = None` (audio must be reassigned separately)
- `synced_with_audio = False`
- `scene_hash = None` (no fingerprint yet)

**When it is called:**
When the user types `duplicate scene 3`.
Useful when two scenes use the same Manim code as a starting point
and you want to make a copy before customizing one of them.

**What it returns:**
The new `Scene` object so the caller can display confirmation.

---

### get_render_summary() -> dict

**What it does:**
Returns a dictionary with the current render statistics for the project.
This is one fast database query instead of multiple filtered queries.

**What it returns:**
```python
{
    "total":    5,    # total number of scenes
    "rendered": 3,    # scenes with status "rendered"
    "pending":  1,    # scenes with status "pending"
    "failed":   1,    # scenes with status "failed"
    "skipped":  0,    # scenes with status "skipped"
    "ready_to_export": False  # True only if all are "rendered"
}
```

**When it is called:**
By `render status` command, by `project info`, by `status` command.
Any time the system needs to display the current render state of the project.

---

### validate_all_video_paths() -> dict[int, bool]

**What it does:**
Checks whether the video file actually EXISTS on disk for every
scene that has `scene_status = "rendered"`.

Returns a dictionary mapping `scene_id` to `True` (file exists) or
`False` (file is missing).

**Why this matters:**
The database says a scene is "rendered" and stores a video path.
But what if someone accidentally deleted the file from the `output/`
folder? The database still says "rendered" but there is no file.
This function catches exactly that problem.

**When it is called:**
By `validate project` command.
By `export` command before assembling the final video — if any
rendered scene's video file is missing, the export stops immediately
and reports which scenes are missing.

**Example:**
```python
results = scene_utility_port.validate_all_video_paths()
# {1: True, 2: True, 3: False, 4: True, 5: True}
# Scene 3's video file was deleted — export would fail
```

---

### export_to_dict() -> dict

**What it does:**
Serializes ALL scene data into a plain Python dictionary.
Every scene's every field is included.
This dictionary can be converted to JSON for backup or migration purposes.

**When it is called:**
When backing up a project.
When migrating a project from one machine to another.
When exporting project state for debugging.

**What it returns:**
```python
{
    "scenes": [
        {
            "scene_id": 1,
            "scene_name": "Introduction",
            "scene_duration": 12500,
            "scene_status": "rendered",
            ...all other fields...
        },
        {
            "scene_id": 2,
            ...
        },
        ...
    ],
    "exported_at": "2024-11-12 14:30:00"
}
```

---

### import_from_dict(data: dict) -> None

**What it does:**
Restores all scene data from a dictionary that was previously created
by `export_to_dict()`. This is the RESTORE operation for backup/migration.

**When it is called:**
When restoring a backed-up project.
When importing a project from another machine.

**Important:**
This REPLACES all existing scene data. It is not a merge.
Before calling this, the system should call `delete_all_scenes()` to
ensure a clean state.

---

# PART 10 — COMPLETE PICTURE: ALL 5 PORTS AND THE ADAPTER

```
+=====================================================================+
|          THE COMPLETE 5-PORT ARCHITECTURE FOR SCENES                |
+=====================================================================+
|                                                                     |
|   CORE (the business logic — never touches SQLite)                  |
|   |                                                                 |
|   +-- SceneLifecycleService                                         |
|   |     uses: SceneWritePort, SceneReadPort, SceneUtilityPort       |
|   |                                                                 |
|   +-- RenderPipelineService                                         |
|   |     uses: SceneReadPort, SceneStatusPort, SceneCachePort        |
|   |                                                                 |
|   +-- RenderCacheService                                            |
|   |     uses: SceneCachePort                                        |
|   |                                                                 |
|   +-- AudioPreparationService                                       |
|   |     uses: SceneReadPort, SceneWritePort                         |
|   |                                                                 |
|   +-- TimelineCoordinatorService                                    |
|   |     uses: SceneReadPort, SceneWritePort                         |
|   |                                                                 |
|   +-- PreviewGenerationService                                      |
|   |     uses: SceneReadPort, SceneStatusPort                        |
|   |                                                                 |
|   +-- ProjectExportService                                          |
|   |     uses: SceneReadPort, SceneUtilityPort                       |
|   |                                                                 |
|   +-- ValidationService                                             |
|         uses: SceneReadPort, SceneUtilityPort                       |
|                                                                     |
|   THE 5 PORTS (interfaces — define the contract)                    |
|   |                                                                 |
|   +-- SceneWritePort   (10 functions)                               |
|   +-- SceneReadPort    (13 functions)                               |
|   +-- SceneStatusPort  (9 functions)                                |
|   +-- SceneCachePort   (6 functions)                                |
|   +-- SceneUtilityPort (8 functions)                                |
|         TOTAL: 46 functions                                         |
|                                                                     |
|   THE 1 ADAPTER (implements all 5 ports)                            |
|   |                                                                 |
|   +-- SqliteSceneRepository                                         |
|         inherits from all 5 ports                                   |
|         implements all 46 functions                                 |
|         is the ONLY place in the codebase with SQL for scenes       |
|         lives in: adapters/repositories/sqlite_scene_repository.py  |
|                                                                     |
+=====================================================================+
```

---

# PART 11 — COMPLETE FUNCTION COUNT TABLE

```
+================================================================+
|          ALL FUNCTIONS ACROSS ALL 5 PORTS                      |
+================================================================+
|                                                                |
|   PORT 1: SceneWritePort (10 functions)                        |
|   ─────────────────────────────────────────────────────────── |
|   save_scene()                                                 |
|   delete_scene()                                               |
|   delete_all_scenes()                                          |
|   update_scene_duration()                                      |
|   update_scene_code_path()                                     |
|   update_scene_video_path()                                    |
|   update_scene_audio_path()                                    |
|   update_scene_audio_range()                                   |
|   save_all_scenes()                                            |
|   reorder_scenes()                                             |
|                                                                |
|   PORT 2: SceneReadPort (13 functions)                         |
|   ─────────────────────────────────────────────────────────── |
|   load_scene()                                                 |
|   scene_exists()                                               |
|   load_all_scenes()                                            |
|   count_scenes()                                               |
|   get_scenes_by_status()                                       |
|   get_rendered_scenes()                                        |
|   get_pending_scenes()                                         |
|   get_failed_scenes()                                          |
|   get_scenes_in_range()                                        |
|   get_scenes_without_code()                                    |
|   get_scenes_without_audio()                                   |
|   get_total_duration_ms()                                      |
|   get_scenes_modified_since()                                  |
|                                                                |
|   PORT 3: SceneStatusPort (9 functions)                        |
|   ─────────────────────────────────────────────────────────── |
|   mark_as_rendered()                                           |
|   mark_as_failed()                                             |
|   mark_as_pending()                                            |
|   mark_as_skipped()                                            |
|   mark_all_as_pending()                                        |
|   reset_render_status_for_scenes()                             |
|   clear_error()                                                |
|   update_scene_hash()                                          |
|   update_preview_path()                                        |
|                                                                |
|   PORT 4: SceneCachePort (6 functions)                         |
|   ─────────────────────────────────────────────────────────── |
|   get_scene_hash()                                             |
|   hash_has_changed()                                           |
|   get_all_hashes()                                             |
|   invalidate_scene_cache()                                     |
|   invalidate_all_caches()                                      |
|   get_scenes_with_changed_hashes()                             |
|                                                                |
|   PORT 5: SceneUtilityPort (8 functions)                       |
|   ─────────────────────────────────────────────────────────── |
|   get_last_rendered_scene()                                    |
|   get_next_scene_id()                                          |
|   swap_scenes()                                                |
|   duplicate_scene()                                            |
|   get_render_summary()                                         |
|   validate_all_video_paths()                                   |
|   export_to_dict()                                             |
|   import_from_dict()                                           |
|                                                                |
|   TOTAL: 46 functions across 5 ports                           |
|                                                                |
+================================================================+
```

---

# PART 12 — FINAL ANSWER TO YOUR QUESTION

```
+================================================================+
|                                                                |
|   Should you use ONE port or MANY ports?                       |
|                                                                |
|   ANSWER: Use 5 ports.                                         |
|                                                                |
|   SceneWritePort    - create and update scene records          |
|   SceneReadPort     - read and query scene records             |
|   SceneStatusPort   - manage render status and output fields   |
|   SceneCachePort    - manage hash fingerprints                 |
|   SceneUtilityPort  - housekeeping, swap, backup               |
|                                                                |
|   Should you use ONE adapter or MANY adapters?                 |
|                                                                |
|   ANSWER: Use ONE adapter.                                     |
|   SqliteSceneRepository implements ALL 5 ports.                |
|   It is the only file that writes SQL for scenes.              |
|                                                                |
|   TOTAL FUNCTIONS: 46                                          |
|   (43 from your original document + 3 new ones added here)    |
|                                                                |
|   NEW FUNCTIONS ADDED:                                         |
|   mark_as_skipped()          - missing from original           |
|   get_scenes_with_changed_hashes() - batch optimization        |
|   update_preview_path()      - for preview workflow            |
|                                                                |
+================================================================+
```





























































**The explanation of each category and its own functions:**
Category 1 — CRUD
==================
These are the most fundamental operations. Every data system needs them: Create, Read, Update, Delete.

`save_scene(scene)`

**What it does:**
Takes a `Scene` object and saves it to storage. If this scene ID already exists,
it updates the existing record. If it does not exist yet, it creates a new one.
This is a single function that handles both "new" and "update"
you do not need a separate `create_scene()` and `update_scene()`.

**When the Core calls it:**
- When the user runs `add scene` — a new Scene object is created and saved.
- When the user runs `set scene 3 duration 12.5` — the scene is loaded,
  its duration is changed, and it is saved back.
- After any change to a scene's data.

**What it takes:**
- `scene` — a `Scene` data object containing all the scene's fields
 (ID, duration, code path, hash, status, video path, audio path, etc.)

**What it returns:**
- Nothing. It either succeeds or raises an exception.

**Example:**
```python
scene = Scene(id=3, duration=12.5, code_path="scenes/scene_03/scene.py")
scene_repo.save_scene(scene)
```

---

 `load_scene(scene_id)`

**What it does:**
Reads one scene from storage by its ID number and returns it as a `Scene` object.

**When the Core calls it:**
- When the user runs `render scene 3` — the Core loads Scene 3 to get its code path and duration.
- When the user runs `scene info 3` — the Core loads Scene 3 to display its details.
- Before any operation that needs to read a scene's current data.

**What it takes:**
- `scene_id` — an integer. For example, `3` for Scene 3.

**What it returns:**
- A `Scene` object with all fields populated.
- Raises `SceneNotFoundError` if no scene with this ID exists.

**Example:**
```python
scene = scene_repo.load_scene(3)
print(scene.duration)     # 12.5
print(scene.status)       # "pending"
print(scene.code_path)    # "scenes/scene_03/scene.py"
```

---

 `scene_exists(scene_id)`

**What it does:**
Returns `True` if a scene with this ID exists in storage. Returns `False` if it does not.
This is a safe check that never raises an exception.

**When the Core calls it:**
- Before calling `load_scene()` to avoid getting an exception on a scene that does not exist.
- When the user types `render scene 7` but the project only has 5 scenes — the Core checks `scene_exists(7)`
  first and gives a clear error message.
- Before any operation that targets a specific scene ID.

**Why this is separate from `load_scene()`:**
Because sometimes you want to check without loading. If you call `load_scene()` on a missing scene,
you get an exception. If you call `scene_exists()`, you get a clean True/False answer.

**What it takes:**
- `scene_id` — an integer.

**What it returns:**
- `True` if the scene exists.
- `False` if it does not.

**Example:**
```python
if scene_repo.scene_exists(7):
    scene = scene_repo.load_scene(7)
else:
    notifier.send_error("Scene 7 does not exist in this project.")
```

---

 `delete_scene(scene_id)`

**What it does:**
Permanently removes the scene record with this ID from storage. This only removes the database record
it does not delete any files on disk (code files, video files, audio files).
File deletion is handled by `FileStoragePort`.

**When the Core calls it:**
- When the user runs `delete scene 3`.
- When a scene is being replaced or the project is being restructured.

**What it takes:**
- `scene_id` — an integer.

**What it returns:**
- Nothing. Raises `SceneNotFoundError` if the scene does not exist.

**Example:**
```python
scene_repo.delete_scene(3)
```

---

 `delete_all_scenes()`

**What it does:**
Permanently removes every scene record in this project from storage. This is a complete wipe of all scene data.
Like `delete_scene()`, it does not delete files — only records.

**When the Core calls it:**
- When the user deletes the entire project.
- When the user wants to reset a project and start the scenes from scratch.

**What it takes:**
- Nothing.

**What it returns:**
- Nothing.

**Example:**
```python
scene_repo.delete_all_scenes()
# After this, all_scenes() returns an empty list
```

---

Category 2 — QUERY
==================
These functions read multiple scenes at once, with various filters. The Core uses them to answer questions
like "which scenes need rendering?" or "how many scenes are done?"

---

 `all_scenes()`

**What it does:**
Returns every scene in the project as a list of `Scene` objects, sorted by scene number in ascending order
(Scene 1 first, Scene 2 second, etc.).

**When the Core calls it:**
- When the user runs `list scenes` — to display all scenes and their statuses.
- When the Core needs to process every scene — for example, to check all hashes before a render.
- When assembling the final video — to get all scenes in the correct order.

**What it takes:**
- Nothing.

**What it returns:**
- A list of `Scene` objects, ordered by ID. Returns an empty list if no scenes exist.

**Example:**
```python
scenes = scene_repo.all_scenes()
for scene in scenes:
    print(f"Scene {scene.id}: {scene.status}")
```

---

 `count_scenes()`

**What it does:**
Returns the total number of scenes in the project as an integer. This is much faster than calling `all_scenes()`
and checking the length, because it asks the database to count rows without loading all the data.

**When the Core calls it:**
- When displaying project summary information ("This project has 8 scenes").
- When validating that the number of scenes matches the expected count.
- Before any loop that iterates over scene IDs, to know where to stop.

**What it takes:**
- Nothing.

**What it returns:**
- An integer. Returns `0` if no scenes exist.

**Example:**
```python
total = scene_repo.count_scenes()
print(f"This project has {total} scenes.")
```

---

`get_scenes_by_status(status)`

**What it does:**
Returns a filtered list of scenes whose status matches the given value.
The t valid status values are `"pending"`, `"rendered"`, and `"failed"`.

**When the Core calls it:**
- When the user runs `render changed` — the Core needs all `"pending"` scenes.
- When the user runs `show failed scenes` — the Core needs all `"failed"` scenes.

**What it takes:**
- `status` — a string: `"pending"`, `"rendered"`, or `"failed"`.

**What it returns:**
- A list of `Scene` objects matching that status. Returns an empty list if none match.

**Example:**
```python
failed = scene_repo.get_scenes_by_status("failed")
for scene in failed:
    print(f"Scene {scene.id} failed: {scene.error_message}")
```

---

 `get_rendered_scenes()`

**What it does:**
A convenient shortcut for `get_scenes_by_status("rendered")`. Returns all scenes that have been successfully
rendered and have a valid video file path stored.

**When the Core calls it:**
- When assembling the final video — the Core needs the list of rendered clips in order.
- When displaying progress — "7 out of 8 scenes are rendered."

**What it takes:**
- Nothing.

**What it returns:**
- A list of `Scene` objects where `status == "rendered"`.

---

 `get_pending_scenes()`

**What it does:**
A convenient shortcut for `get_scenes_by_status("pending")`. Returns all scenes that have not been rendered
yet and are waiting to be processed.

**When the Core calls it:**
- When the user runs `render all` — the Core gets all pending scenes and renders them one by one.
- When checking if there is any work left to do before export.

**What it takes:**
- Nothing.

**What it returns:**
- A list of `Scene` objects where `status == "pending"`.

---

 `get_failed_scenes()`

**What it does:**
A convenient shortcut for `get_scenes_by_status("failed")`. Returns all scenes where the last render attempt
failed and an error message was recorded.

**When the Core calls it:**
- When the user runs `retry failed` — the Core gets all failed scenes and tries to render them again.
- When generating an error report at the end of a render session.

**What it takes:**
- Nothing.

**What it returns:**
- A list of `Scene` objects where `status == "failed"`.

---

 `get_scenes_in_range(start_id, end_id)`

**What it does:**
Returns all scenes whose ID falls between `start_id` and `end_id`, inclusive. Useful for partial operations
— for example, only rendering scenes 3 through 7.

**When the Core calls it:**
- When the user runs `render scenes 3 to 7`.
- When exporting only a portion of the project for a quick preview.

**What it takes:**
- `start_id` — the first scene ID in the range.
- `end_id` — the last scene ID in the range (inclusive).

**What it returns:**
- A list of `Scene` objects in that range, ordered by ID.

**Example:**
```python
scenes = scene_repo.get_scenes_in_range(3, 7)
# Returns scenes 3, 4, 5, 6, 7
```

---

`get_scenes_without_code()`

**What it does:**
Returns all scenes that have no Python code file assigned yet. A scene without code cannot be rendered.
This function helps the Core validate that the project is ready before starting a render.

**When the Core calls it:**
- Before `render all` — the Core calls this to check if any scene is missing its code file.If any are missing,
  it reports them to the user instead of starting a render that will fail halfway through.
- When the user runs `validate project`.

**What it takes:**
- Nothing.

**What it returns:**
- A list of `Scene` objects where `code_path` is `None` or empty.

---

 `get_scenes_without_audio()`

**What it does:**
Returns all scenes that have no audio clip assigned. In `supermanim` mode, every scene must have an audio clip.
This function lets the Core detect which scenes are missing their audio before rendering begins.

**When the Core calls it:**
- In `supermanim` mode, before any render — to validate that the audio plan is complete.
- When the user runs `audio status` — to show which scenes still need audio assigned.

**What it takes:**
- Nothing.

**What it returns:**
- A list of `Scene` objects where `audio_path` is `None` or empty.

---

Category 3 — STATUS
====================
These functions update specific fields on a scene. The Core uses them to record what happened after each step of the render pipeline. Instead of loading a full scene, changing one field, and saving it back, these functions update only the field that changed — which is faster and safer.

---

`mark_as_rendered(scene_id, video_path)`

**What it does:**
Sets a scene's status to `"rendered"`, stores the path to the output video file,
and records the current timestamp as the render completion time.

**When the Core calls it:**
- Immediately after a scene renders successfully.

**What it takes:**
- `scene_id` — the scene that was rendered.
- `video_path` — the full path to the rendered `.mp4` file.

**What it returns:**
- Nothing.

**Example:**
```python
scene_repo.mark_as_rendered(3, "output/scene_03/scene_03.mp4")
```

---

`mark_as_failed(scene_id, error_message)`

**What it does:**
Sets a scene's status to `"failed"` and stores the error message so the user can read what went wrong.

**When the Core calls it:**
- When Manim returns a non-zero exit code (render error).
- When a code file cannot be found before rendering starts.
- When any exception is caught during the render process.

**What it takes:**
- `scene_id` — the scene that failed.
- `error_message` — a string describing what went wrong. Can be a Manim error, a Python traceback summary, or a custom message.

**What it returns:**
- Nothing.

**Example:**
```python
scene_repo.mark_as_failed(3, "Manim exited with code 1: NameError on line 42")
```

---

 `mark_as_pending(scene_id)`

**What it does:**
Resets a scene's status back to `"pending"`. This clears the video path, clears the error message,
and resets the render timestamp. The scene is now treated as if it has never been rendered.

**When the Core calls it:**
- When the user edits a scene's code file — the hash will change, so the scene must be re-rendered.
- When the user manually requests a scene to be re-rendered even if nothing changed.
- When clearing a failed scene's status before retrying.

**What it takes:**
- `scene_id` — an integer.

**What it returns:**
- Nothing.

---

 `mark_all_as_pending()`

**What it does:**
Resets every scene in the project back to `"pending"` in a single operation. Clears all video paths,
error messages, and render timestamps for all scenes.

**When the Core calls it:**
- When the user runs `force render all` — this command ignores the cache and re-renders everything from scratch.
- When global settings change that affect all scenes (for example, changing the frame rate).

**What it takes:**
- Nothing.

**What it returns:**
- Nothing.

---

`update_scene_hash(scene_id, new_hash)`

**What it does:**
Stores a new code fingerprint for this scene. This fingerprint is a SHA-256 hash of the scene's Python code file.
It is computed fresh every time and stored here so that the next run can compare it to detect whether the code
changed.

**When the Core calls it:**
- After a scene is successfully rendered — the current hash is stored so it can be compared next time.
- After the code file is first assigned to a scene.

**What it takes:**
- `scene_id` — an integer.
- `new_hash` — a 64-character SHA-256 hash string.

**What it returns:**
- Nothing.

**Example:**
```python
scene_repo.update_scene_hash(3, "a3f8c2d1e4b9...")
```

---

`update_scene_duration(scene_id, new_duration)`

**What it does:**
Updates only the duration field of a scene, without touching any other data.

**When the Core calls it:**
- When the user runs `set scene 3 duration 14.0`.
- When audio analysis automatically corrects a scene's duration to match its audio clip.
- After the user splits or resizes audio clips, which may change a scene's required duration.

**What it takes:**
- `scene_id` — an integer.
- `new_duration` — a float representing seconds. Example: `14.0`.

**What it returns:**
- Nothing.

---

 `update_scene_code_path(scene_id, new_path)`

**What it does:**
Updates the stored path to the scene's Python code file, without touching any other data.

**When the Core calls it:**
- When the user runs `set scene 3 code path/to/new_code.py`.
- When the project folder is moved and all paths need to be updated.
- When a code file is renamed or relocated.

**What it takes:**
- `scene_id` — an integer.
- `new_path` — a string with the new file path.

**What it returns:**
- Nothing.

---

 `update_scene_video_path(scene_id, new_path)`

**What it does:**
Updates the stored path to the scene's rendered video output file.

**When the Core calls it:**
- When a rendered video file is moved to a different location after rendering.
- When the project output folder is reorganized.

**What it takes:**
- `scene_id` — an integer.
- `new_path` — a string with the new file path.

**What it returns:**
- Nothing.

---

 `update_scene_audio_path(scene_id, audio_path)`

**What it does:**
Assigns or updates the path to the audio clip file that belongs to this scene.

**When the Core calls it:**
- After the main audio file is split into clips — each clip's path is assigned to its scene.
- When the user manually assigns a different audio clip to a scene.

**What it takes:**
- `scene_id` — an integer.
- `audio_path` — a string with the path to the `.mp3` or `.wav` audio clip file.

**What it returns:**
- Nothing.

---

 `update_scene_audio_range(scene_id, start_seconds, end_seconds)`

**What it does:**
Stores the start and end time (in seconds) within the original full-length audio file that corresponds
to this scene's audio clip. For example, Scene 3 might cover seconds 31.0 to 47.8 of the narration.

**When the Core calls it:**
- After the audio timeline is planned — either automatically (through silence detection) or manually (through the user's input).
- When the user reassigns audio boundaries with `map audio scene 3 31.0 47.8`.

**What it takes:**
- `scene_id` — an integer.
- `start_seconds` — a float. The start time in the original audio file.
- `end_seconds` — a float. The end time in the original audio file.

**What it returns:**
- Nothing.

**Example:**
```python
scene_repo.update_scene_audio_range(3, 31.0, 47.8)
```

---

 `clear_error(scene_id)`

**What it does:**
Erases the stored error message on a failed scene, without changing any other field.
Typically called before retrying a render so that old error messages do not persist.

**When the Core calls it:**
- Before retrying a failed scene — the old error is cleared first so that if the retry also fails,
  the new error message is stored cleanly.

**What it takes:**
- `scene_id` — an integer.

**What it returns:**
- Nothing.

---

---

Category 4 — BULK
================
These functions operate on many scenes at once in a single, efficient database operation.
They are faster and safer than calling individual functions in a loop, because they run as
a single atomic transaction.

---

 `save_all_scenes(scenes_list)`

**What it does:**
Takes a list of `Scene` objects and saves all of them in one single database transaction.
If any one fails, none of them are saved (atomic operation). This is much faster than calling
`save_scene()` in a for-loop.

**When the Core calls it:**
- When the project is first set up and all scenes are created at once.
- When importing a project from a backup file.
- When a bulk edit changes many scenes at the same time.

**What it takes:**
- `scenes_list` — a Python list of `Scene` objects.

**What it returns:**
- Nothing.

**Example:**
```python
scenes = [Scene(id=1, duration=12.5), Scene(id=2, duration=8.0), Scene(id=3, duration=15.0)]
scene_repo.save_all_scenes(scenes)
```

---

 `reorder_scenes(new_order_list)`

**What it does:**
Takes a list of scene IDs in the new desired order and updates all scene numbers at once.
For example, if you pass `[3, 1, 2]`, Scene 3 becomes the first scene, Scene 1 becomes the second,
and Scene 2 becomes the third. This is done in one atomic operation.

**When the Core calls it:**
- When the user reorders scenes with a command like `move scene 3 to position 1`.
- When the user drag-and-drops scenes in a GUI.

**What it takes:**
- `new_order_list` — a list of scene IDs in the desired new order.

**What it returns:**
- Nothing.

**Example:**
```python
# Move scene 3 to first position
scene_repo.reorder_scenes([3, 1, 2, 4, 5])
```

---

 `reset_render_status_for_scenes(scene_ids)`

**What it does:**
Marks a specific list of scenes (given by their IDs) back to `"pending"` in one database call.
More efficient than calling `mark_as_pending()` in a loop.

**When the Core calls it:**
- When the hash check at the start of a render run finds that specific scenes have changed —
  those scenes are reset to `"pending"` in one batch call.
- When the user runs `invalidate scenes 2 3 5` to force specific scenes to re-render.

**What it takes:**
- `scene_ids` — a list of integers. Example: `[2, 3, 5]`.

**What it returns:**
- Nothing.

**Example:**
```python
changed_scene_ids = [2, 5, 8]
scene_repo.reset_render_status_for_scenes(changed_scene_ids)
```

---

 `get_total_duration()`

**What it does:**
Adds up the duration fields of every scene and returns the total in seconds.
This is calculated in the database, not by loading all scenes into Python and summing them.

**When the Core calls it:**
- After the audio timeline is set up — to verify that the sum of all scene durations equals the total audio length.
- When displaying project summary information ("Total video length: 60.0 seconds").
- Before final assembly, to confirm the total video duration is correct.

**What it takes:**
- Nothing.

**What it returns:**
- A float representing the total duration in seconds.

**Example:**
```python
total = scene_repo.get_total_duration()
print(f"Total video will be {total} seconds long.")
# Output: Total video will be 60.0 seconds long.
```

---

 `get_scenes_changed_since(timestamp)`

**What it does:**
Returns all scenes whose `last_modified` field is newer than the given timestamp.
This allows the Core to quickly find which scenes were edited since the last render,
without having to compute and compare hashes for every single scene.

**When the Core calls it:**
- As a fast first-pass filter before the hash check — if a scene's `last_modified` time is the same as last time, it definitely has not changed and does not even need a hash comparison.
- When generating a change report: "These scenes were modified in the last hour."

**What it takes:**
- `timestamp` — a Python `datetime` object representing the cutoff time.

**What it returns:**
- A list of `Scene` objects whose `last_modified` is after the given timestamp.

**Example:**
```python
from datetime import datetime, timedelta
one_hour_ago = datetime.now() - timedelta(hours=1)
recent_changes = scene_repo.get_scenes_changed_since(one_hour_ago)
```

---
Category 5 — CACHE / HASH
===========================
These functions are the technical foundation of SuperManim's smart-skip feature. They manage the code fingerprints (hashes) stored for each scene, which the Core uses to decide whether a scene needs to be re-rendered.

---

 `get_scene_hash(scene_id)`

**What it does:**
Returns the stored SHA-256 hash (code fingerprint) for this scene. This is the hash that was saved after
the last successful render. If this scene has never been rendered, returns `None`.

**When the Core calls it:**
- At the start of a render run, for each scene — to compare the stored hash against a freshly computed one.

**What it takes:**
- `scene_id` — an integer.

**What it returns:**
- A 64-character hash string if the scene has been rendered before.
- `None` if the scene has never been rendered.

**Example:**
```python
stored_hash = scene_repo.get_scene_hash(3)
if stored_hash is None:
    print("Scene 3 has never been rendered.")
```

---

 `hash_has_changed(scene_id, current_hash)`

**What it does:**
Compares the given `current_hash` (just computed from the scene's code file right now) against
the stored hash (from the last render).
Returns `True` if they are different — meaning the code changed and the scene needs to be re-rendered.
Returns `False` if they are the same — meaning the code is unchanged and the scene can be skipped.

**When the Core calls it:**
- For every scene at the start of a render run. This is the core decision function for smart-skip.

**What it takes:**
- `scene_id` — an integer.
- `current_hash` — a freshly computed SHA-256 hash string of the scene's current code file.

**What it returns:**
- `True` if the stored hash differs from `current_hash` (scene changed, must render).
- `False` if they match (scene unchanged, can skip).
- `True` if no hash is stored yet (scene never rendered, must render).

**Example:**
```python
fresh_hash = hash_computer.hash_file(scene.code_path)
if scene_repo.hash_has_changed(scene.id, fresh_hash):
    renderer.render(scene)
else:
    notifier.send_info(f"Scene {scene.id} unchanged. Skipping.")
```

---

 `get_all_hashes()`

**What it does:**
Returns a dictionary of every scene's stored hash in one single database query. The dictionary key is the scene ID, and the value is the stored hash string.

**When the Core calls it:**
- At the very start of a render run — instead of making one database query per scene to get its hash, the Core makes one single call to get all hashes at once. This is much faster for projects with many scenes.

**What it takes:**
- Nothing.

**What it returns:**
- A dictionary: `{scene_id: hash_string}`. Example: `{1: "a3f8c...", 2: "b7d4e...", 3: None}`. Scenes that have never been rendered have `None` as their value.

**Example:**
```python
all_stored_hashes = scene_repo.get_all_hashes()
# {1: "a3f8c2d1...", 2: "b7d4e9f2...", 3: None, 4: "c9a1b3e7..."}

for scene in all_scenes:
    fresh_hash = hash_computer.hash_file(scene.code_path)
    stored_hash = all_stored_hashes.get(scene.id)
    if fresh_hash != stored_hash:
        scenes_to_render.append(scene)
```

---

### `invalidate_scene_cache(scene_id)`

**What it does:**
Deletes the stored hash for one scene, effectively forcing it to be re-rendered on the next run regardless of whether its code changed. The scene's status is also reset to `"pending"`.

**When the Core calls it:**
- When the user explicitly requests a specific scene to be re-rendered even if nothing changed.
- When a file that the scene depends on (like an asset image) changes, but the scene's Python code itself did not change.

**What it takes:**
- `scene_id` — an integer.

**What it returns:**
- Nothing.

**Example:**
```python
scene_repo.invalidate_scene_cache(3)
# Scene 3 will now be rendered on the next run, no matter what.
```

---

### `invalidate_all_caches()`

**What it does:**
Deletes the stored hash for every scene in the project in one operation. Resets all scenes to `"pending"`. The next render run will re-render every single scene from scratch.

**When the Core calls it:**
- When the user runs `force render all`.
- When global render settings change (for example, the output resolution or frame rate) — because those changes affect all scenes even if the code did not change.
- When the user explicitly wants a full clean rebuild.

**What it takes:**
- Nothing.

**What it returns:**
- Nothing.

---

---

# Category 6 — UTILITY

These functions handle edge cases, housekeeping, and introspection. They are called less frequently than the other categories but are essential for a complete, production-ready system.

---

### `get_last_rendered_scene()`

**What it does:**
Returns the scene that was most recently rendered, based on the `rendered_at` timestamp stored when `mark_as_rendered()` was called. If no scenes have ever been rendered, returns `None`.

**When the Core calls it:**
- When resuming a render session that was interrupted — the Core finds the last scene that completed successfully and knows where to continue from.
- When displaying a status message like "Last rendered: Scene 5 at 3:42pm."

**What it takes:**
- Nothing.

**What it returns:**
- A `Scene` object for the most recently rendered scene.
- `None` if no scenes have been rendered yet.

---

### `get_next_scene_id()`

**What it does:**
Returns the integer ID that should be used for the next new scene. This is typically the highest existing scene ID plus one. For example, if the project has scenes 1, 2, 3, this returns `4`.

**When the Core calls it:**
- Every time the user runs `add scene` — before creating the new Scene object, the Core asks for the next available ID.

**What it takes:**
- Nothing.

**What it returns:**
- An integer. Returns `1` if no scenes exist yet.

**Example:**
```python
new_id = scene_repo.get_next_scene_id()
new_scene = Scene(id=new_id, duration=10.0)
scene_repo.save_scene(new_scene)
```

---

### `swap_scenes(scene_id_a, scene_id_b)`

**What it does:**
Swaps the positions of two scenes in the sequence. After the swap, the scene that was at position A is now at position B, and vice versa. Done in one atomic operation.

**When the Core calls it:**
- When the user runs `swap scene 2 and scene 4`.
- When a GUI allows the user to click two scenes and swap them.

**What it takes:**
- `scene_id_a` — the ID of the first scene.
- `scene_id_b` — the ID of the second scene.

**What it returns:**
- Nothing.

**Example:**
```python
scene_repo.swap_scenes(2, 4)
# Scene 2 is now where Scene 4 was, and vice versa.
```

---

### `duplicate_scene(scene_id)`

**What it does:**
Creates a new scene that is an exact copy of an existing one. The new scene gets the next available ID. Its status is reset to `"pending"`, its video path is cleared, and its error message is cleared — because it has not been rendered yet. All other fields (duration, code path, audio path, hash) are copied.

**When the Core calls it:**
- When the user runs `duplicate scene 3` — useful when multiple scenes use the same code with slight variations.

**What it takes:**
- `scene_id` — the ID of the scene to copy.

**What it returns:**
- The newly created `Scene` object with its new ID.

**Example:**
```python
new_scene = scene_repo.duplicate_scene(3)
print(new_scene.id)     # 6  (next available ID)
print(new_scene.status) # "pending"
print(new_scene.code_path) # Same as Scene 3's code path
```

---

### `get_render_summary()`

**What it does:**
Returns a summary dictionary with counts of how many scenes are in each status. It is calculated in one database query and is much faster than loading all scenes and counting them in Python.

**When the Core calls it:**
- When displaying project status after a render run: "8 scenes: 6 rendered, 1 failed, 1 pending."
- When deciding whether to proceed with final video assembly (only proceed if all scenes are rendered).

**What it takes:**
- Nothing.

**What it returns:**
- A dictionary with counts. Example:

```python
{
    "total": 8,
    "rendered": 6,
    "pending": 1,
    "failed": 1
}
```

**Example:**
```python
summary = scene_repo.get_render_summary()
print(f"{summary['rendered']} of {summary['total']} scenes rendered.")
if summary['failed'] > 0:
    print(f"Warning: {summary['failed']} scenes failed.")
```

---

### `validate_all_video_paths()`

**What it does:**
Goes through every scene that has a stored video path and checks whether that file actually exists on disk right now. Returns a list of any scenes whose stored video path points to a file that cannot be found.

**When the Core calls it:**
- Before assembling the final video — to make sure all rendered clips are still present and have not been accidentally deleted or moved.
- When the user runs `validate project`.

**What it takes:**
- Nothing.

**What it returns:**
- A list of `Scene` objects whose video file is missing from disk. Returns an empty list if all video files are present.

**Example:**
```python
broken = scene_repo.validate_all_video_paths()
if broken:
    for scene in broken:
        notifier.send_error(f"Scene {scene.id} video file is missing: {scene.video_path}")
```

---

### `export_to_dict()`

**What it does:**
Serializes all scene data into a Python dictionary that can be written to a JSON or YAML file. This is used for creating a human-readable backup of all scene data.

**When the Core calls it:**
- When the user runs `export project` — all scene data is included in the export archive.
- When creating a project backup before making large changes.

**What it takes:**
- Nothing.

**What it returns:**
- A Python dictionary containing all scene data in a serializable format.

**Example:**
```python
data = scene_repo.export_to_dict()
import json
with open("backup.json", "w") as f:
    json.dump(data, f, indent=2)
```

---

### `import_from_dict(data)`

**What it does:**
Reads scene data from a previously exported dictionary and saves it all into storage. This is the reverse operation of `export_to_dict()`. Used for restoring a project from a backup.

**When the Core calls it:**
- When the user runs `import project` from a backup file.
- When migrating a project from one machine to another.

**What it takes:**
- `data` — a Python dictionary in the same format that `export_to_dict()` produces.

**What it returns:**
- Nothing. Raises a `ValidationError` if the data format is invalid.

**Example:**
```python
import json
with open("backup.json", "r") as f:
    data = json.load(f)
scene_repo.import_from_dict(data)
```


**The implementation of Scene Repositoy port and the Alternative Adapters:**

```
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| SceneRepositoryPort       | SqliteSceneRepository     | SQLite (sqlite3)      | JsonSceneRepository       |
|                           |                           |                       | InMemorySceneRepository   |
|                           |                           |                       | YamlSceneRepository       |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

**Default Adapter — SqliteSceneRepository:**
Uses Python's built-in `sqlite3` library to store scene data in a local `.db` file inside the project folder. SQLite is chosen because it is fast, needs no server, and handles structured data well.

**Alternative — JsonSceneRepository:**
Stores all scene data in a `.json` file. Easier to read and edit by hand. Slower for very large projects. Good for testing and debugging.

**Alternative — InMemorySceneRepository:**
Stores everything in a Python dictionary in RAM. Data is lost when the program closes. This is used only in automated tests so tests run fast without touching any real files.

**Alternative — YamlSceneRepository:**
Stores scene data in a human-readable YAML file. Good for projects that are shared with other people who want to see or edit the data in a text editor.

---

Port 1.2 — ProjectRepositoryPort
-----------------------------------
**Simple Definition:**
This port saves the top-level settings of your project. Think of it like the cover page of a folder. It does not store the scenes themselves — it stores the name of the project, the mode it is using, and all global settings.

**Why It Exists:**
When you run `supermanim open MyAnimation`, the program needs to know what mode the project is in (normal, simplemanim, supermanim), what the project name is, and what global preferences are set. Without this port, none of that information would be remembered.

**What Data It Saves for Each Project:**
- Project name
- Project mode (`normal`, `simplemanim`, `supermanim`)
- Total number of scenes
- Project creation date
- Last modified date
- Output folder path
- Global render quality setting (low, medium, high)
- Global frame rate setting (e.g., 30fps, 60fps)
- Whether the project uses audio or not
- Path to the project's SQLite database file

**Functions the Core Calls Through This Port:**
- `save_project(project)` — save a new project or update settings
- `load_project(project_name)` — load project by name
- `project_exists(project_name)` — check if a project exists before loading
- `delete_project(project_name)` — delete all data for a project
- `list_all_projects()` — list every project on this machine
- `update_setting(project_name, key, value)` — change one setting

```
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| ProjectRepositoryPort     | SqliteProjectRepository   | SQLite (sqlite3)      | YamlProjectRepository     |
|                           |                           |                       | TomlProjectRepository     |
|                           |                           |                       | JsonProjectRepository     |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

**Default Adapter — SqliteProjectRepository:**
Writes project metadata into an SQLite database. When you create a new project, a row is inserted. When you change a setting, that row is updated.

**Alternative — YamlProjectRepository:**
Writes project settings to a `project.yaml` file. This is very human-readable. Good for version control with Git because YAML diffs are easy to read.

**Alternative — TomlProjectRepository:**
Uses the TOML format, which is similar to `.ini` files but more powerful. Python has the `tomllib` library built in for reading TOML. Good for configuration-heavy projects.

**Alternative — JsonProjectRepository:**
Writes to a `project.json` file. Works well when the project needs to be loaded by another program or script.

---

## Port 1.3 — AudioRepositoryPort

**Simple Definition:**
This port keeps track of all audio files that belong to a project. In SuperManim mode, you have one long audio narration file, and it is split into clips for each scene. This port remembers every audio file and its metadata.

**Why It Exists:**
Audio synchronization is the hardest part of SuperManim. The tool needs to remember which portion of the original audio belongs to Scene 1, which portion belongs to Scene 2, and so on. It also needs to remember the duration of each clip, the file format, and the path on disk. Without this port, the audio plan would be forgotten every time the program closes.

**What Data It Saves for Each Audio Entry:**
- Audio file ID
- Original audio file path (the source file)
- Split audio clip path (the processed segment)
- Start time in the original file (seconds)
- End time in the original file (seconds)
- Duration of this clip (seconds)
- Scene ID this clip is assigned to
- File format (mp3, wav, ogg, etc.)
- Sample rate (e.g., 44100 Hz)
- Number of channels (mono or stereo)
- Whether this clip has been processed/cut yet

**Functions the Core Calls Through This Port:**
- `save_audio_entry(audio)` — save one audio clip entry
- `load_audio_for_scene(scene_id)` — get the audio clip for a specific scene
- `load_original_audio(project_name)` — get the main audio file record
- `all_audio_entries()` — get every audio entry in the project
- `delete_audio_entry(audio_id)` — remove one entry
- `update_audio_path(audio_id, new_path)` — update file path after processing

```
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| AudioRepositoryPort       | SqliteAudioRepository     | SQLite (sqlite3)      | JsonAudioRepository       |
|                           |                           |                       | DictAudioRepository       |
|                           |                           |                       | CsvAudioRepository        |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

**Default Adapter — SqliteAudioRepository:**
All audio records stored in an SQLite table. Supports fast lookup by scene ID. Perfect for projects with many scenes.

**Alternative — JsonAudioRepository:**
All audio records in one JSON list. Easy to inspect and debug manually. Slightly slower for large projects.

**Alternative — DictAudioRepository:**
In-memory dictionary. Only for testing. Data is gone when the program closes.

**Alternative — CsvAudioRepository:**
Stores audio records in a simple CSV spreadsheet file. Very easy to open in Excel or LibreOffice Calc. Useful when you want to plan or edit the audio split table by hand before running the tool.

---

## Port 1.4 — CacheRepositoryPort

**Simple Definition:**
This port is SuperManim's speed secret. It stores "render hashes" — unique fingerprints of each scene's code. When you run the render command, SuperManim checks the current fingerprint of the code against the stored fingerprint. If they match, the scene has not changed, and rendering is skipped. If they differ, the scene was edited, and rendering runs.

**Why It Exists:**
This is the entire reason SuperManim is faster than raw Manim. If you have 20 scenes and change one, you want to only re-render that one scene. To know which scenes changed, the tool computes a fingerprint (SHA-256 hash) of each scene's Python file. The CacheRepositoryPort stores those fingerprints between runs.

**What Data It Saves:**
- Scene ID
- Hash fingerprint of the scene's code file
- Timestamp of when the hash was last computed
- Path to the rendered video file this hash corresponds to
- A "cache key" — a combined key of scene ID + hash, used for quick lookup

**Functions the Core Calls Through This Port:**
- `save_cache_entry(scene_id, hash, video_path)` — store a new hash record
- `load_cache_entry(scene_id)` — retrieve the stored hash for a scene
- `hash_matches(scene_id, current_hash)` — quick check: did this scene change?
- `invalidate_cache(scene_id)` — delete a scene's cache so it must re-render
- `invalidate_all()` — clear all cache entries to force a full re-render
- `all_cache_entries()` — list everything in cache

```
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| CacheRepositoryPort       | SqliteCacheRepository     | SQLite (sqlite3)      | FileCacheRepository       |
|                           |                           |                       | RedisCacheRepository      |
|                           |                           |                       | InMemoryCacheRepository   |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

**Default Adapter — SqliteCacheRepository:**
Stores render hashes in an SQLite table. Very fast for lookup by scene ID. Survives program restarts.

**Alternative — FileCacheRepository:**
Stores hashes in simple `.hash` text files inside each scene's folder. Easy to delete manually if you want to force a re-render of a specific scene. Very transparent.

**Alternative — RedisCacheRepository:**
Uses Redis (a fast in-memory database) for caching. This would be useful if SuperManim ever becomes a server-side tool or is used by multiple users at the same time. Not needed for the current local CLI tool but demonstrates how easy it is to swap adapters.

**Alternative — InMemoryCacheRepository:**
Stores hashes in a Python dictionary. Used for tests only. Cache is gone after the program exits.

---

## Port 1.5 — RenderHistoryRepositoryPort *(Proposed Addition)*

**Simple Definition:**
This port keeps a permanent log of every render event that ever happened — when it started, how long it took, whether it succeeded or failed, and what error occurred if it failed. It is like a diary of everything the renderer has ever done.

**Why It Exists:**
Without a history log, if a render fails at 3am when you left it running overnight, you have no way to know what went wrong or which scene failed. This port gives you a full audit trail of every render attempt. It also lets you calculate statistics — like how much total time you have spent rendering, or which scenes fail most often.

**What Data It Saves:**
- Render event ID
- Scene ID that was rendered
- Start timestamp
- End timestamp
- Duration of the render in seconds
- Success or failure
- Error message if failed
- Output file path if succeeded
- Quality setting used for this render (low, medium, high)

**Functions the Core Calls Through This Port:**
- `record_render_start(scene_id, quality)` → returns event_id
- `record_render_success(event_id, output_path)` — mark render done
- `record_render_failure(event_id, error_message)` — mark render failed
- `get_history_for_scene(scene_id)` — get all render attempts for one scene
- `get_all_history()` — get every render event ever
- `get_last_successful_render(scene_id)` — find the most recent success
- `clear_history()` — delete all history records

```
+-------------------------------+----------------------------+-----------------------+---------------------------+
| Port (Interface)              | Adapter (Implementation)   | External Technology   | Alternative Adapters      |
+-------------------------------+----------------------------+-----------------------+---------------------------+
| RenderHistoryRepositoryPort   | SqliteRenderHistoryRepo    | SQLite (sqlite3)      | JsonRenderHistoryRepo     |
|                               |                            |                       | CsvRenderHistoryRepo      |
+-------------------------------+----------------------------+-----------------------+---------------------------+
```

---

---

# GROUP 2 — Media Processing Ports (The Heavy Workers)

## What This Group Does

This is where the actual heavy work happens. The Repository Ports just save data. The Media Processing Ports actually run programs, process audio, render video, and stitch everything together. These ports control external tools like Manim and FFmpeg — the two most powerful tools SuperManim uses.

Every call to a port in this group is expensive — it takes time and CPU power. The Core logic calls these ports and waits for results.

---

## Port 2.1 — RenderRunnerPort

**Simple Definition:**
This port is the bridge between SuperManim and Manim. When the core logic decides "it is time to render Scene 5," it calls this port. The adapter then actually launches Manim, passes the right Python file and the right duration, and waits for Manim to finish.

**Why It Exists:**
Without this port, the core logic would have to call `subprocess.run(["manim", ...])` directly. That would be a disaster — you could never swap Manim for another renderer, you could never run tests without actually launching Manim, and you could never run rendering in the background without freezing the whole program. The port abstracts all of that.

**What Operations It Provides:**
- Take a Python file (the Manim scene code)
- Take a duration in seconds
- Take a quality setting (low, medium, high, ultra)
- Run the renderer and wait for it to finish
- Return a result object that says: success or failure, and the path to the output video file

**Functions the Core Calls Through This Port:**
- `render(code_path, scene_class_name, duration, quality, output_path)` — render one scene
- `render_preview(code_path, scene_class_name, output_path)` — render a low-quality draft fast
- `cancel_render()` — stop a running render (for GUI use)
- `is_renderer_available()` — check if Manim is installed and ready

```
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| RenderRunnerPort          | ManimSubprocessRenderer   | Manim (subprocess)    | ManimLibraryRenderer      |
|                           |                           |                       | FakeRenderer (for tests)  |
|                           |                           |                       | DockerManimRenderer       |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

**Default Adapter — ManimSubprocessRenderer:**
Calls Manim by running it as a separate terminal command using Python's `subprocess` module. The command looks like: `manim render scene.py MySceneClass --quality h`. Running as a subprocess means SuperManim does not freeze while Manim works.

**Alternative — ManimLibraryRenderer:**
Calls Manim directly as a Python library (importing and calling its functions directly, rather than as a terminal command). Faster startup but more tightly tied to the exact version of Manim installed.

**Alternative — FakeRenderer (for tests):**
Does not call Manim at all. Simply creates an empty video file and returns "success." This makes it possible to write automated tests for render logic without needing Manim installed or waiting minutes for real renders.

**Alternative — DockerManimRenderer:**
Runs Manim inside a Docker container. Useful for servers where you do not want to install Manim directly on the host machine. The adapter sends the code file into the container and gets back the rendered video.

---

## Port 2.2 — AudioProcessorPort

**Simple Definition:**
This port handles all audio cutting and trimming. When you have a 60-second narration file and 4 scenes, this port cuts that file into 4 smaller clips — the exact right portion of audio for each scene.

**Why It Exists:**
Audio processing is technical and messy. The actual tool that does the cutting (FFmpeg) has a complex command syntax. The port hides all of that. The core just says "give me seconds 12.5 to 31.0 from this file and save it as a new file." The adapter handles the complex FFmpeg command required to do that.

**What Operations It Provides:**
- Cut a portion of an audio file (start time to end time)
- Convert audio from one format to another (mp3 → wav, etc.)
- Get the duration of an audio file
- Normalize audio volume
- Remove silence from an audio file
- Merge two audio files together

**Functions the Core Calls Through This Port:**
- `cut_audio(input_path, start_seconds, end_seconds, output_path)` — extract a portion
- `convert_audio(input_path, output_format, output_path)` — change format
- `get_duration(file_path)` — measure how long an audio file is
- `normalize_volume(input_path, output_path, target_dbfs)` — make it the right volume
- `strip_silence(input_path, output_path, silence_threshold_db)` — remove quiet parts
- `merge_audio(file_paths_list, output_path)` — join multiple clips into one
- `is_tool_available()` — check if FFmpeg is installed

```
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| AudioProcessorPort        | FfmpegAudioProcessor      | FFmpeg (subprocess)   | PydubAudioProcessor       |
|                           |                           |                       | LibrosaAudioProcessor     |
|                           |                           |                       | FakeAudioProcessor        |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

**Default Adapter — FfmpegAudioProcessor:**
Uses FFmpeg (run as a subprocess) to cut, convert, and process audio. FFmpeg is the industry standard. It is fast, free, and supports every audio format. A typical cut command: `ffmpeg -i input.mp3 -ss 12.5 -to 31.0 -c copy output.mp3`.

**Alternative — PydubAudioProcessor:**
Uses the Python `pydub` library for audio processing. Pydub is easier to use in Python code than FFmpeg. Good for simpler operations. It internally uses FFmpeg too, but wraps it in a friendlier Python API.

**Alternative — LibrosaAudioProcessor:**
Uses the `librosa` Python library, which is designed for music and audio analysis. Best for advanced operations like detecting beats, finding silence boundaries, or measuring frequency. Less useful for simple cutting.

**Alternative — FakeAudioProcessor:**
Used only for testing. Returns fake results without actually processing any audio files.

---

## Port 2.3 — VideoAssemblerPort

**Simple Definition:**
After all scenes are rendered as separate video clips, this port stitches them all together into one final video file. It also handles adding the audio track to the final video.

**Why It Exists:**
Manim produces separate video files for each scene. At the end, you need one continuous video. The VideoAssemblerPort handles that joining step, and also merges in the audio track if needed.

**What Operations It Provides:**
- Join multiple video clips in sequence (Scene 1 + Scene 2 + Scene 3 = Final Video)
- Add an audio track to a video (combine the video with the audio narration)
- Remove audio from a video
- Change video format (mp4 → avi, etc.)
- Extract a portion of a video
- Get the duration of a video file
- Get metadata about a video (resolution, framerate, codec)

**Functions the Core Calls Through This Port:**
- `assemble_clips(clip_paths_list, output_path)` — join clips in order
- `add_audio_track(video_path, audio_path, output_path)` — combine video + audio
- `remove_audio_track(video_path, output_path)` — strip the audio out
- `convert_video(input_path, output_format, output_path)` — change format
- `get_video_duration(video_path)` — measure length
- `get_video_metadata(video_path)` — get resolution, fps, codec info
- `extract_clip(input_path, start, end, output_path)` — cut a portion

```
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| VideoAssemblerPort        | FfmpegVideoAssembler      | FFmpeg (subprocess)   | MoviepyVideoAssembler     |
|                           |                           |                       | FakeVideoAssembler        |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

**Default Adapter — FfmpegVideoAssembler:**
Uses FFmpeg to concatenate video files and merge audio tracks. The concat command uses FFmpeg's concat demuxer with a text file listing all clips in order. This is the most reliable and fastest method for joining video files.

**Alternative — MoviepyVideoAssembler:**
Uses the Python `moviepy` library. Moviepy provides a friendlier Python API for video editing. Easier to customize but slower than raw FFmpeg, especially for large video files.

**Alternative — FakeVideoAssembler:**
Used only in tests. Creates empty placeholder files without doing any real processing.

---

## Port 2.4 — AudioAnalyzerPort

**Simple Definition:**
This port listens to an audio file and extracts useful information from it automatically. In SuperManim mode, the tool can automatically detect silence boundaries in your narration audio. This means the tool can suggest "Scene 1 should be 0 to 12.5 seconds, Scene 2 should be 12.5 to 31 seconds" — without you having to measure by hand.

**Why It Exists:**
One of SuperManim's most useful features is automatic audio splitting. Instead of loading your narration into an audio editor and measuring where each sentence ends, you can let SuperManim detect the natural pauses (silences) and use those as scene boundaries.

**What Operations It Provides:**
- Detect silence regions in an audio file (list of start/end times for quiet parts)
- Detect speech regions (list of start/end times where someone is talking)
- Measure total duration of an audio file
- Find beats in music (for music-synchronized animations)
- Compute the waveform data (used for visualizing audio in a GUI)
- Measure loudness (decibels) over time

**Functions the Core Calls Through This Port:**
- `detect_silence_regions(file_path, min_silence_duration, silence_threshold_db)` — find quiet gaps
- `detect_speech_regions(file_path)` — find spoken parts
- `get_duration(file_path)` — total length in seconds
- `detect_beats(file_path)` — find music beat timestamps
- `get_waveform(file_path, sample_rate)` — get amplitude data over time
- `get_loudness_over_time(file_path, window_seconds)` — measure volume changes

```
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| AudioAnalyzerPort         | LibrosaAudioAnalyzer      | Librosa               | PydubSilenceDetector      |
|                           |                           |                       | WhisperAudioAnalyzer      |
|                           |                           |                       | FakeAudioAnalyzer         |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

**Default Adapter — LibrosaAudioAnalyzer:**
Uses the `librosa` Python library. Librosa is a powerful audio analysis library used by musicians and researchers. It can detect silence, beats, pitch, and much more.

**Alternative — PydubSilenceDetector:**
Uses `pydub`'s built-in `detect_silence()` function. Simpler and easier to set up than Librosa. Good enough for basic silence detection but does not support beat detection or waveform analysis.

**Alternative — WhisperAudioAnalyzer:**
Uses OpenAI's Whisper speech recognition model. This adapter is more advanced — it can not only find silence but also transcribe what was said in each segment, giving you both timestamps and text. Useful for future features like auto-generating subtitles.

**Alternative — FakeAudioAnalyzer:**
Returns hardcoded fake results. Used only in tests.

---

## Port 2.5 — PreviewGeneratorPort

**Simple Definition:**
This port creates a quick, low-quality preview of a scene so you can check your animation looks right before committing to a full high-quality render (which takes much longer).

**Why It Exists:**
A full high-quality Manim render can take 5 minutes per scene. If you just want to quickly check "does the text appear in the right place?" you do not want to wait 5 minutes. The preview mode renders at very low quality (small size, low resolution) in seconds so you can spot mistakes fast.

**What Operations It Provides:**
- Generate a low-quality draft video of one scene
- Generate a single still image (thumbnail) of the first frame
- Generate an animated GIF preview (small file, easy to share)
- Generate a preview at a specific timestamp (to check how something looks mid-animation)

**Functions the Core Calls Through This Port:**
- `generate_preview(code_path, scene_class, output_path)` — quick low-res video
- `generate_thumbnail(code_path, scene_class, timestamp, output_path)` — single frame image
- `generate_gif_preview(code_path, scene_class, output_path)` — animated GIF

```
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| PreviewGeneratorPort      | ManimPreviewGenerator     | Manim (low quality)   | ThumbnailImageGenerator   |
|                           |                           |                       | FakePreviewGenerator      |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

**Default Adapter — ManimPreviewGenerator:**
Calls Manim with the `-ql` (quality low) flag. This produces a small 480p video very quickly. Also calls Manim with `--save_last_frame` to produce a thumbnail image.

**Alternative — ThumbnailImageGenerator:**
Uses a lightweight approach — only captures the first or last frame as a PNG image instead of rendering the full video. Much faster but only gives you a static image, not a moving preview.

**Alternative — FakePreviewGenerator:**
Used in tests. Creates empty placeholder files.

---

## Port 2.6 — VideoMetadataReaderPort *(Proposed Addition)*

**Simple Definition:**
This port reads technical information from a video file without playing it. It answers questions like: How long is this video? What is its resolution? What frame rate does it use? What codec was it encoded with?

**Why It Exists:**
SuperManim needs to validate that rendered video files are correct before assembling them. For example, if a scene was supposed to be 12.5 seconds but the rendered file is 12.2 seconds, something went wrong. This port lets the core logic verify each rendered file.

**Functions the Core Calls Through This Port:**
- `get_duration(video_path)` — how long is the video
- `get_resolution(video_path)` — width and height in pixels
- `get_framerate(video_path)` — frames per second
- `get_codec(video_path)` — what codec was used (h264, h265, etc.)
- `get_file_size(video_path)` — file size in bytes
- `validate_video(video_path)` — check if the file is a valid, readable video

```
+----------------------------+----------------------------+-----------------------+---------------------------+
| Port (Interface)           | Adapter (Implementation)   | External Technology   | Alternative Adapters      |
+----------------------------+----------------------------+-----------------------+---------------------------+
| VideoMetadataReaderPort    | FfprobeMetadataReader      | FFprobe (ffmpeg)      | MoviepyMetadataReader     |
|                            |                            |                       | OpenCvMetadataReader      |
+----------------------------+----------------------------+-----------------------+---------------------------+
```

---

---

# GROUP 3 — Infrastructure Ports (System & File Operations)

## What This Group Does

This group handles the boring but essential work of talking to the computer's operating system. Creating folders, moving files, computing fingerprints, managing temporary work files — all of this is covered here. Without this group, the core logic would be full of messy `os.path` and `shutil` code that would break if you ever moved to a different operating system or file system.

---

## Port 3.1 — FileStoragePort

**Simple Definition:**
This port handles everything related to files and folders on the computer's disk. Creating new project folders, checking if a file exists, copying a file, moving a file, deleting a file — all of that goes through this port.

**Why It Exists:**
Without this port, `os.path.exists()`, `shutil.move()`, `pathlib.Path().mkdir()` and similar calls would be scattered throughout the entire codebase. If you ever wanted to store files in the cloud (Amazon S3, Google Drive), you would have to find and change every single one of those calls. With this port, you only change the adapter.

**What Operations It Provides:**
- Create a directory (folder)
- Check if a file exists
- Read a file's text content
- Write text to a file
- Copy a file from one location to another
- Move a file from one location to another
- Delete a file
- Delete a folder and everything inside it
- List all files in a folder
- Get the size of a file

**Functions the Core Calls Through This Port:**
- `create_directory(path)` — make a new folder
- `file_exists(path)` — check if a file is there
- `directory_exists(path)` — check if a folder is there
- `read_text(path)` — read the text content of a file
- `write_text(path, content)` — write text to a file
- `copy_file(source, destination)` — copy a file
- `move_file(source, destination)` — move a file
- `delete_file(path)` — delete one file
- `delete_directory(path)` — delete a folder and its contents
- `list_files(directory, extension_filter)` — list files in a folder
- `get_file_size(path)` — get file size in bytes
- `get_absolute_path(relative_path)` — convert relative path to full path

```
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| FileStoragePort           | LocalFileStorage          | os, shutil, pathlib   | CloudStorageAdapter       |
|                           |                           |                       | S3StorageAdapter          |
|                           |                           |                       | FakeFileStorage           |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

**Default Adapter — LocalFileStorage:**
Uses Python's `os`, `shutil`, and `pathlib` modules to work with the local computer's file system. This is the normal case for a CLI tool running on your own computer.

**Alternative — CloudStorageAdapter:**
Instead of saving to your local disk, this adapter uploads and downloads files from a cloud storage service (like Google Drive or Dropbox). Useful if you are running SuperManim on a server and want the output videos to go to the cloud automatically.

**Alternative — S3StorageAdapter:**
Saves files to Amazon S3 (Simple Storage Service). Uses the `boto3` Python library. For large production pipelines where you generate many videos and want to store them in the cloud.

**Alternative — FakeFileStorage:**
An in-memory fake for tests. It does not touch the real file system at all. All "files" are stored in a Python dictionary. Tests run fast and leave no files on disk.

---

## Port 3.2 — HashComputerPort

**Simple Definition:**
This port computes a unique "fingerprint" of a file. If you give it a Python code file, it reads the entire file and produces a short string of letters and numbers (a hash). If you change even one character in the file, the fingerprint changes completely. If you change nothing, the fingerprint is exactly the same.

**Why It Exists:**
This is the technical heart of SuperManim's smart skipping feature. Before rendering a scene, SuperManim computes the hash of its code file. It compares that hash to the stored hash from the last render. If they match — nothing changed — skip the render. If they differ — the code was edited — run the render. Without this port, there is no way to know which scenes changed.

**Functions the Core Calls Through This Port:**
- `hash_file(file_path)` — compute hash from a file on disk
- `hash_string(text_content)` — compute hash from a text string
- `hash_directory(directory_path)` — compute a combined hash of all files in a folder
- `hashes_match(hash_a, hash_b)` — compare two hashes

```
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| HashComputerPort          | Sha256HashComputer        | Python hashlib        | Md5HashComputer           |
|                           |                           |                       | Blake2HashComputer        |
|                           |                           |                       | FakeHashComputer          |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

**Default Adapter — Sha256HashComputer:**
Uses Python's built-in `hashlib` library to compute a SHA-256 hash. SHA-256 is a well-trusted algorithm used in security and data verification. It produces a 64-character fingerprint. Very unlikely to produce the same fingerprint for two different files.

**Alternative — Md5HashComputer:**
Uses the MD5 algorithm. Produces a shorter 32-character fingerprint. Slightly faster but less collision-resistant than SHA-256. Fine for change detection (not security).

**Alternative — Blake2HashComputer:**
Uses the BLAKE2 algorithm, which is faster than SHA-256 and still very secure. Good for large projects where many files need to be hashed quickly.

**Alternative — FakeHashComputer:**
Returns a hardcoded or randomized fake hash. Used in tests where you want to simulate "scene changed" or "scene unchanged" conditions without touching any real files.

---

## Port 3.3 — TempFileManagerPort

**Simple Definition:**
During rendering and audio processing, SuperManim creates many temporary files. For example, when FFmpeg cuts an audio clip, it might create a `.temp.mp3` file during processing. This port manages the creation and cleanup of all those temporary files so your project folder does not fill up with junk.

**Why It Exists:**
Without careful management of temporary files, any crash or interruption would leave garbage files behind on your disk. This port provides a clean way to create temporary files and guarantees they are deleted when no longer needed.

**Functions the Core Calls Through This Port:**
- `create_temp_file(suffix, prefix)` — make a new temporary file and return its path
- `create_temp_directory()` — make a new temporary folder and return its path
- `delete_temp_file(path)` — delete one temp file
- `delete_temp_directory(path)` — delete one temp folder and all its contents
- `cleanup_all()` — delete every temporary file created in this session
- `get_temp_root()` — get the path of the folder where temp files are stored

```
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| TempFileManagerPort       | SystemTempManager         | Python tempfile       | InMemoryTempManager       |
|                           |                           |                       | ProjectTempManager        |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

**Default Adapter — SystemTempManager:**
Uses Python's built-in `tempfile` module. Creates temporary files in the operating system's standard temp directory (`/tmp` on Linux/Mac, `%TEMP%` on Windows). The OS usually cleans these up automatically after a reboot.

**Alternative — InMemoryTempManager:**
Does not create real files. Stores "temp file" data in a Python dictionary. Used only in tests.

**Alternative — ProjectTempManager:**
Creates temp files inside the project's own folder structure instead of the system temp directory. Useful when you want to see what temp files were created (for debugging), and when you want them to stay until you explicitly clean them.

---

## Port 3.4 — AssetManagerPort

**Simple Definition:**
Your Manim scenes can use extra files — fonts, images, SVG diagrams, data files. This port manages those "asset" files. It knows where they are stored, copies them to the right place when needed, and validates that they are present before a render starts.

**Why It Exists:**
When you render a scene, Manim needs to find any asset files the scene uses. If a scene code file says `SVGMobject("my_diagram.svg")`, Manim needs to find `my_diagram.svg`. This port manages where those files live and makes sure they are accessible during rendering.

**Functions the Core Calls Through This Port:**
- `register_asset(asset_path, asset_type)` — tell the system about a new asset file
- `get_asset_path(asset_name)` — find where an asset is stored
- `asset_exists(asset_name)` — check if an asset file is present
- `copy_assets_to_render_directory(scene_id, render_dir)` — move all needed assets for a scene
- `list_all_assets()` — list every registered asset
- `delete_asset(asset_name)` — remove an asset from the project

```
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| AssetManagerPort          | LocalAssetManager         | File System           | CloudAssetManager         |
|                           |                           |                       | BundledAssetManager       |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

**Default Adapter — LocalAssetManager:**
Manages assets stored in a dedicated `assets/` folder inside the project directory. Tracks asset paths in a simple registry file.

**Alternative — CloudAssetManager:**
Downloads assets from a cloud storage location (URL or S3 bucket) on demand. Good for teams sharing assets across multiple machines.

**Alternative — BundledAssetManager:**
Reads assets that are bundled inside the SuperManim package itself (like built-in fonts or template SVG files that come with the tool).

---

## Port 3.5 — PathResolverPort *(Proposed Addition)*

**Simple Definition:**
This port converts all the different types of paths into consistent, absolute paths. Users might type relative paths, paths with `~` for home directory, or paths with environment variables. This port cleans all of that up so the rest of the system always gets a clean, full path.

**Why It Exists:**
Path handling is a surprisingly common source of bugs. On Windows, paths use backslashes. On Linux, they use forward slashes. Relative paths mean different things depending on where the program was launched from. This port solves all of that in one place.

**Functions the Core Calls Through This Port:**
- `resolve(path_string)` — convert any path to an absolute path
- `to_project_relative(absolute_path, project_root)` — convert to a path relative to the project
- `join(base_path, *parts)` — safely join path parts together
- `get_project_root()` — get the root folder of the current project
- `get_output_directory()` — get the folder where rendered files are saved

```
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| PathResolverPort          | PathlibPathResolver       | Python pathlib        | OsPathResolver            |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

---

---

# GROUP 4 — Driving Ports (Inbound — User Commands)

## What This Group Does

These are the **entry points** of the application. They are the doors through which commands enter SuperManim. The user types a command in the terminal, and the Driving Adapter translates that terminal command into a call to the corresponding Driving Port. The Driving Port then hands the command to the Core.

This group allows SuperManim to support multiple interfaces (CLI, GUI, REST API) without changing any core logic. Only the adapters change.

```
+=========================================================+
|               HOW DRIVING PORTS WORK                    |
+=========================================================+
|                                                         |
|   USER                                                  |
|     |                                                   |
|     |  types: "supermanim render scene 3"               |
|     |                                                   |
|     v                                                   |
|   [ CLI ADAPTER ]  <--- CliRenderCommandAdapter         |
|   "I parse this terminal command"                       |
|     |                                                   |
|     |  calls: port.render_scene(scene_id=3)             |
|     |                                                   |
|     v                                                   |
|   [ PORT ]  <--- RenderCommandPort                      |
|   "I hand this to the Core"                             |
|     |                                                   |
|     v                                                   |
|   [ CORE ]                                              |
|   "I do the actual work"                                |
|                                                         |
+=========================================================+
```

---

## Port 4.1 — ProjectCommandPort

**Simple Definition:**
This port handles all commands that are about the project itself — creating a new project, opening an existing project, listing all projects, and deleting a project.

**Why It Exists:**
Every SuperManim session starts with a project. Before you can add scenes or render anything, you need a project. This port is the first thing the user interacts with.

**Commands It Handles:**
- `new project <name> --mode <mode>` — create a brand new project
- `open project <name>` — open an existing project
- `close project` — close the current project
- `delete project <name>` — delete a project and all its data
- `list projects` — show all projects on this machine
- `project info` — show details about the current project

**Functions the Port Exposes to Adapters:**
- `create_project(name, mode)` — create a new project
- `open_project(name)` — load an existing project into memory
- `close_project()` — unload the current project
- `delete_project(name)` — remove a project permanently
- `list_projects()` — get all project names
- `get_project_info()` — get current project details

```
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| ProjectCommandPort        | CliProjectCommandAdapter  | Terminal (argparse)   | GuiProjectCommandAdapter  |
|                           |                           |                       | ApiProjectCommandAdapter  |
|                           |                           |                       | TestProjectCommandAdapter |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

**Default Adapter — CliProjectCommandAdapter:**
Parses terminal arguments using Python's `argparse` library. Handles commands typed by the user in the terminal.

**Alternative — GuiProjectCommandAdapter:**
A graphical interface version. When the user clicks "New Project" in a window, this adapter calls the same port functions.

**Alternative — ApiProjectCommandAdapter:**
Allows projects to be created and managed through an HTTP REST API. For web-based or remote control use.

**Alternative — TestProjectCommandAdapter:**
Used in automated tests. Directly calls port functions without any user interface.

---

## Port 4.2 — SceneCommandPort

**Simple Definition:**
This port handles all commands that are about managing scenes — adding scenes, setting their duration, assigning their code file, reordering them, or deleting them.

**Commands It Handles:**
- `add scene` — add a new scene to the project
- `set scene <n> duration <seconds>` — set how long a scene plays
- `set scene <n> code <file_path>` — assign a Python code file to a scene
- `delete scene <n>` — remove a scene
- `list scenes` — show all scenes and their status
- `scene info <n>` — show details about one scene
- `move scene <n> to <position>` — reorder scenes

**Functions the Port Exposes:**
- `add_scene()` — add a new scene
- `set_scene_duration(scene_id, seconds)` — set duration
- `set_scene_code(scene_id, code_file_path)` — assign code
- `delete_scene(scene_id)` — remove a scene
- `list_scenes()` — get all scenes
- `get_scene_info(scene_id)` — get one scene's details
- `move_scene(scene_id, new_position)` — reorder

```
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| SceneCommandPort          | CliSceneCommandAdapter    | Terminal (argparse)   | GuiSceneCommandAdapter    |
|                           |                           |                       | ApiSceneCommandAdapter    |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

---

## Port 4.3 — RenderCommandPort

**Simple Definition:**
This port handles all rendering commands. It is the port that triggers actual video production.

**Commands It Handles:**
- `render scene <n>` — render just one specific scene
- `render all` — render every scene that needs it
- `render changed` — render only scenes whose code changed
- `preview scene <n>` — generate a quick low-quality preview
- `force render scene <n>` — render even if nothing changed (ignore cache)
- `cancel render` — stop a render that is in progress

**Functions the Port Exposes:**
- `render_scene(scene_id, quality)` — render one scene
- `render_all(quality)` — render all scenes
- `render_changed_scenes(quality)` — render only changed scenes
- `preview_scene(scene_id)` — generate a preview
- `force_render_scene(scene_id, quality)` — ignore cache and render
- `cancel_current_render()` — stop the running render

```
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| RenderCommandPort         | CliRenderCommandAdapter   | Terminal (argparse)   | GuiRenderCommandAdapter   |
|                           |                           |                       | ApiRenderCommandAdapter   |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

---

## Port 4.4 — AudioCommandPort

**Simple Definition:**
This port handles all audio management commands — adding a main audio file, splitting it, mapping audio clips to scenes, and managing audio metadata.

**Commands It Handles:**
- `add audio <file_path>` — set the main narration audio file
- `split audio auto` — automatically detect silences and split
- `split audio manual <time1> <time2> ...` — split at specific timestamps
- `map audio scene <n> <start> <end>` — manually map a time range to a scene
- `preview audio scene <n>` — play the audio clip assigned to a scene
- `audio info` — show all audio assignments

**Functions the Port Exposes:**
- `add_audio_file(file_path)` — register the main audio file
- `auto_split_audio()` — detect silences and split automatically
- `manual_split_audio(timestamps_list)` — split at specific times
- `map_audio_to_scene(scene_id, start_seconds, end_seconds)` — manual mapping
- `get_audio_assignments()` — show the full audio mapping

```
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| AudioCommandPort          | CliAudioCommandAdapter    | Terminal (argparse)   | GuiAudioCommandAdapter    |
|                           |                           |                       | ApiAudioCommandAdapter    |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

---

## Port 4.5 — ExportCommandPort

**Simple Definition:**
This port handles the final step — exporting the finished project. After all scenes are rendered, this port triggers the assembly of the final video and handles packaging the project files.

**Commands It Handles:**
- `export` — assemble all scenes into the final video
- `export --with-audio` — assemble and add audio track
- `export --format mp4` — export in a specific format
- `package project` — zip the entire project folder for sharing

**Functions the Port Exposes:**
- `export_final_video(format, include_audio)` — assemble and export
- `package_project(output_path)` — create a ZIP of the project
- `get_export_status()` — check if export is in progress

```
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| ExportCommandPort         | CliExportCommandAdapter   | Terminal (argparse)   | GuiExportCommandAdapter   |
|                           |                           |                       | ApiExportCommandAdapter   |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

---

## Port 4.6 — ConfigCommandPort *(Proposed Addition)*

**Simple Definition:**
This port handles commands that change SuperManim's own settings — things like default quality level, default frame rate, preferred output folder, and other global preferences.

**Commands It Handles:**
- `config set quality high` — change default render quality
- `config set fps 60` — change default frame rate
- `config set output_dir ~/Videos` — change where finished videos go
- `config get quality` — read a setting
- `config list` — show all current settings
- `config reset` — reset everything to default

**Functions the Port Exposes:**
- `set_config(key, value)` — change one setting
- `get_config(key)` — read one setting
- `list_config()` — show all settings
- `reset_config()` — restore defaults

```
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| ConfigCommandPort         | CliConfigCommandAdapter   | Terminal (argparse)   | GuiConfigCommandAdapter   |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

---

---

# GROUP 5 — Notification Ports (Outbound — Feedback to User)

## What This Group Does

After the core logic does its work, it needs to tell the user what happened. Did the render succeed? Did it fail? How much time is left? These ports handle all of that feedback. They are the "output" side of the user interface.

By using ports for notifications, SuperManim can switch from printing text in the terminal to showing windows and pop-ups in a GUI — without changing any core logic. The core just calls `notifier.send_success("Render complete")` and it works the same way whether the output is a terminal, a GUI window, or a log file.

---

## Port 5.1 — NotificationPort

**Simple Definition:**
This port sends simple messages to the user. "Render Complete." "Error: File Not Found." "Scene 5 skipped (no changes)." These are the short, direct messages that tell the user what just happened.

**Why It Exists:**
Without this port, `print()` statements would be scattered everywhere in the codebase. Moving to a GUI would require finding every single `print()` and replacing it. With this port, the core only calls `self.notifier.send_info(...)` — and swapping the adapter from CLI to GUI is one line of code.

**Types of Messages:**
- **Info** — normal information (green or white text)
- **Success** — something completed successfully (green checkmark)
- **Warning** — something unusual happened but it's not fatal (yellow)
- **Error** — something failed (red text)
- **Debug** — detailed developer information (grey, only shown in debug mode)

**Functions the Core Calls Through This Port:**
- `send_info(message)` — plain information message
- `send_success(message)` — success message
- `send_warning(message)` — warning message
- `send_error(message)` — error message
- `send_debug(message)` — debug-only message
- `send_scene_skipped(scene_id, reason)` — notify that a scene was skipped
- `send_render_started(scene_id)` — notify that a scene started rendering
- `send_render_finished(scene_id, duration_seconds)` — notify completion with timing

```
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| NotificationPort          | CliNotifier               | print() / rich        | GuiNotifier               |
|                           |                           |                       | LoggingNotifier           |
|                           |                           |                       | SilentNotifier            |
|                           |                           |                       | JsonNotifier              |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

**Default Adapter — CliNotifier:**
Uses Python's `print()` function and the `rich` library to display colored, formatted messages in the terminal. Green for success, yellow for warnings, red for errors.

**Alternative — GuiNotifier:**
Shows messages as pop-up windows or updates a status bar in a graphical interface.

**Alternative — LoggingNotifier:**
Writes all messages to a log file using Python's `logging` module. Useful in server environments where there is no user looking at a screen.

**Alternative — SilentNotifier:**
Does absolutely nothing. Used in tests where you want the code to run without printing any output.

**Alternative — JsonNotifier:**
Outputs all messages as JSON objects to standard output. Useful when SuperManim is called from another program that needs to parse the output programmatically.

---

## Port 5.2 — ProgressReporterPort

**Simple Definition:**
This port shows the user how much work has been done and how much is left. A progress bar that goes from 0% to 100% as scenes are rendered. A counter like "Rendering scene 3 of 8."

**Why It Exists:**
Rendering can take a long time. Without progress feedback, the user stares at a blank screen and wonders if the program crashed. This port provides continuous feedback so the user always knows what is happening.

**Functions the Core Calls Through This Port:**
- `start_task(task_name, total_steps)` — begin tracking a task (e.g., "Rendering 8 scenes")
- `advance(steps, description)` — move the progress forward (e.g., "Rendered Scene 3")
- `finish_task()` — mark the task as 100% complete
- `set_current_operation(description)` — update the current step label
- `show_time_elapsed(seconds)` — display how long has passed
- `show_time_remaining(estimated_seconds)` — display estimated time left

```
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| ProgressReporterPort      | CliProgressReporter       | rich.progress         | GuiProgressBar            |
|                           |                           |                       | SilentProgressReporter    |
|                           |                           |                       | JsonProgressReporter      |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

**Default Adapter — CliProgressReporter:**
Uses the `rich.progress` module to draw a beautiful animated progress bar in the terminal, complete with percentage, elapsed time, and current step description.

**Alternative — GuiProgressBar:**
Updates a visual progress bar widget in a graphical user interface window.

**Alternative — SilentProgressReporter:**
Does nothing. Used in tests.

**Alternative — JsonProgressReporter:**
Outputs progress as JSON objects so another program can parse and display progress however it wants.

---

## Port 5.3 — LoggerPort

**Simple Definition:**
This port writes detailed technical records to a log file. Unlike the NotificationPort (which shows messages to the user), the LoggerPort is for developers and debugging. It records every important event with a timestamp, so that if something goes wrong you can read the log file and trace exactly what happened.

**Why It Exists:**
Debugging a complex multi-step pipeline (render all scenes, cut audio, assemble final video) is very hard without logs. If a render failed at midnight when you were asleep, the log file tells you exactly what happened, when, and why.

**Types of Log Records:**
- **DEBUG** — extremely detailed technical information
- **INFO** — general events (project opened, scene saved, render started)
- **WARNING** — unusual but non-fatal events
- **ERROR** — failures
- **CRITICAL** — catastrophic failures

**Functions the Core Calls Through This Port:**
- `debug(message, context)` — log a debug detail
- `info(message, context)` — log a normal event
- `warning(message, context)` — log a warning
- `error(message, context, exception)` — log a failure
- `critical(message, context, exception)` — log a fatal failure
- `set_log_level(level)` — change how much detail is recorded
- `get_log_file_path()` — find the current log file location

```
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| LoggerPort                | FileLogger                | Python logging        | ConsoleLogger             |
|                           |                           |                       | SilentLogger              |
|                           |                           |                       | RotatingFileLogger        |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

**Default Adapter — FileLogger:**
Uses Python's `logging` module to write log records to a `.log` file inside the project folder. Each line includes a timestamp, severity level, and the message.

**Alternative — ConsoleLogger:**
Prints log records to the terminal. Useful during development when you want to see everything happening in real time.

**Alternative — SilentLogger:**
Discards all log records. Used in tests.

**Alternative — RotatingFileLogger:**
Writes to log files but automatically creates a new file when the current one gets too large, keeping only the last N log files. Prevents log files from filling up your disk.

---

## Port 5.4 — ErrorReporterPort *(Proposed Addition)*

**Simple Definition:**
When something goes wrong in SuperManim, this port collects detailed error information and presents it to the user in a helpful, structured way. Instead of just showing "Error: Manim failed," it shows exactly what went wrong, suggests how to fix it, and tells the user which log file to look at for more details.

**Why It Exists:**
Raw Python exception stack traces are terrifying to non-developers. This port turns ugly technical error messages into friendly, actionable feedback.

**Functions the Core Calls Through This Port:**
- `report_render_error(scene_id, exception, manim_output)` — report a render failure
- `report_audio_error(operation, exception)` — report an audio processing failure
- `report_file_not_found(expected_path)` — report a missing file
- `report_validation_error(field, value, reason)` — report bad user input
- `suggest_fix(error_type)` — show a suggested fix to the user

```
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| ErrorReporterPort         | CliErrorReporter          | rich / print()        | GuiErrorReporter          |
|                           |                           |                       | JsonErrorReporter         |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

---

---

# GROUP 6 — Configuration Ports (Settings & Environment)

## What This Group Does

This group handles reading settings, preferences, and environment information that SuperManim needs to know before it starts working. This includes the user's preferences (like default quality level), environment information (like which Python is installed), and system configuration (like where to store the project database).

---

## Port 6.1 — SettingsPort

**Simple Definition:**
This port reads and writes the user's global preferences. These are settings that apply to every project — not just one. For example, the default render quality (low/medium/high), whether to show verbose output, where to store project databases, etc.

**Why It Exists:**
Users should be able to set their preferences once and have them apply every time they use SuperManim, without having to specify them on every command. This port reads those preferences from a config file and makes them available to the core.

**Settings It Manages:**
- Default render quality (low, medium, high, ultra)
- Default frame rate (24, 30, 60 fps)
- Default output directory path
- Whether to show color in terminal output
- Whether to show debug messages
- Maximum number of parallel render jobs (for future parallel rendering)
- Default audio format for output (mp3, wav, aac)

**Functions the Core Calls Through This Port:**
- `get(key)` — get one setting value
- `set(key, value)` — change one setting
- `get_all()` — get every setting as a dictionary
- `reset_to_defaults()` — restore all settings to factory defaults
- `has(key)` — check if a setting exists
- `export_settings(file_path)` — save settings to a file
- `import_settings(file_path)` — load settings from a file

```
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| SettingsPort              | TomlSettingsAdapter       | Python tomllib        | JsonSettingsAdapter       |
|                           |                           |                       | EnvVarSettingsAdapter     |
|                           |                           |                       | InMemorySettingsAdapter   |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

**Default Adapter — TomlSettingsAdapter:**
Reads and writes a `settings.toml` file in the user's home directory (or the SuperManim config folder). TOML is easy to read and edit by hand.

**Alternative — JsonSettingsAdapter:**
Stores settings in a `settings.json` file. Good for programmatic access.

**Alternative — EnvVarSettingsAdapter:**
Reads settings from environment variables. Useful for running SuperManim in containers or CI pipelines where settings are set in the environment.

**Alternative — InMemorySettingsAdapter:**
Stores settings only in memory. Used in tests.

---

## Port 6.2 — EnvironmentInspectorPort

**Simple Definition:**
Before SuperManim can do anything, it needs to check if all the required tools are installed. Is Manim installed? Is FFmpeg installed? Is the correct version of Python being used? Is there enough disk space? This port answers all those questions.

**Why It Exists:**
If Manim is not installed and the user tries to render, SuperManim should give a clear, helpful error ("Manim is not installed. Please install it with: pip install manim") rather than crashing with a confusing Python error. This port lets the core check the environment before starting work.

**Functions the Core Calls Through This Port:**
- `is_manim_installed()` — check if Manim is available
- `get_manim_version()` — get the installed Manim version string
- `is_ffmpeg_installed()` — check if FFmpeg is available
- `get_ffmpeg_version()` — get the installed FFmpeg version
- `get_python_version()` — get the Python version running SuperManim
- `get_available_disk_space(path)` — get free disk space in bytes
- `get_total_ram()` — get total system memory
- `validate_all_dependencies()` — check everything at once and return a report

```
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| EnvironmentInspectorPort  | SystemEnvironmentInspector| subprocess, shutil    | FakeEnvironmentInspector  |
|                           |                           | platform, os          |                           |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

**Default Adapter — SystemEnvironmentInspector:**
Uses Python's `subprocess`, `shutil.which()`, `platform`, and `os` modules to check what tools are installed on the actual machine.

**Alternative — FakeEnvironmentInspector:**
Returns hardcoded answers. Used in tests where you want to simulate "Manim installed" or "Manim missing" conditions without depending on what is actually installed.

---

## Port 6.3 — ProjectValidatorPort *(Proposed Addition)*

**Simple Definition:**
Before running a render or export operation, this port validates that the project is in a correct, complete state. Are all scene code files present? Do all scene durations add up correctly? Is every scene assigned a code file? This port checks all of that and returns a list of problems if any are found.

**Why It Exists:**
It is frustrating to start a long render only to have it fail at scene 7 because you forgot to assign a code file. This port lets the core validate the entire project first, report all problems at once, and stop before wasting time on a render that will fail.

**Functions the Core Calls Through This Port:**
- `validate_project(project)` — full validation, returns list of errors
- `validate_scene(scene)` — validate one scene
- `validate_audio_mapping()` — check that audio assignments are consistent
- `validate_durations()` — check that scene durations match audio clip lengths
- `check_code_files_exist()` — verify that every code file path points to a real file

```
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| ProjectValidatorPort      | DefaultProjectValidator   | Pure Python           | StrictProjectValidator    |
|                           |                           |                       | LenientProjectValidator   |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

---

---

# Complete Summary Table

The following table shows every single port in SuperManim in one place. Use this as a quick reference.

```
+------+---+-------------------------------+----------------------------+---------------------------------------------+
| Grp  | # | Port Name                     | Default Adapter            | Purpose                                     |
+------+---+-------------------------------+----------------------------+---------------------------------------------+
|      | 1 | SceneRepositoryPort           | SqliteSceneRepository      | Save/load all scene data                    |
|  R   | 2 | ProjectRepositoryPort         | SqliteProjectRepository    | Save/load project settings                  |
|  E   | 3 | AudioRepositoryPort           | SqliteAudioRepository      | Save/load audio file records                |
|  P   | 4 | CacheRepositoryPort           | SqliteCacheRepository      | Store render hashes for smart skipping      |
|  O   | 5 | RenderHistoryRepositoryPort   | SqliteRenderHistoryRepo    | Log every render event (proposed)           |
+------+---+-------------------------------+----------------------------+---------------------------------------------+
|      | 6 | RenderRunnerPort              | ManimSubprocessRenderer    | Actually run Manim to render a scene        |
|  M   | 7 | AudioProcessorPort            | FfmpegAudioProcessor       | Cut, convert, and merge audio files         |
|  E   | 8 | VideoAssemblerPort            | FfmpegVideoAssembler       | Stitch scenes into final video              |
|  D   | 9 | AudioAnalyzerPort             | LibrosaAudioAnalyzer       | Detect silence and analyze audio            |
|  I   |10 | PreviewGeneratorPort          | ManimPreviewGenerator      | Generate fast low-quality preview           |
|  A   |11 | VideoMetadataReaderPort       | FfprobeMetadataReader      | Read technical info from video files        |
+------+---+-------------------------------+----------------------------+---------------------------------------------+
|      |12 | FileStoragePort               | LocalFileStorage           | Create/move/delete files and folders        |
|  I   |13 | HashComputerPort              | Sha256HashComputer         | Compute fingerprints to detect changes      |
|  N   |14 | TempFileManagerPort           | SystemTempManager          | Create and clean up temporary files         |
|  F   |15 | AssetManagerPort              | LocalAssetManager          | Manage image/font/SVG assets                |
|  R   |16 | PathResolverPort              | PathlibPathResolver        | Normalize and resolve file paths (proposed) |
+------+---+-------------------------------+----------------------------+---------------------------------------------+
|      |17 | ProjectCommandPort            | CliProjectCommandAdapter   | Accept create/open/delete project commands  |
|  D   |18 | SceneCommandPort              | CliSceneCommandAdapter     | Accept add/edit/delete scene commands       |
|  R   |19 | RenderCommandPort             | CliRenderCommandAdapter    | Accept render/preview commands              |
|  I   |20 | AudioCommandPort              | CliAudioCommandAdapter     | Accept audio add/split commands             |
|  V   |21 | ExportCommandPort             | CliExportCommandAdapter    | Accept final export commands                |
|  E   |22 | ConfigCommandPort             | CliConfigCommandAdapter    | Accept settings change commands (proposed)  |
+------+---+-------------------------------+----------------------------+---------------------------------------------+
|      |23 | NotificationPort              | CliNotifier                | Send messages to the user                   |
|  N   |24 | ProgressReporterPort          | CliProgressReporter        | Show progress bar and step info             |
|  O   |25 | LoggerPort                    | FileLogger                 | Write detailed technical log records        |
|  T   |26 | ErrorReporterPort             | CliErrorReporter           | Show friendly error messages (proposed)     |
+------+---+-------------------------------+----------------------------+---------------------------------------------+
|      |27 | SettingsPort                  | TomlSettingsAdapter        | Read/write global user preferences          |
|  C   |28 | EnvironmentInspectorPort      | SystemEnvironmentInspector | Check if Manim, FFmpeg, etc. are installed  |
|  F   |29 | ProjectValidatorPort          | DefaultProjectValidator    | Validate project before render (proposed)   |
+------+---+-------------------------------+----------------------------+---------------------------------------------+

Legend:
  REP  = Repository Ports (Data Persistence)
  MEDIA = Media Processing Ports (Heavy Workers)
  INFR = Infrastructure Ports (System & Files)
  DRIVE = Driving Ports (Inbound / User Commands)
  NOT  = Notification Ports (Outbound / Feedback)
  CF   = Configuration Ports (Settings & Environment)
  (proposed) = New port suggested to complete the architecture
```

---

## A Final Reminder: Why All This Matters

Every port in this document follows the same rule:

```
+=========================================================+
|                    THE GOLDEN RULE                      |
+=========================================================+
|                                                         |
|  THE CORE NEVER TOUCHES EXTERNAL TOOLS DIRECTLY.        |
|                                                         |
|  It never calls sqlite3.connect()                       |
|  It never calls subprocess.run(["manim", ...])          |
|  It never calls os.path.exists()                        |
|  It never calls print()                                 |
|                                                         |
|  The Core ONLY calls Port methods.                      |
|  The Ports ONLY define what methods exist.              |
|  The Adapters do all the real work.                     |
|                                                         |
|  Result:                                                |
|  - You can swap any adapter without touching the Core.  |
|  - You can test the Core without real tools.            |
|  - You can add a GUI without rewriting anything.        |
|  - You can switch databases in one place only.          |
|                                                         |
+=========================================================+
```

This is Hexagonal Architecture. SuperManim is built on this foundation so it stays clean, testable, and flexible — no matter how big it grows.









###### Repository Ports (Data Persistence)
The **Repository Ports** act as the "long-term memory" of the SuperManim tool.Their job is to save data
so it is not lost when the program closes.

```
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| SceneRepositoryPort       | SqliteSceneRepository     | SQLite (sqlite3)      | JsonSceneRepository,      |
|                           |                           |                       | InMemorySceneRepository   |
+---------------------------+---------------------------+-----------------------+---------------------------+
| ProjectRepositoryPort     | SqliteProjectRepository   | SQLite (sqlite3)      | YamlProjectRepository,    |
|                           |                           |                       | TomlProjectRepository     |
+---------------------------+---------------------------+-----------------------+---------------------------+
| AudioRepositoryPort       | SqliteAudioRepository     | SQLite (sqlite3)      | JsonAudioRepository,      |
|                           |                           |                       | DictAudioRepository       |
+---------------------------+---------------------------+-----------------------+---------------------------+
| CacheRepositoryPort       | SqliteCacheRepository     | SQLite (sqlite3)      | FileCacheRepository,      |
|                           |                           |                       | RedisCacheRepository      |
+---------------------------+---------------------------+-----------------------+---------------------------+

```
**SceneRepositoryPort:**
This is responsible for saving details about every scene like
- The duration of each scene
- The content of each scene
- The code content of each scene
- The code file path
- The status of each scene  and whether it has been rendered.
The main adapter uses SQLite because it is fast and reliable for structured data.And you can use any different
adaptors you wants.

*   **ProjectRepositoryPort:**
This saves the overall project settings (like the project name, the mode "supermanim" or "normal", and global settings).
*   **AudioRepositoryPort:**
This keeps track of audio files and their metadata (like duration and path).
*   **CacheRepositoryPort:**
This is used to store temporary data that speeds up the tool, like render hashes, so the tool knows if a scene changed or not.



###### Media Processing Ports (Heavy Lifting)

```text
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| RenderRunnerPort          | ManimSubprocessRenderer   | Manim (subprocess)    | ManimLibraryRenderer,     |
|                           |                           |                       | FakeRenderer (for tests)  |
+---------------------------+---------------------------+-----------------------+---------------------------+
| AudioProcessorPort        | FfmpegAudioProcessor      | FFmpeg (subprocess)   | PydubAudioProcessor,      |
|                           |                           |                       | LibrosaAudioProcessor     |
+---------------------------+---------------------------+-----------------------+---------------------------+
| VideoAssemblerPort        | FfmpegVideoAssembler      | FFmpeg (subprocess)   | MoviepyVideoAssembler     |
+---------------------------+---------------------------+-----------------------+---------------------------+
| AudioAnalyzerPort         | LibrosaAudioAnalyzer      | Librosa               | PydubSilenceDetector      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| PreviewGeneratorPort      | ManimPreviewGenerator     | Manim (low quality)   | ThumbnailImageGenerator   |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

**Explanation:**
The **Media Processing Ports** are the "workers" of the system. They perform the heavy computational tasks.
*   **RenderRunnerPort:** This is the boss of rendering. It takes the code for a scene and tells Manim to create the video. The adapter uses `subprocess` to run Manim as a separate program, which prevents SuperManim from freezing while rendering.
*   **AudioProcessorPort:** This cuts audio files. If you have a 60-second audio file and want to split it into 4 scenes, this port does the cutting. It usually uses FFmpeg because it is the industry standard.
*   **VideoAssemblerPort:** After all scenes are rendered, this port stitches them together into one final video file.
*   **AudioAnalyzerPort:** In "SuperManim Mode," this port listens to the audio to find silence or measure duration automatically.

---

###### Infrastructure Ports (System & Files)

```text
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| FileStoragePort           | LocalFileStorage          | os, shutil, pathlib   | CloudStorageAdapter,      |
|                           |                           |                       | S3StorageAdapter          |
+---------------------------+---------------------------+-----------------------+---------------------------+
| HashComputerPort          | Sha256HashComputer        | Python hashlib        | Md5HashComputer,          |
|                           |                           |                       | FakeHashComputer          |
+---------------------------+---------------------------+-----------------------+---------------------------+
| TempFileManagerPort       | SystemTempManager         | Python tempfile       | InMemoryTempManager       |
+---------------------------+---------------------------+-----------------------+---------------------------+
| AssetManagerPort          | LocalAssetManager         | File System           | CloudAssetManager         |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

**Explanation:**
The **Infrastructure Ports** handle the "dirty work" of interacting with the computer's operating system.
*   **FileStoragePort:** This creates folders, moves files, and checks if a file exists. It keeps the Core logic clean from messy file path code.
*   **HashComputerPort:** This creates a unique "fingerprint" for files. SuperManim uses this to check if a scene's code changed. If the fingerprint is the same as last time, it skips rendering. This is the secret to SuperManim's speed.
*   **TempFileManagerPort:** Manages temporary files that are created during processing and then deleted.

---

###### Driving Ports (Input / User Commands)

```text
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| ProjectCommandPort        | CliProjectCommandAdapter  | Terminal (argparse)   | GuiProjectCommandAdapter, |
|                           |                           |                       | ApiProjectCommandAdapter  |
+---------------------------+---------------------------+-----------------------+---------------------------+
| SceneCommandPort          | CliSceneCommandAdapter    | Terminal (argparse)   | GuiSceneCommandAdapter    |
+---------------------------+---------------------------+-----------------------+---------------------------+
| RenderCommandPort         | CliRenderCommandAdapter   | Terminal (argparse)   | GuiRenderCommandAdapter   |
+---------------------------+---------------------------+-----------------------+---------------------------+
| AudioCommandPort          | CliAudioCommandAdapter    | Terminal (argparse)   | GuiAudioCommandAdapter    |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

**Explanation:**
The **Driving Ports** are the entry points. They are how the user "drives" or controls the application.
*   **ProjectCommandPort:** Handles commands like `new project` or `open project`.
*   **SceneCommandPort:** Handles commands like `add scene` or `set duration`.
*   **RenderCommandPort:** Handles the `render` command.
*   By using these ports, SuperManim can switch from a text-based Terminal interface (CLI) to a graphical window interface (GUI) without changing any of the core logic.

---

###### Notification Ports (Output / Feedback)

```text
+---------------------------+---------------------------+-----------------------+---------------------------+
| Port (Interface)          | Adapter (Implementation)  | External Technology   | Alternative Adapters      |
+---------------------------+---------------------------+-----------------------+---------------------------+
| NotificationPort          | CliNotifier               | print() / rich        | GuiNotifier,              |
|                           |                           |                       | LoggingNotifier           |
+---------------------------+---------------------------+-----------------------+---------------------------+
| ProgressReporterPort      | CliProgressReporter       | rich.progress         | GuiProgressBar            |
+---------------------------+---------------------------+-----------------------+---------------------------+
| LoggerPort                | FileLogger                | Python logging        | ConsoleLogger             |
+---------------------------+---------------------------+-----------------------+---------------------------+
```

**Explanation:**
The **Notification Ports** handle sending information back to the user.
*   **NotificationPort:** Sends simple messages like "Render Complete" or "Error: File not found". In the CLI adapter, this prints text. In a GUI adapter, this would show a pop-up window.
*   **ProgressReporterPort:** Shows how much work is done (e.g., a progress bar).
*   **LoggerPort:** Writes detailed logs to a file for debugging purposes later.




---


