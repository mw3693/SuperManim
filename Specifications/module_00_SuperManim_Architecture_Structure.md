

# SuperManim — Module 00: Architecture & Design Reference

**Project:** SuperManim CLI Tool  
**Purpose:** Incremental, Audio-Synchronized Manim Animation Production  
**Language:** Python 3.10+

---
### Section 0.1  — What Is SuperManim?
Imagine you are making a 30-minute educational video using a Python animation tool called **Manim**.
Your video has **20 scenes**. Each scene takes about **5 minutes** to render on your computer.  
Total rendering time: **100 minutes**.

You watch the finished video and spot a tiny mistake in **Scene 14**. One shape is the wrong color.  
You fix the one line of code that caused the mistake.

Now what?

Without any tooling, you have to **re-render all 20 scenes** from scratch.It does not matter
that only one scene changed.The default workflow does not remember what was already done.
So you wait another **100 minutes** for something that only needed **5 minutes**.

**SuperManim solves exactly this.**

With SuperManim, you fix Scene 14. SuperManim checks every scene.
It sees that Scenes 1–13 and 15–20 have not changed at all — their code is identical,
their audio clips are the same. It skips them. It only re-renders Scene 14.
You wait **5 minutes** instead of **100**.

This is the core idea. Everything else in SuperManim is built on top of this idea.

```
+----------------------------------------------------------------------+
|                   The SuperManim Core Idea                           |
+----------------------------------------------------------------------+
|                                                                      |
|  WITHOUT SuperManim:                                                 |
|                                                                      |
|  You fix 1 scene.                                                    |
|  You run Manim.                                                      |
|  Manim renders ALL 20 scenes.                                        |
|  You wait 100 minutes.                                               |
|                                                                      |
|  WITH SuperManim:                                                    |
|                                                                      |
|  You fix 1 scene.                                                    |
|  SuperManim checks all 20 scenes.                                    |
|        |                                                             |
|        +-- Scene 1  unchanged? --> use saved render. Skip. (0 sec)  |
|        +-- Scene 2  unchanged? --> use saved render. Skip. (0 sec)  |
|        +-- ...                                                       |
|        +-- Scene 14 CHANGED   --> call Manim. Render it. (5 min)    |
|        +-- Scene 15 unchanged? --> use saved render. Skip. (0 sec)  |
|        +-- ...                                                       |
|        +-- Scene 20 unchanged? --> use saved render. Skip. (0 sec)  |
|                                                                      |
|  Total wait: 5 minutes.                                              |
|                                                                      |
+----------------------------------------------------------------------+
```

SuperManim does **not** replace Manim. Manim still does all the actual animation rendering.
SuperManim is the **manager** that sits on top of Manim and decides what work Manim actually
needs to do.

Think of it like a boss and an employee:
- **Manim** is the employee. It is very good at rendering animations, but it has no memory.
   Every time you ask it to do something, it starts from scratch.
- **SuperManim** is the boss. It remembers everything that was already done.
  It is smart enough to say "don't bother re-rendering Scene 3, nothing changed there."

---



### Section 0.2 What the main  problem does SuperManim solve?

SuperManim is a multi-purpose tool. It can do many things:

- Edit audio files (split them, change their format, measure their duration)
- Edit video files (remove audio from a video, split a video into parts, change format)
- Create Manim animations without audio
- Create Manim animations **synchronized perfectly with audio** (the main feature)

But the hardest problem it solves — the one that no other tool handles automatically — is this:

**How do you make a Manim video that matches your audio file perfectly, and how do you do it
without rebuilding everything from scratch every single time you change one small thing?**

Here is why this is so hard without SuperManim.

Suppose you have a 60-second narration audio file. You want to make an animation that plays
alongside it. Here is what you have to do **manually, by hand, without any tooling**:

```
Step 1.  Load your audio file into an audio editor.
Step 2.  Measure the total duration. It is 60.0 seconds.
Step 3.  Decide which parts of the audio go with which visual scenes.
         Example:
           Seconds  0.0 to 12.5 --> Scene 1 (introduction)
           Seconds 12.5 to 31.0 --> Scene 2 (main concept)
           Seconds 31.0 to 47.8 --> Scene 3 (example)
           Seconds 47.8 to 60.0 --> Scene 4 (conclusion)
Step 4.  Write Manim Python code for Scene 1.
         Make sure the animation runs for exactly 12.5 seconds.
         Not 12.4. Not 12.6. Exactly 12.5.
Step 5.  Repeat for Scenes 2, 3, and 4.
Step 6.  Render each scene separately using the Manim command line.
Step 7.  Assemble all four rendered video files into one video using FFmpeg.
Step 8.  Check that the total video length equals 60.0 seconds exactly.
Step 9.  Play the video alongside the audio. Check if they match.
Step 10. They do not match perfectly. Go back to Step 3.
         Repeat everything from scratch.
```

This is painful. It requires:
- A lot of manual file management (keeping track of which clip goes with which scene)
- Mental arithmetic (adding up durations to make sure they sum correctly)
- Running multiple terminal commands in the right order
- Rebuilding the entire assembled video every time even one scene changes

SuperManim replaces all ten of those steps with a few simple commands:

```bash
supermanim new MyAnimation
supermanim add audio voice.mp3
supermanim set scenes_number 5
supermanim set scene 1 duration 12.5
supermanim add scene 1 code scene1.py
supermanim render scene 1
```

SuperManim handles:
- All file management automatically
- All duration calculations automatically
- All timeline tracking automatically
- All rendering coordination automatically (only re-renders what changed)
- All audio/video assembly automatically

---




### Section 0.3 The General usages of the SuperManim

The tool can be used for different types of projects based on the mode the user wants.
SuperManim has three modes. You pick one when you start working. Think of them as
three different personalities the tool can have:

```
+------------------------------------------------------------------+
|  Mode 1: "normal"      |  Media editor. Fix existing files.     |
+------------------------------------------------------------------+
|  Mode 2: "simplemanim" |  Create Manim animations. No audio.    |
+------------------------------------------------------------------+
|  Mode 3: "supermanim"  |  Create Manim animations + audio sync. |
+------------------------------------------------------------------+
```
These modes can be stored in the Module 1 The global constants in the file `config/constants.py`

```python
NORMAL_MODE       = "normal"
SIMPLE_MANIM_MODE = "simplemanim"
SUPER_MANIM_MODE  = "supermanim"
```

#### Subsection 0.3.1 The Normal Media Editor

##### Subsubsection 0.3.1.1 Definition of this mode:

This mode is for fixing videos and songs you already have. Think of it like a simple cutting table.
If you have a long video and want to make it shorter, or if you have a song and want to cut out
the quiet parts, you use this mode.

##### Subsubsection 0.3.1.2 How to use it:

###### 1. Choose the Mode**
First, you must tell the tool, "I want to be a Normal Editor today." You write this command:
`app_mode = "normal"`

###### 2. Create Your Project Space**
Before you start working, the tool needs a place to save your work. It creates a "project folder structure.
" Imagine this like opening a new folder on your desk to keep all your papers organized so they don't get lost.

###### 3. Add Your Files**
Now you need to give the tool the file you want to fix. It is like handing a photo to a friend to look at.

**If you want to edit sound:**
You tell the tool where the sound file lives on your computer.
Command: `add audio "path to audio"` or `add audio_file "path to audio"`

**If you want to edit a movie:**
You tell the tool where the video file is.
Command: `add video "path to video"` or `add video_file "path to video"`

###### 4. Perform Operations:**
Once the file is loaded, you can change it. The tool can do many things:

**Split:**
You can cut the file into two pieces. For example, cut a 10-minute video into two 5-minute videos.

**Change Format:**
You can change the file type, like turning a big heavy video file into a lighter one
that is easier to send to friends.

##### Subsubsection 0.3.1.3 Diagram of Normal Editor:

```
+---------------------------------------------------------+
|                  NORMAL EDITOR WORKFLOW                 |
+---------------------------------------------------------+

      [ User Starts ]
            |
            v
   +-----------------------+
   |  Set Mode: "normal"   |  <-- Telling the tool what to be.
   +-----------------------+
            |
            v
   +-----------------------+
   | Setup Project Folder  |  <-- Making a workspace.
   +-----------------------+
            |
            v
   +-----------------------+
   | Add Media File        |  <-- Put video or audio inside.
   | (Video or Audio)      |
   +-----------------------+
            |
            v
   +-----------------------+
   | Edit the File         |  <-- Cut, split, or change format.
   +-----------------------+
            |
            v
   +-----------------------+
   | Save the New File     |
   +-----------------------+
```

---

#### Subsection 0.3.2 The Simple Manim Editor

##### Subsubsection 0.3.2.1 Definition of this mode:

This mode is for creating cartoons using code. It is built on a tool called "Manim.
" Think of this mode as a robot that draws pictures for you. It creates "silent movies"
because it makes video scenes without any sound or music to match.

##### Subsubsection 0.3.2.2 How to use it:

###### 1. Choose the Mode
First, you tell the tool to be a Simple Manim Editor. You write this command:
`app_mode = "simpleManim"`

###### 2. Create Your Project Space**
Just like the other mode, the tool sets up a folder to keep your work safe.

###### 3. Choose the Number of Scenes**
A scene is like one page in a storybook. You tell the tool how many pages you want in your story.
Command: `set scenes_number 2` (for two scenes)
Or     : `set scene` (for just one scene)

###### 4. Set the Duration**
You must tell the tool how long each page stays on the screen. You count this in seconds.
Command: `set scene 1 duration 3.4` (Scene 1 plays for 3.4 seconds)
Command: `set scene 3 duration 5` (Scene 3 plays for 5 seconds)

###### 5. Add Your Code**
Now you give the tool the instructions for what to draw. You give it a file with the code.
Command: `set scene 1 code "path to the manim code"`

###### 6. Preview or Render**
**Preview:** You can look at a quick drawing to check your work.
Command: `preview scene 1` (This shows a low-quality draft fast).
**Render:** You make the final movie.
Command: `render all` (Makes all scenes in high quality).

##### Subsubsection 0.3.2.3 Diagram of Simple Editor:



```
+---------------------------------------------------------+
|                  SIMPLE MANIM WORKFLOW                  |
+---------------------------------------------------------+
  [ You run SuperManim ]
          |
          v
  [ Set mode: "simpleManim" ]
          |
          v
  [ Create project folder ]
          |
          v
  [ Set number of scenes ]
  [ Example: 4 scenes    ]
          |
          v
  [ For each scene:                      ]
  [ - Set duration                       ]
  [ - Provide .py file with Manim code   ]
          |
          v
  [ Preview (optional) ]
  [ Quick check draft   ]
          |
          v
  [ Render all scenes ]
  [ SuperManim only re-renders ]
  [ scenes that changed        ]
          |
          v
  [ SuperManim assembles all scene clips ]
  [ into one final video file            ]
```


#### Subsection 0.3.3 The Super Manim Editor

##### Subsubsection 0.3.3.1 Definition of this mode:

This is the most powerful mode. It is like a movie director.It does everything the Simple Editor does,
but it adds a superpower: **Synchronization**. It makes sure the video matches the sound perfectly.
If a ball bounces on screen, the sound "BOING" plays at the exact same time.

##### Subsubsection 0.3.3.2 How to use it:

###### 1. Choose the Mode
First, you tell the tool to use its superpower. You write this command:
`app_mode = "superManim"`


###### 2. Create Your Project Space
The tool creates a folder that keeps your sound and video plans together.


###### 3. Add Your Sound
Because the video needs to match the sound, you must give the tool the sound file first.
This is usually a voice recording or music.

Command: `add audio_file "path to voiceover"`

###### 4. Map the video 
The tool helps you split your video into scenes to match the sound. There are two ways to do this: 

**Method 1: The Manual Way**
You tell the tool exactly how many scenes you want.Then, you set the duration (time) for each scene. 
Rule: The total time of all your scenes added together must be exactly the same as the length of the audio file.
     
**Method 2: The Automatic Way**
If you do not enter the number of scenes or times, the tool will do it for you.
It listens to the audio and looks for silence (the quiet parts).
It automatically cuts a new scene every time it hears a pause in the sound. 

###### 5. Add Your Code
You give the tool the drawing instructions for each time section.
Command: `set scene 1 code "path to code"`

###### 6. Render the Final Video
You tell the tool to combine the video and sound into one movie.
Command: `render all`

##### Subsubsection 0.3.3.3 Diagram of Super Editor:

```
  [ You run SuperManim ]
          |
          v
  [ Set mode: "superManim" ]
          |
          v
  [ Create project folder ]
          |
          v
  [ Add your audio file FIRST ]
  [ This is the foundation.   ]
          |
          v
  [ Map the video to the audio ]
  [                            ]
  [ Option A: set scenes and durations manually ]
  [ Option B: let SuperManim detect silences    ]
          |
          v
  [ For each scene:                ]
  [ Provide .py file with Manim code ]
          |
          v
  [ Render ]
  [ SuperManim renders each scene  ]
  [ clips the matching audio slice ]
  [ pairs them together            ]
          |
          v
  [ SuperManim assembles:          ]
  [ Scene 1 video + audio clip 1   ]
  [ Scene 2 video + audio clip 2   ]
  [ Scene 3 video + audio clip 3   ]
  [ ...                            ]
  [ into one final synchronized video ]
```



##### Subsubsection 0.3.3.4 The full file structure of the project space:
After the user open the tool and create a new project or open a recent project whater ever then the
tool will automatically create the full file structures of the new project:

Assume the user type:
`set mode "supermanim"` then

`create new_project` "project name"`
`create project "project name"`

Then the tool will create:
```
/projects/MyAnimation/
+-- project_data.db        |
+-- audio_clips/              <- managed by AudioManager
|   +-- original_audio.mp3    <- the user's audio file, copied here
|   +-- clip_001.mp3          <- scene clips (after splitting)
|   +-- clip_002.mp3
|
+-- scenes/              <- managed by ScenesManager
|   +-- scene_01/
|   +-- scene_02/
|
+-- cache/               <- managed by CacheManager
+-- output/              <- rendered video lives here 
+-- previews/            <- preview files by previewManager
+-- exports/             <- exported packages by exportManager
+-- assets/              <- user-provided images, fonts, videos
+-- temp/                <- temporary working files
```

Here is a simple explanation of what each part of this structure does, along with some fixes to make sure the logic works perfectly. 

**1. The Brain (project_data.db)**
This is a database file. Think of it as the project's brain. It remembers everything: how many scenes you have, the duration of each scene, and which audio file belongs to which scene. It keeps track of all the settings so you don't have to remember them. 

**2. The Sound Room (audio_clips/)**
This folder is managed by the AudioManager. 

     original_audio.mp3: When you add your sound, the tool copies it here. This is the master sound file.
     clip_001.mp3: When the tool "maps" the video (splits the scenes), it cuts the big audio file into small pieces. Each piece matches one scene. This makes sure the video for Scene 1 matches the audio for Scene 1 perfectly.
     

**3. The Workshop (scenes/)**
This folder is managed by the ScenesManager. 

     Inside, there is a folder for each scene (like scene_01, scene_02).
     Note: This is where the magic happens. Each folder will contain the specific Python/Manim code file (the instructions) for that specific scene.
     

**4. The Library (assets/)**
This is where you put things you want to show in the video. If you have a picture of a cat, a special font, or a logo, you put it here. The tool looks here when you say "show this image." 

**5. The Cinema (output/ and previews/)** 

     output/: This is where the final, high-quality movie appears after you click "Render." It is the finished product.
     previews/: This is for quick tests. When you say "Preview," the tool makes a low-quality, fast video and puts it here so you can check for mistakes without waiting a long time.
     

**6. The Helpers (cache/, temp/, exports/)** 

     cache/: The tool remembers things here to make it faster next time. For example, if you render a scene once, it saves some data here so it doesn't have to start from zero if you render it again.
     temp/: This is the trash bin. The tool puts files here while it is working, and then deletes them when it is done. You usually do not need to look in here.
     exports/: If you want to share your project with a friend, the tool puts a zip file here with everything they need.
     

### Section 0.4 — Full File Structure of the superManim tool  on Disk
This is the complete directory layout for a SuperManim installation.

```

```

### Section 0.5 The Architecture design of the SuperManim tool:
The tool architecture design is a combination of two architectures one to isolate the core
of the tool form the external world and the second architecture inside the core itself to organize
the internal componenets of the core.The two architectures are:


#### Subsection 0.5.1 The Hexagonal Architecture:

##### Subsubsection 0.5.1.1 What is Hexagonal Architecture:

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


---
##### Subsubsection 0.5.1.2 Why SuperManim Uses Hexagonal Architecture

###### The Problem: SuperManim Talks to a LOT of Different Things
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

######  The Disasters: What Happens When You Mix Everything Together

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

######  The Root Cause: Why All Three Disasters Happen
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

###### — The Fix: Hexagonal Architecture
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

######  How Each Disaster Is Now Fixed

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



###### Appendix — The Ports and Their Adapters in SuperManim

This is the full list of every Port and every Adapter in the SuperManim system.

```
+------------------------+--------------------------------+-----------------------------+---------------------------------------------------------------+
| Port Name              | What the Core Asks For         | Adapter Name                | How the Adapter Does It                                       |
+------------------------+--------------------------------+-----------------------------+---------------------------------------------------------------+
| SceneRepositoryPort    | Save/load scene data           | SqliteSceneRepository       | Reads/writes SQLite scenes table (sqlite3)                    |
+------------------------+--------------------------------+-----------------------------+---------------------------------------------------------------+
| ProjectRepositoryPort  | Save/load project settings     | SqliteProjectRepository     | Reads/writes SQLite projects table (sqlite3)                  |
+------------------------+--------------------------------+-----------------------------+---------------------------------------------------------------+
| AudioRepositoryPort    | Save/load audio metadata       | SqliteAudioRepository       | Reads/writes SQLite audio table (sqlite3)                     |
+------------------------+--------------------------------+-----------------------------+---------------------------------------------------------------+
| RenderRunnerPort       | Render a scene                 | ManimLibraryRenderer        | Imports module, calls scene.render() (Manim API)              |
+------------------------+--------------------------------+-----------------------------+---------------------------------------------------------------+
| AudioProcessorPort     | Slice audio, get duration      | FfmpegPythonProcessor       | Uses ffmpeg-python chains (.output().run())                   |
+------------------------+--------------------------------+-----------------------------+---------------------------------------------------------------+
| VideoAssemblerPort     | Assemble final video           | FfmpegPythonAssembler       | Uses ffmpeg-python concat chains                              |
+------------------------+--------------------------------+-----------------------------+---------------------------------------------------------------+
| FileStoragePort        | Check/read/write files         | LocalFileStorage            | Uses os, shutil, pathlib                                      |
+------------------------+--------------------------------+-----------------------------+---------------------------------------------------------------+
| HashComputerPort       | Get fingerprint of a file      | Sha256HashComputer          | Uses Python's hashlib.sha256()                                |
+------------------------+--------------------------------+-----------------------------+---------------------------------------------------------------+
| NotificationPort       | Send messages to user          | CliNotifier                 | Uses print() and rich library (or cmd module)                 |
+------------------------+--------------------------------+-----------------------------+---------------------------------------------------------------+
| SilenceDetectorPort    | Find silences in audio         | LibrosaSilenceDetector      | Uses librosa.effects.split()                                  |
+------------------------+--------------------------------+-----------------------------+---------------------------------------------------------------+
```
Every single external technology in SuperManim — SQLite, FFmpeg, Manim, the file system,
the terminal, Librosa — is behind one of these Adapters. The Core never touches any of
them directly. It only ever calls the Port.

---


##### Subsubsection 0.5.1.5 The components of the Hexagonal Architecture:
###### The fist component is the Core of the tool(The Brain):

The Core is the centerpiece of Hexagonal Architecture.It contains all the **real logic** of
SuperManim — the decisions, the rules, the calculations. It is pure Python.
It does not import `os`, `sqlite3`, `subprocess`, or anything external.

The Core answers questions like:
- "Should this scene be re-rendered?" (Check if its hash changed)
- "Do all the scene durations add up to the audio duration?" (Validation rule)
- "What is the correct order to assemble the final video?" (Timeline logic)
- "Is this project in a valid state to render?" (Business rule check)

The Core does **not** answer questions like:
- "Where on disk is the file?" (That's the file system adapter's job)
- "How do I write to SQLite?" (That's the database adapter's job)
- "How do I call Manim?" (That's the Manim adapter's job)

Here is what lives inside the Core of SuperManim:

```
+------------------------------------------------------------------+
|                         THE CORE                                 |
+------------------------------------------------------------------+
|                                                                  |
|  ProjectManager      - Rules for creating/opening projects       |
|                        "A project must have a name."             |
|                        "A project must have at least 1 scene."   |
|                                                                  |
|  AudioManager        - Rules for audio handling                  |
|                        "Audio must be loaded before scenes."     |
|                        "Scene durations must sum to audio length"|
|                                                                  |
|  ScenesManager       - Rules for scene management               |
|                        "Scene IDs must be unique."               |
|                        "Each scene must have a duration > 0."    |
|                                                                  |
|  RenderOrchestrator  - The render decision logic                 |
|                        "If hash unchanged, skip this scene."     |
|                        "Render scenes in order 1, 2, 3..."       |
|                                                                  |
|  TimelineEngine      - The timing calculations                   |
|                        "Scene 3 starts at second 31.0"           |
|                        "Scene 3's audio clip is 31.0 to 47.8"   |
|                                                                  |
|  CacheManager        - The change detection logic                |
|                        "This scene's hash matches. Skip."        |
|                        "That scene's hash changed. Re-render."   |
|                                                                  |
|  ExportManager       - Rules for packaging projects              |
|                                                                  |
+------------------------------------------------------------------+
|  The Core ONLY talks to the outside world through Ports.         |
|  It does NOT touch files, databases, or external tools directly. |
+------------------------------------------------------------------+
```
###### The second component is the ports (Interfaces):
A Port is an **interface**. It is a contract. It says: "If you want to give me a service,
you must provide these exact functions. I don't care how you implement them.
Just give me these functions."

The Core defines Ports. The Core says: "I need someone who can save a scene.I need someone
who can run a render. I need someone who can read audio duration." The Core does not care
*how* these things are done. It just defines the shape of what it needs.

In Python, Ports are typically written as Abstract Base Classes (ABCs) or Protocols.

There are two types of Ports:

**Inbound Ports (also called "Driving Ports")**  
These are how the outside world talks TO the Core. The outside world says "do this thing."
The CLI uses an Inbound Port when it sends a command like `render scene 1` to the Core.

**Outbound Ports (also called "Driven Ports")**  
These are how the Core talks to the outside world to GET things done. The Core says "save this scene"
using an Outbound Port. Someone on the other end of that port fulfills the request
(the database adapter, the file system adapter, etc.).

**Example of a Port in Python:**

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
It never asks "are you using SQLite?" or "are you using a JSON file?"
It does not know. It does not care.

**All Ports in SuperManim:**

```
INBOUND PORTS (Outside world --> Core)
---------------------------------------
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


OUTBOUND PORTS (Core --> Outside world)
-----------------------------------------
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

---

###### The third component is the Adaptors:

An Adapter is the **real implementation** of a Port. An Adapter does the actual work.
The Core defined the Port (the contract). The Adapter fulfills that contract.

An Adapter takes the Core's clean request and translates it into whatever
the specific external technology needs.

**Example — the SQLite Adapter for SceneRepositoryPort:**

```python
# This is the Adapter.
# It knows about SQLite. The Core does not.
# It fulfills the SceneRepositoryPort contract.

import sqlite3

class SqliteSceneRepository(SceneRepositoryPort):   # implements the Port

    def __init__(self, db_path: str):
        self.db_path = db_path

    def save_scene(self, scene: Scene) -> None:
        # Here is where the messy SQLite code lives.
        # The Core never sees any of this.
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT OR REPLACE INTO scenes (id, duration, code_path, hash) VALUES (?, ?, ?, ?)",
            (scene.id, scene.duration, scene.code_path, scene.hash)
        )
        conn.commit()
        conn.close()

    def load_scene(self, scene_id: int) -> Scene:
        conn = sqlite3.connect(self.db_path)
        row = conn.execute("SELECT * FROM scenes WHERE id = ?", (scene_id,)).fetchone()
        conn.close()
        return Scene(id=row[0], duration=row[1], code_path=row[2], hash=row[3])

    def all_scenes(self) -> list[Scene]:
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute("SELECT * FROM scenes ORDER BY id").fetchall()
        conn.close()
        return [Scene(id=r[0], duration=r[1], code_path=r[2], hash=r[3]) for r in rows]
```

If tomorrow you decide to switch from SQLite to a JSON file, you write a new adapter:

```python
class JsonSceneRepository(SceneRepositoryPort):     # same Port, different Adapter
    def save_scene(self, scene: Scene) -> None:
        # ... write to a JSON file ...
    def load_scene(self, scene_id: int) -> Scene:
        # ... read from a JSON file ...
    def all_scenes(self) -> list[Scene]:
        # ... read all from JSON file ...
```

You plug in the new adapter. The Core logic is completely untouched.

---

## 1.6 Complete Port and Adapter Map for SuperManim

| Port (Interface) | Adapter (Implementation) | External Technology Used |
|---|---|---|
| `SceneRepositoryPort` | `SqliteSceneRepository` | SQLite via `sqlite3` |
| `ProjectRepositoryPort` | `SqliteProjectRepository` | SQLite via `sqlite3` |
| `AudioRepositoryPort` | `SqliteAudioRepository` | SQLite via `sqlite3` |
| `RenderRunnerPort` | `ManimSubprocessRenderer` | Manim via `subprocess.run()` |
| `AudioProcessorPort` | `FFmpegAudioProcessor` | FFmpeg via `subprocess.run()` |
| `VideoAssemblerPort` | `FFmpegVideoAssembler` | FFmpeg via `subprocess.run()` |
| `FileStoragePort` | `LocalFileStorage` | `os`, `shutil`, `pathlib` |
| `HashComputerPort` | `Sha256HashComputer` | Python's `hashlib` |
| `NotificationPort` | `CliNotifier` | Python's `print()` / `rich` |
| `ProjectCommandPort` | `CliProjectCommandAdapter` | The terminal (argparse / click) |
| `SceneCommandPort` | `CliSceneCommandAdapter` | The terminal |
| `RenderCommandPort` | `CliRenderCommandAdapter` | The terminal |

---

###### The forth commonents is the Services:




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
