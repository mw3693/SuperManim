


### Section 0.5 The Architecture design of the SuperManim tool:
The tool architecture design is a combination of two architectures one to isolate the core
of the tool form the external world and the second architecture inside the core itself to organize
the internal componenets of the core.The two architectures are:


#### Subsection 0.5.1 The Hexagonal Architecture:

##### Subsubsection 0.5.1.1 What is Hexagonal Architecture:

---

##### Subsubsection 0.5.1.5 The components of the Hexagonal Architecture:


###### The forth commonents is the Services:




##### Subsubsection 0.5.1.6 Complete Port and Adapter Map for SuperManim:
Before mapping the ports and adapters we should know these:

1 -**PORT** — A Port is like an electrical socket in your wall. The socket does not care if you plug in a lamp,
a phone charger, or a fan. It just provides a connection point.

In SuperManim, a Port is a simple Python interface (a list of function names) that the core logic uses.
The Core says "give me the data through this socket" — it does not care how the data is actually fetched.

2- **ADAPTER**  An Adapter is the actual plug and device. The SQLite Adapter is the lamp.The JSON Adapter
is the phone charger. They both fit the same socket (Port), but they work in completely different ways
behind the scenes.The Core never sees the adapter — it only sees the port.

3- **EXTERNAL TECHNOLOGY**  This is the real tool that the Adapter actually uses to do its job.
For example, the `FfmpegAudioProcessor` adapter uses a real program called FFmpeg installed on
your computer to cut audio files.

---

```
+=========================================================+
|              HOW PORTS AND ADAPTERS WORK                |
+=========================================================+
|                                                         |
|   THE CORE (your smart logic)                           |
|        |                                                |
|        |  calls:  scene_repo.save_scene(...)            |
|        |                                                |
|        v                                                |
|   [ PORT ]  <--- SceneRepositoryPort                    |
|   "I promise these functions exist."                    |
|        |                                                |
|        v                                                |
|   [ ADAPTER ]  <--- SqliteSceneRepository               |
|   "I actually do the work using SQLite."                |
|        |                                                |
|        v                                                |
|   [ EXTERNAL TECH ]  <--- SQLite database file          |
|   "I am the real storage engine."                       |
|                                                         |
+=========================================================+
```


##### Subsubsection 0.5.1.6 The Full Hexagonal Architecture  Diagram

```
+============================================================+
|                                                            |
|                   OUTSIDE WORLD (LEFT SIDE)                |
|                   Inbound / Driving Adapters               |
|                                                            |
|   +------------------+    +------------------+            |
|   | CliProjectAdapter|    | CliRenderAdapter |            |
|   | "create project" |    | "render scene 2" |            |
|   +--------+---------+    +--------+---------+            |
|            |                       |                       |
+============================================================+
             |                       |
             v                       v
   +---------+---------+   +---------+---------+
   | ProjectCommandPort|   | RenderCommandPort |   <-- INBOUND PORTS
   +-------------------+   +-------------------+
             |                       |
             v                       v
+============================================================+
|                                                            |
|                        THE CORE                            |
|                                                            |
|   ProjectManager   AudioManager    ScenesManager           |
|                                                            |
|   RenderOrchestrator   TimelineEngine   CacheManager       |
|                                                            |
|   "I contain only rules and logic."                        |
|   "I do not know SQLite exists."                           |
|   "I do not know Manim exists."                            |
|   "I only speak through Ports."                            |
|                                                            |
+============================================================+
             |                       |
             v                       v
   +---------+---------+   +---------+---------+
   | SceneRepositoryP. |   | RenderRunnerPort  |   <-- OUTBOUND PORTS
   +-------------------+   +-------------------+
             |                       |
             v                       v
+============================================================+
|                                                            |
|                   OUTSIDE WORLD (RIGHT SIDE)               |
|                   Outbound / Driven Adapters               |
|                                                            |
|   +------------------+    +------------------+            |
|   |SqliteSceneRepo.  |    |ManimSubprocess   |            |
|   | (writes SQLite)  |    | Renderer         |            |
|   +------------------+    | (calls Manim)    |            |
|                           +------------------+            |
|   +------------------+    +------------------+            |
|   |FFmpegAudioProcess|    |LocalFileStorage  |            |
|   | (calls FFmpeg)   |    | (reads/writes    |            |
|   +------------------+    |  disk files)     |            |
|                           +------------------+            |
+============================================================+
```



#### Subsection 0.5.2 The Layered Architecture:


### Section 0.6 The SuperManim State management:

**THE FUNDAMENTAL RULE: ONE PROJECT AT A TIME**

Before anything else, we must establish the most important rule in the
entire project system. This rule shapes everything — the Entity design,
the session file, the AppState service, and every command that touches projects.

```
+=====================================================================+
|                  THE ONE-PROJECT RULE                               |
+=====================================================================+
|                                                                     |
|   SuperManim can only have ONE project open at any time.            |
|                                                                     |
|   It is not possible to have two projects open simultaneously.      |
|   It is not possible to run two commands on two different projects  |
|   in the same session.                                              |
|                                                                     |
|   There are exactly two states the tool can be in:                  |
|                                                                     |
|   STATE 1 — NO PROJECT OPEN                                         |
|   The tool is running. No project is loaded.                        |
|   is_project_open = False                                           |
|   The user must either create a new project or open an existing one.|
|   Every command except "new project", "open project",               |
|   "list projects", "help", "version", and "exit" will be refused.   |
|                                                                     |
|   STATE 2 — ONE PROJECT OPEN                                        |
|   The tool is running. One specific project is loaded in memory.    |
|   is_project_open = True                                            |
|   All commands are available.                                       |
|   Every command operates on this one open project.                  |
|                                                                     |
+=====================================================================+
```

The tool NEVER has two projects open. Period.

---

**THE TWO FILES THAT MATTER**

SuperManim uses two completely separate database files. They have different
purposes, live in different locations, and are managed by different parts
of the system.

```
+=====================================================================+
|             TWO DATABASE FILES — COMPLETELY DIFFERENT JOBS          |
+=====================================================================+
|                                                                     |
|   FILE 1 — session.db                                               |
|   ─────────────────────────────────────────────────────────────    |
|   Purpose:  Tracks the application-level session state.             |
|             Which project was last open?                            |
|             Which projects has the user opened recently?            |
|                                                                     |
|   Location: Operating-system specific application data folder.      |
|             Windows:  %APPDATA%\SuperManim\session.db               |
|             macOS:    ~/Library/Application Support/SuperManim/     |
|                        session.db                                   |
|             Linux:    ~/.supermanim/session.db                      |
|                       (or $XDG_DATA_HOME/SuperManim/session.db)     |
|                                                                     |
|   Who owns it:  AppStateService ONLY.                               |
|                 No other Service touches this file.                  |
|   Created:      On first run of SuperManim.                         |
|   Survives:     All sessions. Lives as long as the app is installed.|
|                                                                     |
|   ─────────────────────────────────────────────────────────────    |
|                                                                     |
|   FILE 2 — project_data.db                                          |
|   ─────────────────────────────────────────────────────────────    |
|   Purpose:  Stores everything about ONE specific project.           |
|             Scenes, audio, cache, render history, settings.         |
|                                                                     |
|   Location: Inside the project's own folder on disk.                |
|             /projects/MyAnimation/project_data.db                   |
|             /projects/Chapter1_Intro/project_data.db                |
|             (each project has its own separate copy)                |
|                                                                     |
|   Who owns it:  All repository adapters (SqliteSceneRepository,     |
|                 SqliteProjectRepository, etc.).                      |
|                 ProjectSettings table is READ-ONLY after creation.  |
|   Created:      When a new project is created.                      |
|   Survives:     Only as long as the project folder exists.          |
|                                                                     |
+=====================================================================+
```

---

**THE session.db FILE IN DEPTH**

## What Is session.db?

`session.db` is a small SQLite database that SuperManim keeps in the
operating system's standard application data directory. It is created
automatically the first time the user ever creates or opens a project.

Its entire job is to answer two questions:

```
Question 1: "What project did the user have open last time?"
            Answer: stored in last_opened_project

Question 2: "What projects has this user worked on recently?"
            Answer: stored in the recent_projects list
```

That is all this file does. It does not store scenes. It does not store
audio clips. It does not store render settings. It stores session-level
memory — the information that belongs to the application itself rather
than to any specific project.

## Where session.db Lives

The location follows each operating system's standard for application data.
SuperManim follows this convention so the file is stored in the right place
on every operating system:

```
+=====================================================================+
|                WHERE session.db LIVES ON EACH OS                    |
+=====================================================================+
|                                                                     |
|   WINDOWS                                                           |
|   %APPDATA%\SuperManim\session.db                                   |
|   Expands to something like:                                        |
|   C:\Users\Ahmed\AppData\Roaming\SuperManim\session.db              |
|                                                                     |
|   macOS                                                             |
|   ~/Library/Application Support/SuperManim/session.db              |
|   Expands to something like:                                        |
|   /Users/Ahmed/Library/Application Support/SuperManim/session.db   |
|                                                                     |
|   LINUX                                                             |
|   ~/.supermanim/session.db                                          |
|   Or if XDG_DATA_HOME is set:                                       |
|   $XDG_DATA_HOME/SuperManim/session.db                              |
|   Expands to something like:                                        |
|   /home/ahmed/.supermanim/session.db                                |
|                                                                     |
+=====================================================================+
```

## What Is Inside session.db

The file contains two tables:

```
+=====================================================================+
|                     session.db STRUCTURE                            |
+=====================================================================+
|                                                                     |
|   TABLE 1: app_session                                              |
|   ─────────────────────────────────────────────────────────────    |
|   Stores exactly ONE row — the current/last session state.          |
|                                                                     |
|   Column               Type        Description                      |
|   ─────────────────────────────────────────────────────────────    |
|   last_project_name    TEXT        Name of the last opened project. |
|                                    NULL if no project ever opened.  |
|   last_project_path    TEXT        Full path to that project folder.|
|   last_opened_at       TEXT        Timestamp when it was opened.    |
|   is_project_open      INTEGER     0 = no project open.             |
|                                    1 = a project was open when      |
|                                    the app last closed.             |
|                                                                     |
|   TABLE 2: recent_projects                                          |
|   ─────────────────────────────────────────────────────────────    |
|   Stores the list of recently opened projects.                      |
|   New entries are added at the top. Old entries fall off the        |
|   bottom when the list exceeds the maximum (default: 10).           |
|                                                                     |
|   Column               Type        Description                      |
|   ─────────────────────────────────────────────────────────────    |
|   project_name         TEXT        Name of the project.             |
|   project_path         TEXT        Full path to the project folder. |
|   project_mode         TEXT        "normal"/"simplemanim"/          |
|                                    "supermanim"                     |
|   last_opened_at       TEXT        When the user last opened it.    |
|   open_count           INTEGER     How many times it was opened.    |
|                                                                     |
+=====================================================================+
```

## How session.db Is Used in Practice

**When SuperManim starts:**

The `AppStateService` reads `session.db` at startup. This is the very
first thing the application does before showing the prompt. It reads
`is_project_open` and `last_project_name` to decide which state to start in.

```
+-------------------------------------------------------------+
|   WHAT HAPPENS WHEN SUPERMANIM STARTS                       |
+-------------------------------------------------------------+
|                                                             |
|   AppStateService reads session.db                          |
|                                                             |
|   Case A: session.db does not exist yet                     |
|   (first time ever running SuperManim)                      |
|   -> Create the file and both tables.                       |
|   -> Start in STATE 1 (no project open).                    |
|   -> Show the prompt. Wait for user.                         |
|                                                             |
|   Case B: session.db exists, is_project_open = 0           |
|   (user closed the tool cleanly last time)                  |
|   -> Start in STATE 1 (no project open).                    |
|   -> Show the prompt. Wait for user.                         |
|                                                             |
|   Case C: session.db exists, is_project_open = 1           |
|   (the tool was closed while a project was open,            |
|    OR the previous session crashed)                         |
|   -> Read last_project_name and last_project_path.          |
|   -> Attempt to reopen that project automatically.          |
|   -> If successful: start in STATE 2 (project open).        |
|   -> If project folder is missing: start in STATE 1,        |
|      show a warning that the last project was not found.    |
|                                                             |
+-------------------------------------------------------------+
```

**When a project is opened:**

Every time the user opens a project (whether with `new project` or
`open project`), the `AppStateService` updates `session.db` immediately:

```
1. Update app_session table:
   last_project_name  = "MyAnimation"
   last_project_path  = "/projects/MyAnimation"
   last_opened_at     = "2024-11-12 14:18:05"
   is_project_open    = 1

2. Update or insert into recent_projects table:
   If "MyAnimation" already exists in the list:
     Update its last_opened_at and increment open_count.
     Move it to the top of the list.
   If "MyAnimation" is new to the list:
     Insert a new row at the top.
     If list now exceeds 10 items, delete the oldest entry.
```

**When the tool closes cleanly:**

```
AppStateService updates app_session:
  is_project_open = 0
  (everything else stays as-is for reference)
```

---

# PART 4 — THE AppStateService

## What Is AppStateService?

The `AppStateService` is a special Application Service inside the Core.
It has one job that no other Service has: it is the ONLY part of the
system allowed to read and write `session.db`.

Think of it as a watcher — it watches over the application's own state
(which is different from any individual project's state) and keeps
`session.db` perfectly synchronized with reality.

```
+=====================================================================+
|                    AppStateService — ITS JOB                        |
+=====================================================================+
|                                                                     |
|   1. READ session.db at startup to determine initial state.         |
|                                                                     |
|   2. WRITE to session.db whenever:                                  |
|      - A project is opened (new or existing)                        |
|      - A project is closed                                          |
|      - The tool shuts down cleanly                                  |
|                                                                     |
|   3. PROVIDE the current session state to anyone who needs it:      |
|      - is_project_open?                                             |
|      - what is the currently open project's name and path?          |
|      - what is the recent projects list?                            |
|                                                                     |
|   4. ENFORCE the one-project-at-a-time rule.                        |
|      Before opening a new project, AppStateService checks if        |
|      another project is already open. If yes, it tells the system   |
|      to close the current one first.                                |
|                                                                     |
+=====================================================================+
```

## How AppStateService Differs from Other Services

The other Application Services (SceneLifecycleService, RenderPipelineService,
etc.) all operate on the currently open project. They read and write
`project_data.db` through their Port interfaces.

`AppStateService` is different in three ways:

```
+=====================================================================+
|      AppStateService vs OTHER Application Services                  |
+=====================================================================+
|                                                                     |
|   OTHER SERVICES:                                                   |
|   - Operate ON a project (they need a project to be open)           |
|   - Read and write project_data.db                                  |
|   - Work through Repository Ports                                   |
|   - Refused if no project is open                                   |
|                                                                     |
|   AppStateService:                                                  |
|   - Operates on the APPLICATION itself (not on any project)         |
|   - Reads and writes session.db                                     |
|   - Works through its own SessionRepositoryPort                     |
|   - Always available — even when no project is open                 |
|   - Is the ONLY service that runs before a project exists           |
|                                                                     |
+=====================================================================+
```

## What Ports AppStateService Uses

```python
# AppStateService uses only one Port:

class AppStateService:

    def __init__(
        self,
        session_repo:  SessionRepositoryPort,   # reads/writes session.db
        notifier:      NotificationPort,         # tells user what happened
    ):
        self._session_repo = session_repo
        self._notifier     = notifier
```

The `SessionRepositoryPort` is implemented by one Adapter:
`SqliteSessionRepository`, which is the only piece of code in the
entire system that opens and writes to `session.db`. Just like
`SqliteSceneRepository` is the only piece of code that touches
the scenes table in `project_data.db`, `SqliteSessionRepository`
is the only piece of code that touches `session.db`.

## The AppStateService Methods

```python
class AppStateService:
    """
    The application-level state watcher.
    Manages session.db and enforces the one-project-at-a-time rule.
    This service is available at all times — even when no project is open.
    """

    def load_session_on_startup(self) -> AppSession:
        """
        Called once when SuperManim starts.
        Reads session.db and returns the current session state.
        Decides whether to auto-reopen the last project.
        """

    def record_project_opened(self, project_name: str,
                               project_path: str,
                               project_mode: str) -> None:
        """
        Called by ProjectLifecycleService every time a project is opened.
        Updates app_session and recent_projects in session.db.
        """

    def record_project_closed(self) -> None:
        """
        Called by ProjectLifecycleService when a project is closed.
        Sets is_project_open = 0 in session.db.
        """

    def record_clean_shutdown(self) -> None:
        """
        Called when the user types "exit" or "quit".
        Sets is_project_open = 0 to mark clean shutdown.
        """

    def get_recent_projects(self) -> list[RecentProject]:
        """
        Returns the list of recently opened projects from session.db.
        Used by the "list projects" command.
        """

    def get_last_opened_project(self) -> RecentProject | None:
        """
        Returns the last opened project's name and path, or None
        if no project has ever been opened.
        """

    def is_session_open(self) -> bool:
        """
        Returns True if a project is currently open in this session.
        This is the authoritative answer to "is a project open right now?"
        """
```

---

# PART 5 — THE AppSession ENTITY

The `AppStateService` works with a small Entity called `AppSession`.
This Entity represents the data inside `session.db` — the application-level
session state. It is the in-memory representation of what is stored in
the session database.

```python
# core/entities/app_session.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RecentProject:
    """
    One entry in the recent projects list.
    Stored in session.db, table: recent_projects.
    """
    project_name:     str
    project_path:     str
    project_mode:     str
    last_opened_at:   str
    open_count:       int   = 1


@dataclass
class AppSession:
    """
    Represents the application-level session state.
    This is the in-memory mirror of what is stored in session.db.

    This Entity is NOT about any specific project.
    It is about the application itself — what it remembers
    between sessions, independently of any project.

    ONLY AppStateService reads and writes this Entity.
    """

    # ── CURRENT SESSION STATE ─────────────────────────────────────────
    is_project_open:        bool                    = False
    current_project_name:   Optional[str]           = None
    current_project_path:   Optional[str]           = None
    session_opened_at:      Optional[str]           = None

    # ── LAST SESSION MEMORY ───────────────────────────────────────────
    last_project_name:      Optional[str]           = None
    last_project_path:      Optional[str]           = None
    last_opened_at:         Optional[str]           = None

    # ── RECENT PROJECTS LIST ──────────────────────────────────────────
    recent_projects:        list[RecentProject]     = field(default_factory=list)
    max_recent:             int                     = 10
```

---

# PART 6 — PROJECT SETTINGS: READ-ONLY AFTER CREATION

## Where Project Settings Live

Every project has a `project_settings` table inside its own
`project_data.db` file. This is NOT a separate file. It is a table
inside the same database that stores scenes, audio clips, and cache records.

```
project_data.db  (one file per project, inside the project folder)
│
├── table: scenes          <- SceneLifecycleService reads/writes this
├── table: audio_clips     <- AudioPreparationService reads/writes this
├── table: cache_records   <- RenderCacheService reads/writes this
├── table: render_history  <- RenderPipelineService reads/writes this
└── table: project_settings  <- READ-ONLY after initial creation
```

## What Project Settings Stores

The `project_settings` table stores the configuration that was locked in
when the project was created plus settings that change during the project's
life (export settings, render defaults).

```
+=====================================================================+
|                project_settings TABLE CONTENTS                      |
+=====================================================================+
|                                                                     |
|   LOCKED AT CREATION (never change after project is created):       |
|   ─────────────────────────────────────────────────────────────    |
|   project_name          TEXT    The name given at creation.         |
|   project_mode          TEXT    "normal"/"simplemanim"/"supermanim" |
|   project_folder_path   TEXT    Where the project lives on disk.    |
|   project_db_path       TEXT    Path to this database file.         |
|   project_created_at    TEXT    Timestamp of creation.              |
|                                                                     |
|   UPDATED DURING THE PROJECT'S LIFE:                                |
|   ─────────────────────────────────────────────────────────────    |
|   project_updated_at    TEXT    Last time anything changed.         |
|   export_format         TEXT    mp4/webm/mov/avi. Default: "mp4"   |
|   export_quality        TEXT    low/medium/high/ultra. Def: "high" |
|   export_name           TEXT    Custom output filename. Default: NULL|
|   render_resolution     TEXT    Default: "1920x1080"                |
|   render_fps            INTEGER Default: 60                         |
|   render_background_color TEXT  Default: "#000000"                  |
|   preview_resolution    TEXT    Always "854x480" (not editable)     |
|   preview_fps           INTEGER Default: 30                         |
|   audio_format          TEXT    Default: "mp3"                      |
|                                                                     |
+=====================================================================+
```

## The Read-Only Rule for project_settings

You said: **no one can edit this table.** Let us be precise about what
this means in the system.

The locked fields (project_name, project_mode, project_folder_path,
project_created_at) are written exactly once — when the project is
created — and can never be changed by any command or any service
after that moment.

The updatable fields (export_format, export_quality, render_resolution,
etc.) CAN be changed by the user through commands like `set export format`
and `set export quality`. But the rule is that only ONE specific class is
allowed to write to this table: the `ProjectSettingsRepository` adapter.
No other Service, no other Adapter, no other piece of code writes to
`project_settings` directly.

```
+=====================================================================+
|              WHO CAN READ AND WRITE project_settings               |
+=====================================================================+
|                                                                     |
|   ALL SERVICES can READ project_settings through the Port:          |
|   ProjectSettingsRepositoryPort.load_settings(project_id)          |
|                                                                     |
|   ONLY ProjectLifecycleService can UPDATE the mutable fields:       |
|   set_export_format(), set_export_quality(), set_export_name(),     |
|   set_render_resolution(), etc.                                     |
|   It does this through ProjectSettingsRepositoryPort.               |
|                                                                     |
|   NO ONE can UPDATE the locked fields after creation:               |
|   project_name, project_mode, project_folder_path,                 |
|   project_created_at                                                |
|   These are written once. Never touched again.                      |
|                                                                     |
|   THE ADAPTER (SqliteProjectSettingsRepository) enforces this:      |
|   It has a method update_settings() that only accepts the           |
|   mutable fields. It has no method that allows changing             |
|   project_name, project_mode, or project_created_at.               |
|   It is physically impossible to change them through the Port.      |
|                                                                     |
+=====================================================================+
```

---


# PART 8 — HOW EVERYTHING CONNECTS: THE COMPLETE SYSTEM FLOW

## Flow 1 — SuperManim Starts With No Previous Session

```
+=====================================================================+
|   STARTUP — FIRST TIME EVER (no session.db exists yet)             |
+=====================================================================+
|                                                                     |
|   1. SuperManim launches.                                           |
|   2. AppStateService checks for session.db in the OS data folder.  |
|   3. session.db does not exist.                                     |
|   4. AppStateService creates session.db with empty tables.          |
|   5. AppSession is created in memory:                               |
|      AppSession(is_project_open=False, recent_projects=[])          |
|   6. Shell shows the welcome banner.                                |
|   7. Shell shows the prompt:  supermanim>                           |
|   8. Tool is in STATE 1 — waiting for user to create/open project. |
|                                                                     |
|   supermanim> _                                                     |
|                                                                     |
+=====================================================================+
```

## Flow 2 — User Creates a New Project

```
+=====================================================================+
|   USER TYPES: new project MyAnimation                               |
+=====================================================================+
|                                                                     |
|   1. Shell calls ProjectLifecycleService.create_project(            |
|          "MyAnimation")                                             |
|                                                                     |
|   2. ProjectLifecycleService:                                       |
|      a. Validates the name (no spaces, not empty).                  |
|      b. Checks no project with this name already exists.            |
|      c. Creates all folders on disk via FileStoragePort.            |
|      d. Creates project_data.db inside the folder.                  |
|      e. Creates and populates project_settings table (locked        |
|         fields written here — project_name, mode, path,             |
|         created_at — never to be changed again).                    |
|      f. Creates the Project Entity in memory.                       |
|      g. Stores the Project in self._current_project.               |
|                                                                     |
|   3. ProjectLifecycleService calls AppStateService.                 |
|      record_project_opened(                                         |
|          project_name = "MyAnimation",                              |
|          project_path = "/projects/MyAnimation",                    |
|          project_mode = "supermanim"                                |
|      )                                                              |
|                                                                     |
|   4. AppStateService updates session.db:                            |
|      app_session table:                                             |
|        is_project_open    = 1                                       |
|        last_project_name  = "MyAnimation"                           |
|        last_project_path  = "/projects/MyAnimation"                 |
|        last_opened_at     = "2024-11-12 14:18:05"                   |
|      recent_projects table:                                         |
|        INSERT new row for "MyAnimation"                             |
|                                                                     |
|   5. AppSession in memory is updated:                               |
|      is_project_open       = True                                   |
|      current_project_name  = "MyAnimation"                          |
|                                                                     |
|   6. Tool is now in STATE 2 — one project open.                     |
|                                                                     |
|   7. Shell shows confirmation. Prompt returns.                      |
|                                                                     |
+=====================================================================+
```

## Flow 3 — User Closes the Project and Opens a Different One

```
+=====================================================================+
|   CLOSING ONE PROJECT AND OPENING ANOTHER                           |
+=====================================================================+
|                                                                     |
|   STEP A: User types "close project"                                |
|   ─────────────────────────────────────────────────────────────    |
|   1. Shell calls ProjectLifecycleService.close_project()            |
|   2. ProjectLifecycleService saves any unsaved data.                |
|   3. ProjectLifecycleService calls                                  |
|      AppStateService.record_project_closed()                        |
|   4. AppStateService updates session.db:                            |
|      is_project_open = 0                                            |
|   5. AppSession in memory: is_project_open = False                  |
|   6. self._current_project = None                                   |
|   7. Tool is back in STATE 1 — no project open.                     |
|                                                                     |
|   STEP B: User types "open project Chapter1_Intro"                  |
|   ─────────────────────────────────────────────────────────────    |
|   1. Shell calls ProjectLifecycleService.open_project(              |
|          "Chapter1_Intro")                                          |
|   2. ProjectLifecycleService:                                       |
|      a. Finds the folder at /projects/Chapter1_Intro/               |
|      b. Opens project_data.db from that folder.                     |
|      c. Reads project_settings table to load the Project Entity.    |
|      d. Reads all scene records to load Scenes.                     |
|      e. Stores in self._current_project.                            |
|   3. Calls AppStateService.record_project_opened(                   |
|          "Chapter1_Intro", "/projects/Chapter1_Intro", "simplemanim"|
|      )                                                              |
|   4. AppStateService updates session.db:                            |
|      is_project_open   = 1                                          |
|      last_project_name = "Chapter1_Intro"                           |
|      recent_projects   updated — "Chapter1_Intro" moved to top      |
|   5. Tool is in STATE 2 — Chapter1_Intro is now the open project.  |
|                                                                     |
|   THE KEY POINT: MyAnimation is completely unaware any of this      |
|   happened. Its project_data.db was not touched. Its Project Entity |
|   is no longer in memory. Only Chapter1_Intro exists now.           |
|                                                                     |
+=====================================================================+
```

## Flow 4 — SuperManim Restarts After a Previous Session

```
+=====================================================================+
|   STARTUP — RETURNING USER (session.db exists from before)          |
+=====================================================================+
|                                                                     |
|   1. SuperManim launches.                                           |
|   2. AppStateService reads session.db.                              |
|   3. session.db has:                                                |
|      is_project_open   = 1                                          |
|      last_project_name = "MyAnimation"                              |
|      last_project_path = "/projects/MyAnimation"                    |
|                                                                     |
|   4. AppStateService checks: does /projects/MyAnimation/ exist?     |
|                                                                     |
|      Case A: YES — the folder and database are still there.         |
|      -> AppStateService tells ProjectLifecycleService to open it.   |
|      -> Tool starts in STATE 2 with MyAnimation already open.       |
|      -> The user sees:                                              |
|                                                                     |
|         Opening last project: MyAnimation                           |
|         Project "MyAnimation" loaded.                               |
|         Mode:   supermanim                                          |
|         Scenes: 5  (3 rendered, 1 pending, 1 failed)               |
|         supermanim>                                                  |
|                                                                     |
|      Case B: NO — the folder was deleted or moved.                  |
|      -> AppStateService cannot reopen the project.                  |
|      -> Sets is_project_open = 0 in session.db.                     |
|      -> Tool starts in STATE 1 with a warning:                      |
|                                                                     |
|         WARNING: Last project "MyAnimation" was not found at        |
|         /projects/MyAnimation/. It may have been moved or deleted.  |
|         supermanim>                                                  |
|                                                                     |
+=====================================================================+
```

---

# PART 9 — THE COMPLETE TWO-FILE PICTURE

Here is the full picture showing both files, who owns each one,
what each stores, and how they relate to each other.

```
+=====================================================================+
|              THE COMPLETE FILE AND SERVICE PICTURE                  |
+=====================================================================+
|                                                                     |
|   OS APPLICATION DATA FOLDER                                        |
|   (%APPDATA%\SuperManim\  or  ~/.supermanim/)                       |
|   │                                                                 |
|   └── session.db                                                    |
|       │  Owned by: AppStateService ONLY                             |
|       │  Contains:                                                  |
|       ├── table: app_session                                        |
|       │     is_project_open, last_project_name,                     |
|       │     last_project_path, last_opened_at                       |
|       └── table: recent_projects                                    |
|             project_name, project_path, project_mode,               |
|             last_opened_at, open_count                              |
|                                                                     |
|   ─────────────────────────────────────────────────────────────    |
|                                                                     |
|   USER'S PROJECTS FOLDER                                            |
|   (/projects/)                                                      |
|   │                                                                 |
|   ├── MyAnimation/                                                  |
|   │   ├── project_data.db                                           |
|   │   │   ├── table: project_settings  <- READ-ONLY locked fields  |
|   │   │   │         Writable: export_format, export_quality,        |
|   │   │   │                   render_resolution, etc.               |
|   │   │   │         Locked:   project_name, project_mode,           |
|   │   │   │                   project_created_at                    |
|   │   │   ├── table: scenes                                         |
|   │   │   ├── table: audio_clips                                    |
|   │   │   └── table: cache_records                                  |
|   │   │                                                             |
|   │   ├── audio_clips/                                              |
|   │   ├── scenes/                                                   |
|   │   ├── output/                                                   |
|   │   ├── previews/                                                 |
|   │   ├── exports/                                                  |
|   │   ├── assets/                                                   |
|   │   ├── cache/                                                    |
|   │   └── temp/                                                     |
|   │                                                                 |
|   └── Chapter1_Intro/                                               |
|       └── project_data.db                                           |
|           └── (same table structure as above)                       |
|                                                                     |
|   ─────────────────────────────────────────────────────────────    |
|                                                                     |
|   IN MEMORY (while SuperManim is running)                           |
|                                                                     |
|   AppStateService holds:                                            |
|     AppSession (is_project_open, current_project_name,              |
|                 recent_projects list)                               |
|                                                                     |
|   ProjectLifecycleService holds (when open):                        |
|     self._current_project = Project(...)    <- ONE project only     |
|                                                                     |
+=====================================================================+
```

---

# PART 10 — FINAL SUMMARY: THE FOUR THINGS TO REMEMBER

```
+================================================================+
|                                                                |
|   1. ONE PROJECT AT A TIME                                     |
|      The tool has exactly two states:                          |
|      is_project_open = False  (waiting for user)              |
|      is_project_open = True   (one project loaded)            |
|      Two projects cannot be open simultaneously. Ever.         |
|                                                                |
|   2. TWO SEPARATE DATABASE FILES                               |
|      session.db       lives in the OS data folder.            |
|                       tracks which project was last open.      |
|                       tracks the recent projects list.         |
|                       owned exclusively by AppStateService.    |
|                                                                |
|      project_data.db  lives inside the project folder.        |
|                       stores everything about that project.    |
|                       owned by all repository adapters.        |
|                                                                |
|   3. PROJECT SETTINGS IS READ-ONLY FOR LOCKED FIELDS           |
|      project_settings is a table inside project_data.db.       |
|      Locked fields (project_name, mode, created_at, path)      |
|      are written once at creation and never changed again.     |
|      Mutable fields (export_format, quality, resolution)       |
|      can only be changed through ProjectLifecycleService.      |
|                                                                |
|   4. AppStateService IS THE ONLY WATCHER OF session.db         |
|      No other Service reads or writes session.db.              |
|      AppStateService is always running.                        |
|      It is the only Service active before any project opens.   |
|                                                                |
+================================================================+
```



