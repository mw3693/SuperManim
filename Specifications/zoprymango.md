# SuperManim — Deep Architecture Explanation
## The Core, The Ports, The Adapters, The Services — And What Layered Architecture Does INSIDE the Core

---

# PART 1 — THE FULL PICTURE FIRST

Before we go deep into any one piece, look at this full map.
Every piece of the architecture is shown here.
We will then zoom into each box one by one.

```
+====================================================================================+
|                     THE COMPLETE SUPERMANIM ARCHITECTURE                           |
+====================================================================================+
|                                                                                    |
|   THE OUTSIDE WORLD                                                                |
|   (things that are NOT SuperManim — they are external programs and technologies)  |
|                                                                                    |
|   [ Terminal / User ]   [ SQLite ]   [ Manim ]   [ FFmpeg ]   [ File System ]    |
|          |                  |            |            |              |             |
|          |                  |            |            |              |             |
+----------+------------------+------------+------------+--------------+-------------+
|                                                                                    |
|   THE ADAPTERS                                                                     |
|   (the bridge between the outside world and the inside world)                     |
|                                                                                    |
|   [ CliShell ]   [ SqliteSceneRepo ]   [ ManimRenderer ]   [ FfmpegProcessor ]   |
|          |                  |                  |                   |              |
|          |                  |                  |                   |              |
+----------+------------------+------------------+-------------------+--------------+
|                                                                                    |
|   THE PORTS                                                                        |
|   (the contracts — what the Core says it needs, without knowing who provides it)  |
|                                                                                    |
|   [ ProjectCommandPort ]   [ SceneRepositoryPort ]   [ RenderRunnerPort ]        |
|   [ NotificationPort   ]   [ AudioProcessorPort  ]   [ FileStoragePort  ]        |
|              |                       |                       |                    |
|              |                       |                       |                    |
+==============+=======================+=======================+====================+
||                                                                                  ||
||   THE CORE                                                                       ||
||   (the inside world — pure logic, no external technology)                        ||
||                                                                                  ||
||   +--------------------------------------------------------------------------+  ||
||   |  APPLICATION SERVICES (Use Cases)                                        |  ||
||   |                                                                          |  ||
||   |  ProjectManager   SceneManager   AudioManager   RenderOrchestrator       |  ||
||   |  TimelineEngine   CacheManager   PreviewManager  ExportManager           |  ||
||   +--------------------------------------------------------------------------+  ||
||                              |                                                   ||
||                              | (these services use the domain objects below)     ||
||                              v                                                   ||
||   +--------------------------------------------------------------------------+  ||
||   |  DOMAIN SERVICES + DOMAIN MODELS                                         |  ||
||   |                                                                          |  ||
||   |  Scene    Project    AudioClip    RenderResult                           |  ||
||   |  TimelineCalculator   HashChecker   ValidationRules                     |  ||
||   +--------------------------------------------------------------------------+  ||
||                                                                                  ||
+==================================================================================+
```

Now let's understand every piece — what it IS, what it DOES, and WHY it exists.

---

# PART 2 — THE CORE

## What is the Core?

The Core is the brain of SuperManim. It is a completely self-contained world.

The Core knows:
- What a Scene is (it has a duration, a code file, a status)
- What a Project is (it has a name, a list of scenes, an audio file)
- The rules of the system (if a scene's hash has not changed, skip the render)
- How to coordinate work (render scene 3, then mark it as rendered, then notify the user)

The Core does NOT know:
- That SQLite exists
- That Manim exists
- That FFmpeg exists
- That the terminal (print) exists
- That the file system exists
- That `os`, `subprocess`, `sqlite3` are Python libraries

This is not accidental. This is the most important design rule:

```
+------------------------------------------------------------------+
|                                                                  |
|   THE CORE'S PRIME RULE:                                         |
|                                                                  |
|   The Core never imports or calls any external technology.       |
|   It only uses Python's built-in types (int, str, bool, list)   |
|   and its own objects (Scene, Project, AudioClip).               |
|                                                                  |
|   If you open any file inside core/ and you see this:           |
|                                                                  |
|       import sqlite3                                             |
|       import subprocess                                          |
|       import os                                                  |
|       from manim import *                                        |
|                                                                  |
|   Something is WRONG. That file does not belong in the Core.    |
|                                                                  |
+------------------------------------------------------------------+
```

## Where Does the Core Live (in Files)?

```
supermanim/
│
└── core/                    <--- Everything in this folder is "The Core"
    │
    ├── models/              <--- Domain Layer (inside the Core)
    │   ├── scene.py
    │   ├── project.py
    │   └── audio_clip.py
    │
    ├── services/            <--- This is where the two types of services live
    │   ├── domain/          <--- Domain Services (inside the Core)
    │   │   ├── timeline_calculator.py
    │   │   ├── hash_checker.py
    │   │   └── validation_rules.py
    │   │
    │   └── application/     <--- Application Services (inside the Core)
    │       ├── project_manager.py
    │       ├── scene_manager.py
    │       ├── audio_manager.py
    │       ├── render_orchestrator.py
    │       ├── cache_manager.py
    │       ├── preview_manager.py
    │       └── export_manager.py
    │
    └── ports/               <--- The Ports (the contracts the Core defines)
        ├── repository_ports.py
        ├── media_ports.py
        ├── infrastructure_ports.py
        ├── driving_ports.py
        └── notification_ports.py
```

---

# PART 3 — THE TWO TYPES OF SERVICES

This is the part you said you don't understand. Let's go very deep here.

## The Big Confusion

When people first hear "Domain Services" and "Application Services," they think:
"What's the difference? They're both inside the Core. They both contain logic.
Why do I need two types?"

The answer becomes clear when you understand **what kind of question each one answers**.

```
+---------------------------------------------------------------------+
|                                                                     |
|   DOMAIN SERVICE answers:                                           |
|   "Is this THING valid according to our business rules?"            |
|   "What is the correct VALUE for this THING?"                       |
|   "Does this relationship make sense?"                              |
|                                                                     |
|   It works with DATA OBJECTS only.                                  |
|   It does NOT coordinate with Ports.                                |
|   It is PURE CALCULATION.                                           |
|                                                                     |
+---------------------------------------------------------------------+
|                                                                     |
|   APPLICATION SERVICE answers:                                      |
|   "How do we complete this USER REQUEST from start to finish?"      |
|   "Which steps happen in which order?"                              |
|   "Who do I need to call to make this happen?"                      |
|                                                                     |
|   It coordinates between Domain objects AND Ports.                  |
|   It is the WORKFLOW DIRECTOR.                                       |
|                                                                     |
+---------------------------------------------------------------------+
```

Let's make this concrete with SuperManim examples.

---

## DOMAIN SERVICES — Explained in Depth

### What is a Domain Service?

A Domain Service is a piece of logic that:
1. Takes some data objects as input
2. Applies a business rule to them
3. Returns an answer or raises an error

It does NOT touch the database. It does NOT call Manim. It does NOT read files.
It only works with the data objects you give it.

Think of a Domain Service like a CALCULATOR or a JUDGE:
- You give it numbers (data objects)
- It computes the answer or decides if something is allowed
- It gives you back the result

### The Domain Services in SuperManim

SuperManim has three Domain Services. Let's look at each one in detail.

---

### Domain Service 1 — TimelineCalculator

**The Question It Answers:**
"Do the scene durations make sense? Do they add up to the audio length?
Is Scene 3's duration the same as its audio clip's duration?"

**Why It Exists:**
Duration math is one of the most important rules in SuperManim.
A scene cannot be synced with audio unless their durations match EXACTLY.
If Scene 3 is 16.8 seconds but its audio clip is 17.2 seconds, that is an error.
This rule needs to be checked in many places:
- When you set a scene duration
- When you try to sync a scene with audio
- Before rendering a synced scene
- Before exporting

If you put this math directly inside SceneManager or RenderOrchestrator,
you have to write it multiple times and keep it consistent.
Instead, you put it in one place: TimelineCalculator.
Anything that needs timeline math just calls TimelineCalculator.

**What It Looks Like in Code:**

```python
# core/services/domain/timeline_calculator.py

class TimelineCalculator:
    """
    Pure timeline math. No database. No files. No Manim.
    Takes data objects, returns calculated results.
    """

    def total_duration(self, scenes: list[Scene]) -> float:
        """Add up the durations of all scenes. Return the total in seconds."""
        return sum(scene.duration for scene in scenes)

    def durations_match(self, scene: Scene, audio_clip: AudioClip) -> bool:
        """
        Check if a scene's duration and its audio clip's duration are identical.
        Returns True if they match. Returns False if they do not.
        """
        return abs(scene.duration - audio_clip.duration) < 0.001
        # Note: we use < 0.001 instead of == because floating point
        # numbers are not perfectly equal. 16.800 might be stored as
        # 16.8000000001 internally. So we check if the difference is
        # smaller than 1 millisecond.

    def duration_difference(self, scene: Scene, audio_clip: AudioClip) -> float:
        """
        Return the exact difference in seconds between the scene and clip.
        Used to tell the user exactly how far off they are.
        Example: returns 2.3 if scene=7.0s and clip=9.3s.
        """
        return abs(scene.duration - audio_clip.duration)

    def total_matches_audio(self, scenes: list[Scene], audio: AudioFile) -> bool:
        """
        Check if the sum of all scene durations equals the total audio length.
        """
        total_scenes = self.total_duration(scenes)
        return abs(total_scenes - audio.total_duration) < 0.001

    def find_unmatched_scenes(
        self, scenes: list[Scene], clips: list[AudioClip]
    ) -> list[tuple[Scene, AudioClip, float]]:
        """
        Find all scenes whose duration does NOT match their audio clip.
        Returns a list of (scene, clip, difference) tuples for reporting.
        """
        unmatched = []
        for scene, clip in zip(scenes, clips):
            if not self.durations_match(scene, clip):
                diff = self.duration_difference(scene, clip)
                unmatched.append((scene, clip, diff))
        return unmatched
```

**How It Is Used:**

The Application Services (like SyncManager or RenderOrchestrator) call TimelineCalculator
when they need to check durations. They don't re-write the math themselves.

```python
# Inside RenderOrchestrator (an Application Service)
# Notice: it uses TimelineCalculator to do the math

def render_scene(self, scene_id: int):
    scene = self.scene_repo.load_scene(scene_id)
    clip  = self.audio_repo.load_clip_for_scene(scene_id)

    if scene.synced_with_audio:
        # Use the Domain Service to check durations
        if not self.timeline.durations_match(scene, clip):
            diff = self.timeline.duration_difference(scene, clip)
            self.notifier.send_error(
                f"Cannot render. Scene={scene.duration}s, "
                f"Clip={clip.duration}s. Difference={diff}s."
            )
            return
    # ... continue with render
```

---

### Domain Service 2 — HashChecker

**The Question It Answers:**
"Has this scene's code file changed since the last time we rendered it?
Is the current fingerprint different from the stored fingerprint?"

**Why It Exists:**
The whole speed advantage of SuperManim comes from one idea:
"If the code has not changed, don't render again."
To check this, you need to compare fingerprints (SHA-256 hashes).

This comparison logic is used in two places:
1. Before rendering a single scene
2. Before rendering all scenes (to find which ones changed)

Instead of writing this comparison logic twice, it lives in HashChecker.
HashChecker compares hashes. CacheManager stores hashes.
They are separate because "comparing" and "storing" are different jobs.

**What It Looks Like in Code:**

```python
# core/services/domain/hash_checker.py

class HashChecker:
    """
    Compares hash fingerprints to decide if a file has changed.
    Does NOT compute hashes (that is the HashComputerPort's job).
    Does NOT store hashes (that is the CacheRepositoryPort's job).
    Only COMPARES them.
    """

    def has_changed(self, current_hash: str, stored_hash: str | None) -> bool:
        """
        Returns True if the file has changed (hashes are different).
        Returns True if there is no stored hash (never been rendered before).
        Returns False if the hashes are identical (file is unchanged).
        """
        if stored_hash is None:
            return True   # Never rendered before. Must render.
        return current_hash != stored_hash

    def find_changed_scenes(
        self,
        scenes: list[Scene],
        current_hashes: dict[int, str],
        stored_hashes:  dict[int, str | None]
    ) -> list[Scene]:
        """
        Given a list of scenes and two dictionaries of hashes,
        return only the scenes that have changed (or never been rendered).

        current_hashes  = {scene_id: current_hash_of_code_file}
        stored_hashes   = {scene_id: last_known_hash_from_database}

        Returns the list of scenes that NEED to be rendered.
        """
        changed = []
        for scene in scenes:
            current = current_hashes.get(scene.id)
            stored  = stored_hashes.get(scene.id)
            if self.has_changed(current, stored):
                changed.append(scene)
        return changed

    def all_unchanged(
        self,
        current_hashes: dict[int, str],
        stored_hashes:  dict[int, str | None]
    ) -> bool:
        """
        Quick check: have ALL scenes remained unchanged?
        Returns True only if every single scene's hash matches.
        """
        for scene_id, current in current_hashes.items():
            stored = stored_hashes.get(scene_id)
            if self.has_changed(current, stored):
                return False
        return True
```

**How It Is Used:**

```python
# Inside RenderOrchestrator (an Application Service)

def render_all(self):
    scenes = self.scene_repo.load_all_scenes()

    # Compute current hashes (via Port — calls the real file on disk)
    current_hashes = {
        s.id: self.hash_computer.compute(s.code_path) for s in scenes
    }

    # Load stored hashes (via Port — reads from database)
    stored_hashes = self.cache_repo.load_all_hashes()

    # Use the Domain Service to find what changed
    scenes_to_render = self.hash_checker.find_changed_scenes(
        scenes, current_hashes, stored_hashes
    )

    if not scenes_to_render:
        self.notifier.send("All scenes unchanged. Nothing to render.")
        return

    for scene in scenes_to_render:
        self._render_one_scene(scene)
```

---

### Domain Service 3 — ValidationRules

**The Question It Answers:**
"Is this project in a valid state? Is this scene complete and ready to be rendered?
Is the audio setup correct?"

**Why It Exists:**
Before SuperManim does any major operation (render, export, sync), it should check
that everything is set up correctly. These checks are the "rules of the game":

- A scene cannot be rendered without a code file
- A synced scene cannot be rendered if durations don't match
- A project cannot be exported if any scene has status "failed"
- A scene number must be between 1 and the total number of scenes

All of these are business rules. They belong in the Domain, not in the
Application Services. If SceneManager contains validation logic, and
RenderOrchestrator also contains validation logic, and ExportManager also
contains validation logic — you will have duplicate code and inconsistent rules.

ValidationRules is the single source of truth for all rules.

**What It Looks Like in Code:**

```python
# core/services/domain/validation_rules.py

from dataclasses import dataclass

@dataclass
class ValidationError:
    scene_id: int | None
    message:  str
    fix_hint: str      # What the user should do to fix this

class ValidationRules:
    """
    The rulebook. Checks data objects against business rules.
    Returns lists of errors. Does NOT call any ports.
    Does NOT modify any data. READ ONLY.
    """

    def scene_is_renderable(self, scene: Scene) -> list[ValidationError]:
        """
        Returns a list of errors that prevent this scene from being rendered.
        Returns an empty list if the scene is ready to render.
        """
        errors = []

        if scene.code_path is None:
            errors.append(ValidationError(
                scene_id = scene.id,
                message  = f"Scene {scene.id} has no code file assigned.",
                fix_hint = f"set scene {scene.id} code <path_to_file.py>"
            ))

        if scene.duration is None:
            errors.append(ValidationError(
                scene_id = scene.id,
                message  = f"Scene {scene.id} has no duration set.",
                fix_hint = f"set scene {scene.id} duration <seconds>"
            ))

        if scene.synced_with_audio and scene.audio_clip is None:
            errors.append(ValidationError(
                scene_id = scene.id,
                message  = f"Scene {scene.id} is marked synced but has no audio clip.",
                fix_hint = f"sync scene {scene.id} audio_clip <clip_number>"
            ))

        return errors

    def project_is_exportable(self, scenes: list[Scene]) -> list[ValidationError]:
        """
        Returns a list of errors that prevent the project from being exported.
        An empty list means the project is ready to export.
        """
        errors = []
        for scene in scenes:
            if scene.status == "pending":
                errors.append(ValidationError(
                    scene_id = scene.id,
                    message  = f"Scene {scene.id} has not been rendered yet.",
                    fix_hint = f"render scene {scene.id}"
                ))
            elif scene.status == "failed":
                errors.append(ValidationError(
                    scene_id = scene.id,
                    message  = f"Scene {scene.id} failed to render: {scene.error_message}",
                    fix_hint = f"Fix the code error, then run: render failed"
                ))
        return errors

    def scene_number_is_valid(self, scene_number: int, total_scenes: int) -> bool:
        """
        Check if a scene number makes sense for this project.
        Example: Scene 7 is not valid if the project only has 5 scenes.
        """
        return 1 <= scene_number <= total_scenes

    def audio_sync_is_valid(
        self, scene: Scene, clip: AudioClip
    ) -> list[ValidationError]:
        """
        Check if a scene can be synced to an audio clip.
        """
        errors = []
        diff = abs(scene.duration - clip.duration)
        if diff >= 0.001:
            errors.append(ValidationError(
                scene_id = scene.id,
                message  = (
                    f"Duration mismatch. "
                    f"Scene {scene.id}={scene.duration}s, "
                    f"Clip={clip.duration}s. "
                    f"Difference={diff:.3f}s."
                ),
                fix_hint = (
                    f"Option A: set scene {scene.id} duration {clip.duration}\n"
                    f"Option B: re-cut the audio to {scene.duration}s"
                )
            ))
        return errors
```

---

## APPLICATION SERVICES — Explained in Depth

### What is an Application Service?

An Application Service is a Use Case — it represents ONE complete task
that a user wants to accomplish.

When the user types `render all` in the shell, something has to:
1. Load all the scenes from the database
2. Compute the hash of each scene's code file
3. Compare current hashes to stored hashes
4. Decide which scenes to render
5. Call Manim for each changed scene
6. Save the render result back to the database
7. Update the progress bar
8. Print a success or failure message

That sequence of steps — that **workflow** — is what an Application Service does.

```
+----------------------------------------------------------------------+
|                                                                      |
|   DOMAIN SERVICE   =   "Is this valid?" / "What is the value?"      |
|                        Pure calculation. No steps. No coordination.  |
|                                                                      |
|   APPLICATION      =   "Here are all the steps to complete          |
|   SERVICE              this user request."                           |
|                        Coordination. Steps. Calls Ports.             |
|                                                                      |
+----------------------------------------------------------------------+
```

An Application Service is the ONLY type of object in the Core that is
allowed to call Ports. Domain Services never call Ports.
Domain Models never call Ports.
Only Application Services call Ports.

```
+----------------------------------------------------------------------+
|   WHO IS ALLOWED TO CALL PORTS?                                      |
+----------------------------------------------------------------------+
|                                                                      |
|   Domain Models (Scene, Project, AudioClip)  --> NO. Never.         |
|   Domain Services (TimelineCalc, HashChecker) -> NO. Never.         |
|   Application Services (SceneManager, etc.)  --> YES. This is       |
|                                                   their job.         |
|                                                                      |
+----------------------------------------------------------------------+
```

### The Application Services in SuperManim

Let's look at each Application Service and understand exactly what it does.

---

### Application Service 1 — ProjectManager

**The User Request It Handles:**
`new project MyAnimation`, `open project MyAnimation`,
`close project`, `delete project OldTest`, `project info`

**Its Job:**
It manages the lifecycle of a project. Creating it, opening it,
closing it, deleting it, and reporting its current state.

**What Ports It Uses:**

```
+----------------------------------------------------------+
|   ProjectManager uses these Ports:                       |
|                                                          |
|   ProjectRepositoryPort  --> to save/load project data  |
|   FileStoragePort        --> to create/delete folders   |
|   NotificationPort       --> to tell the user what      |
|                              happened                    |
+----------------------------------------------------------+
```

**What It Looks Like in Code:**

```python
# core/services/application/project_manager.py

class ProjectManager:

    def __init__(
        self,
        project_repo:  ProjectRepositoryPort,
        file_storage:  FileStoragePort,
        notifier:      NotificationPort,
    ):
        self.project_repo = project_repo
        self.file_storage = file_storage
        self.notifier     = notifier
        self.current_project: Project | None = None

    def create_project(self, name: str) -> None:
        """
        STEP 1: Check that no project with this name already exists.
        STEP 2: Create the project folder and all subfolders.
        STEP 3: Save the new project record in the database.
        STEP 4: Set this as the active project.
        STEP 5: Tell the user it was created.
        """
        if self.project_repo.project_exists(name):
            self.notifier.send_error(f'Project "{name}" already exists.')
            return

        # Step 2: Create folders (via Port — no os.mkdir here)
        self.file_storage.create_folder(f"projects/{name}")
        self.file_storage.create_folder(f"projects/{name}/scenes")
        self.file_storage.create_folder(f"projects/{name}/audio_clips")
        self.file_storage.create_folder(f"projects/{name}/output")
        self.file_storage.create_folder(f"projects/{name}/previews")
        self.file_storage.create_folder(f"projects/{name}/cache")
        self.file_storage.create_folder(f"projects/{name}/assets")
        self.file_storage.create_folder(f"projects/{name}/temp")
        self.file_storage.create_folder(f"projects/{name}/exports")

        # Step 3: Save to database (via Port — no SQL here)
        project = Project(name=name, mode=None)
        self.project_repo.save_project(project)

        # Step 4: Set as active
        self.current_project = project

        # Step 5: Tell the user (via Port — no print() here)
        self.notifier.send_success(f'Project "{name}" created successfully.')
```

Notice: ProjectManager never writes `os.mkdir()` or `sqlite3.connect()` or `print()`.
All of those are hidden inside the Adapters behind the Ports.

---

### Application Service 2 — SceneManager

**The User Request It Handles:**
`set scenes_number 5`, `add scene`, `set scene 3 duration 12.5`,
`set scene 3 code intro.py`, `list scenes`, `delete scene 4`,
`swap scenes 2 4`, `duplicate scene 3`

**Its Job:**
It manages all scene data inside a project.
When you add a scene, it creates it. When you set a duration, it updates it.
When you list scenes, it loads them all and passes them to the notifier to display.

**What Ports It Uses:**

```
+----------------------------------------------------------+
|   SceneManager uses these Ports:                         |
|                                                          |
|   SceneRepositoryPort  --> to save/load/delete scenes   |
|   FileStoragePort      --> to check if code files exist |
|   HashComputerPort     --> to fingerprint code files    |
|   NotificationPort     --> to tell the user the result  |
+----------------------------------------------------------+
```

**And It Uses This Domain Service:**

```
+----------------------------------------------------------+
|   SceneManager also uses:                                |
|                                                          |
|   ValidationRules      --> to check if the scene        |
|                            number is valid, if the      |
|                            code file path is correct    |
+----------------------------------------------------------+
```

**What It Looks Like in Code:**

```python
# core/services/application/scene_manager.py

class SceneManager:

    def __init__(
        self,
        scene_repo:      SceneRepositoryPort,
        file_storage:    FileStoragePort,
        hash_computer:   HashComputerPort,
        notifier:        NotificationPort,
        validation:      ValidationRules,   # <-- Domain Service injected here
    ):
        self.scene_repo    = scene_repo
        self.file_storage  = file_storage
        self.hash_computer = hash_computer
        self.notifier      = notifier
        self.validation    = validation

    def set_scene_code(self, scene_id: int, code_path: str) -> None:
        """
        Assign a code file to a scene.

        STEP 1: Check the file actually exists on disk.
        STEP 2: Compute a fingerprint of the file.
        STEP 3: Update the scene record in the database.
        STEP 4: Tell the user the file was assigned.
        """
        # Step 1: Check file exists (via Port)
        if not self.file_storage.file_exists(code_path):
            self.notifier.send_error(f"File not found: {code_path}")
            return

        # Step 2: Compute fingerprint (via Port)
        fingerprint = self.hash_computer.compute(code_path)

        # Step 3: Update database (via Port)
        self.scene_repo.update_scene_code_path(scene_id, code_path)
        self.scene_repo.update_scene_hash(scene_id, fingerprint)

        # Step 4: Notify (via Port)
        self.notifier.send_success(
            f"Scene {scene_id} code file assigned.\n"
            f"File: {code_path}\n"
            f"Fingerprint: {fingerprint[:16]}..."
        )
```

---

### Application Service 3 — AudioManager

**The User Request It Handles:**
`add audio voice.mp3`, `change audio_format wav`,
`split audio auto`, `split audio half`,
`split audio duration 12.5 18.5 16.8`,
`audio info`

**Its Job:**
It manages everything related to the audio file:
copying it into the project, converting its format, splitting it into clips,
and reporting its properties.

**What Ports It Uses:**

```
+----------------------------------------------------------+
|   AudioManager uses these Ports:                         |
|                                                          |
|   AudioRepositoryPort  --> to save/load audio records   |
|   AudioProcessorPort   --> to convert/split audio files |
|                             (this calls FFmpeg)          |
|   AudioAnalyzerPort    --> to detect silences            |
|                             (this calls librosa)         |
|   FileStoragePort      --> to copy the audio file in    |
|   NotificationPort     --> to report results            |
+----------------------------------------------------------+
```

**And It Uses This Domain Service:**

```
+----------------------------------------------------------+
|   AudioManager also uses:                                |
|                                                          |
|   TimelineCalculator   --> to check if the split clips  |
|                            add up to the total duration |
+----------------------------------------------------------+
```

---

### Application Service 4 — RenderOrchestrator

**The User Request It Handles:**
`render scene 3`, `render all`, `render pending`, `render failed`,
`force render scene 3`, `force render all`

**Its Job:**
This is the most complex Application Service. It is the one that implements
the core superpower of SuperManim: smart, incremental rendering.

Its complete workflow for `render all`:

```
+------------------------------------------------------------+
|   RenderOrchestrator.render_all() — Full Workflow          |
+------------------------------------------------------------+
|                                                            |
|   1.  Load all scenes from database.          [Port]       |
|   2.  Check each scene has a code file.       [DomainSvc]  |
|   3.  Compute current hash of each code file. [Port]       |
|   4.  Load stored hashes from cache.          [Port]       |
|   5.  Find which scenes changed.              [DomainSvc]  |
|   6.  For each CHANGED scene:                              |
|       a. Validate it is ready to render.      [DomainSvc]  |
|       b. Check synced_with_audio flag.        [Model]      |
|       c. If synced: check durations match.    [DomainSvc]  |
|       d. Call renderer to run Manim.          [Port]       |
|       e. If success: mark scene rendered.     [Port]       |
|                      save new hash.           [Port]       |
|                      notify user.             [Port]       |
|       f. If failure: mark scene failed.       [Port]       |
|                      save error message.      [Port]       |
|                      notify user.             [Port]       |
|   7.  For each UNCHANGED scene:                            |
|       a. Notify user "Scene X skipped."       [Port]       |
|   8.  Report summary.                         [Port]       |
|                                                            |
+------------------------------------------------------------+
```

**What Ports and Domain Services It Uses:**

```
+----------------------------------------------------------+
|   RenderOrchestrator uses these Ports:                   |
|                                                          |
|   SceneRepositoryPort   --> load/save/update scenes     |
|   CacheRepositoryPort   --> load/save hash fingerprints |
|   HashComputerPort      --> compute hashes of files     |
|   RenderRunnerPort      --> actually call Manim         |
|   AudioRepositoryPort   --> load audio clip for scene   |
|   NotificationPort      --> report progress and results |
|   ProgressReporterPort  --> show progress bar           |
|                                                          |
|   And these Domain Services:                             |
|   HashChecker           --> decide if scene changed     |
|   TimelineCalculator    --> check duration matches      |
|   ValidationRules       --> check scene is renderable   |
+----------------------------------------------------------+
```

---

### Application Service 5 — CacheManager

**The User Request It Handles:**
`clear cache`, `clear cache scene 3`, `cache info`
(Also used internally by RenderOrchestrator)

**Its Job:**
It manages the stored fingerprints (hashes) that make smart rendering possible.
When you force a re-render of a scene, CacheManager deletes the stored hash for that scene.
When you clear all caches, it deletes all stored hashes.

**What Ports It Uses:**

```
+----------------------------------------------------------+
|   CacheManager uses these Ports:                         |
|                                                          |
|   CacheRepositoryPort  --> read/delete stored hashes    |
|   NotificationPort     --> report cache status          |
+----------------------------------------------------------+
```

---

### Application Service 6 — TimelineEngine

**The User Request It Handles:**
`set scene 3 duration 12.5` (updates timeline after setting duration)
`sync all` (verifies all durations before syncing)
`timeline info` (shows the full audio/scene timeline)

**Its Job:**
It manages the timeline of the whole project — the sequence of scenes,
their start/end timestamps, and how they relate to the audio.

Think of it as the "timeline view" that a video editor shows you.
It knows that Scene 1 starts at 0:00, ends at 0:12.5,
Scene 2 starts at 0:12.5, ends at 0:31.0, and so on.

**What Ports and Domain Services It Uses:**

```
+----------------------------------------------------------+
|   TimelineEngine uses:                                   |
|                                                          |
|   SceneRepositoryPort   --> load all scenes             |
|   AudioRepositoryPort   --> load audio info             |
|   NotificationPort      --> display timeline            |
|                                                          |
|   TimelineCalculator    --> all the duration math       |
|   ValidationRules       --> check timeline is valid     |
+----------------------------------------------------------+
```

---

### Application Service 7 — PreviewManager

**The User Request It Handles:**
`preview scene 3`, `preview all`, `force preview scene 3`,
`preview status`, `open preview 3`, `clear previews`

**Its Job:**
It generates low-quality preview videos for scenes so the user can check
their work without waiting for a full render.

**What Ports It Uses:**

```
+----------------------------------------------------------+
|   PreviewManager uses these Ports:                       |
|                                                          |
|   SceneRepositoryPort   --> load scene data             |
|   PreviewGeneratorPort  --> call Manim in low-Q mode    |
|   FileStoragePort       --> check/delete preview files  |
|   NotificationPort      --> report results              |
+----------------------------------------------------------+
```

---

### Application Service 8 — ExportManager

**The User Request It Handles:**
`export`, `export status`, `set export format mp4`,
`set export quality high`, `set export name MyVideo`

**Its Job:**
It assembles all the rendered scene clips into one final video file.
It also manages export settings (format, quality, output name).

**What Ports It Uses:**

```
+----------------------------------------------------------+
|   ExportManager uses these Ports:                        |
|                                                          |
|   SceneRepositoryPort   --> load all scenes             |
|   ProjectRepositoryPort --> load/save export settings   |
|   FileStoragePort       --> check all clip files exist  |
|   VideoAssemblerPort    --> call FFmpeg to stitch clips |
|   NotificationPort      --> report export progress      |
|   ProgressReporterPort  --> show progress bar           |
|                                                          |
|   ValidationRules       --> check all scenes rendered   |
+----------------------------------------------------------+
```

---

# PART 4 — THE COMPLETE SERVICES PICTURE

Now that you know each service, here is the full picture in one diagram.
This shows every service, what type it is, and who it talks to.

```
+======================================================================+
|              ALL SERVICES IN SUPERMANIM — COMPLETE MAP               |
+======================================================================+
|                                                                      |
|  DOMAIN SERVICES (pure calculation — no Ports allowed)               |
|  +------------------------------------------------------------------+|
|  |                                                                  ||
|  |  TimelineCalculator          HashChecker       ValidationRules   ||
|  |  - total_duration()          - has_changed()   - scene_is_      ||
|  |  - durations_match()         - find_changed_     renderable()   ||
|  |  - find_unmatched()            _scenes()       - project_is_    ||
|  |  - total_matches_audio()     - all_unchanged()   exportable()   ||
|  |                                                - scene_number_  ||
|  |                                                  is_valid()     ||
|  |                                                - audio_sync_    ||
|  |                                                  is_valid()     ||
|  +------------------------------------------------------------------+|
|                          ^         ^         ^                       |
|                          |         |         |                       |
|              (used by Application Services below)                    |
|                          |         |         |                       |
|  APPLICATION SERVICES (workflow coordinators — CAN use Ports)        |
|  +------------------------------------------------------------------+|
|  |                                                                  ||
|  |  ProjectManager    SceneManager    AudioManager                  ||
|  |  - create_project  - set_scenes_  - add_audio                   ||
|  |  - open_project      number       - split_auto                  ||
|  |  - close_project   - add_scene    - split_manual                ||
|  |  - delete_project  - set_duration - change_format               ||
|  |  - project_info    - set_code     - audio_info                  ||
|  |                    - list_scenes                                 ||
|  |                    - delete_scene                                ||
|  |                    - swap_scenes                                 ||
|  |                                                                  ||
|  |  RenderOrchestrator   CacheManager   TimelineEngine             ||
|  |  - render_scene        - clear_cache  - show_timeline           ||
|  |  - render_all          - clear_scene  - recalculate             ||
|  |  - render_pending        _cache       - validate_timeline       ||
|  |  - force_render        - cache_info                             ||
|  |  - render_status                                                ||
|  |                                                                  ||
|  |  PreviewManager        ExportManager                            ||
|  |  - preview_scene       - export                                 ||
|  |  - preview_all         - export_status                          ||
|  |  - force_preview       - set_format                             ||
|  |  - open_preview        - set_quality                            ||
|  |  - clear_previews      - set_name                               ||
|  +------------------------------------------------------------------+|
|                          |         |                                 |
|                          v         v                                 |
|  PORTS (what Application Services call — the contracts)              |
|  +------------------------------------------------------------------+|
|  |  SceneRepo  ProjectRepo  AudioRepo  CacheRepo                   ||
|  |  RenderRunner  AudioProcessor  VideoAssembler  AudioAnalyzer    ||
|  |  FileStorage  HashComputer  TempManager                         ||
|  |  Notifier  ProgressReporter  Logger                             ||
|  +------------------------------------------------------------------+|
|                          |         |                                 |
|                          v         v                                 |
|  ADAPTERS (the real implementations behind the Ports)                |
|  +------------------------------------------------------------------+|
|  |  SqliteSceneRepo  ManimRenderer  FfmpegProcessor  LocalFiles    ||
|  |  Sha256Hasher  CliNotifier  CliProgressBar  FileLogger          ||
|  +------------------------------------------------------------------+|
|                                                                      |
+======================================================================+
```

---

# PART 5 — THE LAYERED ARCHITECTURE INSIDE THE CORE

## Your Correction (And Why It Matters)

You said something very important:

> "The Layered Architecture is used to structure the CORE itself.
> Not the whole project."

You are completely correct. Let me explain this properly.

Hexagonal Architecture describes the OUTER boundary of the system:
- How the Core is separated from the outside world through Ports and Adapters.
- How you can swap Adapters without touching the Core.

Layered Architecture describes the INNER structure of the Core itself:
- How the pieces INSIDE the Core are organized.
- Which layer inside the Core is allowed to talk to which other layer.

Think of it like this:

```
+=====================================================================+
|                    TWO ARCHITECTURES, TWO JOBS                      |
+=====================================================================+
|                                                                     |
|  HEXAGONAL ARCHITECTURE   =   Describes the BORDER                 |
|                               Between Core and Outside World        |
|                               "The Core talks to Ports, not to     |
|                               real tools directly."                 |
|                                                                     |
|  LAYERED ARCHITECTURE     =   Describes the INTERIOR               |
|                               Inside the Core itself               |
|                               "Inside the Core, models don't call  |
|                               application services, and domain     |
|                               services don't call ports."          |
|                                                                     |
+=====================================================================+
```

## The 3 Layers INSIDE the Core

The Core itself has three internal layers.

```
+===================================================================+
|                   INSIDE THE CORE — 3 LAYERS                      |
+===================================================================+
|                                                                   |
|  LAYER 3 — APPLICATION LAYER                                      |
|  +---------------------------------------------------------------+|
|  |                                                               ||
|  |  ProjectManager   SceneManager   AudioManager                ||
|  |  RenderOrchestrator   CacheManager   TimelineEngine          ||
|  |  PreviewManager   ExportManager                              ||
|  |                                                               ||
|  |  These are the Use Cases. They receive user commands.         ||
|  |  They coordinate everything.                                  ||
|  |  They CAN call: Layer 2 (domain services + models)           ||
|  |  They CAN call: Ports (the Ports are defined in Layer 1)     ||
|  |  They CANNOT call: other Application Services directly       ||
|  |                    (one use case should not call another)    ||
|  +---------------------------------------------------------------+|
|                              |                                    |
|                  (depends on)  (calls)                            |
|                              v                                    |
|  LAYER 2 — DOMAIN LAYER                                           |
|  +---------------------------------------------------------------+|
|  |                                                               ||
|  |  DOMAIN SERVICES:                                             ||
|  |  TimelineCalculator   HashChecker   ValidationRules          ||
|  |                                                               ||
|  |  DOMAIN MODELS:                                               ||
|  |  Scene   Project   AudioClip   RenderResult                  ||
|  |                                                               ||
|  |  This is the "vocabulary" and "rules" of the system.         ||
|  |  Domain Services DO pure calculation.                        ||
|  |  Domain Models ARE the data shapes.                          ||
|  |  CANNOT call: Application Services (Layer 3)                 ||
|  |  CANNOT call: Ports (Layer 1)                                ||
|  |  CAN use: each other (models and domain services)            ||
|  +---------------------------------------------------------------+|
|                              |                                    |
|                  (depends on)                                     |
|                              v                                    |
|  LAYER 1 — PORT DEFINITIONS LAYER                                 |
|  +---------------------------------------------------------------+|
|  |                                                               ||
|  |  SceneRepositoryPort    ProjectRepositoryPort                ||
|  |  AudioRepositoryPort    CacheRepositoryPort                  ||
|  |  RenderRunnerPort       AudioProcessorPort                   ||
|  |  FileStoragePort        HashComputerPort                     ||
|  |  NotificationPort       ProgressReporterPort                 ||
|  |  ... (all 29 ports)                                          ||
|  |                                                               ||
|  |  These are CONTRACTS (abstract interfaces).                   ||
|  |  They say WHAT can be done, not HOW.                         ||
|  |  They know nothing about SQLite or Manim.                    ||
|  |  They ARE part of the Core (they live in core/ports/).       ||
|  |  They are at the BOTTOM because everything depends on them.  ||
|  |  Application Services call through them.                     ||
|  |  Adapters (outside the Core) implement them.                 ||
|  +---------------------------------------------------------------+|
|                                                                   |
+===================================================================+
```

## Why Ports Are at the Bottom (Layer 1) Inside the Core

This might seem strange. You might think: "The Ports are the outermost layer — they connect
to the outside world. Why are they at the bottom of the Core's internal layers?"

Here is the reason:

In Layered Architecture, the layer at the bottom is the one that every other layer DEPENDS ON.
It is the foundation.

The Ports define the vocabulary for all communication with the outside world.
Everything in the Core (both Application Services and Domain Services via the Application layer)
ultimately needs to communicate through these contracts.
The Ports are more stable than the Application Services.
If you add a new feature, you add new Application Service code — but the Ports stay the same.
So Ports go at the bottom, as the stable foundation.

```
+------------------------------------------------------------------+
|   DEPENDENCY DIRECTION (inside the Core)                         |
+------------------------------------------------------------------+
|                                                                  |
|   LAYER 3 (Application Services)                                 |
|       depends on  LAYER 2 (Domain)                               |
|       depends on  LAYER 1 (Ports)                                |
|                                                                  |
|   LAYER 2 (Domain Services + Models)                             |
|       depends on  nothing (pure Python only)                     |
|                                                                  |
|   LAYER 1 (Ports)                                                |
|       depends on  LAYER 2 (the models — e.g., SceneRepositoryPort|
|                   takes and returns Scene objects)               |
|                                                                  |
+------------------------------------------------------------------+

Arrow diagram:

   Layer 3 (Application) -----> Layer 2 (Domain)  <----- Layer 1 (Ports)
                         -----> Layer 1 (Ports)
```

Note that Layer 1 (Ports) depends on Layer 2 (Domain Models).
This is because the Ports describe operations using the domain objects.
For example, `SceneRepositoryPort.load_scene(id) -> Scene` — it returns a `Scene`,
which is a Domain Model. So the Port definition needs to know what a `Scene` is.
That is why the Ports layer also depends on the Domain Models layer.

---

## The Dependency Rules (The Law of the Core)

```
+=====================================================================+
|                    DEPENDENCY RULES INSIDE THE CORE                 |
+=====================================================================+
|                                                                     |
|  RULE 1: Application Services can call Domain Services.            |
|          "RenderOrchestrator can use HashChecker."                  |
|          ALLOWED.                                                   |
|                                                                     |
|  RULE 2: Application Services can call through Ports.              |
|          "SceneManager calls scene_repo.save_scene()"               |
|          ALLOWED.                                                   |
|                                                                     |
|  RULE 3: Domain Services can use Domain Models.                    |
|          "TimelineCalculator works with Scene objects."             |
|          ALLOWED.                                                   |
|                                                                     |
|  RULE 4: Domain Services CANNOT call Ports.                        |
|          "TimelineCalculator CANNOT call scene_repo.load_scene()"  |
|          FORBIDDEN. This would make the domain service know         |
|          about external technology. It would be impure.            |
|                                                                     |
|  RULE 5: Domain Models CANNOT call anyone.                         |
|          "The Scene class CANNOT call scene_repo or notifier."     |
|          FORBIDDEN. Models are pure data containers.               |
|                                                                     |
|  RULE 6: Application Services CANNOT call other Application        |
|          Services directly.                                         |
|          "SceneManager CANNOT call RenderOrchestrator."            |
|          FORBIDDEN. Each Use Case is independent.                  |
|          (They can share data through Ports/Repos though.)         |
|                                                                     |
+=====================================================================+
```

---

# PART 6 — A COMPLETE WALKTHROUGH: `render scene 3`

Let's trace exactly what happens, showing every layer, every service, every port.

```
USER TYPES:  render scene 3
```

```
+------------------------------------------------------------------+
|  OUTSIDE THE CORE — The Adapter receives the command             |
|                                                                  |
|  SuperManimShell.do_render("scene 3")                            |
|  [This is an Adapter — in adapters/cli/shell.py]                 |
|                                                                  |
|  It parses the text: command="render", target="scene", n=3       |
|  It calls: render_orchestrator.render_scene(scene_id=3)          |
|                                                                  |
|  <-- Crosses into the Core here                                  |
+------------------------------------------------------------------+
                      |
                      v
+------------------------------------------------------------------+
|  INSIDE THE CORE — Layer 3: Application Service                  |
|                                                                  |
|  RenderOrchestrator.render_scene(scene_id=3)                     |
|  [This is an Application Service]                                |
|                                                                  |
|  Step 1: Check a project is open.                                |
|    (just checks self.current_project is not None)                |
|                                                                  |
|  Step 2: Load the scene from the database.                       |
|    scene = self.scene_repo.load_scene(3)                         |
|    [calls SceneRepositoryPort -> Port Layer 1]                   |
|    [Port calls SqliteSceneRepository Adapter -> SQLite on disk]  |
|                                                                  |
|  Step 3: Validate the scene is renderable.                       |
|    errors = self.validation.scene_is_renderable(scene)           |
|    [calls ValidationRules -> Domain Service Layer 2]             |
|    [ValidationRules checks: code_path? duration? audio clip?]    |
|    if errors: report them via self.notifier, return.             |
|                                                                  |
|  Step 4: Compute the current hash of the code file.              |
|    current_hash = self.hash_computer.compute(scene.code_path)    |
|    [calls HashComputerPort -> Port Layer 1]                       |
|    [Port calls Sha256HashComputer Adapter -> reads file on disk] |
|                                                                  |
|  Step 5: Load the stored hash from cache.                        |
|    stored_hash = self.cache_repo.load_hash(scene_id=3)           |
|    [calls CacheRepositoryPort -> Port Layer 1]                   |
|    [Port calls SqliteCacheRepository Adapter -> SQLite on disk]  |
|                                                                  |
|  Step 6: Check if the code changed.                              |
|    changed = self.hash_checker.has_changed(current_hash,         |
|                                            stored_hash)          |
|    [calls HashChecker -> Domain Service Layer 2]                 |
|    [HashChecker compares two strings. Pure Python. No Ports.]    |
|                                                                  |
|  Step 7a: If NOT changed:                                        |
|    self.notifier.send("Scene 3 unchanged. Skipped.")             |
|    [calls NotificationPort -> Port Layer 1]                      |
|    [Port calls CliNotifier Adapter -> prints to terminal]        |
|    return.                                                       |
|                                                                  |
|  Step 7b: If CHANGED:                                            |
|                                                                  |
|    If scene.synced_with_audio:                                   |
|      clip = self.audio_repo.load_clip_for_scene(3)               |
|      [calls AudioRepositoryPort -> Port Layer 1]                 |
|                                                                  |
|      errors = self.timeline.durations_match(scene, clip)         |
|      [calls TimelineCalculator -> Domain Service Layer 2]        |
|      [TimelineCalculator compares two float numbers. Pure math.] |
|      if not match: report error, return.                         |
|                                                                  |
|    result = self.renderer.render(scene, include_audio=True)      |
|    [calls RenderRunnerPort -> Port Layer 1]                      |
|    [Port calls ManimSubprocessRenderer Adapter -> runs Manim]    |
|                                                                  |
|  Step 8: Save results.                                           |
|    if result.success:                                            |
|      self.scene_repo.mark_as_rendered(3, result.video_path)     |
|      self.cache_repo.save_hash(3, current_hash)                  |
|      self.notifier.send_success("Scene 3 rendered.")             |
|    else:                                                         |
|      self.scene_repo.mark_as_failed(3, result.error_message)    |
|      self.notifier.send_error("Scene 3 FAILED: ...")             |
|                                                                  |
|  <-- Returns to the Shell Adapter outside the Core              |
+------------------------------------------------------------------+
                      |
                      v
+------------------------------------------------------------------+
|  OUTSIDE THE CORE — Shell shows result to user                   |
|                                                                  |
|  supermanim>                                                     |
|  Scene 3 rendered successfully.                                  |
|  Output: output/scene_03/scene_03.mp4                            |
|                                                                  |
+------------------------------------------------------------------+
```

---

# PART 7 — THE FINAL CLEAN PICTURE

Here is the final, complete view of the architecture.
Print this page. Stick it on your wall. Refer to it every day while coding.

```
+==================================================================================+
|                     SUPERMANIM — FINAL ARCHITECTURE MAP                          |
+==================================================================================+
|                                                                                  |
|  THE USER                                                                        |
|  types: render scene 3                                                           |
|                                                                                  |
|  +--------------------+                                                          |
|  |   DRIVING ADAPTER  |  CliShell, CliProjectAdapter, CliRenderAdapter          |
|  |   (outside Core)   |  Lives in: adapters/cli/                                |
|  +--------------------+                                                          |
|          |  calls                                                                |
|          v                                                                       |
|  CORE BOUNDARY ---------------------------------------------------------------  |
|  |                                                                              ||
|  |  +----------------------------------------------------+                     ||
|  |  |  LAYER 3: APPLICATION SERVICES (Use Cases)         |                     ||
|  |  |                                                    |                     ||
|  |  |  ProjectManager    SceneManager    AudioManager    |                     ||
|  |  |  RenderOrchestrator  CacheManager  TimelineEngine  |                     ||
|  |  |  PreviewManager    ExportManager                   |                     ||
|  |  |                                                    |                     ||
|  |  |  - Receive user commands from Driving Adapters.   |                     ||
|  |  |  - Coordinate the workflow step by step.          |                     ||
|  |  |  - Call Domain Services for pure logic.           |                     ||
|  |  |  - Call Ports for external operations.            |                     ||
|  |  +----------------------------------------------------+                     ||
|  |          |  uses                        |  calls through                    ||
|  |          v                              v                                    ||
|  |  +------------------------+   +------------------------+                    ||
|  |  |  LAYER 2: DOMAIN       |   |  LAYER 1: PORTS        |                    ||
|  |  |                        |   |  (Contracts/Interfaces) |                    ||
|  |  |  DOMAIN SERVICES:      |   |                        |                    ||
|  |  |  TimelineCalculator    |   |  SceneRepositoryPort   |                    ||
|  |  |  HashChecker           |   |  RenderRunnerPort      |                    ||
|  |  |  ValidationRules       |   |  AudioProcessorPort    |                    ||
|  |  |                        |   |  FileStoragePort       |                    ||
|  |  |  DOMAIN MODELS:        |   |  HashComputerPort      |                    ||
|  |  |  Scene                 |   |  NotificationPort      |                    ||
|  |  |  Project               |   |  ... (all 29 ports)    |                    ||
|  |  |  AudioClip             |   |                        |                    ||
|  |  |  RenderResult          |   |  - Are defined INSIDE  |                    ||
|  |  |                        |   |    the Core.           |                    ||
|  |  |  - Pure Python.        |   |  - Are implemented     |                    ||
|  |  |  - No Ports.           |   |    OUTSIDE the Core    |                    ||
|  |  |  - No external calls.  |   |    by Adapters.        |                    ||
|  |  +------------------------+   +------------------------+                    ||
|  |                                         |  implemented by                   ||
|  CORE BOUNDARY ---------------------------------------------------------------  |
|                                            v                                     |
|  +--------------------+   +--------------------+   +--------------------+       |
|  |  SQLITE ADAPTER    |   |  MANIM ADAPTER     |   |  FFMPEG ADAPTER    |       |
|  |  SqliteSceneRepo   |   |  ManimRenderer     |   |  FfmpegProcessor   |       |
|  |  SqliteProjectRepo |   |  (subprocess.run)  |   |  FfmpegAssembler   |       |
|  +--------------------+   +--------------------+   +--------------------+       |
|          |                        |                        |                    |
|          v                        v                        v                    |
|  [ SQLite on disk ]      [ Manim Program ]       [ FFmpeg Program ]            |
|  [ .db file ]            [ renders animation ]   [ cuts/merges audio ]         |
|                                                                                  |
+==================================================================================+
```

---

# PART 8 — SUMMARY: ANSWERING YOUR EXACT QUESTIONS

**Question 1: "What are the services in this project?"**

There are two types of services, both living INSIDE the Core:

```
TYPE 1 — DOMAIN SERVICES (3 of them):
  TimelineCalculator   — Duration math
  HashChecker          — Fingerprint comparison
  ValidationRules      — Business rule checking

  These are CALCULATORS and JUDGES.
  They take data objects, apply rules, return answers.
  They NEVER call Ports.

TYPE 2 — APPLICATION SERVICES (8 of them):
  ProjectManager       — new/open/close/delete project
  SceneManager         — add/set/list/delete scenes
  AudioManager         — add/split/format audio
  RenderOrchestrator   — smart, incremental rendering
  CacheManager         — manage stored fingerprints
  TimelineEngine       — timeline coordination
  PreviewManager       — low-quality preview generation
  ExportManager        — assemble final video

  These are WORKFLOW DIRECTORS.
  They coordinate steps to complete a user request.
  They CAN (and do) call Ports.
  They USE Domain Services for the pure logic parts.
```

**Question 2: "How do I use the services?"**

```
STEP 1: A Driving Adapter (the CLI Shell) receives the user's typed command.
STEP 2: The Shell calls the correct Application Service.
        Example: render_orchestrator.render_scene(3)
STEP 3: The Application Service runs its workflow.
        It calls Domain Services for pure logic.
        It calls Ports for any external operation.
STEP 4: The Port calls the Adapter.
        Example: RenderRunnerPort -> ManimSubprocessRenderer
STEP 5: The Adapter does the real work.
        Example: ManimSubprocessRenderer runs "manim -ql scene_03.py"
STEP 6: The result flows back up through the Port to the Application Service.
STEP 7: The Application Service calls the Notification Port.
STEP 8: The Notification Port calls the CLI Notifier Adapter.
STEP 9: The CLI Notifier prints the result to the terminal.
STEP 10: The user sees the result.
```

**Question 3: "The Layered Architecture structures the Core itself, not the whole project."**

```
CORRECT. Here is the exact statement:

  Hexagonal Architecture  =  describes how the Core boundary works
                              (Ports, Adapters, the wall between inside/outside)

  Layered Architecture    =  describes how the INSIDE of the Core is organized
                              (3 layers: Application, Domain, Ports)
                              with dependency rules between those layers
```

The three layers inside the Core are:
- Layer 3 (top): Application Services — the Use Cases
- Layer 2 (middle): Domain Services + Domain Models — the rules and data shapes
- Layer 1 (bottom): Port Definitions — the contracts for external communication

Dependencies flow downward only:
- Application Services depend on Domain and Ports
- Domain Services depend on Models only
- Port Definitions depend on Models only
- Nothing depends on Application Services
- Nothing inside the Core depends on Adapters (which live outside)


# SuperManim — Services vs Adapters
## The Deepest Possible Explanation, From Zero

---

# STEP 1 — FORGET EVERYTHING. START WITH ONE QUESTION.

Imagine you are the tool. You are SuperManim.

A user types this:

```
supermanim> render scene 3
```

Now ask yourself honestly:

```
+------------------------------------------------------------+
|                                                            |
|   To render Scene 3, what do I actually need to DO?        |
|                                                            |
|   1. Load the scene data from somewhere.                   |
|   2. Check if the code file changed.                       |
|   3. If yes  → run Manim to produce the video.            |
|   4. If no   → skip it. Nothing to do.                    |
|   5. Tell the user what happened.                          |
|                                                            |
+------------------------------------------------------------+
```

Five steps. Simple.

Now here is the REAL question:

```
+------------------------------------------------------------+
|                                                            |
|   WHO does each step?                                      |
|                                                            |
|   Step 1: Load scene data           → ???                  |
|   Step 2: Check if code changed     → ???                  |
|   Step 3: Run Manim                 → ???                  |
|   Step 4: Skip if unchanged         → ???                  |
|   Step 5: Tell the user             → ???                  |
|                                                            |
+------------------------------------------------------------+
```

Filling in those ??? boxes is the entire architecture.

Let's fill them in one by one.

---

# STEP 2 — SPLIT THE STEPS INTO TWO GROUPS

Look at the five steps again. They are NOT all the same kind of work.

Some steps are about **THINKING** — making decisions, applying rules, doing logic.
Some steps are about **DOING** — talking to real external programs and files.

```
+================================================================+
|                  THE TWO KINDS OF WORK                         |
+================================================================+
|                                                                |
|   THINKING (pure logic — no external programs needed)          |
|   ─────────────────────────────────────────────────────────   |
|   Step 2: Check if the code changed.                           |
|            This is just comparing two strings.                 |
|            "a3f8c2" == "a3f8c2" ? YES → unchanged.            |
|            "a3f8c2" == "ff91b3" ? NO  → changed.              |
|            You need no database, no Manim, no files.           |
|            Just two strings and a comparison.                  |
|                                                                |
|   Step 4: Decide to skip.                                      |
|            This is just an if/else.                            |
|            if changed: render. else: skip.                     |
|            Pure logic. No external program needed.             |
|                                                                |
|   ─────────────────────────────────────────────────────────   |
|                                                                |
|   DOING (talks to real external programs)                      |
|   ─────────────────────────────────────────────────────────   |
|   Step 1: Load scene data.                                     |
|            This needs the DATABASE (SQLite).                   |
|            You have to open a file on disk.                    |
|                                                                |
|   Step 3: Run Manim.                                           |
|            This needs MANIM — an external program.             |
|            You have to launch a subprocess.                    |
|                                                                |
|   Step 5: Tell the user.                                       |
|            This needs the TERMINAL.                            |
|            You have to call print().                           |
|                                                                |
+================================================================+
```

This split is the most important idea in the entire architecture.

```
+------------------------------------------------------------+
|                                                            |
|   THINKING  →  lives in SERVICES (inside the Core)        |
|                                                            |
|   DOING     →  lives in ADAPTERS (outside the Core)       |
|                                                            |
+------------------------------------------------------------+
```

---

# STEP 3 — WHAT IS AN ADAPTER? (VERY DEEP)

## Definition

An Adapter is a piece of code that **talks to one specific external technology**.

Every Adapter has exactly one job:
"I am the only part of this codebase that knows how to talk to X."

Where X is one specific real thing: SQLite, Manim, FFmpeg, the terminal, the file system.

```
+================================================================+
|                   THE ADAPTERS IN SUPERMANIM                   |
+================================================================+
|                                                                |
|   Adapter                    Talks To              Lives In   |
|   ─────────────────────────────────────────────────────────   |
|   SqliteSceneRepository   →  SQLite database      adapters/  |
|   SqliteProjectRepository →  SQLite database      adapters/  |
|   SqliteAudioRepository   →  SQLite database      adapters/  |
|   SqliteCacheRepository   →  SQLite database      adapters/  |
|   ─────────────────────────────────────────────────────────   |
|   ManimSubprocessRenderer →  Manim program        adapters/  |
|   FfmpegAudioProcessor    →  FFmpeg program       adapters/  |
|   FfmpegVideoAssembler    →  FFmpeg program       adapters/  |
|   LibrosaAudioAnalyzer    →  librosa library      adapters/  |
|   ─────────────────────────────────────────────────────────   |
|   LocalFileStorage        →  File system (disk)   adapters/  |
|   Sha256HashComputer      →  hashlib library      adapters/  |
|   SystemTempManager       →  tempfile library     adapters/  |
|   ─────────────────────────────────────────────────────────   |
|   SuperManimShell         →  Terminal (input)     adapters/  |
|   CliNotifier             →  Terminal (output)    adapters/  |
|   CliProgressReporter     →  Terminal (output)    adapters/  |
|                                                                |
+================================================================+
```

## What Does an Adapter Look Like in Code?

Let's look at three real examples.

---

### Adapter Example 1: SqliteSceneRepository

This adapter knows how to talk to SQLite.
It knows the table names. It writes SQL. It uses `sqlite3.connect()`.
Nothing else in the codebase is allowed to do this.

```python
# adapters/repositories/sqlite_scene_repository.py

import sqlite3                        # <-- only Adapter imports this
from core.models.scene import Scene   # <-- it uses the Core's model

class SqliteSceneRepository:
    """
    I am the ONLY part of this codebase that touches SQLite.
    I know the table name "scenes". I write SQL.
    Nobody else does this.
    """

    def __init__(self, db_path: str):
        self.db_path = db_path

    def load_scene(self, scene_id: int) -> Scene:
        conn = sqlite3.connect(self.db_path)   # real SQLite call
        row = conn.execute(
            "SELECT * FROM scenes WHERE id = ?", (scene_id,)
        ).fetchone()
        conn.close()
        return Scene(
            id        = row[0],
            duration  = row[1],
            code_path = row[2],
            status    = row[3],
        )

    def mark_as_rendered(self, scene_id: int, video_path: str) -> None:
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "UPDATE scenes SET status='rendered', video_path=? WHERE id=?",
            (video_path, scene_id)
        )
        conn.commit()
        conn.close()
```

See how it is full of SQLite-specific things:
`sqlite3.connect()`, `conn.execute()`, `"SELECT * FROM scenes"`, `conn.commit()`.
This is its job. It is the SQLite expert.

---

### Adapter Example 2: ManimSubprocessRenderer

This adapter knows how to talk to Manim.
It knows the Manim command-line arguments. It uses `subprocess.run()`.

```python
# adapters/media/manim_subprocess_renderer.py

import subprocess                          # <-- only Adapter imports this
from core.models.scene import Scene

class ManimSubprocessRenderer:
    """
    I am the ONLY part of this codebase that runs Manim.
    I know the command: "manim -ql scene.py SceneClass"
    Nobody else does this.
    """

    def render(self, scene: Scene) -> bool:
        command = [
            "manim",
            "--quality", "high",
            scene.code_path,
            scene.class_name,
            "--output_file", scene.output_path,
        ]
        result = subprocess.run(command, capture_output=True)  # real Manim call
        return result.returncode == 0
```

---

### Adapter Example 3: CliNotifier

This adapter knows how to write to the terminal.
It uses `print()`. That's it.

```python
# adapters/cli/cli_notifier.py

class CliNotifier:
    """
    I am the ONLY part of this codebase that calls print().
    I format messages and send them to the terminal.
    Nobody else does this.
    """

    def send_success(self, message: str) -> None:
        print(f"  [OK] {message}")

    def send_error(self, message: str) -> None:
        print(f"  [ERROR] {message}")

    def send_info(self, message: str) -> None:
        print(f"  {message}")
```

---

## The Adapter Rule

```
+------------------------------------------------------------+
|                                                            |
|   ADAPTER RULE:                                            |
|                                                            |
|   An Adapter is allowed to use any external library        |
|   or program it needs to do its job.                       |
|                                                            |
|   sqlite3      ✓  (only inside SqliteSceneRepository)     |
|   subprocess   ✓  (only inside ManimSubprocessRenderer)   |
|   print()      ✓  (only inside CliNotifier)               |
|   os.path      ✓  (only inside LocalFileStorage)          |
|                                                            |
|   But the Adapter must NEVER be called directly by        |
|   the Core's logic.                                       |
|   The Core only calls through a PORT.                     |
|   (We will explain Ports in Step 5.)                      |
|                                                            |
+------------------------------------------------------------+
```

---

# STEP 4 — WHAT IS A SERVICE? (VERY DEEP)

## Definition

A Service is a piece of code that **contains logic** — decisions, rules, workflows.

A Service does NOT know that SQLite, Manim, FFmpeg, or `print()` exist.
It does NOT import `sqlite3`. It does NOT call `subprocess.run()`.

A Service only works with two kinds of things:
1. **Data objects** — Scene, Project, AudioClip (simple Python objects with fields)
2. **Ports** — abstract contracts that say "give me a scene" without saying how

```
+================================================================+
|                  THE SERVICES IN SUPERMANIM                    |
+================================================================+
|                                                                |
|   There are TWO TYPES of services:                             |
|                                                                |
|   TYPE A — Domain Services   (pure logic, no Ports)           |
|   TYPE B — Application Services  (workflow, uses Ports)       |
|                                                                |
+================================================================+
```

---

## Service Type A — Domain Services

### What Are They?

Domain Services are the **pure thinkers**.
They take data objects as input, apply a rule, and return an answer.

They do NOT call Ports.
They do NOT touch the database, Manim, FFmpeg, or the terminal.
They are 100% pure Python logic.

Think of them as calculators or rule-checkers that you can run on any machine,
anywhere, without installing anything.

### The 3 Domain Services in SuperManim

---

#### Domain Service 1: TimelineCalculator

**Its one job:** Answer questions about durations and time.

```
"Do Scene 3's duration and its audio clip's duration match?"
"Do all scene durations add up to the total audio length?"
"What is the difference in seconds between scene and clip?"
```

It takes Scene objects and AudioClip objects as input.
It does math on their `.duration` fields.
It returns True/False or a number.

```python
# core/services/domain/timeline_calculator.py

class TimelineCalculator:
    """
    I only do math on duration numbers.
    I receive data objects. I return answers.
    I know nothing about SQLite, Manim, or the terminal.
    """

    def durations_match(self, scene: Scene, clip: AudioClip) -> bool:
        return abs(scene.duration - clip.duration) < 0.001

    def total_duration(self, scenes: list[Scene]) -> float:
        return sum(s.duration for s in scenes)

    def difference(self, scene: Scene, clip: AudioClip) -> float:
        return abs(scene.duration - clip.duration)
```

No `import sqlite3`. No `import subprocess`. No `print()`.
Just math.

---

#### Domain Service 2: HashChecker

**Its one job:** Answer questions about whether code files have changed.

```
"Has this scene's code changed since the last render?"
"Which scenes in this list have changed?"
"Have ALL scenes stayed the same?"
```

It takes hash strings (fingerprints) as input and compares them.

```python
# core/services/domain/hash_checker.py

class HashChecker:
    """
    I compare fingerprint strings to detect changes.
    I do not compute fingerprints (that is the HashComputerPort's job).
    I do not store fingerprints (that is the CacheRepositoryPort's job).
    I only COMPARE them.
    """

    def has_changed(self, current: str, stored: str | None) -> bool:
        if stored is None:
            return True           # never rendered before → must render
        return current != stored  # compare two strings

    def find_changed(
        self,
        scenes: list[Scene],
        current_hashes: dict[int, str],
        stored_hashes:  dict[int, str | None]
    ) -> list[Scene]:
        return [
            s for s in scenes
            if self.has_changed(
                current_hashes.get(s.id),
                stored_hashes.get(s.id)
            )
        ]
```

Again: no SQLite, no Manim, no print. Just string comparisons.

---

#### Domain Service 3: ValidationRules

**Its one job:** Check if data objects satisfy business rules.

```
"Is Scene 3 ready to be rendered?"
"Is the project ready to be exported?"
"Can Scene 3 be synced to this audio clip?"
```

It takes data objects and checks their fields against the rules.
It returns a list of errors (empty list = everything is fine).

```python
# core/services/domain/validation_rules.py

class ValidationRules:
    """
    I am the rulebook.
    I check data objects against the rules of the system.
    I return lists of errors. Empty list = valid.
    I call no Ports. I touch no external technology.
    """

    def scene_is_renderable(self, scene: Scene) -> list[str]:
        errors = []
        if scene.code_path is None:
            errors.append(f"Scene {scene.id} has no code file.")
        if scene.duration is None:
            errors.append(f"Scene {scene.id} has no duration.")
        return errors

    def project_is_exportable(self, scenes: list[Scene]) -> list[str]:
        errors = []
        for scene in scenes:
            if scene.status != "rendered":
                errors.append(
                    f"Scene {scene.id} is not rendered yet (status={scene.status})."
                )
        return errors
```

---

## Service Type B — Application Services

### What Are They?

Application Services are the **workflow directors**.

When a user types `render scene 3`, something has to:
- Know which steps to run
- Know which order to run them in
- Call the right Domain Services for thinking
- Call the right Ports for doing

That "something" is an Application Service.

An Application Service is NOT a calculator or rule-checker.
It is a COORDINATOR.
It reads the user's request, runs the steps in the right order,
and makes sure everything gets done.

### The 8 Application Services in SuperManim

```
ProjectLifecycleService   →  handles: new/open/close/delete project
SceneLifecycleService     →  handles: add/set/list/delete/swap scenes
AudioPreparationService   →  handles: add/split/convert audio
RenderPipelineService     →  handles: render scene/all/pending/failed
RenderCacheService        →  handles: clear cache, cache info
TimelineCoordinatorService→  handles: timeline view, sync validation
PreviewGenerationService  →  handles: preview scene/all/clear previews
ProjectExportService      →  handles: export, set format/quality/name
```

Each one handles a group of commands that belong together.

---

### Let's See One Application Service in Full Detail

#### RenderPipelineService

This is the most important and complex Application Service.
It implements SuperManim's core superpower: smart incremental rendering.

**What commands it handles:**
- `render scene 3`
- `render all`
- `render pending`
- `force render scene 3`

**What it needs to do for `render scene 3`:**

```
+------------------------------------------------------------+
|   RenderPipelineService.render_scene(3) — Full Workflow    |
+------------------------------------------------------------+
|                                                            |
|   STEP 1: Load the scene from the database.               |
|            → needs SceneRepositoryPort (a Port)            |
|                                                            |
|   STEP 2: Check if the scene is renderable.               |
|            → needs ValidationRules (a Domain Service)      |
|                                                            |
|   STEP 3: Compute the current hash of the code file.      |
|            → needs HashComputerPort (a Port)               |
|                                                            |
|   STEP 4: Load the stored hash from the cache.            |
|            → needs CacheRepositoryPort (a Port)            |
|                                                            |
|   STEP 5: Decide if it changed.                           |
|            → needs HashChecker (a Domain Service)          |
|                                                            |
|   STEP 6: If unchanged → skip. Notify user.               |
|            → needs NotificationPort (a Port)               |
|                                                            |
|   STEP 7: If synced with audio → check durations match.   |
|            → needs AudioRepositoryPort (a Port)            |
|            → needs TimelineCalculator (a Domain Service)   |
|                                                            |
|   STEP 8: Run Manim.                                      |
|            → needs RenderRunnerPort (a Port)               |
|                                                            |
|   STEP 9: Save result. Notify user.                       |
|            → needs SceneRepositoryPort (a Port)            |
|            → needs CacheRepositoryPort (a Port)            |
|            → needs NotificationPort (a Port)               |
|                                                            |
+------------------------------------------------------------+
```

**What it looks like in code:**

```python
# core/services/application/render_pipeline_service.py

class RenderPipelineService:
    """
    I coordinate the render workflow.
    I use Domain Services for thinking.
    I use Ports for everything that touches the outside world.
    I never import sqlite3, subprocess, or call print().
    """

    def __init__(
        self,
        # --- Ports (contracts to external world) ---
        scene_repo:    SceneRepositoryPort,
        cache_repo:    CacheRepositoryPort,
        audio_repo:    AudioRepositoryPort,
        hash_computer: HashComputerPort,
        renderer:      RenderRunnerPort,
        notifier:      NotificationPort,
        # --- Domain Services (pure logic) ---
        hash_checker:  HashChecker,
        timeline:      TimelineCalculator,
        validation:    ValidationRules,
    ):
        self.scene_repo    = scene_repo
        self.cache_repo    = cache_repo
        self.audio_repo    = audio_repo
        self.hash_computer = hash_computer
        self.renderer      = renderer
        self.notifier      = notifier
        self.hash_checker  = hash_checker
        self.timeline      = timeline
        self.validation    = validation

    def render_scene(self, scene_id: int) -> None:

        # STEP 1: Load scene  (Port → SQLite Adapter → SQLite on disk)
        scene = self.scene_repo.load_scene(scene_id)

        # STEP 2: Validate  (Domain Service → pure Python)
        errors = self.validation.scene_is_renderable(scene)
        if errors:
            for e in errors:
                self.notifier.send_error(e)
            return

        # STEP 3: Hash current code file  (Port → Sha256 Adapter → reads disk)
        current_hash = self.hash_computer.compute(scene.code_path)

        # STEP 4: Load stored hash  (Port → SQLite Adapter → SQLite on disk)
        stored_hash = self.cache_repo.load_hash(scene_id)

        # STEP 5: Did it change?  (Domain Service → pure Python)
        changed = self.hash_checker.has_changed(current_hash, stored_hash)

        # STEP 6: If unchanged, skip
        if not changed:
            self.notifier.send_info(
                f"Scene {scene_id} unchanged. Skipped."
            )
            return

        # STEP 7: Check audio sync  (Port + Domain Service)
        if scene.synced_with_audio:
            clip = self.audio_repo.load_clip_for_scene(scene_id)
            if not self.timeline.durations_match(scene, clip):
                diff = self.timeline.difference(scene, clip)
                self.notifier.send_error(
                    f"Duration mismatch: scene={scene.duration}s "
                    f"clip={clip.duration}s diff={diff:.3f}s"
                )
                return

        # STEP 8: Run Manim  (Port → Manim Adapter → real Manim program)
        success = self.renderer.render(scene)

        # STEP 9: Save result
        if success:
            self.scene_repo.mark_as_rendered(scene_id, scene.output_path)
            self.cache_repo.save_hash(scene_id, current_hash)
            self.notifier.send_success(f"Scene {scene_id} rendered.")
        else:
            self.scene_repo.mark_as_failed(scene_id, "Manim returned error.")
            self.notifier.send_error(f"Scene {scene_id} FAILED.")
```

Look at every line carefully.
Every time it needs to talk to the outside world, it calls a Port variable (`self.scene_repo`, `self.renderer`, etc.)
Every time it needs to do pure logic, it calls a Domain Service (`self.hash_checker`, `self.timeline`, `self.validation`).
It never calls `sqlite3`, `subprocess`, or `print()` directly.

---

# STEP 5 — WHAT IS A PORT?

You have now seen Ports mentioned many times.
Let's understand exactly what they are.

## The Problem That Ports Solve

Imagine the `RenderPipelineService` wants to load a scene.
It could do this:

```python
# WITHOUT a Port — BAD
import sqlite3

conn = sqlite3.connect("/projects/MyProject/project_data.db")
row = conn.execute("SELECT * FROM scenes WHERE id=3").fetchone()
scene = Scene(id=row[0], duration=row[1], ...)
```

This works. But now `RenderPipelineService` is GLUED to SQLite forever.
If you want to switch to a JSON file instead, you have to change this Service.
If you want to test this Service without a real database, you cannot — it always needs SQLite.

The solution: instead of calling SQLite directly, the Service calls a **Port**.

A Port is a Python **interface** — it lists what functions exist and what they return,
but it does NOT say HOW they work.

```python
# A Port — the CONTRACT
from abc import ABC, abstractmethod

class SceneRepositoryPort(ABC):
    """
    I define WHAT can be done with scenes.
    I do NOT say HOW it is done.
    SQLite? JSON? Memory? I don't know. That's not my job.
    """

    @abstractmethod
    def load_scene(self, scene_id: int) -> Scene: ...

    @abstractmethod
    def mark_as_rendered(self, scene_id: int, video_path: str) -> None: ...

    @abstractmethod
    def mark_as_failed(self, scene_id: int, error: str) -> None: ...
```

Now `RenderPipelineService` calls `self.scene_repo.load_scene(3)`.
It does NOT know if `scene_repo` is SQLite, JSON, or a fake for testing.
It just knows the Port's contract: "give me scene 3 and I will return a Scene object."

The Port is the bridge. The contract. The promise.

```
+================================================================+
|                    WHAT A PORT DOES                            |
+================================================================+
|                                                                |
|   SERVICE says:     "I need a scene. Give me scene number 3."  |
|                                                                |
|   PORT says:        "OK. Whoever implements me must provide    |
|                      load_scene(id) → Scene."                  |
|                                                                |
|   ADAPTER says:     "I implement this Port. Here is how I      |
|                      do it: I use SQLite."                     |
|                     (or: "I use JSON.")                        |
|                     (or: "I return fake data for tests.")      |
|                                                                |
+================================================================+
```

---

# STEP 6 — THE COMPLETE PICTURE IN ONE DIAGRAM

Now let's put everything together.
This diagram shows every piece and how they all connect.

```
USER TYPES: render scene 3
       |
       v
+==============================+
|   ADAPTER (input side)       |
|   SuperManimShell            |
|   File: adapters/cli/shell.py|
|                              |
|   Reads the text.            |
|   Parses the command.        |
|   Calls the Service.         |
+==============================+
       |
       | calls render_pipeline_service.render_scene(3)
       |
       v
+==============================+       +==========================+
|   APPLICATION SERVICE        |       |   DOMAIN SERVICES        |
|   RenderPipelineService      | ----> |                          |
|   File: core/services/       |       |   HashChecker            |
|         application/         |       |   TimelineCalculator     |
|         render_pipeline_     |       |   ValidationRules        |
|         service.py           |       |                          |
|                              |       |   Pure Python.           |
|   Runs the workflow.         |       |   No Ports.              |
|   Calls Domain Services      |       |   No external tech.      |
|   for thinking.              |       |   Just logic.            |
|   Calls Ports for doing.     |       +==========================+
+==============================+
       |
       | calls Ports:
       | scene_repo.load_scene(3)
       | hash_computer.compute(path)
       | renderer.render(scene)
       | notifier.send_success(msg)
       |
       v
+==============================+
|   PORTS (contracts)          |
|   File: core/ports/          |
|                              |
|   SceneRepositoryPort        |
|   HashComputerPort           |
|   RenderRunnerPort           |
|   NotificationPort           |
|                              |
|   These are just interfaces. |
|   They say WHAT, not HOW.   |
+==============================+
       |
       | each Port is implemented by one Adapter
       |
       v
+================================================================+
|   ADAPTERS (output side — the real workers)                    |
|   File: adapters/                                              |
|                                                                |
|   SceneRepositoryPort  ←→  SqliteSceneRepository              |
|                             uses sqlite3                       |
|                             talks to: SQLite file on disk      |
|                                                                |
|   HashComputerPort     ←→  Sha256HashComputer                 |
|                             uses hashlib                       |
|                             talks to: the code file on disk    |
|                                                                |
|   RenderRunnerPort     ←→  ManimSubprocessRenderer            |
|                             uses subprocess                    |
|                             talks to: Manim program            |
|                                                                |
|   NotificationPort     ←→  CliNotifier                        |
|                             uses print()                       |
|                             talks to: the terminal             |
|                                                                |
+================================================================+
       |          |          |          |
       v          v          v          v
   [SQLite]    [disk]    [Manim]   [Terminal]

    THE REAL WORLD (outside SuperManim completely)
```

---

# STEP 7 — SIDE BY SIDE COMPARISON

Now that you understand each piece, here is a comparison table
that shows exactly how Services and Adapters differ.

```
+=====================================================================+
|                   SERVICE  vs  ADAPTER — FULL COMPARISON            |
+=====================================================================+
|                        |                    |                       |
|   QUESTION             |   SERVICE          |   ADAPTER             |
|   ─────────────────────|────────────────────|─────────────────────  |
|   Where does it live?  | core/services/     | adapters/             |
|                        |                    |                       |
|   What does it do?     | Contains logic,    | Talks to one specific |
|                        | rules, workflows   | external technology   |
|                        |                    |                       |
|   Does it use SQLite?  | NEVER              | Yes (if it's the      |
|                        |                    | SQLite adapter)       |
|                        |                    |                       |
|   Does it use Manim?   | NEVER              | Yes (if it's the      |
|                        |                    | Manim adapter)        |
|                        |                    |                       |
|   Does it call print()?| NEVER              | Yes (if it's the      |
|                        |                    | CLI notifier)         |
|                        |                    |                       |
|   Does it call Ports?  | App.Services: YES  | NEVER. Adapters       |
|                        | Domain Svc: NO     | implement Ports,      |
|                        |                    | they don't call them  |
|                        |                    |                       |
|   Can it be tested     | YES — very easily. | HARD — needs the      |
|   without real tools?  | No SQLite needed.  | real tool to be       |
|                        | No Manim needed.   | installed.            |
|                        |                    |                       |
|   Can you swap it?     | Rarely. The logic  | YES. You can swap     |
|                        | doesn't change.    | SQLite for JSON,      |
|                        |                    | Manim for Pygame,     |
|                        |                    | print for a GUI popup |
|                        |                    |                       |
|   What does it know    | Only: Scene,       | Only: its one         |
|   about?               | Project, AudioClip,| external tool         |
|                        | Ports (contracts)  | (SQLite, Manim, etc.) |
|                        |                    |                       |
+=====================================================================+
```

---

# STEP 8 — THE MOST IMPORTANT ANALOGY

Think of a restaurant.

```
+================================================================+
|                   THE RESTAURANT ANALOGY                       |
+================================================================+
|                                                                |
|   THE CHEF       =   Application Service                       |
|                                                                |
|   The chef knows the RECIPE (the workflow):                    |
|   Step 1: get the vegetables.                                  |
|   Step 2: chop them.                                           |
|   Step 3: heat the pan.                                        |
|   Step 4: cook.                                                |
|   Step 5: plate and serve.                                     |
|                                                                |
|   The chef does NOT grow the vegetables.                       |
|   The chef does NOT build the stove.                           |
|   The chef does NOT make the plates.                           |
|   The chef USES these things, but does not BUILD them.         |
|                                                                |
|   ─────────────────────────────────────────────────────────   |
|                                                                |
|   THE RECIPE RULES  =   Domain Services                        |
|                                                                |
|   "Is this chicken cooked enough?" (ValidationRules)          |
|   "How long does this dish take?" (TimelineCalculator)        |
|   "Did the sauce change from last time?" (HashChecker)        |
|                                                                |
|   Pure knowledge. No equipment needed.                         |
|   Just rules and calculations.                                 |
|                                                                |
|   ─────────────────────────────────────────────────────────   |
|                                                                |
|   THE SUPPLIERS  =   Adapters                                  |
|                                                                |
|   The vegetable farmer  =  SqliteSceneRepository               |
|   The stove builder     =  ManimSubprocessRenderer             |
|   The plate factory     =  LocalFileStorage                    |
|   The waiter            =  CliNotifier                         |
|                                                                |
|   Each supplier has ONE job.                                   |
|   The farmer grows vegetables. That's all.                     |
|   The chef doesn't know HOW the farmer grows them.             |
|   The chef just says: "bring me 3 tomatoes."                   |
|                                                                |
|   ─────────────────────────────────────────────────────────   |
|                                                                |
|   THE ORDER SLIP  =   Port                                     |
|                                                                |
|   The chef writes: "3 tomatoes, fresh."                        |
|   The slip is the PORT.                                        |
|   It says WHAT is needed, not HOW to get it.                   |
|   The farmer (adapter) reads the slip and delivers.            |
|                                                                |
+================================================================+
```

---

# STEP 9 — PUTTING IT ALL TOGETHER FOR SUPERMANIM

Here is every piece of SuperManim, organized by what type it is.

```
+================================================================+
|               EVERY PIECE OF SUPERMANIM — LABELED              |
+================================================================+
|                                                                |
|  ── ADAPTERS (outside the Core) ──────────────────────────    |
|                                                                |
|  INPUT ADAPTERS (receive commands from the user)              |
|    SuperManimShell          → reads the terminal              |
|                                                                |
|  DATABASE ADAPTERS (talk to SQLite)                           |
|    SqliteSceneRepository    → stores/loads scene data         |
|    SqliteProjectRepository  → stores/loads project data       |
|    SqliteAudioRepository    → stores/loads audio data         |
|    SqliteCacheRepository    → stores/loads hash fingerprints  |
|                                                                |
|  MEDIA ADAPTERS (talk to external programs)                   |
|    ManimSubprocessRenderer  → runs Manim                      |
|    FfmpegAudioProcessor     → cuts/converts audio             |
|    FfmpegVideoAssembler     → stitches video clips            |
|    LibrosaAudioAnalyzer     → detects silences in audio       |
|    ManimPreviewGenerator    → runs Manim in low-quality mode  |
|                                                                |
|  FILE ADAPTERS (talk to the file system)                      |
|    LocalFileStorage         → creates/moves/deletes files     |
|    Sha256HashComputer       → reads files, computes hashes    |
|    SystemTempManager        → manages temporary files         |
|                                                                |
|  OUTPUT ADAPTERS (send output to the user)                    |
|    CliNotifier              → prints messages to terminal     |
|    CliProgressReporter      → shows progress bars            |
|    FileLogger               → writes log files               |
|                                                                |
|  ── PORTS (the contracts — inside Core, defines the border) ─  |
|                                                                |
|    SceneRepositoryPort      CacheRepositoryPort               |
|    ProjectRepositoryPort    RenderRunnerPort                   |
|    AudioRepositoryPort      AudioProcessorPort                 |
|    HashComputerPort         VideoAssemblerPort                 |
|    FileStoragePort          NotificationPort                   |
|    ProgressReporterPort     LoggerPort                         |
|    ... (all 29 ports)                                          |
|                                                                |
|  ── DOMAIN SERVICES (inside Core — pure logic, no Ports) ───  |
|                                                                |
|    TimelineCalculator       → duration math                   |
|    HashChecker              → fingerprint comparison          |
|    ValidationRules          → business rule checking          |
|                                                                |
|  ── APPLICATION SERVICES (inside Core — workflow, uses Ports) ─|
|                                                                |
|    ProjectLifecycleService  → new/open/close/delete project   |
|    SceneLifecycleService    → add/set/list/delete scenes      |
|    AudioPreparationService  → add/split/convert audio         |
|    RenderPipelineService    → smart incremental rendering     |
|    RenderCacheService       → manage stored fingerprints      |
|    TimelineCoordinatorService → timeline and sync             |
|    PreviewGenerationService → low-quality preview rendering   |
|    ProjectExportService     → assemble final video            |
|                                                                |
|  ── DOMAIN MODELS (inside Core — pure data objects) ─────────  |
|                                                                |
|    Scene         Project        AudioClip      RenderResult   |
|                                                                |
+================================================================+
```

---

# STEP 10 — HOW TO USE THEM WHEN WRITING CODE

When you sit down to write code for SuperManim, use this decision tree:

```
+================================================================+
|   DECISION TREE: "Where does this code go?"                    |
+================================================================+
|                                                                |
|   Is this code TALKING TO AN EXTERNAL TECHNOLOGY?             |
|   (SQLite, Manim, FFmpeg, file system, terminal, hashlib)     |
|                                                                |
|   YES → It is an ADAPTER.                                      |
|          Write it in adapters/                                 |
|          Make it implement a Port interface.                   |
|                                                                |
|   NO → Is this code DOING PURE CALCULATION OR RULE CHECKING?  |
|         (math on durations, comparing hash strings,            |
|          checking if a scene has a code file)                  |
|                                                                |
|         YES → It is a DOMAIN SERVICE.                          |
|                Write it in core/services/domain/              |
|                Do NOT give it any Port variables.              |
|                                                                |
|         NO → Is this code COORDINATING A MULTI-STEP WORKFLOW? |
|               (run these 9 steps to handle "render scene 3")  |
|                                                                |
|               YES → It is an APPLICATION SERVICE.              |
|                      Write it in core/services/application/   |
|                      Give it Ports and Domain Services         |
|                      through __init__().                       |
|                                                                |
|               NO → Is this a simple DATA CONTAINER?           |
|                     (a Scene with id, duration, code_path)    |
|                                                                |
|                     YES → It is a DOMAIN MODEL.               |
|                            Write it in core/models/            |
|                                                                |
+================================================================+
```

---

# FINAL SUMMARY — THREE SENTENCES

```
+================================================================+
|                                                                |
|   ADAPTERS talk to the outside world.                          |
|   (SQLite, Manim, FFmpeg, the terminal, the file system)       |
|   They live in adapters/ and implement Ports.                  |
|                                                                |
|   DOMAIN SERVICES think about data.                            |
|   (duration math, hash comparison, rule checking)              |
|   They live in core/services/domain/ and call nothing external.|
|                                                                |
|   APPLICATION SERVICES run workflows.                          |
|   (the 9 steps to render a scene, in the right order)          |
|   They live in core/services/application/ and use both         |
|   Domain Services (for thinking) and Ports (for doing).        |
|                                                                |
+================================================================+
```
