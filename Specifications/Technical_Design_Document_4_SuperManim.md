
# Module 0 — An Overview of SuperManim

**Project:** SuperManim CLI Tool
**Language:** Python 3.10+
**Purpose:** Incremental, Audio-Synchronized Manim Animation Production

---
# Section 0.1 — What Is SuperManim?
Imagine you are making a 30-minute educational video using a Python animation
tool called **Manim**. Your video has **20 scenes**. Each scene takes about
**5 minutes** to render on your computer.Total rendering time: **100 minutes**.

You watch the finished video. You spot a tiny mistake in **Scene 14**.
One shape is the wrong color. You fix the one line of code that caused the mistake.

Now what?

Without any tooling, you have to **re-render all 20 scenes** from scratch.
It does not matter that only one scene changed.The default Manim workflow
does not remember what was already done.So you wait another **100 minutes**
for something that only needed **5 minutes**.

**SuperManim solves exactly this.**

With SuperManim, you fix Scene 14. SuperManim checks every scene.
It sees that Scenes 1–13 and 15–20 have not changed at all — their code is
identical, their audio clips are the same. It skips them.
It only re-renders Scene 14. You wait **5 minutes** instead of **100**.

This is the core idea. Everything else in SuperManim is built on top of this idea.

```
+----------------------------------------------------------------------+
|                    THE SUPERMANIM CORE IDEA                          |
+----------------------------------------------------------------------+
|                                                                      |
|   WITHOUT SuperManim:                                                |
|   ───────────────────────────────────────────────────────────────   |
|   You fix 1 scene.                                                   |
|   You run Manim.                                                     |
|   Manim renders ALL 20 scenes from scratch.                          |
|   You wait 100 minutes.                                              |
|                                                                      |
|   WITH SuperManim:                                                   |
|   ───────────────────────────────────────────────────────────────   |
|   You fix 1 scene.                                                   |
|   SuperManim checks all 20 scenes using fingerprints.                |
|                                                                      |
|        +-- Scene 1   unchanged? --> use saved render. Skip. (0 sec) |
|        +-- Scene 2   unchanged? --> use saved render. Skip. (0 sec) |
|        +-- Scene 3   unchanged? --> use saved render. Skip. (0 sec) |
|        +-- ...                                                       |
|        +-- Scene 14  CHANGED!   --> call Manim. Render it. (5 min)  |
|        +-- Scene 15  unchanged? --> use saved render. Skip. (0 sec) |
|        +-- ...                                                       |
|        +-- Scene 20  unchanged? --> use saved render. Skip. (0 sec) |
|                                                                      |
|   Total wait: 5 minutes instead of 100.                              |
|                                                                      |
+----------------------------------------------------------------------+
```

---

**SuperManim is NOT a Replacement for Manim**

SuperManim does **not** replace Manim. Manim still does all the actual animation rendering.
SuperManim is the **manager** that sits on top of Manim and decides what work Manim actually
needs to do.Think of it like a boss and an employee:

```
+================================================================+
|              THE BOSS AND THE EMPLOYEE                         |
+================================================================+
|                                                                |
|   MANIM (the employee)                                         |
|   ─────────────────────────────────────────────────────────── |
|   Very good at rendering animations.                           |
|   But has NO memory.                                           |
|   Every time you ask it to do something, it starts from zero.  |
|   It does not know what it rendered last time.                 |
|   It does not know if anything changed.                        |
|   It just does what you tell it, every single time.            |
|                                                                |
|   SUPERMANIM (the boss)                                        |
|   ─────────────────────────────────────────────────────────── |
|   Remembers everything that was already done.                  |
|   Keeps a fingerprint of every scene's code file.              |
|   Compares the fingerprint before each render.                 |
|   If the fingerprint matches: "Skip it. Nothing changed."      |
|   If the fingerprint differs: "Manim, render this one."        |
|   Handles all file management and audio sync automatically.    |
|                                                                |
+================================================================+
```
---

# Section 0.2 — What Is the Main Problem SuperManim Solves?

SuperManim is a multi-purpose tool. It can:

- Edit audio files — split them, convert their format, measure their duration
- Edit video files — remove audio, split a video, change format
- Create Manim animations without audio
- Create Manim animations **synchronized perfectly with audio** (the main feature)

But the hardest problem it solves — the one that no other tool handles automatically — is this:

How do you make a Manim video that matches your audio file perfectly, and how do you do it
without rebuilding everything from scratch every single time you change one small thing?

---

This Is So Hard Without SuperManim

Suppose you have a 60-second narration audio file. You want to make an animation that plays
alongside it. Here is what you must do manually, by hand, without any tooling:

```
+=====================================================================+
|             THE PAINFUL MANUAL WORKFLOW (10 steps)                  |
+=====================================================================+
|                                                                     |
|  Step 1.  Load your audio file into an audio editor.                |
|  Step 2.  Measure the total duration. It is 60.0 seconds.           |
|  Step 3.  Decide which parts of the audio go with which scenes.     |
|                                                                     |
|           Seconds  0.0 to 12.5  -->  Scene 1 (introduction)        |
|           Seconds 12.5 to 31.0  -->  Scene 2 (main concept)        |
|           Seconds 31.0 to 47.8  -->  Scene 3 (example)             |
|           Seconds 47.8 to 60.0  -->  Scene 4 (conclusion)          |
|                                                                     |
|  Step 4.  Write Manim Python code for Scene 1.                      |
|           Make sure the animation runs for exactly 12.5 seconds.   |
|           Not 12.4. Not 12.6. Exactly 12.5.                        |
|  Step 5.  Repeat for Scenes 2, 3, and 4.                           |
|  Step 6.  Render each scene separately using the Manim CLI.         |
|  Step 7.  Assemble all four rendered video files with FFmpeg.       |
|  Step 8.  Check that the total video length equals 60.0 seconds.   |
|  Step 9.  Play the video alongside the audio. Check if they match.  |
|  Step 10. They do not match perfectly. Go back to Step 3.           |
|           Repeat everything from scratch.                           |
|                                                                     |
+=====================================================================+
```

This is painful. It requires:
- A lot of manual file management — tracking which clip goes with which scene
- Mental arithmetic — adding up durations to make sure they sum correctly
- Running multiple terminal commands in the right order every single time
- Rebuilding the entire assembled video every time even one scene changes


SuperManim replaces all ten of those steps with a few simple commands:

```bash
supermanim> new project MyAnimation
supermanim> add audio voice.mp3
supermanim> set scenes_number 5
supermanim> set scene 1 duration 12.5
supermanim> set scene 1 code scene1.py
supermanim> render all
```

SuperManim handles automatically:

```
+================================================================+
|             WHAT SUPERMANIM HANDLES FOR YOU                    |
+================================================================+
|                                                                |
|   File management       All scene clips, audio clips,         |
|                          and output files are organized        |
|                          automatically in a project folder.    |
|                                                                |
|   Duration calculations Scene start and end times are         |
|                          computed and kept in sync.            |
|                                                                |
|   Timeline tracking     The system always knows when each     |
|                          scene starts in the final video.      |
|                                                                |
|   Smart rendering       Only re-renders scenes whose code     |
|                          actually changed since last time.     |
|                                                                |
|   Audio/video assembly  Joins all clips into one final         |
|                          synchronized video automatically.     |
|                                                                |
+================================================================+
```
---

# Section 0.3 — The General Usages of SuperManim

SuperManim can be used in three different ways. Each usage serves a different
purpose and handles a different kind of work. The three usages are not
exclusive — you pick the one that matches what you are trying to do.

```
+================================================================+
|               THE THREE USAGES AT A GLANCE                     |
+================================================================+
|                                                                |
|   USAGE 1 — Normal Media Editor                                |
|   You already have a video or audio file.                      |
|   You want to cut it, convert it, or change it.                |
|   No Manim. No animations. No code.                            |
|                                                                |
|   USAGE 2 — Simple Manim Editor                                |
|   You want to build a silent animated video using Manim.       |
|   You write Python code for each scene.                        |
|   SuperManim renders them and joins them into one video.       |
|   No audio synchronization.                                    |
|                                                                |
|   USAGE 3 — SuperManim Editor   (the main usage)               |
|   You want to build an animated video synchronized to audio.   |
|   You provide a narration audio file.                          |
|   SuperManim splits it, maps it to scenes, renders,            |
|   and assembles everything into one synchronized video.        |
|                                                                |
+================================================================+
```

---

## Subsection 0.3.1 — Usage 1: The Normal Media Editor

### Subsubsection  0.3.1.1 — What Is This Usage?

This usage is for editing videos and audio files you already have.
Think of it like a simple cutting table.
If you have a long video and want to make it shorter, or if you have a song
and want to cut out certain parts, you use this.

There is no Manim involved. No scenes. No animations. No Python code.
It is purely about working with existing media files.

### Subsubsection  0.3.1.2 — How to Use It

**Step 1 — Create Your Project Space:**
Before you start working, the tool needs a place to save your work.
It creates a project folder structure on disk — like opening a folder
on your desk to keep all your papers organized.

```bash
supermanim> new project MyMediaProject 
```
**Step 2 — Add Your File:**
You give the tool the file you want to edit.

If you want to edit a sound file:

```bash
supermanim> add audio "path/to/audio.mp3"
```
or

```bash
supermanim> add audio_file "path/to/audio.mp3"
```

If you want to edit a video file:
```bash
supermanim> add video "path/to/video.mp4"
```

**Step 3 — Perform Your Operation:**
Once the file is loaded, you perform the change you need.

```bash
supermanim> split audio 30.0         # cut the audio at 30 seconds
supermanim> convert audio wav         # convert mp3 to wav
supermanim> remove audio from video   # strip the audio out of a video
```

**Step 4 — The Result:**
The new file is saved automatically in your project's `output/` folder.

### Subsubsection  0.3.1.3 — Workflow Diagram

```
+-------------------------------------------------------------+
|               USAGE 1 — NORMAL MEDIA EDITOR                 |
+-------------------------------------------------------------+

      [ User Opens SuperManim ]
                |
                v
    +-------------------------+
    | Create Project Space    |  <-- Makes a workspace folder
    +-------------------------+
                |
                v
    +-------------------------+
    | Add Media File          |  <-- Give the tool a video or audio file
    | (video or audio)        |
    +-------------------------+
                |
                v
    +-------------------------+
    | Perform Operation       |  <-- Cut, split, convert, remove audio...
    +-------------------------+
                |
                v
    +-------------------------+
    | Result Saved in output/ |  <-- The new file is ready
    +-------------------------+
```

### Subsubsection  0.3.1.4 — The commands that used in this Usage:
These are the specific commands available for the Normal Media Editor.
These commands focus on file management and basic media editing operations. 

#### `new project <ProjectName>`
This command initializes your workspace. When you run it, SuperManim creates a new directory using
the name you provided. Inside this directory, it automatically generates the necessary subfolders
such as `audio_clips`, `video_clips`, `output`, `assets`, and `temp`—and creates the `project_data.db` file.

This ensures you have a clean, organized environment ready to store your media and track your progress.
It is the first command you run before doing any work.

#### `add audio "<path>"` (and `add audio_file "<path>"`):
This command is used to import sound files into your project. You provide the full path to the audio file
on your computer (for example, `"C:/music/song.mp3"`). SuperManim then copies this file from its original
location into the project's `audio_clips/` folder.

This ensures that the original file remains untouched and that the project has its own dedicated copy to
work with. The tool also records the file details in the database, making it the "active" audio file
for subsequent operations. The command `add audio_file` acts as an alias and does the exact same thing.

#### `add video "<path>"`:
This command works similarly to the audio import command but is designed for video files.
You provide the path to a video file (like `"videos/clip.mp4"`). The tool copies this file into
the `video_clips/` folder within your project structure.

Once imported, the video becomes the active subject for editing, allowing you to perform operations
like removing its audio track. The database updates immediately to reflect this new addition.

#### `split audio <seconds>`
This command allows you to divide a single audio file into two separate parts.
You specify the exact time in seconds where you want the cut to happen.

For instance, if you type `split audio 30.0`, the tool processes the audio file
and cuts it precisely at the 30-second mark. The system generates new audio segments
based on your instruction.

These resulting clips are saved within the project, allowing you to use them individually
or discard the parts you do not need.


#### `convert audio <format>`:
This command changes the file format of your audio. You specify the desired target format,
such as `wav` or `ogg`. The tool takes the active audio file and re-encodes it into the new
format you specified.

Once the conversion is complete, the new file is saved in the `output/` folder.
This is useful for compatibility reasons, ensuring your media works with different players
or platforms without needing a separate converter tool.

#### `remove audio from video`**
This command separates the sound from the visuals in a video file. When you run this,
SuperManim takes the active video file and strips out the audio track entirely,
leaving only the visual content. I

t then saves a new version of the video file that has no sound.
This new silent video file is saved automatically in the `output/` folder.

It is commonly used when you want to replace the background music of a video or
when you only need the visual part for further processing.

#### **`list projects`**

This command displays all the projects available on your system. When you run this,
SuperManim scans the workspace directory and collects the names of all existing projects.

It then presents them in a simple list so you can easily choose which one to work on.

This is commonly used when you have multiple projects and need a quick overview before opening one.

---

#### **`open project <ProjectName>`**

This command opens an existing project. When you run this,
SuperManim sets the selected project as the current working environment.

All subsequent commands will operate inside this project, including file operations
and database updates.

This is typically used before performing any work on a previously created project.

---

#### **`project info`**

This command shows detailed information about the current project. When you run this,
SuperManim gathers metadata such as the number of audio and video files, storage usage,
and the currently active media.

It then displays this information in a clear and structured format.

This is useful for understanding the current state of your project at any time.

---

#### **`list audio`**

This command lists all audio files inside the project. When you run this,
SuperManim reads the audio records from the database and retrieves their details.

It then displays each file along with useful information such as name and duration.

This helps you quickly browse and manage your available audio clips.

---

#### **`list video`**

This command lists all video files inside the project. When you run this,
SuperManim retrieves video records from the database and prepares them for display.

It then shows each video file along with its associated details.

This is useful for reviewing all video assets currently stored in the project.

---

#### **`set active audio <audio_id>`**

This command selects a specific audio file as the active one. When you run this,
SuperManim updates the database to mark the chosen file as active.

All future audio operations—such as splitting, trimming, or converting—
will automatically use this file.

This ensures that you are always working on the correct audio clip.

---

#### **`set active video <video_id>`**

This command selects a specific video file as the active one. When you run this,
SuperManim updates the system state to mark this video as active.

All upcoming video-related operations will be applied to this file.

This helps prevent accidental modifications to the wrong video.

---

#### **`delete audio <audio_id>`**

This command removes an audio file from the project. When you run this,
SuperManim deletes the file from the `audio_clips/` directory.

It also removes the corresponding record from the database to keep everything consistent.

This is useful when you no longer need a specific audio file in your project.

---

#### **`delete video <video_id>`**

This command removes a video file from the project. When you run this,
SuperManim deletes the file from the `video_clips/` directory.

It also updates the database by removing the associated record.

This keeps your project clean and free of unused video files.

---

#### **`merge audio "<path1>" "<path2>"`**

This command combines two audio files into a single file. When you run this,
SuperManim loads both audio sources and joins them together in sequence.

It then generates a new audio file containing the merged result.

The output is saved automatically in the `output/` folder for later use.

---

#### **`extract audio from video`**

This command extracts the audio track from the active video file. When you run this,
SuperManim separates the sound component from the video.

It then saves the extracted audio as a new file inside the `audio_clips/` folder.

The new file is also registered in the database for future operations.

---

#### **`trim audio <start> <end>`**

This command cuts a specific segment from an audio file. When you run this,
SuperManim processes the active audio file and keeps only the portion
between the given start and end times.

It then saves the trimmed result as a new audio file.

This is useful for removing unwanted sections or isolating important parts.

---

#### **`trim video <start> <end>`**

This command cuts a specific segment from a video file. When you run this,
SuperManim processes the active video file and extracts the portion
between the specified timestamps.

It then creates a new video file containing only that segment.

This is commonly used to remove unnecessary scenes or shorten clips.

---

#### **`rename project <NewName>`**

This command changes the name of the current project. When you run this,
SuperManim renames the project directory on disk.

It also updates the project name inside the database to maintain consistency.

This is useful when you want a more descriptive or organized naming structure.

---

#### **`delete project <ProjectName>`**

This command deletes an entire project. When you run this,
SuperManim removes the project directory along with all its files and subfolders.

It also deletes the associated database and all stored records.

This action is permanent and should be used carefully, as it cannot be undone.

---

#### **`export project`**

This command prepares the project for sharing or backup. When you run this,
SuperManim gathers the necessary files, including outputs and important assets.

It may also compress the project into a single archive for easy transfer.

This is commonly used when you want to move your project to another system
or share it with others.

---

#### **`status`**

This command provides a quick overview of the current state. When you run this,
SuperManim checks the active project and retrieves the current active audio
and video files.

It then displays this information in a short and readable format.

This is useful for quickly confirming what you are working on at any moment.

---

## Subsection 0.3.2 — Usage 2: The Simple Manim Editor

### Subsubsection  0.3.2.1 — What Is This Usage?

This usage is for creating animated videos using code — without any sound.
It is built on Manim, an animation tool that draws pictures and shapes using Python.
Think of this as a robot that draws cartoons for you.

It creates **silent videos** — there is no audio track to match.
You write the animation code, SuperManim renders each scene, and then joins them all
into one final video.

The key advantage over using Manim directly: SuperManim only re-renders scenes
whose code actually changed. If you fix Scene 2, it does not touch Scenes 1, 3, 4, or 5.

### Subsubsection 0.3.2.2 — How to Use It

**Step 1 — Create Your Project Space:**
```bash
supermanim> new project MySilentAnimation
```

**Step 2 — Tell It How Many Scenes You Have:**
A scene is like one page in a storybook. You say how many pages your story has.
```bash
supermanim> set scenes_number 4
```

**Step 3 — Set the Duration of Each Scene:**
You tell the tool how long each scene plays, in seconds.
```bash
supermanim> set scene 1 duration 3.4
supermanim> set scene 2 duration 5.0
supermanim> set scene 3 duration 7.2
supermanim> set scene 4 duration 4.5
```

**Step 4 — Give Each Scene Its Code File:**
You point to the Python file that contains the Manim code for that scene.
```bash
supermanim> set scene 1 code "my_scenes/intro.py"
supermanim> set scene 2 code "my_scenes/concept.py"
supermanim> set scene 3 code "my_scenes/example.py"
supermanim> set scene 4 code "my_scenes/conclusion.py"
```

**Step 5 — Preview (optional) or Render:**
Preview is fast and low-quality — just to check your work.
Render is high-quality — the final video.
```bash
supermanim> preview scene 2       # quick check of Scene 2
supermanim> render all            # render everything
```

### Subsubsection 0.3.2.3 — Workflow Diagram

```
+-------------------------------------------------------------+
|               USAGE 2 — SIMPLE MANIM EDITOR                 |
+-------------------------------------------------------------+

    [ Open SuperManim ]
            |
            v
    [ Create project folder ]
            |
            v
    [ set scenes_number 4 ]
    [ Tell it: 4 scenes total ]
            |
            v
    [ For each scene:               ]
    [ set scene N duration X        ]
    [ set scene N code "file.py"    ]
            |
            v
    [ Preview (optional)        ]
    [ Quick low-quality check   ]
            |
            v
    [ render all                              ]
    [ SuperManim checks EVERY scene:          ]
    [   Scene 1 code unchanged? --> SKIP      ]
    [   Scene 2 code CHANGED?   --> RENDER    ]
    [   Scene 3 code unchanged? --> SKIP      ]
    [   Scene 4 code unchanged? --> SKIP      ]
            |
            v
    [ SuperManim joins all clips         ]
    [ into one final video file          ]
    [ output/MySilentAnimation_final.mp4 ]
```

### Subsubsection 0.3.2.4 — The commands that used in this Usage

These are the main commands for the Simple Manim Editor.
They focus on defining scenes, linking them to code, previewing, and rendering the final video.

#### `new project <ProjectName>`

This command creates a new project folder for your animation work.
SuperManim sets up all necessary subfolders: one for scenes, a temporary folder, an assets folder, and an output folder. It also creates a small database to track your project progress.
Use this as the first step before doing any work.

---

#### `open project <ProjectName>`

Opens an existing project. All following commands will operate within this project until you switch.
This ensures that all scene edits, assets, and render operations are applied to the correct project.

---

#### `list projects`

Displays a list of all projects in your workspace.
This helps you quickly find which projects exist and choose the one you want to open.

---

#### `project info`

Shows detailed information about the currently opened project.
It lists the number of scenes, code file paths, durations, and assets. You can see what’s already set up before making changes.

---

#### `delete project <ProjectName>`

Completely removes a project, including all scenes, assets, and outputs.
Be careful — this is permanent.

---

#### `rename project <NewName>`

Changes the project’s folder name and updates internal records in the database.
Useful for organizing or correcting project names.

---

#### `export project`

Prepares your project for backup or sharing.
SuperManim collects all code files, assets, and output videos into a single folder or archive for transfer to another computer.

---

#### `status`

Provides a quick overview of the current project.
Shows active scenes, which scenes have changed, and what is ready for rendering.

---

#### `set scenes_number <number>`

Sets the total number of scenes your video will contain.
This allows SuperManim to manage the order and allocation of code files for each scene.

---

#### `set scene <scene_number> code "<path>"`

Assigns a Python file containing Manim code to a specific scene.
The code will run when rendering, producing the animated visuals for that scene.

---

#### `set scene <scene_number> duration <seconds>`

Specifies how long a scene should last in the final video.
SuperManim uses this to calculate scene timing and total video length.

---

#### `set scene <scene_number> fps <number>`

Adjusts the frames per second for a scene.
Higher FPS produces smoother animations but larger files. Lower FPS produces smaller files but less smooth motion.

---

#### `set default fps <number>`

Sets the default FPS for all new scenes, so you don’t need to specify it for every scene individually.

---

#### `set scene <scene_number> width <pixels>`

Defines the width of a scene in pixels.
Useful for setting custom resolutions for different platforms.

---

#### `set scene <scene_number> height <pixels>`

Defines the height of a scene in pixels.
Used together with width to control video resolution.

---

#### `add asset "<path>"`

Adds an image, font, or other resource to the project’s `assets/` folder.
Assets can then be referenced in any scene for consistency.

---

#### `list assets`

Displays all assets currently available in the project.

---

#### `remove asset "<asset_name>"`

Deletes an asset from the project folder and removes its record from the database.

---

#### `delete scene <scene_number>`

Removes a specific scene from the project.
The scene’s code, settings, and references are deleted, freeing up project space.

---

#### `duplicate scene <scene_number>`

Creates a copy of a scene, including its code and settings.
Useful when you want to reuse or slightly modify an existing scene.

---

#### `move scene <from> <to>`

Changes the order of scenes in the project.
SuperManim renders scenes in the updated order.

---

#### `merge scenes <scene1> <scene2> ... <sceneN>`

Combines multiple scenes into a single scene for rendering.
Useful to join short segments or create continuous animations.

---

#### `trim scene <scene_number> <start> <end>`

Keeps only a portion of a scene between the start and end times.
The result is saved as a new scene.

---

#### `reset scene <scene_number>`

Clears all settings for a scene, including code, duration, background, camera, and FPS.
Useful for starting a scene fresh.

---

#### `preview scene <scene_number>`

Shows a low-quality preview of a single scene.
Faster than rendering, useful for checking animation quickly.

---

#### `preview all`

Shows a low-quality preview of all scenes combined in sequence.
Good for checking story flow before full rendering.

---

#### `render scene <scene_number>`

Renders a single scene in high-quality video.
SuperManim saves it temporarily to combine with other scenes later.

---

#### `render all`

Renders all scenes in high quality.
SuperManim automatically skips unchanged scenes to save time.
The final video is saved in `output/` as `<ProjectName>_final.mp4`.

---

#### `export scene <scene_number>`

Saves a scene as a separate video file in the output folder.
Useful if you want to share or test one scene without rendering the full video.

---

#### `set scene <scene_number> audio "<path>"`

Links an audio file to a scene for later synchronization.
Even though Simple Manim Editor creates silent videos, this prepares the scene for adding sound later.

---

#### `delete output`

Removes previously rendered video files from the `output/` folder.
Useful for clearing space or re-rendering from scratch.

---

#### `reset all scenes`

Clears settings and code for all scenes in the project.
Useful for starting an entirely new animation sequence.

---

#### `check dependencies`

Verifies that Manim and required Python packages are installed and ready.

---

## Subsection 0.3.3 — Usage 3: The SuperManim Editor

### Subsubsection  0.3.3.1 — What Is This Usage?

This is the most powerful usage. It is like a movie director.

It does everything Usage 2 does — it creates animated video scenes using Manim code —
but it adds the most important superpower: **perfect audio synchronization**.

The tool makes sure the video matches the sound exactly.
If a ball bounces on screen, the sound plays at the exact same moment.
If the narrator says "now look at this graph," the graph appears at that exact second.

This is what makes SuperManim unique. No other tool does this automatically.

### Subsubsection 0.3.3.2 — How to Use It

**Step 1 — Create Your Project Space:**
```bash
supermanim> new project MyVoicedAnimation
```
The tool whether the user uses the tool in the different usages the user have to add the minimum
project folder structures and substructure :



**Step 2 — Add Your Audio File FIRST:**
Because everything is built around the audio, the audio file comes first.
This is usually a voice recording or narration.
```bash
supermanim> add audio "voice_narration.mp3"
```

**Step 3 — Map the Video to the Audio:**
You need to tell the tool how to divide the audio into scenes.
There are two ways to do this:

**Method A — The Manual Way:**
You tell it exactly how many scenes and how long each one is.
The rule: the total time of all scene durations MUST equal the audio file length.
```bash
supermanim> set scenes_number 4
supermanim> set scene 1 duration 12.5
supermanim> set scene 2 duration 18.5
supermanim> set scene 3 duration 16.8
supermanim> set scene 4 duration 12.2
# Total: 60.0 seconds == audio file duration
```

**Method B — The Automatic Way:**
You let SuperManim listen to the audio and detect silences automatically.
Every time it hears a pause, it creates a new scene boundary.
```bash
supermanim> split audio silence
# SuperManim listens, detects 3 pauses, creates 4 clips automatically
```

**Step 4 — Give Each Scene Its Code File:**
```bash
supermanim> set scene 1 code "my_scenes/intro.py"
supermanim> set scene 2 code "my_scenes/concept.py"
supermanim> set scene 3 code "my_scenes/example.py"
supermanim> set scene 4 code "my_scenes/conclusion.py"
```

**Step 5 — Sync Each Scene to Its Audio Clip:**
This links Scene 1 to the first audio slice, Scene 2 to the second, and so on.
The tool checks that each scene's duration matches its audio clip's duration exactly.
```bash
supermanim> sync all
```

**Step 6 — Render and Export:**
```bash
supermanim> render all
supermanim> export
```

### Subsubsection  0.3.3.3 — Workflow Diagram

```
+-------------------------------------------------------------+
|               USAGE 3 — SUPERMANIM EDITOR                   |
+-------------------------------------------------------------+

    [ Open SuperManim ]
            |
            v
    [ Create project folder ]
            |
            v
    [ add audio voice_narration.mp3  ]
    [ This is the foundation.        ]
    [ Everything must match this.    ]
            |
            v
    [ Map the video to the audio ]
    [                            ]
    [ Option A: set scenes and durations manually ]
    [ Total durations must == audio duration      ]
    [                                             ]
    [ Option B: split audio silence               ]
    [ SuperManim detects pauses, creates clips    ]
            |
            v
    [ For each scene:                   ]
    [ set scene N code "file.py"        ]
            |
            v
    [ sync all                          ]
    [ Links Scene 1 <--> clip_001.mp3   ]
    [ Links Scene 2 <--> clip_002.mp3   ]
    [ Verifies durations match exactly  ]
            |
            v
    [ render all                              ]
    [ SuperManim renders each scene           ]
    [ clips the matching audio slice          ]
    [ pairs them together                     ]
    [ (skips scenes whose code did not change)]
            |
            v
    [ export                                  ]
    [ SuperManim assembles:                   ]
    [ Scene 1 video + audio clip 1            ]
    [ Scene 2 video + audio clip 2            ]
    [ Scene 3 video + audio clip 3            ]
    [ Scene 4 video + audio clip 4            ]
    [ --> one final synchronized video file   ]
```

### Subsubsection  0.3.3.4 — The Project Folder Created by This Usage
---

# Section 0.4 — Full File Structure of the SuperManim Tool on Disk

This section shows the complete file and folder structure of the entire
SuperManim tool — not one project, but the tool itself and everything it creates.

There are **two separate locations** on your disk that SuperManim uses.
They serve completely different purposes and must never be confused.
The definitions of the Two Locations:

```
+================================================================+
|              TWO SEPARATE DISK LOCATIONS                       |
+================================================================+
|                                                                |
|   LOCATION 1 — The Tool Itself (your installation)            |
|   ─────────────────────────────────────────────────────────── |
|   Where you installed SuperManim.                              |
|   Contains the Python source code, requirements, README.       |
|   This never changes while you use the tool.                   |
|                                                                |
|   LOCATION 2a — The App Data Folder (global session state)     |
|   ─────────────────────────────────────────────────────────── |
|   Windows:  %APPDATA%\SuperManim\                              |
|   macOS:    ~/Library/Application Support/SuperManim/         |
|   Linux:    ~/.supermanim/                                     |
|   Contains: session.db — tracks which project was last open.  |
|   Created automatically on first run.                          |
|                                                                |
|   LOCATION 2b — Your Projects Folder (your work)              |
|   ─────────────────────────────────────────────────────────── |
|   Wherever you create your projects.                           |
|   Example: /home/you/projects/                                 |
|   Contains: one subfolder per project.                         |
|   Each subfolder has its own project_data.db inside it.        |
|                                                                |
+================================================================+
```

---

## Subsection 0.4.1  The Tool's Source Code Structure

```

```



## Subsection 0.4.2  The App Data Folder (session.db lives here)

```
~/.supermanim/                        <- Linux  (or %APPDATA%\SuperManim\ on Windows)
    |
    +-- session.db                    <- The only file here.
                                         Tracks which project was last open.
                                         Tracks the recent projects list.
                                         Owned EXCLUSIVELY by AppStateService.
                                         Nothing else touches this file.
```

**What is inside session.db:**

```
+================================================================+
|                   INSIDE session.db                            |
+================================================================+
|                                                                |
|   TABLE: app_session  (always exactly ONE row)                 |
|   ─────────────────────────────────────────────────────────── |
|   is_project_open    = 0 or 1                                  |
|   last_project_name  = "MyAnimation"  (or NULL)                |
|   last_project_path  = "/projects/MyAnimation"  (or NULL)      |
|   last_opened_at     = "2024-11-12 14:18:05"  (or NULL)        |
|                                                                |
|   TABLE: recent_projects  (up to 10 rows)                      |
|   ─────────────────────────────────────────────────────────── |
|   project_name       = "MyAnimation"                           |
|   project_path       = "/projects/MyAnimation"                 |
|   last_opened_at     = "2024-11-12 14:18:05"                   |
|                |
|                                                                |
+================================================================+
```

---

## Subsection 0.4.3  The full Project Folder structure (your work)


When you create a new project, the tool automatically builds this
complete folder structure on disk:

```
/projects/Project_Name/
    |
    +-- project_data.db           <-- The project brain (database)
    |
    +-- audio_clips/              
    |       original_audio.mp3    <-- Your audio file, copied here (never cut)
    |       clip_001.mp3          <-- Slice for Scene 1 (cut from original)
    |       clip_002.mp3          <-- Slice for Scene 2
    |       clip_003.mp3          <-- Slice for Scene 3
    |       clip_004.mp3          <-- Slice for Scene 4
    |
    +-- video_clips/              
    |       background.mp4        <-- Source video files used in animations
    |
    +-- scenes/                   <-- Managed by ScenesManager
    |       scene_01/             <-- Folder for Scene 1
    |       scene_02/             <-- Folder for Scene 2
    |       scene_03/             <-- Folder for Scene 3
    |       scene_04/             <-- Folder for Scene 4
    |
    +-- output/                   <-- Rendered clips live here
    |       scene_01/
    |           scene_01.mp4
    |       scene_02/
    |           scene_02.mp4
    |
    +-- previews/                 <-- Low-quality draft renders
    |       scene_01_preview.mp4
    |
    +-- exports/                  <-- The final assembled video
    |       Project_Name_final.mp4
    |
    +-- assets/                   <-- External resources for your animations
    |       |
    |       +-- images/           <-- PNG, JPG, JPEG files
    |       +-- fonts/            <-- TTF, OTF font files
    |       +-- svg/              <-- Vector graphics (SVG files)
    |       +-- data/             <-- JSON, CSV, or text files for data visuals
    |
    +-- temp/                     <-- Temporary files (auto-cleaned)
```

**What each folder does:**

```
+================================================================+
|              WHAT EACH FOLDER IN THE PROJECT DOES              |
+================================================================+
|                                                                |
|   project_data.db                                              |
|   ─────────────────────────────────────────────────────────── |
|   The project brain. An SQLite database file.                  |
|   Remembers: how many scenes, their durations,                 |
|   which audio file belongs to which scene,                     |
|   which scenes are rendered, and all settings.                 |
|                                                                |
|   audio_clips/                                                 |
|   ─────────────────────────────────────────────────────────── |
|   Managed by AudioManager.                                     |
|   original_audio.mp3: the master audio file. Never cut.       |
|   clip_001.mp3, clip_002.mp3...: pieces cut from the master.  |
|   Each clip matches exactly one scene in duration.             |
|                                                                |
|   scenes/                                                      |
|   ─────────────────────────────────────────────────────────── |
|   Managed by ScenesManager.                                    |
|   One subfolder per scene.                                     |
|   Each subfolder holds the Manim .py code file for that scene. |
|   This is where the animation instructions live.               |
|                                                                |
|   assets/                                                      |
|   ─────────────────────────────────────────────────────────── |
|   Extra files for your animations: images, custom fonts,       |
|   SVG diagrams, data files. Manim looks here when you say      |
|   "show this image" in your scene code.                        |
|                                                                |
|   output/                                                      |
|   ─────────────────────────────────────────────────────────── |
|   The finished rendered clips. After "render all", each        |
|   scene's high-quality .mp4 clip appears here.                 |
|                                                                |
|   previews/                                                    |
|   ─────────────────────────────────────────────────────────── |
|   Managed by PreviewManager.                                   |
|   When you run "preview scene N", a fast low-quality draft     |
|   clip appears here. Use this to check your work quickly       |
|   without waiting for a full render.                           |
|                                                                |
|   cache/                                                       |
|   ─────────────────────────────────────────────────────────── |
|   Managed by CacheManager.                                     |
|   Stores the SHA-256 fingerprint of each scene's code file.    |
|   This is how SuperManim knows what changed between runs.      |
|   If the fingerprint matches: skip the render.                 |
|   If the fingerprint differs: run the render.                  |
|                                                                |
|   temp/                                                        |
|   ─────────────────────────────────────────────────────────── |
|   Scratch space. Files created here during processing are      |
|   deleted automatically when no longer needed.                 |
|   You never need to look in here.                              |
|                                                                |
|   exports/                                                     |
|   ─────────────────────────────────────────────────────────── |
|   Managed by ExportManager.                                    |
|   The final assembled video appears here after "export".       |
|   This is the file you share with the world.                   |
|                                                                |
+================================================================+
```

---


**What is inside project_data.db:**

```
+================================================================+
|                 INSIDE project_data.db                         |
+================================================================+
|                                                                |
|   TABLE: project_settings                                      |
|   ─────────────────────────────────────────────────────────── |
|   project_name, project_path, project_created_at  <- locked   |
|   export_format, export_quality, render_fps        <- editable |
|                                                                |
|   TABLE: scenes                                                |
|   ─────────────────────────────────────────────────────────── |
|   scene_id, scene_name, scene_index,                           |
|   scene_duration, scene_start_time, scene_end_time,            |
|   code_file_path, scene_status, render_output_path,            |
|   audio_clip_path, synced_with_audio                           |
|                                                                |
|   TABLE: audio_files                                           |
|   ─────────────────────────────────────────────────────────── |
|   audio_file_id, stored_path, audio_format,                    |
|   total_duration, sample_rate, channels, is_split              |
|                                                                |
|   TABLE: audio_clips                                           |
|   ─────────────────────────────────────────────────────────── |
|   clip_id, scene_id, clip_path, clip_duration,                 |
|   start_in_original, end_in_original, is_synced                |
|                                                                |
|   TABLE: cache_records                                         |
|   ─────────────────────────────────────────────────────────── |
|   scene_id, code_hash, video_path, cached_at                   |
|                                                                |
+================================================================+
```

---

**The Critical Rule: Two Databases, Completely Separate**

```
+================================================================+
|         TWO DATABASE FILES — NEVER CONFUSE THEM                |
+================================================================+
|                                                                |
|   session.db                                                   |
|   ─────────────────────────────────────────────────────────── |
|   WHERE:   OS app data folder (~/.supermanim/)                 |
|   OWNS:    AppStateService ONLY. Nothing else reads or         |
|            writes this file. Ever.                             |
|   STORES:  Which project was last open.                        |
|            The list of recent projects.                        |
|   LIVES:   As long as SuperManim is installed.                 |
|            Not inside any project folder.                      |
|                                                                |
|   project_data.db                                              |
|   ─────────────────────────────────────────────────────────── |
|   WHERE:   /projects/MyAnimation/project_data.db               |
|            One file PER PROJECT, inside its folder.            |
|   OWNS:    All repository adapters (scene, audio, cache, etc.) |
|   STORES:  Everything about that ONE project.                  |
|   LIVES:   As long as the project folder exists.               |
|                                                                |
+================================================================+
```

---
---

# Section 0.5 — An Overview of the Architecture Design of SuperManim

Before writing any code, it is important to understand WHY SuperManim is
built the way it is. This section explains the two architectural patterns
that shape the entire codebase.

---

## Subsection 0.5.1 — The Hexagonal Architecture

### Subsubsection 0.5.1.1 What Is Hexagonal Architecture?

Hexagonal Architecture is a way of designing software.It was invented by a programmer named Alistair Cockburn.
The other name for it is **"Ports and Adapters Architecture"**, which is actually a much better description
of what it does.The big idea is very simple:

 **The core logic of your application should not know or care about the outside world.**

What is "the outside world"? Everything that is not your core business logic:
- The terminal (how the user types commands)
- The database (where data is saved)
- The file system (where files are read/written)
- External tools (like Manim or FFmpeg)
- The internet

The core logic should only contain the **rules and decisions** of your application.
Not the mechanics of storage, not the details of user input, not the specifics of third-party tools.

Why does this matter? Because the outside world changes all the time. You might:
- Switch from SQLite to PostgreSQL
- Switch from a CLI interface to a GUI
- Replace FFmpeg with a different video tool
- Switch from reading files locally to reading from cloud storage

If your core logic is tightly woven together with these external details,every single change like
this requires you to dig through and rewrite your core logic too.That is dangerous and slow.

With Hexagonal Architecture, you change only the "adapter" for that external thing  the thin translation layer
and the core logic stays completely untouched.

Hexagonal Architecture means your core logic only speaks to clean, simple interfaces called Ports,
and the messy details of real databases, real files, and real external tools are hidden inside Adapters
 so you can swap, test, or extend any part without touching the core logic at all.**

Hexagonal Architecture is a way of organizing code so that the **core logic**
(the business rules, the real brain of the tool) is completely separated from
**everything external** (databases, terminal input, Manim, FFmpeg, file system).

The name "Hexagonal" comes from drawing the core as a hexagon with connections
going in and out through its sides.

The key idea is this:

```
+================================================================+
|               THE KEY IDEA OF HEXAGONAL ARCHITECTURE           |
+================================================================+
|                                                                |
|   The Core contains ONLY rules and logic.                      |
|                                                                |
|   The Core does NOT know:                                      |
|     - That SQLite exists                                       |
|     - That FFmpeg exists                                       |
|     - That Manim exists                                        |
|     - That there is a terminal at all                          |
|     - What operating system it runs on                         |
|                                                                |
|   The Core ONLY speaks through Ports.                          |
|                                                                |
|   Ports are abstract contracts: "I need someone who can        |
|   save a scene. I don't care how."                             |
|                                                                |
|   Adapters are the real implementations: "I will save the      |
|   scene using SQLite." or "I will save it in a JSON file."     |
|                                                                |
+================================================================+
```

---



### Subsubsection 0.5.1.2 Why SuperManim Uses Hexagonal Architecture

#### The Problem: SuperManim Talks to a LOT of Different Things
SuperManim is not a simple program.It does not just calculate a number and print it.
It has to talk to **six completely different external things** just to do its job:

```
+----------------------------------------------------------+
|              WHO DOES SUPERMANIM TALK TO?                |
+----------------------------------------------------------+
|                                                          |
|   1. The Terminal (CLI)                                  |
|      The user types commands here.                       |
|      SuperManim has to read what they typed.             |
|                                                          |
|   2. SQLite Database                                     |
|      A file on disk that stores all project settings.    |
|      Scene durations, render history, audio paths, etc.  |
|                                                          |
|   3. The File System                                     |
|      The folders and files on the hard drive.            |
|      Reading .py code files, audio files, video clips.   |
|                                                          |
|   4. Manim or any other animation tool (as a subprocess) |
|      An external Python animation tool.                  |
|      SuperManim calls it to actually render scenes.      |
|                                                          |
|   5. FFmpeg (as a subprocess)                            |
|      An external video/audio tool.                       |
|      Slices audio clips, assembles the final video.      |
|                                                          |
|   6. PyDub or Librosa                                    |
|      Audio analysis libraries.                           |
|      Used to detect silence in audio files.              |
|                                                          |
+----------------------------------------------------------+
```

Each of these six things speaks a **different language**:
Six different things. Six different APIs. Six different ways of talking.

```         
`+----------------+---------------------------------------------------------------+
| External Thing |                      How You Talk to It                       |
+----------------+---------------------------------------------------------------+
| Terminal (CLI) |  import cmd                                                   |
|                |  class MyShell(cmd.Cmd): do_command(self, arg)                |
|                |  (Using 'cmd' library to build an interactive shell loop)     |
+----------------+---------------------------------------------------------------+
| GUI Interface  |  import tkinter as tk                                         |
|                |  root = tk.Tk(); button = tk.Button(text="Click")            |
|                |  (Using widgets, event loops, and callbacks)                  |
+----------------+---------------------------------------------------------------+
| SQLite         |  sqlite3.connect(), SQL queries: "SELECT * FROM ..."          |
+----------------+---------------------------------------------------------------+
| File System    |  os.path.exists(), open(), shutil.copy()                      |
+----------------+---------------------------------------------------------------+
| Manim          |  config.quality = "high"; scene.render()                      |
|                |  (Using Manim library objects)                                |
+----------------+---------------------------------------------------------------+
| FFmpeg         |  ffmpeg.input('in.mp4').output('out.mp4').run()               |
|                |  (Using ffmpeg-python fluent chains)                          |
+----------------+---------------------------------------------------------------+
| PyDub          |  AudioSegment.from_mp3("file.mp3").duration_seconds           |
+----------------+---------------------------------------------------------------+

```

####  The Disasters: What Happens When You Mix Everything Together

Imagine you are writing the `render_scene()` function.Your job is simple: **render one scene**.
But to do that, you need to:
- Read scene info from the **database**
- Find the code file on the **file system**
- Check if the file exists (also **file system**)
- Call **Manim** to do the actual rendering
- Print results to the **terminal**
- Update the **database** to say the render is done

If you just write all of this in one function without thinking about architecture, it looks like this:
 
```python
# THE BAD VERSION — everything mixed together

def render_scene(scene_id):

    # ---- DATABASE CODE ----
    conn = sqlite3.connect("project_data.db")
    cursor = conn.execute("SELECT * FROM scenes WHERE id=?", (scene_id,))
    scene = cursor.fetchone()

    # ---- FILE SYSTEM CODE ----
    code_path = f"scenes/scene_{scene_id:02d}/scene.py"
    if not os.path.exists(code_path):

        # ---- TERMINAL CODE ----
        print(f"Error: file not found")
        return

    # ---- MANIM CODE ----
    result = subprocess.run(["manim", code_path, "--quality", "h"])
    if result.returncode != 0:

        # ---- TERMINAL CODE ----
        print("Manim failed")
        return

    # ---- DATABASE CODE ----
    conn.execute("UPDATE scenes SET rendered=1 WHERE id=?", (scene_id,))
    conn.commit()
```

This code **works**. But it is a trap.

Let's draw what this function looks like from a dependency perspective:
```
+--------------------------------------------------------------------+
|                                                                    |
|                     render_scene()                                 |
|                    "The One Big Function"                          |
|                                                                    |
|   This single function is DIRECTLY WIRED to:                       |
|                                                                    |
|        +----------+                                                |
|        |  SQLite  |  <-- sqlite3.connect() called directly here    |
|        +----------+                                                |
|                                                                    |
|        +---------+                                                 |
|        |   OS /  |  <-- os.path.exists() called directly here     |
|        |  Files  |                                                 |
|        +---------+                                                 |
|                                                                    |
|        +----------+                                                |
|        | Terminal |  <-- print() called directly here             |
|        +----------+                                                |
|                                                                    |
|        +-------+                                                   |
|        | Manim |  <-- config.quality, module.render() called here |
|        +-------+                                                   |
|                                                                    |
+--------------------------------------------------------------------+


This is called "tight coupling."
The function is GLUED to all four external things at the same time.
```

Now the problems start.The Three Disasters That Come From Tight Coupling:

**Disaster #1 — You Want to Add a GUI**
Right now, your tool is a terminal tool.You type commands, it prints output.
Later, you decide: "I want to make a nice graphical window for this."
Instead of typing `render scene 3` in the terminal, you click a button in a window.

You start building the GUI.Then you realize the problem:

```
+------------------------------------------------------------+
|                      THE GUI PROBLEM                       |
+------------------------------------------------------------+
|                                                            |
|  Your render_scene() function has print() calls in it.    |
|                                                            |
|  print("Error: file not found")                           |
|  print("Manim failed")                                    |
|  print("Render complete")                                  |
|                                                            |
|  print() sends text to the terminal.                       |
|  A GUI does not HAVE a terminal.                           |
|  The GUI needs to show a popup window, or update a label.  |
|                                                            |
|  But where are these print() calls?                        |
|  They are INSIDE render_scene().                           |
|  Also inside load_project(). Also inside add_scene().      |
|  Also inside set_audio(). Also inside export_project().    |
|                                                            |
|  They are SCATTERED EVERYWHERE.                            |
|                                                            |
|  To add a GUI you have to:                                 |
|  1. Find every single print() in the entire codebase.      |
|  2. Replace each one with the GUI-equivalent code.         |
|  3. Hope you didn't miss any.                              |
|  4. Test everything again from scratch.                    |
|                                                            |
|  This is painful, risky, and takes a very long time.       |
|                                                            |
+------------------------------------------------------------+
```

**Disaster #2 — You Want to Change the Database**

You started with SQLite because it is simple.Later you need something more powerful — maybe PostgreSQL,
or maybe you want to store everything in a simple JSON file instead.You decide to switch.

You look at your code. Every function that touches the database has raw SQL inside it:

```
render_scene()         --> "SELECT * FROM scenes WHERE id=?"
load_project()         --> "SELECT * FROM projects WHERE name=?"
add_scene()            --> "INSERT INTO scenes (id, duration) VALUES (?, ?)"
update_scene()         --> "UPDATE scenes SET duration=? WHERE id=?"
delete_scene()         --> "DELETE FROM scenes WHERE id=?"
save_render_result()   --> "UPDATE scenes SET rendered=1, hash=? WHERE id=?"
get_all_scenes()       --> "SELECT * FROM scenes ORDER BY id"
...
```

These SQL statements are written in the SQLite dialect.PostgreSQL uses a slightly different syntax.
A JSON file uses no SQL at all.You have to find every single SQL statement in every single function
and rewrite it.You can easily miss one. When you miss one, you get a bug that is very hard to find.

```
+------------------------------------------------------------+
|                  THE DATABASE PROBLEM                      |
+------------------------------------------------------------+
|                                                            |
|  SQLite SQL is sprinkled throughout the entire codebase.   |
|                                                            |
|  render_scene()    --> SQL here                            |
|  load_project()    --> SQL here                            |
|  add_scene()       --> SQL here                            |
|  update_scene()    --> SQL here                            |
|  save_result()     --> SQL here                            |
|  ...               --> SQL here                            |
|                                                            |
|  To switch databases, you must hunt through ALL of these   |
|  and rewrite them. One missed statement = one hidden bug.  |
|                                                            |
+------------------------------------------------------------+
```

**Disaster #3 — You Cannot Test Your Logic**
You want to write a test that checks this:
"If a scene's code file has not changed, `render_scene()` should skip the render
and not call Manim."Simple rule. Easy to test, right? Wrong. Because `render_scene()`
calls `subprocess.run(["manim", ...])` directly.

When you run your test, it will **actually launch Manim**. Manim takes minutes to run.
Your test suite now takes hours to complete. And if Manim is not installed on the machine
running the tests, the tests crash entirely.

You want to "fake" Manim for the test — to replace it with a simple fake that just says
"yes I rendered it" without actually doing anything. But you cannot. Manim is called with
a hardcoded `subprocess.run()` inside the function.You cannot replace it without changing
the function itself.

```
+------------------------------------------------------------+
|                   THE TESTING PROBLEM                      |
+------------------------------------------------------------+
|                                                            |
|  You want to test the LOGIC:                               |
|  "If hash unchanged, skip the render."                     |
|                                                            |
|  But to run render_scene(), it will also:                  |
|  - Connect to a REAL SQLite database                       |
|  - Check REAL files on disk                                |
|  - Launch the REAL Manim program                           |
|  - Print to the REAL terminal                              |
|                                                            |
|  You cannot test just the logic.                           |
|  Every test drags in the entire real world.                |
|  Tests are slow, fragile, and hard to run.                 |
|                                                            |
+------------------------------------------------------------+
```

---

####  The Root Cause: Why All Three Disasters Happen
All three disasters come from the same root cause.Look at this diagram:

```
TIGHT COUPLING — The Root Cause
================================

                       +-------------+
                       |  YOUR LOGIC |
                       |  "The Core" |
                       +------+------+
                              |
         +--------------------+--------------------+
         |            |            |               |
         v            v            v               v
    +--------+   +--------+   +--------+   +----------+
    | SQLite |   |  Files |   |Terminal|   |  Manim   |
    +--------+   +--------+   +--------+   +----------+

Your logic is DIRECTLY WIRED to all four things.If any of those four things changes,
your logic HAS to change too.They are all entangled. Like headphone wires in a pocket.
You pull on one, you move all the others.
```

The problem is not that you talked to SQLite.The problem is **how** you talked to it directly,
by name, with its specific API baked into your logic.The same goes for Manim. The same goes for `print()`.
The same goes for `os.path`.

---

#### — The Fix: Hexagonal Architecture
Hexagonal Architecture says:

> "Your core logic should NEVER call external things directly.
> It should only call a **simple, abstract interface** — a Port.
> The actual external thing is hidden behind an Adapter, which the Core never sees."

Let's draw what this looks like:

```
HEXAGONAL ARCHITECTURE — The Fix
==================================

                       +-------------+
                       |  YOUR LOGIC |
                       |  "The Core" |
                       +------+------+
                              |
         +--------------------+--------------------+
         |            |            |               |
         v            v            v               v
    +---------+  +---------+  +---------+  +---------+
    |SceneRepo|  |FileStore|  |Notifier |  |Renderer |
    |  PORT   |  |  PORT   |  |  PORT   |  |  PORT   |
    +---------+  +---------+  +---------+  +---------+
         |            |            |               |
         v            v            v               v
    +--------+   +--------+   +--------+   +----------+
    | SQLite |   |  Files |   |Terminal|   |  Manim   |
    | ADAPTER|   | ADAPTER|   | ADAPTER|   | ADAPTER  |
    +--------+   +--------+   +--------+   +----------+

The Core talks to Ports.
The Ports are simple, clean interfaces.
The Adapters do the messy real work.
The Core never knows what is behind the Port.
```

Now let's see what `render_scene()` looks like when rewritten with this approach:

```python
# THE GOOD VERSION — Core logic only, no external details

def render_scene(scene_id: int):

    # Load scene via PORT — no SQLite here
    scene = self.scene_repo.load_scene(scene_id)

    # Check file via PORT — no os.path here
    if not self.file_storage.file_exists(scene.code_path):
        self.notifier.send_error("File not found")    # no print() here
        return

    # Run render via PORT — no subprocess here
    result = self.renderer.render(scene.code_path, scene.duration)

    if result.failed:
        self.notifier.send_error("Render failed")     # no print() here
        return

    # Save result via PORT — no SQL here
    self.scene_repo.mark_as_rendered(scene_id)
```

Count the external technologies in this version: **zero**.
No `sqlite3`. No `os.path`. No `print`. No `subprocess`. No `manim`. No `ffmpeg`.

The function only speaks to Ports. Ports are simple Python interfaces.
The actual technology is hidden inside the Adapters, somewhere else, completely separate.

---

####  How Each Disaster Is Now Fixed

**Disaster #1 Fixed — Adding a GUI**

```
BEFORE (tight coupling):
  render_scene() --> print("Render failed")
  add_scene()    --> print("Scene added")
  load_project() --> print("Project loaded")
  ... 40 more places with print() ...

  To add GUI: find all 40+ print() calls. Rewrite each one. Risky.


AFTER (hexagonal):
  render_scene() --> self.notifier.send_error("Render failed")
  add_scene()    --> self.notifier.send_info("Scene added")
  load_project() --> self.notifier.send_info("Project loaded")

  The Core only calls self.notifier.To switch from terminal to GUI:

  OLD adapter:                    NEW adapter:
  class CliNotifier:              class GuiNotifier:
    def send_error(self, msg):      def send_error(self, msg):
      print(f"ERROR: {msg}")          show_popup_window(msg, color="red")

  Swap in the new adapter.
  The Core is completely untouched.
  Done.
```

```
+----------------------------------------------------------+
|            SWITCHING THE NOTIFIER ADAPTER                |
+----------------------------------------------------------+
|                                                          |
|              THE CORE                                    |
|              (never changes)                             |
|                   |                                      |
|                   | calls self.notifier.send_error()     |
|                   |                                      |
|                   v                                      |
|            NotifierPort                                  |
|            (the interface — never changes)               |
|                   |                                      |
|       +-----------+-----------+                          |
|       |                       |                          |
|       v                       v                          |
|  CliNotifier          GuiNotifier                        |
|  (prints to terminal) (shows popup window)               |
|                                                          |
|  Swap from left to right. Core never changes.            |
|                                                          |
+----------------------------------------------------------+
```

**Disaster #2 Fixed — Changing the Database**

```
BEFORE (tight coupling):
  SQL sprinkled everywhere in every function.
  Switch database = find and rewrite every SQL statement.


AFTER (hexagonal):
  The Core calls: self.scene_repo.load_scene(scene_id)
  The Core calls: self.scene_repo.mark_as_rendered(scene_id)
  The Core NEVER writes SQL.

  ALL the SQL is in ONE place: the SQLiteSceneRepository adapter.
  To switch to a different database:

  OLD adapter:                    NEW adapter:
  class SqliteSceneRepository:    class JsonSceneRepository:
    def load_scene(self, id):       def load_scene(self, id):
      conn = sqlite3.connect(...)     with open("scenes.json") as f:
      row = conn.execute(...)           data = json.load(f)
      return Scene(...)                 return Scene(...)

  Write the new adapter.
  The Core is completely untouched.
  Done.
```

```
+----------------------------------------------------------+
|          SWITCHING THE SCENE REPOSITORY ADAPTER          |
+----------------------------------------------------------+
|                                                          |
|              THE CORE                                    |
|              (never changes)                             |
|                   |                                      |
|                   | calls self.scene_repo.load_scene()   |
|                   |                                      |
|                   v                                      |
|          SceneRepositoryPort                             |
|          (the interface — never changes)                 |
|                   |                                      |
|       +-----------+-----------+                          |
|       |                       |                          |
|       v                       v                          |
|  SqliteSceneRepo        JsonSceneRepo                    |
|  (reads from SQLite)    (reads from JSON file)           |
|                                                          |
|  Swap from left to right. Core never changes.            |
|                                                          |
+----------------------------------------------------------+
```

**Disaster #3 Fixed — Testing**

```
BEFORE (tight coupling):
  To test the "skip if hash unchanged" logic,
  you had to actually run Manim (slow, external, fragile).


AFTER (hexagonal):
  The Core calls: result = self.renderer.render(code_path, duration)
  The renderer is a Port. In tests, you plug in a FAKE adapter:

  class FakeRenderer(RenderRunnerPort):   # a fake for testing
      def render(self, code_path, duration):
          return RenderResult(succeeded=True, elapsed_time=0.001)

  Now your test runs in milliseconds.
  No Manim. No files. No database.
  Just pure logic, tested cleanly.
```

```
+----------------------------------------------------------+
|             TESTING WITH A FAKE ADAPTER                  |
+----------------------------------------------------------+
|                                                          |
|              THE CORE                                    |
|              (same code in production and in tests)      |
|                   |                                      |
|                   | calls self.renderer.render()         |
|                   |                                      |
|                   v                                      |
|          RenderRunnerPort                                |
|          (the interface — same in both cases)            |
|                   |                                      |
|       +-----------+-----------+                          |
|       |                       |                          |
|       v                       v                          |
|  ManimRenderer          FakeRenderer                     |
|  (used in production)   (used in tests)                  |
|  calls Manim subprocess returns instantly, no real work  |
|  takes minutes          takes milliseconds               |
|                                                          |
|  In tests: plug in the fake. In production: plug in real.|
|  The Core never knows the difference.                    |
|                                                          |
+----------------------------------------------------------+
```

---

**The Complete Before and After Picture**

```
BEFORE — Tight Coupling (The Nightmare)
=========================================

  render_scene()
       |
       +-----> sqlite3.connect(...)         <-- SQLite baked in
       |
       +-----> os.path.exists(...)          <-- File system baked in
       |
       +-----> print("Error...")            <-- Terminal baked in
       |
       +-----> subprocess.run(["manim"...]) <-- Manim baked in
       |
       +-----> conn.execute("UPDATE ...")   <-- SQLite again

  Change any one external thing --> touch this function.
  Add new external thing --> touch this function.
  Write a test --> real Manim launches. Real DB accessed.

AFTER — Hexagonal Architecture (The Fix)
==========================================

  render_scene()
       |
       +-----> self.scene_repo.load_scene()     <-- Port (clean)
       |
       +-----> self.file_storage.file_exists()  <-- Port (clean)
       |
       +-----> self.notifier.send_error()       <-- Port (clean)
       |
       +-----> self.renderer.render()           <-- Port (clean)
       |
       +-----> self.scene_repo.mark_rendered()  <-- Port (clean)

  Behind each Port, an Adapter does the real work:

  self.scene_repo  --> SqliteSceneRepository  (or JsonSceneRepository, or any other)
  self.file_storage --> LocalFileStorage      (or CloudFileStorage, or FakeStorage)
  self.notifier    --> CliNotifier            (or GuiNotifier, or FakeNotifier)
  self.renderer    --> ManimRenderer          (or FakeRenderer, for testing)

  Change external thing --> only change the one adapter.
  Swap external thing   --> only write a new adapter.
  Write a test          --> use fake adapters. Instant. Clean.
```

### Subsubsection 0.5.1.3 The  Components of Hexagonal Architecture: Core, Ports, and Adapters

#### Component 1 — The Core

The Core is the brain of SuperManim. It lives in the `core/` folder.
It contains all the business rules and all the step-by-step workflows.

```
+================================================================+
|                        THE CORE                                |
+================================================================+
|                                                                |
|   What the Core IS:                                            |
|   - All business rules ("scene must have a duration to render")|
|   - All workflows ("here are the 9 steps to render a scene")  |
|   - All validation logic ("is this duration valid?")           |
|   - All calculations ("what is the timeline start time?")      |
|                                                                |
|   What the Core is NOT:                                        |
|   - Not SQLite code                                            |
|   - Not FFmpeg commands                                        |
|   - Not Manim calls                                            |
|   - Not file system operations                                 |
|   - Not print() statements                                     |
|                                                                |
|   The Core NEVER changes when you:                             |
|   - Switch from SQLite to a JSON file for storage              |
|   - Switch from FFmpeg to another video tool                   |
|   - Switch from a terminal UI to a graphical UI                |
|                                                                |
+================================================================+
```

The Core contains these managers and services:

```
INSIDE THE CORE:

    ProjectService          Handles creating, opening, closing projects
    AudioService            Handles loading and splitting audio
    ScenesService           Handles adding, editing, deleting scenes
    RenderService           Decides WHAT to render and in what order
    TimelineEngine          Calculates start/end times for all scenes
    CacheService            Stores and compares code fingerprints
    ExportService           Assembles the final video
    ValidationService       Checks if inputs are valid
    HashService             Computes SHA-256 fingerprints
```
These are the general services.
---

#### Component 2 — Ports (The Contracts)

A Port is a Python abstract interface. It defines **what** needs to happen,
not **how** it happens.

Think of a Port like an electrical socket on a wall. The socket does not care
if you plug in a lamp, a phone charger, or a fan. It just provides
a standard connection point.

```
+=========================================================+
|              HOW PORTS AND ADAPTERS WORK                |
+=========================================================+
|                                                         |
|   THE CORE (the smart logic)                            |
|        |                                                |
|        |  calls:  scene_repo.save_scene(my_scene)       |
|        |          "I need someone to save this scene.   |
|        |           I don't care how."                   |
|        v                                                |
|   [ PORT ]  <--- SceneRepositoryPort                    |
|   "I am the socket. I promise save_scene() exists."     |
|        |                                                |
|        v                                                |
|   [ ADAPTER ]  <--- SqliteSceneRepository               |
|   "I am the plug. I actually do it using SQLite."        |
|        |                                                |
|        v                                                |
|   [ EXTERNAL TECHNOLOGY ]  <--- SQLite database file    |
|   "I am the real storage engine on your disk."          |
|                                                         |
+=========================================================+
```
**The five groups of Ports in SuperManim:**

```
+================================================================+
|                THE FIVE PORT GROUPS (UPDATED)                  |
+================================================================+
|                                                                |
|   GROUP 1 — Repository Ports (long-term memory)               |
|   ─────────────────────────────────────────────────────────── |
|   SessionRepositoryPort      Save/load global session state    |
|                              (last project, recent list).      |
|   ProjectSettingsRepositoryPort  Read/write active project    |
|                              settings from project_data.db.    |
|   ProjectRepositoryPort      Create/Delete project structure   |
|                              and manage project metadata.      |
|   SceneRepositoryPort        Save and load scene data.         |
|   AudioRepositoryPort        Save and load audio file records. |
|   CacheRepositoryPort        Store render fingerprints.        |
|   RenderHistoryRepositoryPort  Log every render event.         |
|                                                                |
|   GROUP 2 — Media Processing Ports (heavy workers)            |
|   ─────────────────────────────────────────────────────────── |
|   RenderRunnerPort         Actually call Manim to render.      |
|   AudioProcessorPort       Cut and convert audio with FFmpeg.  |
|   VideoAssemblerPort       Stitch clips into final video.      |
|   AudioAnalyzerPort        Detect silence boundaries.          |
|   PreviewGeneratorPort     Generate fast low-quality previews. |
|                                                                |
|   GROUP 3 — Infrastructure Ports (system and files)           |
|   ─────────────────────────────────────────────────────────── |
|   FileStoragePort          Create/delete/copy files/folders.   |
|   HashComputerPort         Compute SHA-256 fingerprints.       |
|   TempFileManagerPort      Manage temporary files.             |
|   AssetManagerPort         Manage images/fonts/SVG files.      |
|                                                                |
|   GROUP 4 — Driving Ports (inbound — user commands)           |
|   ─────────────────────────────────────────────────────────── |
|   ProjectCommandPort       Handle project lifecycle commands   |
|                            (new, open, close, list).           |
|   SceneCommandPort         Handle scene commands.              |
|   RenderCommandPort        Handle render commands.             |
|   AudioCommandPort         Handle audio commands.              |
|   ExportCommandPort        Handle export commands.             |
|                                                                |
|   GROUP 5 — Notification Ports (outbound — user feedback)     |
|   ─────────────────────────────────────────────────────────── |
|   NotificationPort         Send messages to the user.          |
|   ProgressReporterPort     Show progress bars.                 |
|   LoggerPort               Write technical log records.        |
|                                                                |
+================================================================+
```

---

#### Component 3 — Adapters (The Real Work)
##### Definition of Adapters:
In SuperManim's architecture, an **Adapter** is a translator. The Core of the
application speaks one language — Python objects, domain concepts, and abstract
interfaces called Ports. The outside world speaks a completely different language —
terminal commands, SQL queries, shell subprocesses, and file paths.

An Adapter sits in between and translates from one language to the other.
Without adapters, the Core would have to know about SQLite, Manim, FFmpeg,
and the terminal all at the same time. That would make it messy, hard to test,
and impossible to change without breaking everything.

An Adapter is the concrete Python class that **implements** a Port.
It knows about the specific external technology and does the actual work.

```
+================================================================+
|              ADAPTERS — WHO DOES THE REAL WORK                 |
+================================================================+
|                                                                |
|   Port                    Adapter                  Technology  |
|   ─────────────────────────────────────────────────────────── |
|   SceneRepositoryPort  -> SqliteSceneRepository     SQLite      |
|   AudioRepositoryPort  -> SqliteAudioRepository     SQLite      |
|   CacheRepositoryPort  -> SqliteCacheRepository     SQLite      |
|   RenderRunnerPort     -> ManimSubprocessRenderer   Manim       |
|   AudioProcessorPort   -> FfmpegAudioProcessor      FFmpeg      |
|   VideoAssemblerPort   -> FfmpegVideoAssembler      FFmpeg      |
|   AudioAnalyzerPort    -> LibrosaAudioAnalyzer      Librosa     |
|   FileStoragePort      -> LocalFileStorage          os/shutil   |
|   HashComputerPort     -> Sha256HashComputer        hashlib     |
|   NotificationPort     -> CliNotifier               print()     |
|   ProjectCommandPort   -> CliProjectCommandAdapter  Terminal    |
|                                                                |
|   ALTERNATIVE ADAPTERS (same port, different technology):      |
|   SceneRepositoryPort  -> JsonSceneRepository       JSON file   |
|   SceneRepositoryPort  -> InMemorySceneRepository   dict (tests)|
|   RenderRunnerPort     -> FakeRenderer              nothing     |
|   FileStoragePort      -> CloudStorageAdapter       Google Drive|
|                                                                |
+================================================================+
```

The power of this: if you swap `SqliteSceneRepository` for
`JsonSceneRepository`, the Core does not change. Not one line.

##### Types of Adapters:
There are **two types** of adapters, and they are defined by a single question:
**Who calls who?**

###### TYPE 1 — Driving Adapters (Primary Adapters)

**The Definition of driving adapters**

A Driving Adapter is anything that **receives input from the outside world**
and uses it to **call the Core**. It drives the application forward.

**Where It Lives**

Driving Adapters live in **Layer 1 — the CLI Shell** of SuperManim.
This is the outermost layer, the one the user directly interacts with.

 **The Direction of the Call**

```
[ OUTSIDE WORLD ]
       |
       v
+--------------------+
|  Driving Adapter   |  -- "I received something. I will now call the Core."
+--------------------+
       |
       | calls a Driving Port
       v
+--------------------+
|       CORE         |
+--------------------+
```

The Adapter always calls the Core. The Core never reaches out and calls the
Driving Adapter. Think of it like a normal Python function call — the Adapter
calls a function, the function does its work, and the function *returns* a value.
The Adapter is the one waiting for that return. The Core is not calling anyone.
It is just finishing its job and handing the result back.

**What It Actually Does — Step by Step**

Each step below names exactly WHO is acting and WHAT they are doing.

```
+================================================================+
|           WHAT A DRIVING ADAPTER DOES — WHO DOES WHAT          |
+================================================================+
|                                                                |
|  Step 1.  WHO: The USER (or a test script)                     |
|           WHAT: Types a command into the terminal.             |
|           Example: supermanim render scene 1                   |
|           The Adapter is just sitting there waiting.           |
|           Nothing inside SuperManim has moved yet.             |
|                                                                |
|  Step 2.  WHO: command_parser.py (part of the CLI Adapter)     |
|           WHAT: Reads the raw text string and understands it.  |
|           Input:  the raw string "render scene 1"              |
|           Output: a structured Python object                   |
|                   RenderCommand(scene_number=1)                |
|           The Core still has not been touched yet.             |
|                                                                |
|  Step 3.  WHO: shell.py (part of the CLI Adapter)              |
|           WHAT: Takes the structured command object and        |
|                 decides which Core Port to call.               |
|           It calls: RenderCommandPort.render_scene(1)          |
|           This is the moment the Adapter knocks on the         |
|           Core's door. The Core wakes up now.                  |
|                                                                |
|  Step 4.  WHO: The CORE (RenderOrchestrationService)           |
|           WHAT: Does all the real thinking and work.           |
|           - Checks if scene 1's code file has changed          |
|           - Decides if rendering is needed                     |
|           - Calls Driven Adapters to render and save           |
|           The CLI Adapter is now just waiting.                 |
|           It made the call. It is not doing anything else.     |
|                                                                |
|  Step 5.  WHO: The CORE returns. The CLI Adapter receives.     |
|           WHAT: The Core finishes its work and the function    |
|                 call that shell.py made in Step 3 now          |
|                 returns a value — like any Python function.    |
|           IMPORTANT: The Core did NOT call the Adapter back.   |
|           The Core just RETURNED from the function.            |
|           shell.py was waiting at Step 3 for the return.       |
|           Now it has it: RenderResult(success=True, time=5.2s) |
|                                                                |
|  Step 6.  WHO: cli_notifier.py (part of the CLI Adapter)       |
|           WHAT: Takes the RenderResult object and translates   |
|                 it into a human-readable message.              |
|           Output: prints to terminal:                          |
|                   "Scene 1 rendered. (5.2 sec)"                |
|           The user sees this. The round-trip is complete.      |
|                                                                |
+================================================================+
```

A simple way to think about Steps 3–5:

```
  shell.py says:
  result = RenderCommandPort.render_scene(1)
              ^                               ^
              |  Core runs here               |
              |  (Step 4)                     |
              |                               |
  Step 3:     |                   Step 5:     |
  shell.py    |                   shell.py    |
  makes the   |                   receives    |
  call        |                   the return  |
              +-------------------------------+
              This is ONE function call.
              The Core did not call anyone.
              It just returned a value.
```

### The Two Driving Adapters in SuperManim

**1. The CLI Adapter (`shell.py` + `command_parser.py` + `cli_notifier.py`)**

This is the main Driving Adapter. It is the interactive terminal shell that
the user types commands into. It has three responsibilities:

- `command_parser.py` reads the raw text the user typed and figures out what
  it means. It converts `"render scene 1"` into a structured command object.
- `shell.py` takes that structured command and calls the correct Service
  through a Driving Port.
- `cli_notifier.py` receives the result from the Core and prints a clean,
  readable message back to the user.

```
[ USER TYPES: supermanim render scene 1 ]
              |
              v
+------------------------------------------+
|  command_parser.py                        |
|  "render scene 1" --> RenderCommand(1)   |
+------------------------------------------+
              |
              v
+------------------------------------------+
|  shell.py                                 |
|  calls RenderCommandPort.render_scene(1) |
+------------------------------------------+
              |
              v
         [ CORE ]
              |
              v
+------------------------------------------+
|  cli_notifier.py                          |
|  prints: "Scene 1 rendered. (5.2 sec)"   |
+------------------------------------------+
              |
              v
[ USER SEES RESULT IN THE TERMINAL ]
```

**2. The Test Adapter (automated test scripts)**

This is the invisible Driving Adapter. When developers write automated tests
for SuperManim, they do not type commands into a terminal. Instead, a test
script calls the exact same Driving Ports that the CLI calls.

The Core does not know the difference. It receives a method call from a Port
and does its job. Whether that call came from a human typing or from a test
script running automatically does not matter at all.

This means the entire Core logic of SuperManim can be tested without opening
a terminal, without a real database, and without a real Manim installation.

```
[ AUTOMATED TEST SCRIPT ]
         |
         | calls the same Port the CLI would call
         v
+-------------------------------+
|  Test Adapter                 |
|  test_render_scene.py         |
|  calls RenderCommandPort      |
|        .render_scene(1)       |
+-------------------------------+
         |
         v
+-------------------------------+
|  CORE (exact same logic)      |
+-------------------------------+
```

**The Rules That Define Every Driving Adapter**

- The Adapter calls the Core. Never the other way around.
- The Adapter depends on the Core (specifically on the Driving Ports).
  The Core does not know the Adapter exists.
- The Adapter translates external input into internal method calls.
- You can replace the CLI Adapter with a GUI Adapter and the Core never changes.

---

---

###### TYPE 2 — Driven Adapters (Secondary Adapters)

### The One-Line Definition

A Driven Adapter is anything that **the Core calls** when it needs to interact
with the outside world. It is driven by the Core to do real work.

### Where It Lives

Driven Adapters live in **Layer 4 — the Adapters layer** of SuperManim.
This is the outermost layer on the other side, the one that touches real
tools like SQLite, Manim, FFmpeg, and the file system.

### The Direction of the Call

```
+--------------------+
|       CORE         |  -- "I need to save this. I will call the Port."
+--------------------+
       |
       | calls a Driven Port
       v
+--------------------+
|  Driven Adapter    |  -- "I received the call. I will do the real work."
+--------------------+
       |
       v
[ OUTSIDE WORLD: SQLite, Manim, FFmpeg, Disk ]
```

The Core always calls the Adapter. The Adapter never pushes anything into the Core.

### What It Actually Does — Step by Step

```
+================================================================+
|           WHAT A DRIVEN ADAPTER DOES                           |
+================================================================+
|                                                                |
|  Step 1.  The Core decides it needs something done.            |
|           Example: "Save Scene 1 to storage."                  |
|                                                                |
|  Step 2.  The Core calls a Driven Port (abstract interface).   |
|           Example: SceneRepositoryPort.save(scene_1)           |
|           The Core does not know who will handle this.         |
|                                                                |
|  Step 3.  The Driven Adapter receives the call.                |
|           Example: SqliteSceneRepository.save(scene_1)         |
|                                                                |
|  Step 4.  The Adapter translates the Python object             |
|           into something the external tool understands.        |
|           Example: builds an SQL INSERT statement.             |
|                                                                |
|  Step 5.  The Adapter calls the real external tool.            |
|           Example: executes the SQL on project_data.db         |
|                                                                |
|  Step 6.  The Adapter returns a clean result to the Core.      |
|           The Core never saw SQL. It just got a result.        |
|                                                                |
+================================================================+
```

### The Four Driven Adapters in SuperManim

---

**1. SqliteSceneRepository**

- **Port it implements:** `SceneRepositoryPort`
- **What it does:** Saves and retrieves Scene objects from the `scenes` table
  inside `project_data.db`.
- **What the Core says:** `SceneRepositoryPort.save(scene)`
- **What the Adapter does:** Converts the Scene object into SQL and writes it
  to the SQLite file on disk.

```
[ CORE calls SceneRepositoryPort.save(scene_1) ]
              |
              v
+------------------------------------------+
|  SqliteSceneRepository                    |
|  Converts scene object --> SQL INSERT     |
|  Executes against project_data.db        |
+------------------------------------------+
              |
              v
[ project_data.db — table: scenes ]
```

---

**2. SqliteCacheRepository**

- **Port it implements:** `CacheRepositoryPort`
- **What it does:** Saves and checks the fingerprint (hash) of scene code files
  in the `cache_records` table inside `project_data.db`.
- **Why it matters:** This is the adapter that makes SuperManim's "skip unchanged
  scenes" feature work. When a scene is rendered, its code file's hash is saved
  here. Next time, before rendering, the Core checks this adapter to see if the
  hash has changed. If it has not changed, the scene is skipped entirely.

```
[ CORE calls CacheRepositoryPort.get_hash(scene_id=1) ]
              |
              v
+------------------------------------------+
|  SqliteCacheRepository                    |
|  Runs: SELECT hash FROM cache_records    |
|        WHERE scene_id = 1                |
|  Returns the stored hash string          |
+------------------------------------------+
              |
              v
[ project_data.db — table: cache_records ]
```

---

**3. ManimSubprocessRenderer**

- **Port it implements:** `RenderRunnerPort`
- **What it does:** Calls the external Manim command-line tool to render
  a scene's Python file into a `.mp4` video file.
- **What the Core says:** `RenderRunnerPort.render(scene_1)`
- **What the Adapter does:** Builds a full shell command, opens a subprocess,
  runs Manim, waits for it to finish, checks the exit code, and returns the
  path of the output file.

```
[ CORE calls RenderRunnerPort.render(scene_1) ]
              |
              v
+------------------------------------------+
|  ManimSubprocessRenderer                  |
|  Builds shell command:                    |
|  manim render scene1.py                  |
|    --resolution 1920x1080                |
|    --output_file scene1.mp4              |
|  Opens subprocess. Waits. Checks result.  |
+------------------------------------------+
              |
              v
[ Manim runs and produces scene1.mp4 ]
```

The Core never touches a subprocess. It never builds a shell command. It never
reads command output. All of that is completely hidden inside this adapter.

---

**4. FfmpegAudioProcessor**

- **Port it implements:** `AudioProcessorPort`
- **What it does:** Calls the external FFmpeg/ffprobe tool to measure audio
  durations, split audio clips, and convert audio formats.
- **What the Core says:** `AudioProcessorPort.get_duration("voice.mp3")`
- **What the Adapter does:** Builds an ffprobe shell command, runs it, parses
  the text output, and returns a clean Python float back to the Core.

```
[ CORE calls AudioProcessorPort.get_duration("voice.mp3") ]
              |
              v
+------------------------------------------+
|  FfmpegAudioProcessor                     |
|  Runs: ffprobe -show_entries             |
|        format=duration voice.mp3         |
|  Parses output: "60.000000"              |
|  Returns: 60.0 (a Python float)          |
+------------------------------------------+
              |
              v
[ FFmpeg reads voice.mp3 from disk ]
```

---

**5. LocalFileStorage**

- **Port it implements:** `FileStoragePort`
- **What it does:** Creates folders, moves files, and checks file existence
  on the operating system's file system.
- **What the Core says:** `FileStoragePort.save_clip(scene_id=1, path=...)`
- **What the Adapter does:** Checks if the output folder exists, creates it
  if needed, and moves the rendered file to its final location.

```
[ CORE calls FileStoragePort.save_clip(scene_id=1, tmp_path) ]
              |
              v
+------------------------------------------+
|  LocalFileStorage                         |
|  Checks: does /output/ folder exist?     |
|  Creates it if not.                      |
|  Moves scene1.mp4 to /output/scene1.mp4  |
|  Returns final saved path.               |
+------------------------------------------+
              |
              v
[ /projects/MyAnimation/output/scene1.mp4 ]
```

**The Rules That Define Every Driven Adapter**

- The Core calls the Adapter. The Adapter never pushes anything into the Core.
- The Adapter implements a Port (an abstract interface) that is defined inside
  the Core. The Core owns the contract. The Adapter just fulfills it.
- The Adapter translates Core domain objects into real external tool calls.
- You can replace any Driven Adapter (swap SQLite for PostgreSQL, swap Manim
  for another renderer) and the Core never changes.

---

---

## The Complete Picture — Both Types Together

```
+===========================================================================+
|              SUPERMANIM — BOTH ADAPTER TYPES IN ONE VIEW                  |
+===========================================================================+
|                                                                           |
|   [ USER or TEST SCRIPT ]                                                 |
|              |                                                            |
|              v                                                            |
|   +-------------------------------+                                       |
|   |  DRIVING ADAPTER              |  The Adapter calls the Core.          |
|   |  CLI Shell / Test Script      |  Translates: user input --> Port call |
|   +-------------------------------+                                       |
|              |                                                            |
|              | calls Driving Port                                         |
|              v                                                            |
|   +-------------------------------+                                       |
|   |  LAYER 2 — Services           |  Workflow logic.                      |
|   |  RenderOrchestrationService   |  Coordinates all the steps.           |
|   |  SceneService, AudioService   |  Calls Driven Ports when needed.      |
|   +-------------------------------+                                       |
|              |                                                            |
|              | calls Driven Ports                                         |
|              v                                                            |
|   +-------------------------------+                                       |
|   |  LAYER 3 — DOMAIN CORE        |  Pure logic. No I/O. No tools.       |
|   |  Entities, Ports, Services    |  Owns all abstract interfaces.        |
|   +-------------------------------+                                       |
|              |                                                            |
|              | Ports implemented by Driven Adapters below                |
|              v                                                            |
|   +-------------------------------+                                       |
|   |  DRIVEN ADAPTERS              |  The Core calls these Adapters.       |
|   |  SqliteSceneRepository        |  Each one implements one Port.        |
|   |  SqliteCacheRepository        |  Each one talks to one external tool. |
|   |  ManimSubprocessRenderer      |                                       |
|   |  FfmpegAudioProcessor         |                                       |
|   |  LocalFileStorage             |                                       |
|   +-------------------------------+                                       |
|              |                                                            |
|              v                                                            |
|   [ EXTERNAL WORLD ]                                                      |
|   SQLite database files — Manim renderer — FFmpeg tool — OS file system   |
|                                                                           |
+===========================================================================+
```

---

---

## Side-by-Side Comparison

```
+===========================================================================+
|                    DRIVING vs DRIVEN — FULL COMPARISON                    |
+===========================================================================+
|                                                                           |
|  PROPERTY              DRIVING ADAPTER            DRIVEN ADAPTER          |
|  ──────────────────────────────────────────────────────────────────────  |
|  Other name            Primary Adapter            Secondary Adapter       |
|                                                                           |
|  Who starts the work?  The Adapter starts it.     The Core starts it.    |
|                                                                           |
|  Direction of call     Adapter --> Core            Core --> Adapter       |
|                                                                           |
|  Where it lives        Layer 1 (CLI Shell)         Layer 4 (Adapters)    |
|                                                                           |
|  Side of the hexagon   Left side (input side)      Right side (output)   |
|                                                                           |
|  What it translates    User input --> Port call     Port call --> I/O     |
|                                                                           |
|  Depends on            Driving Ports (in Core)     Driven Ports (in Core)|
|                                                                           |
|  SuperManim examples   CLI Shell (shell.py)         SqliteSceneRepository |
|                        command_parser.py            SqliteCacheRepository |
|                        cli_notifier.py              ManimSubprocessRenderer|
|                        Test scripts                 FfmpegAudioProcessor  |
|                                                     LocalFileStorage      |
|                                                                           |
|  What you can swap it  CLI --> GUI or Web API       SQLite --> PostgreSQL  |
|  for (Core unchanged)                               Manim --> OtherTool   |
|                                                                           |
+===========================================================================+
```
---
### Subsubsection 0.5.1.3 The Complete Port and Adapter Reference Table

```
+------+---+-------------------------------+----------------------------+
| Grp  | # | Port Name                     | Default Adapter            |
+------+---+-------------------------------+----------------------------+
|      | 1 | SceneRepositoryPort           | SqliteSceneRepository      |
|  R   | 2 | ProjectRepositoryPort         | SqliteProjectRepository    |
|  E   | 3 | AudioRepositoryPort           | SqliteAudioRepository      |
|  P   | 4 | CacheRepositoryPort           | SqliteCacheRepository      |
|  O   | 5 | RenderHistoryRepositoryPort   | SqliteRenderHistoryRepo    |
+------+---+-------------------------------+----------------------------+
|      | 6 | RenderRunnerPort              | ManimSubprocessRenderer    |
|  M   | 7 | AudioProcessorPort            | FfmpegAudioProcessor       |
|  E   | 8 | VideoAssemblerPort            | FfmpegVideoAssembler       |
|  D   | 9 | AudioAnalyzerPort             | LibrosaAudioAnalyzer       |
|  I   |10 | PreviewGeneratorPort          | ManimPreviewGenerator      |
|  A   |11 | VideoMetadataReaderPort       | FfprobeMetadataReader      |
+------+---+-------------------------------+----------------------------+
|      |12 | FileStoragePort               | LocalFileStorage           |
|  I   |13 | HashComputerPort              | Sha256HashComputer         |
|  N   |14 | TempFileManagerPort           | SystemTempManager          |
|  F   |15 | AssetManagerPort              | LocalAssetManager          |
+------+---+-------------------------------+----------------------------+
|      |16 | ProjectCommandPort            | CliProjectCommandAdapter   |
|  D   |17 | SceneCommandPort              | CliSceneCommandAdapter     |
|  R   |18 | RenderCommandPort             | CliRenderCommandAdapter    |
|  I   |19 | AudioCommandPort              | CliAudioCommandAdapter     |
|  V   |20 | ExportCommandPort             | CliExportCommandAdapter    |
+------+---+-------------------------------+----------------------------+
|      |21 | NotificationPort              | CliNotifier                |
|  N   |22 | ProgressReporterPort          | CliProgressReporter        |
|  O   |23 | LoggerPort                    | FileLogger                 |
+------+---+-------------------------------+----------------------------+
|      |24 | SettingsPort                  | TomlSettingsAdapter        |
|  C   |25 | EnvironmentInspectorPort      | SystemEnvironmentInspector |
+------+---+-------------------------------+----------------------------+

Legend:
  REP   = Repository Ports   (Data Persistence)
  MEDIA = Media Ports        (Heavy Workers: Manim, FFmpeg)
  INF   = Infrastructure     (Files, Hashes, Temp files)
  DRIV  = Driving Ports      (Inbound: User Commands)
  NOT   = Notification Ports (Outbound: User Feedback)
  C     = Configuration      (Settings & Environment)
```

---






### Subsubsection 0.5.1.4  The Full Hexagonal Architecture Diagram

```
+============================================================+
|                                                            |
|                   OUTSIDE WORLD (LEFT SIDE)                |
|                   Inbound / Driving Adapters               |
|                   (things that talk TO the Core)           |
|                                                            |
|   +------------------+    +------------------+            |
|   | CliProjectAdapter|    | CliRenderAdapter |            |
|   | "create project" |    | "render scene 2" |            |
|   +--------+---------+    +--------+---------+            |
|            |                       |                       |
+============================================================+
             |                       |
             | calls                 | calls
             v                       v
   +---------+---------+   +---------+---------+
   | ProjectCommandPort|   | RenderCommandPort |   <-- INBOUND PORTS
   | (abstract)        |   | (abstract)        |
   +-------------------+   +-------------------+
             |                       |
             v                       v
+============================================================+
|                                                            |
|                        THE CORE                            |
|             (Application & Domain Services)                |
|                                                            |
|   [ Application Services (Orchestration) ]                 |
|   AppStateService        SessionService                    |
|   RenderOrchestrationService  ProjectLifecycleService      |
|                                                            |
|   [ Domain Services (Pure Logic) ]                         |
|   SceneService           AudioService                      |
|   ExportService          TimelineService                   |
|   CacheService           ValidationService                 |
|   HashService                                             |
|                                                            |
|   "I contain only business rules and workflows."           |
|   "I do not know SQLite exists."                           |
|   "I do not know Manim exists."                            |
|   "I only speak through Ports."                            |
|                                                            |
+============================================================+
             |                       |
             | calls                 | calls
             v                       v
   +---------+---------+   +---------+---------+
   | SceneRepositoryP. |   | RenderRunnerPort  |   <-- OUTBOUND PORTS
   | (abstract)        |   | (abstract)        |
   +-------------------+   +-------------------+
             |                       |
             v                       v
+============================================================+
|                                                            |
|                   OUTSIDE WORLD (RIGHT SIDE)               |
|                   Outbound / Driven Adapters               |
|                   (things the Core calls OUT to)           |
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

---

### Subsubsection 0.5.1.4 The Golden Rule of Hexagonal Architecture

```
+================================================================+
|                     THE GOLDEN RULE                            |
+================================================================+
|                                                                |
|   THE CORE NEVER TOUCHES EXTERNAL TOOLS DIRECTLY.             |
|                                                                |
|   It never calls:   sqlite3.connect()                          |
|   It never calls:   subprocess.run(["manim", ...])             |
|   It never calls:   os.path.exists()                           |
|   It never calls:   print()                                    |
|   It never calls:   open("file.txt")                           |
|                                                                |
|   The Core ONLY calls Port methods.                            |
|   The Ports ONLY define what methods exist.                    |
|   The Adapters do all the real work.                           |
|                                                                |
|   Result:                                                      |
|   - Swap any adapter without touching the Core.                |
|   - Test the Core without real tools (use fakes).              |
|   - Add a GUI without rewriting any business logic.            |
|   - Switch databases by changing one file only.                |
|                                                                |
+================================================================+
```

---

## Subsection 0.5.2 — The Layered Architecture

### Subsubsection 0.5.2.1  What Is Layered Architecture?

While Hexagonal Architecture explains how the Core is protected from external
tools, Layered Architecture explains how the code is organized from top to bottom
in terms of who calls whom.

Think of the system as a stack of layers. Each layer:
- Only talks to the layer directly below it
- Never skips a layer to talk to something deeper
- Can be replaced without affecting the layers above or below

```
+================================================================+
|                 THE FOUR LAYERS OF SUPERMANIM                  |
+================================================================+
|                                                                |
|   LAYER 1 — User Interface Layer (top)                         |
|   ─────────────────────────────────────────────────────────── |
|   What it is: The interactive terminal shell.                  |
|   What it does: Reads what the user types.                     |
|                 Calls the Application Layer below.             |
|                 Prints responses back to the user.             |
|   Files: adapters/cli/shell.py                                 |
|          adapters/cli/command_parser.py                        |
|          adapters/cli/output_formatter.py                      |
|          adapters/cli/cli_notifier.py                          |
|                                                                |
|   LAYER 2 — Application Layer                                  |
|   ─────────────────────────────────────────────────────────── |
|   What it is: The services that carry out workflows.           |
|   What it does: Receives commands from Layer 1.                |
|                 Coordinates the steps of each operation.       |
|                 Calls the Domain Layer below for rules.        |
|                 Calls Adapters for data and tools.             |
|   Files: core/services/project_lifecycle_service.py            |
|          core/services/scene_service.py                        |
|          core/services/render_orchestration_service.py         |
|          core/services/export_service.py                       |
|          core/services/audio_service.py  ...etc                |
|                                                                |
|   LAYER 3 — Domain Layer (Core)                                |
|   ─────────────────────────────────────────────────────────── |
|   What it is: Pure business rules and data definitions.        |
|   What it does: Defines what is valid and what is not.         |
|                 Defines all Entities (data classes).           |
|                 Defines all Ports (abstract contracts).        |
|                 Contains zero I/O of any kind.                 |
|   Files: domain/entities/scene.py                              |
|          domain/entities/project.py  ...etc                    |
|          domain/ports/...                                      |
|          core/services/validation_service.py                   |
|          core/services/timeline_service.py                     |
|          core/services/hash_service.py                         |
|                                                                |
|   LAYER 4 — Infrastructure Layer (bottom)                      |
|   ─────────────────────────────────────────────────────────── |
|   What it is: All the real-world adapters.                     |
|   What it does: Talks to SQLite, FFmpeg, Manim, disk.          |
|                 Implements the Port contracts from Layer 3.    |
|                 Does all the dirty work.                       |
|   Files: adapters/repositories/sqlite_scene_repository.py      |
|          adapters/media/manim_subprocess_renderer.py           |
|          adapters/media/ffmpeg_audio_processor.py  ...etc      |
|                                                                |
+================================================================+
```

---

### Subsubsection 0.5.2.2 The Layer Stack Drawn Vertically

```
+============================================================+
|                                                            |
|   USER types:  "render all"                                |
|                                                            |
|        |                                                   |
|        v                                                   |
|   +--------------------------------------------------+    |
|   |          LAYER 1 — CLI Shell                     |    |
|   |  CommandParser reads "render all"                |    |
|   |  Calls: render_service.render_all()              |    |
|   +--------------------------------------------------+    |
|        |                                                   |
|        v                                                   |
|   +--------------------------------------------------+    |
|   |       LAYER 2 — Application Services            |    |
|   |  RenderOrchestrationService.render_all()         |    |
|   |  Loops over every scene.                         |    |
|   |  For each scene, checks hash, calls render.      |    |
|   +--------------------------------------------------+    |
|        |                                                   |
|        v                                                   |
|   +--------------------------------------------------+    |
|   |          LAYER 3 — Domain Core                   |    |
|   |  ValidationService: "does this scene have code?" |    |
|   |  HashService: "compute fingerprint of file"      |    |
|   |  CacheRepositoryPort: "does hash match stored?"  |    |
|   +--------------------------------------------------+    |
|        |                                                   |
|        v                                                   |
|   +--------------------------------------------------+    |
|   |       LAYER 4 — Infrastructure Adapters          |    |
|   |  SqliteCacheRepository: reads cache_records      |    |
|   |  ManimSubprocessRenderer: calls Manim            |    |
|   |  LocalFileStorage: saves rendered .mp4 file      |    |
|   +--------------------------------------------------+    |
|        |                                                   |
|        v                                                   |
|   EXTERNAL WORLD: SQLite file, Manim process, Disk         |
|                                                            |
+============================================================+
```

---

### Subsubsection 0.5.2.3 The Dependency Rule

The Dependency Rule is the law that makes this architecture work:

```
+================================================================+
|                    THE DEPENDENCY RULE                         |
+================================================================+
|                                                                |
|   Dependencies only point INWARD and DOWNWARD.                 |
|                                                                |
|   Layer 1 (CLI)           knows about Layer 2                  |
|   Layer 2 (Services)      knows about Layer 3                  |
|   Layer 3 (Domain/Core)   knows about NOTHING below it        |
|   Layer 4 (Adapters)      knows about Layer 3 (its Ports)     |
|                                                                |
|   WHAT IS FORBIDDEN:                                           |
|   Layer 3 (Core) NEVER imports from Layer 4 (Adapters).       |
|   Layer 3 (Core) NEVER imports from Layer 1 (CLI).            |
|   The Core is the most protected part of the system.           |
|                                                                |
|   WHY THIS MATTERS:                                            |
|   You can replace the entire CLI with a GUI.                   |
|   The Core never changes.                                      |
|                                                                |
|   You can replace SQLite with PostgreSQL.                      |
|   The Core never changes.                                      |
|                                                                |
|   You can replace FFmpeg with another video tool.              |
|   The Core never changes.                                      |
|                                                                |
+================================================================+
```

---

### Subsubsection 0.5.2.4 How the Two Architectures Work Together

Hexagonal Architecture and Layered Architecture are not two different systems.
They describe the same design from two different angles.

```
+================================================================+
|          THE SAME DESIGN, TWO ANGLES                           |
+================================================================+
|                                                                |
|   HEXAGONAL ARCHITECTURE says:                                 |
|   "The Core is a protected island. Ports are the bridges.      |
|    Adapters connect the bridges to the outside world."         |
|   -- Describes the SHAPE of how things connect.               |
|                                                                |
|   LAYERED ARCHITECTURE says:                                   |
|   "Dependencies flow inward and downward.                      |
|    The CLI calls Services. Services call the Core.             |
|    Adapters are at the bottom, implementing Ports."            |
|   -- Describes the DIRECTION of how things call each other.    |
|                                                                |
|   Together they produce a system that is:                      |
|   - Testable: you can test the Core with fake adapters         |
|   - Flexible: you can swap any adapter without touching Core   |
|   - Clean: each part has exactly one job                       |
|   - Understandable: you always know where to find each thing   |
|                                                                |
+================================================================+
```

---

###### Subsubsection 0.5.2.5  The Complete System in One Diagram

```
+===========================================================================+
|                    SUPERMANIM — COMPLETE ARCHITECTURE                     |
+===========================================================================+
|                                                                           |
|   [ USER TYPES A COMMAND IN THE TERMINAL ]                                |
|              |                                                            |
|              v                                                            |
|   +---------------------------------+                                     |
|   |   LAYER 1 — CLI SHELL           |  <-- Reads commands                |
|   |   shell.py + command_parser.py  |      Calls services                |
|   |   cli_notifier.py               |      Prints results                |
|   +---------------------------------+                                     |
|              |                                                            |
|              v                                                            |
|   +---------------------------------+                                     |
|   |   LAYER 2 — SERVICES            |  <-- Workflows live here           |
|   |   ProjectLifecycleService       |      Validates inputs              |
|   |   SceneService                  |      Coordinates steps             |
|   |   RenderOrchestrationService    |      Calls ports below             |
|   |   AudioService  ExportService   |                                    |
|   +---------------------------------+                                     |
|              |                                                            |
|              v                                                            |
|   +---------------------------------+                                     |
|   |   LAYER 3 — DOMAIN CORE         |  <-- Pure logic, no I/O           |
|   |   Entities: Scene, Project,     |      Business rules                |
|   |             AudioFile, Clip...  |      Port contracts                |
|   |   Ports: (abstract interfaces)  |      Zero external calls          |
|   |   ValidationService             |                                    |
|   |   TimelineService  HashService  |                                    |
|   +---------------------------------+                                     |
|              |                                                            |
|              v                                                            |
|   +---------------------------------+                                     |
|   |   LAYER 4 — ADAPTERS            |  <-- Real implementations         |
|   |   SqliteSceneRepository         |      Talk to SQLite, FFmpeg        |
|   |   SqliteAudioRepository         |      Manim, disk, OS              |
|   |   ManimSubprocessRenderer       |      One adapter per port          |
|   |   FfmpegAudioProcessor          |                                    |
|   |   FfmpegVideoAssembler          |                                    |
|   |   LocalFileStorage              |                                    |
|   +---------------------------------+                                     |
|              |                                                            |
|              v                                                            |
|   EXTERNAL WORLD: SQLite files, Manim, FFmpeg, OS file system            |
|                                                                           |
+===========================================================================+
```

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

