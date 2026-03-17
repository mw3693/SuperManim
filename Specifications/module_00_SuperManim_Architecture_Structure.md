

# SuperManim — Module 00: Architecture & Design Reference

**Project:** SuperManim CLI Tool  
**Purpose:** Incremental, Audio-Synchronized Manim Animation Production  
**Language:** Python 3.10+

---
### Section 0.1  — What Is SuperManim?

Imagine you are making a 30-minute educational video with Manim.
The video has 20 scenes. Each scene takes 5 minutes to render.
Total render time: 100 minutes.

You spot a small mistake in scene 14. You fix it.
Without SuperManim, you re-render all 20 scenes. 100 minutes again.
With SuperManim, only scene 14 re-renders. 5 minutes. The other 19 are untouched.

This is the core problem SuperManim solves.

SuperManim is a CLI tool that sits on top of Manim.It does not replace Manim.
It adds a production layer on top of it.Manim renders individual scenes.
SuperManim manages the whole project.

```
+-------------------------------------------------------------------+
|              The SuperManim Idea in One Picture                   |
|                                                                   |
|  Without SuperManim:                                              |
|  User -> Manim -> renders EVERYTHING every time -> video          |
|                                                                   |
|  With SuperManim:                                                 |
|  User -> SuperManim -> checks what changed                        |
|               |                                                   |
|               +-- Scene unchanged? -> reuse cached render (fast)  |
|               +-- Scene changed?   -> call Manim to render (slow) |
|                                                                   |
|  SuperManim says to Manim: "Render only this one scene."          |
|  SuperManim handles: caching, audio sync, timeline, export.       |
+-------------------------------------------------------------------+
```


The audio-first philosophy:

```
Traditional approach:               SuperManim approach:
---------------------------------   ---------------------------------
1. Write animation code             1. Load the audio file
2. Render video                     2. Measure total duration
3. Record narration separately      3. Divide audio into scenes
4. Manually sync audio to video     4. Write Manim code per scene
5. Hope they match                  5. Render -- already in sync
```

In SuperManim, the audio file is the spine of the project.Everything is measured and timed relative to it.
There is no separate sync step -- synchronisation is built in.


### Section 0.2 What the main  problem does SuperManim solve?
SuperManim is a versatile tool. It can be used to edit audio files and video files separately.
For example, it can edit audio file formats, split audio files, extract metadata,
and remove sound from video.

The tool works as a media editor, but there are other functions it can perform,
like creating Manim scenes without audio—just what Manim does:

-determine the number of scenes
- write scripts for each scene
-and then render them.

But the main problem that SuperManim solves is the synchronization of Manim videos with audio.
Making a Manim animation that is synchronized to audio is hard.Here is what you have to do
manually without SuperManim:


```
1. Load your audio file.
2. Figure out how long it is.
3. Split it into segments that correspond to visual scenes.
4. Write Manim code for each segment.
5. Make sure each scene runs for exactly the right number of seconds.
6. Render each scene separately.
7. Assemble all scenes into one video.
8. Make sure the final video matches the audio length.
9. If anything is wrong, go back to step 3 and repeat everything.
```

Without tooling, this process involves manually managing files,
running terminal commands, doing mental arithmetic about durations,
and rebuilding the entire video every time one scene changes.

SuperManim eliminates all of that.

With SuperManim, the process becomes:

```
1. supermanim new MyAnimation
2. supermanim add audio voice.mp3
3. supermanim set scenes_numbers  5
4. supermanim set scene 1 duration 2.5
5. supermanim add scene 1  code scene1.py
6. supermanim render scene 1

```

SuperManim handles all file management, all duration calculations,
all timeline tracking, all rendering coordination, and all exports.

---


### Section 0.3 The General usages of the SuperManim :
The tool can be used different type of projects based on the mode of the tool that the user
wants for example:
**App Mode = Normal Editor**
In this mode the tool is used to edit media files audio , video files

after creating the 
**App Mode = Normal Manim Editor**
in this mode the tool is used to edit create manim video scenes without audio to syncronize
in this mode the tool is a wrapper above manim it is manim but with wrapper
the user just one create project
he can write these commands

set the number of scenes he want to create
set scenes_number 2
set scenes_number 4

or if he wants to make one scene
set scene
or set scenes_number 1

after determine the number of scenes he can determine the duration for each one
set scene 1 duration 3.4
set scene 3 duration 5
set scene 6 duration 2
etc

after determine the duration he should set the




### Section 0.4 — Full File Structure of the Project on Disk

#### Subsection 0.4.1 The complete directory layout for a SuperManim installation:
This is the complete directory layout for a SuperManim installation.
Every file is listed. Every directory is explained.

```
supermanim/
│
├── config/
│   ├── constants.py          <- Module 01: all fixed values used across the project
│   └── project_settings.py  <- Module 02: reads and writes settings.json
│
├── core/
│   ├── state.py              <- Module 04: AppState (runtime in-memory state)
│   ├── coordinator.py        <- Module 05: ProjectCoordinator (only AppState writer)
│   ├── session_manager.py    <- Module 06: reads and writes session.json
│   ├── project_manager.py    <- Module 07: creates/opens/closes projects
│   ├── audio_manager.py      <- Module 08: all audio operations
│   ├── scenes_manager.py     <- Module 09: all scene operations
│   ├── timeline_manager.py   <- Module 10: all timeline operations (Floor 5)
│   ├── rendering_manager.py  <- Module 11: calls Manim, assembles video
│   ├── preview_manager.py    <- Module 12: fast low-quality previews
│   ├── cache_manager.py      <- Module 13: hash-to-frame cache (Floor 2)
│   ├── export_manager.py     <- Module 14: packages output for delivery
│   └── utilities.py          <- Module 13: shared helper functions
│
├── ui/
│   └── cli/
│       └── commands.py       <- Module 15: CLI (Floor 6, top of the stack)
│


```
Every file on disk is owned by exactly one module.No two modules write to the same file.
This is enforced by design, not by a lock mechanism.The design itself makes it impossible
for two modules to accidentally share a file.

#### Subsection 0.4.2 The complete structure of the drirectory of created projects:
The tool can be used different type of projects based on the mode of the tool that the user
wants for example:
**App Mode = Normal Editor**
In this mode the tool is used to edit media files audio , video files

after creating the 
**App Mode = Normal Manim Editor**
in this mode the tool is used to edit create manim video scenes without audio to syncronize
in this mode the tool is a wrapper above manim it is manim but with wrapper
the user just one create project
he can write these commands

set the number of scenes he want to create
set scenes_number 2
set scenes_number 4

or if he wants to make one scene
set scene
or set scenes_number 1

after determine the number of scenes he can determine the duration for each one
set scene 1 duration 3.4
set scene 3 duration 5
set scene 6 duration 2
etc

after determine the duration he should set the








When a user creates a project called "MyAnimation", this is created on disk:

```
/projects/MyAnimation/
+-- settings.json        <- owned by ProjectSettings (Module 04)
+-- audio.json           <- owned by AudioManager (Module 06)
+-- scenes.json          <- owned by ScenesManager (Module 07)
+-- timeline.json        <- owned by TimelineManager (Module 08)
|
+-- audio_clips/         <- managed by AudioManager
|   +-- original_audio.mp3    <- the user's audio file, copied here
|   +-- clip_001.mp3          <- scene clips (after splitting)
|   +-- clip_002.mp3
|
+-- scenes/              <- managed by ScenesManager
|   +-- scene_01/
|   +-- scene_02/
|
+-- cache/               <- managed by CacheManager (Module 12)
+-- output/              <- rendered video lives here (Module 09)
+-- previews/            <- preview files (Module 11)
+-- exports/             <- exported packages (Module 14)
+-- assets/              <- user-provided images, fonts, videos
+-- temp/                <- temporary working files
```

