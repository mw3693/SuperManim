

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

Here is a simple explanation of what each part of this structure does, along with some fixes
to make sure the logic works perfectly. 

**1. The Brain (project_data.db)**
This is a database file. Think of it as the project's brain. It remembers everything:
how many scenes you have, the duration of each scene, and which audio file belongs to which scene.
It keeps track of all the settings so you don't have to remember them. 

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

### Section 0.4  — The SuperManim Interactive Shell and Command Reference (User Interaction):
This section is specifically about the interactive shell that the tool gives the user  after they start it,
and it documents every command the user can type in that shell.The word "Reference" is important because
this section is something you come back to look things up in it is not just a one-time explanation.

When you install SuperManim and run it, your terminal does not just sit there waiting.
The tool opens its own mini-environment — a shell — where you can type commands and
the tool responds immediately.This section explains:

- What that interactive shell is and how it works.
- How the shell is built with Python's `cmd` library.
- What commands exist in the shell.
- What every command does, what you type exactly, and what happens when you type it.
- How commands are organized into categories based on what they do.

#### Subsection 0.4.1 — The Interactive Shell

##### Subsubsection 0.4.1.1 — What Is the Interactive Shell?

When most people think of running a program, they think: you run it, it does something, it finishes,
and it closes.That is how simple programs work.

SuperManim is different. SuperManim is a **tool you work inside of**. When you start it, it opens and stays open.
It gives you a prompt — a small blinking line waiting for your input — and it keeps waiting there until you
tell it to close. While it is open, you can type commands one after another, and the tool responds to each one.

This kind of environment is called an **interactive shell**

        (also called an **interactive command-line interface** or an **interactive REPL**).

Think of it like this:

```
+---------------------------------------------------------------+
|                                                               |
|  Normal Program (not interactive):                            |
|                                                               |
|  You run it --> It does one thing --> It closes.              |
|  Done.                                                        |
|                                                               |
+---------------------------------------------------------------+
|                                                               |
|  SuperManim (interactive shell):                              |
|                                                               |
|  You run it --> It opens --> It waits for you.                |
|                                                               |
|  You type:  new project MyAnimation                           |
|  It responds: "Project MyAnimation created."                  |
|                                                               |
|  You type:  add audio voice.mp3                               |
|  It responds: "Audio file added. Duration: 60.3 seconds."     |
|                                                               |
|  You type:  render all                                         |
|  It responds: "Rendering 5 scenes..."                         |
|               [===========] Scene 1 done.                     |
|               [===========] Scene 2 done.                     |
|               ...                                             |
|                                                               |
|  You type:  exit                                              |
|  It closes.                                                   |
|                                                               |
+---------------------------------------------------------------+
```

The important thing to understand is that you are not running separate programs over and over.
You are inside one session with the tool, and all the work you do in that session is remembered by the tool.
If you create a project in one command, the next command you type already knows about that project.
The tool keeps its state in memory and in its database while you are working.

---

##### Subsubsection 0.4.1.2 — How the Shell Is Built (The `cmd` Library)

SuperManim builds its interactive shell using a Python standard library called **`cmd`**.

The `cmd` library is a tool that comes built into Python. You do not have to install it separately.
What it does is very simple: it gives you a framework for building a shell where the user can type commands.

Here is how it works in simple terms:

When you start SuperManim, a Python class called `SuperManimShell` (which inherits from `cmd.Cmd`) starts running.
This class has a special method called `cmdloop()`. When `cmdloop()` runs, it does the following thing forever,
in a loop:

```
Step 1: Print the prompt (the "supermanim> " text you see waiting for input).
Step 2: Wait for the user to type something and press Enter.
Step 3: Read what the user typed.
Step 4: Look at the first word. That is the command name.
Step 5: Find the method that handles that command.
Step 6: Call that method, passing the rest of the text as the argument.
Step 7: Go back to Step 1. Repeat.
```

For every command that SuperManim supports, there is a method inside the shell class whose name starts
with `do_`.

For example:
- The command `new` is handled by a method called `do_new(self, args)`.
- The command `render` is handled by a method called `do_render(self, args)`.
- The command `add` is handled by a method called `do_add(self, args)`.

When you type `render all` and press Enter, the `cmd` library automatically:
1. Reads the input `render all`.
2. Splits it into the command name `render` and the argument `all`.
3. Calls `do_render(self, "all")`.
4. The `do_render` method reads the argument `"all"` and decides what to do.

This is how every single command in SuperManim works. The `cmd` library handles the loop and the routing.
The SuperManim code handles what actually happens for each command.

When you type `help` in the shell, the `cmd` library automatically shows you a list of all available commands.
When you type `help render`, it shows you the help text for the `render` command specifically.

The shell looks like this when you start it:

```
$ python supermanim.py

   ____                        __  __             _
  / ___| _   _ _ __   ___ _ __|  \/  | __ _ _ __ (_)_ __ ___
  \___ \| | | | '_ \ / _ \ '__| |\/| |/ _` | '_ \| | '_ ` _ \
   ___) | |_| | |_) |  __/ |  | |  | | (_| | | | | | | | | | |
  |____/ \__,_| .__/ \___|_|  |_|  |_|\__,_|_| |_|_|_| |_| |_|
              |_|

  Version: 1.0.0
  Type "help" to see all commands.
  Type "help <command>" to get help on a specific command.
  Type "exit" or "quit" to close the tool.

supermanim>
```

The `supermanim>` at the bottom is the prompt. This is where you type your commands.

---

##### Subsubsection 0.4.1.3 — How Commands Are Structured

Every command you type in the SuperManim shell follows this general pattern:

```
<command>  <subcommand or target>  <value or argument>
```

Let's break this down with real examples:

```
new project MyAnimation
^           ^
|           |
|           The name of the project you are creating.
|
The command word. This is always the first word.


set scene 3 duration 12.5
^   ^       ^        ^
|   |       |        |
|   |       |        The value you are setting.
|   |       |
|   |       Which field you are setting.
|   |
|   The target of the command.
|
The command word.


render all
^      ^
|      |
|      The scope. "all" means render every scene.
|
The command word.
```

Some commands are very short. Some commands need several pieces of information.
The section below explains every single command in detail, grouped by what they do.

---

---
#### Subsection 0.4.2 — The classifications of commands :
All the commands in SuperManim are organized into six groups.Each group handles a different part of the tool.

```
+---+----------------------------------+---------------------------------------------------+
| # | Category Name                    | What It Covers                                    |
+---+----------------------------------+---------------------------------------------------+
| 1 | Project Commands                 | Creating, opening, closing, and deleting projects |
| 2 | Mode Commands                    | Choosing which mode the project works in          |
| 3 | Scene Commands                   | Adding, setting up, and managing scenes           |
| 4 | Audio Commands                   | Adding audio and mapping it to scenes             |
| 5 | Render Commands                  | Rendering scenes and previewing them              |
| 6 | Export and Utility Commands      | Exporting the final video and other tools         |
+---+----------------------------------+---------------------------------------------------+
```
 The Golden Rule of the commands:
Before you can use any  command, you must have a project open.

The tool always checks this first. If no project is open, every  command will stop immediately
and tell you to open or create a project first.

```
+----------------------------------------------------------+
|  BEFORE EVERY  COMMAND, THE TOOL CHECKS:                 |
|                                                          |
|  Is a project currently open?                            |
|                                                          |
|  YES --> continue with the command.                      |
|  NO  --> stop. Print:                                    |
|          "No project is open.                            |
|           Please open or create a project first."        |
|                                                          |
+----------------------------------------------------------+
`
```
#### Subsection 0.4.3 — Category 1: Project Commands

##### Subsubsection 0.4.3.1 — What Are Project Commands?

Before you do anything in SuperManim, you need a **project**.A project is like a folder for your video work.
It holds everything: the scenes, the audio clips, the render history, the settings, and the final output video.
Every piece of work you do in SuperManim belongs to a project.

Project commands are the commands that let you:
- Create a brand new project.
- Open a project you already made before.
- See what projects you have.
- Delete a project you no longer need.
- See information about the current project.

You almost always start your SuperManim session by either creating a new project or opening an existing one.
Without doing one of these first, the other commands will tell you that no project is currently loaded.

---

### Subsubsection 0.4.3.2 The command of creating project — `new project` or `create project` `create new_project`

**What it does:**

This command creates a brand new project from scratch. When you type this command, SuperManim:
1. Creates a new folder on your computer with the name you give it.
2. Inside that folder, creates the full project directory structure (the scenes folder, audio_clips folder, output folder, cache folder, etc.).
3. Creates a new database file (`project_data.db`) inside the project folder. This database will store everything about the project.
4. Sets the project as the "currently active project" so the next commands you type already know which project to work on.

After you run this command, you are inside your new project and ready to start working.

**Syntax:**
SuperManim is flexible about how you type commands. You do not have to memorize one exact spelling.
The tool understands many different forms of the same command and treats them all as identical.

There are two things the tool is flexible about:

**1. The command word itself** — you can use `new` or `create`. Both mean the same thing.

**2. The case of the letters** — the tool does not care if you use capital letters or lowercase letters.
`project`, `Project`, `PROJECT`, and `PROJect` are all accepted equally.

---

The Full Syntax Family
All of the following are valid ways to create a new project.They all do exactly the same thing.

```
new project <project_name>
new <project_name>

create <project_name>

create project <project_name>

create new_project <project_name>
```

The tool accepts every capitalization variation of the above.
Here are examples using `create project` — the same rule applies to all the forms above:

```
create project   <project_name>
create Project   <project_name>
create PROJECT   <project_name>
create PROJect   <project_name>
create pRoJeCt   <project_name>

create new_project   <project_name>
create New_project   <project_name>
create New_Project   <project_name>
create NEW_PROJECT   <project_name>
create NEW_project   <project_name>
```

All of the above are valid. The tool converts everything to lowercase internally before reading it,
so no matter how you capitalize, the result is the same.

---

The Full Accepted Forms in One Table

```
+-------------------------------+-------------------------------------------+
| What you type                 | What the tool reads it as                 |
+-------------------------------+-------------------------------------------+
| new project MyAnimation       | create a new project named MyAnimation    |
| new MyAnimation               | create a new project named MyAnimation    |
| create project MyAnimation    | create a new project named MyAnimation    |
| create Project MyAnimation    | create a new project named MyAnimation    |
| create PROJECT MyAnimation    | create a new project named MyAnimation    |
| create PROJect MyAnimation    | create a new project named MyAnimation    |
| create new_project MyAnimation| create a new project named MyAnimation    |
| create New_project MyAnimation| create a new project named MyAnimation    |
| create New_Project MyAnimation| create a new project named MyAnimation    |
| create NEW_PROJECT MyAnimation| create a new project named MyAnimation    |
+-------------------------------+-------------------------------------------+
```

> **Note:** The `<project_name>` itself IS case-sensitive.
> `MyAnimation` and `myanimation` are two different project names.
> The case tolerance only applies to the command words (`create`, `project`, `new_project`),
> not to the name you give your project.


**What `<project_name>` means:**
This is the name you want to give your project. It should be one word or words joined by underscores or hyphens.
Do not use spaces in the project name.

Good project names: `MyAnimation`, `Chapter1_Video`, `lecture-intro`, `PythonTutorial`
Bad project names: `My Animation` (has a space — will cause problems)

**Examples:**

```
supermanim> new project MyAnimation
```

```
supermanim> new project Chapter1_Intro
```

```
supermanim> new MyFirstVideo
```

**What the tool prints back:**

```
supermanim> new project MyAnimation

  Creating project: MyAnimation
  Creating folder:  /projects/MyAnimation/
  Creating folder:  /projects/MyAnimation/scenes/
  Creating folder:  /projects/MyAnimation/audio_clips/
  Creating folder:  /projects/MyAnimation/output/
  Creating folder:  /projects/MyAnimation/previews/
  Creating folder:  /projects/MyAnimation/cache/
  Creating folder:  /projects/MyAnimation/assets/
  Creating folder:  /projects/MyAnimation/temp/
  Creating folder:  /projects/MyAnimation/exports/
  Creating database: /projects/MyAnimation/project_data.db

  Project "MyAnimation" created successfully.
  You are now working inside this project.

supermanim>
```

---

##### Subsubsection 0.4.3.3  — `open project`

**What it does:**

This command opens a project that you already created before. Maybe you worked on a project yesterday
and closed SuperManim. Today you run SuperManim again and you want to continue where you left off.
You use this command to load that project back into memory.

When you type this command, SuperManim:
1. Looks for a folder with the name you give it in the projects directory.
2. Opens the database file inside that folder.
3. Loads all the scene data, audio data, and settings from the database into memory.
4. Sets this project as the "currently active project."

After running this command, you can continue working exactly where you left off.

**Syntax:**

```
open project <project_name>
```

or the shorter version:

```
open <project_name>
```

**Examples:**

```
supermanim> open project MyAnimation
```

```
supermanim> open Chapter1_Intro
```

**What the tool prints back:**

```
supermanim> open project MyAnimation

  Opening project: MyAnimation
  Loading database: /projects/MyAnimation/project_data.db

  Project "MyAnimation" loaded.
  Mode:   supermanim
  Scenes: 5  (3 rendered, 1 pending, 1 failed)
  Audio:  voice.mp3 (60.3 seconds)

  You are now working inside this project.

supermanim>
```

The tool shows you a summary of the project state so you immediately know where things stand.

---

##### Subsubsection 0.4.3.4 — `list projects`

**What it does:**

This command shows you a list of all the recently opened  projects that exist on your computer.
It is useful when you have multiple projects and you cannot remember the exact name
of the one you want to open.

**Syntax:**

```
list projects
```

**What the tool prints back:**

```
supermanim> list projects

  Your projects:
  +-----------------------+---------------+----------+-------------------+
  | Project Name          | Mode          | Scenes   | Last Modified     |
  +-----------------------+---------------+----------+-------------------+
  | MyAnimation           | supermanim    | 5        | 2024-11-12 14:30  |
  | Chapter1_Intro        | simplemanim   | 3        | 2024-11-10 09:15  |
  | LectureEditing        | normal        | -        | 2024-11-08 16:45  |
  +-----------------------+---------------+----------+-------------------+
  Total: 3 projects.

supermanim>
```

---

##### Subsubsection 0.4.3.5 — `project info` `show project info`

**What it does:**

This command shows detailed information about the project that is currently open.
It tells you the project name, the mode, how many scenes there are, the status of each scene,
the audio file, and other settings.

This is a useful command to run at the start of a session to remind yourself of the current state of your project.

**Syntax:**

```
project info
```


```
show project info
```


**What the tool prints back:**

```
supermanim> project info

  ==========================================
  Project: MyAnimation
  ==========================================
  Mode:          supermanim
  Created:       2024-11-10 09:00
  Last modified: 2024-11-12 14:30
  Location:      /projects/MyAnimation/

  AUDIO
  -----
  File:          voice.mp3
  Duration:      60.3 seconds

  SCENES
  ------
  Total:         5
  Rendered:      3
  Pending:       1
  Failed:        1

  Scene 1 | duration: 12.5s | rendered  | scene_01.py
  Scene 2 | duration: 18.5s | rendered  | scene_02.py
  Scene 3 | duration: 16.8s | rendered  | scene_03.py
  Scene 4 | duration:  7.0s | pending   | scene_04.py
  Scene 5 | duration:  5.5s | FAILED    | scene_05.py  [ERROR: NameError on line 12]

  OUTPUT VIDEO
  ------------
  Status: Not assembled yet (1 scene still pending or failed)

  ==========================================

supermanim>
```

---

##### Subsubsection 0.4.3.6  — `close project`

**What it does:**

This command closes the currently active project. The project's data is saved
(it is always saved in the database automatically), and SuperManim returns to
a state where no project is loaded.

You are still inside the SuperManim shell — you have not quit the tool.
You can now open a different project or create a new one.

**Syntax:**

```
close project
```

or just:

```
close
```

**What the tool prints back:**

```
supermanim> close project

  Project "MyAnimation" closed. All data has been saved.

supermanim>
```

---

##### Subsubsection 0.4.3.7 — `delete project`

**What it does:**

This command permanently deletes a project. It removes the project's folder, all the files inside it
(scenes, audio clips, rendered videos, the database), and all the data associated with it.
**This cannot be undone.** The tool will ask you to confirm before it deletes anything.

**Syntax:**


```
delete project <project_name>
```

or

```
delete <project_name>
```



**Example:**

```
supermanim> delete project OldTest
```

**What the tool prints back:**

```
supermanim> delete project OldTest

  WARNING: This will permanently delete the project "OldTest" and all its files.
  This action cannot be undone.

  Are you sure? Type "yes" to confirm, or anything else to cancel:
  > yes

  Deleting project "OldTest"...
  Deleted: /projects/OldTest/

  Project "OldTest" has been permanently deleted.

supermanim>
```

#### Subsection 0.4.4 — Category 2: Scene Commands

##### Subsubsection 0.4.4.1  — What Are Scene Commands?

A **scene** is one section of your video.

Think of your video like a book. Each scene is one chapter of that book.
If your video has 5 scenes, then Scene 1 is the first part that plays, Scene 2 plays after it,
Scene 3 plays after that, and so on until the end.

Each scene holds three things:

```
+----------------------------------------------------------+
|  Every Scene Has:                                        |
|                                                          |
|  1. A DURATION  — how many seconds it lasts.             |
|                  Example: 12.5 seconds.                  |
|                                                          |
|  2. A CODE FILE — the Python file that tells the         |
|                  animation engine what to draw.          |
|                  Example: intro.py                       |
|                                                          |
|  3. An AUDIO CLIP (optional) — the piece of audio        |
|                  that plays while this scene is shown.   |
|                  Example: clip_001.mp3                   |
|                                                          |
+----------------------------------------------------------+
```

Scene commands are the commands that let you build and manage these scenes.
They let you:

- Tell the tool how many scenes your project will have.
- Add new scenes one at a time.
- Set the duration of each scene.
- Assign the animation code file to each scene.
- Look at information about your scenes.
- Delete scenes you do not need anymore.
- Move scenes to a different position.
- Swap two scenes with each other.
- Make a copy of a scene.

---
---

##### Subsubsection 0.4.4.2 — `set scenes_number`

**What it does:**

This command tells the tool how many scenes your project will have.
When you run it, the tool creates that many empty scene slots in the database.

Each slot is like an empty box waiting for you to put things inside it —
a duration, a code file, and later an audio clip.

Think of it like this: you are telling the tool "I am going to make a video with 5 chapters."
The tool then creates 5 empty chapters, all blank, waiting for you to fill them in.

This is almost always the first scene command you run after you create a new project.

**Syntax:**

```
set scenes_number <number>
```

**Examples:**

```
supermanim> set scenes_number 5
```

```
supermanim> set scenes_number 10
```

**What the tool does step by step:**

1. Checks that a project is open. If not, stops and prints an error.
2. Creates `<number>` scene records in the database, all with empty fields.
3. Prints a table showing all the created scenes.

**What the tool prints back:**

```
supermanim> set scenes_number 5

  5 scene slots created.

  +-------+------------+----------+-----------+---------------------+
  | Scene | Duration   | Code     | Audio     | synced_with_audio   |
  +-------+------------+----------+-----------+---------------------+
  |   1   | not set    | not set  | not set   | False               |
  |   2   | not set    | not set  | not set   | False               |
  |   3   | not set    | not set  | not set   | False               |
  |   4   | not set    | not set  | not set   | False               |
  |   5   | not set    | not set  | not set   | False               |
  +-------+------------+----------+-----------+---------------------+

  Next step: Set the duration for each scene.
  Example:   set scene 1 duration 12.5

supermanim>
```

Notice the `synced_with_audio` column. Every new scene starts with `False`.
This means the scene is not linked to any audio clip yet.
This flag will become important later when you work with audio and rendering.

---

##### Subsubsection 0.4.4.3 — `add scene`

**What it does:**

This command adds one single new scene to the project.

It is different from `set scenes_number` which creates many scenes at once.
`add scene` adds exactly one scene at the end of whatever you already have.

For example: if you already have 4 scenes and you type `add scene`, the tool creates Scene 5.

You use this command when you decide you need one more scene after you have already started working.
Maybe you set up 4 scenes, worked on them for a while, and then realized you need a 5th scene at the end.

**Syntax:**

```
add scene
```

You can also add a scene and set its duration at the same time:

```
add scene duration <seconds>
```

**Examples:**

```
supermanim> add scene
```

```
supermanim> add scene duration 15.0
```

**What the tool prints back:**

```
supermanim> add scene

  Scene 5 added.

  +-------+------------+----------+-----------+---------------------+
  | Scene | Duration   | Code     | Audio     | synced_with_audio   |
  +-------+------------+----------+-----------+---------------------+
  |   5   | not set    | not set  | not set   | False               |
  +-------+------------+----------+-----------+---------------------+

supermanim>
```

---

##### Subsubsection 0.4.4.4 — `set scene <n> duration`

**What it does:**

This command tells the tool how long a specific scene lasts.
You give it the scene number and the number of seconds.

The duration is how many seconds the animation for that scene will play on screen.
For example, `set scene 1 duration 12.5` means Scene 1 will play for 12.5 seconds.

This duration matters a lot because:
- The Manim code you write for that scene must produce an animation that lasts exactly this many seconds.
- If you later add audio to this scene, the audio clip must also be exactly this many seconds.

**Syntax:**

```
set scene <scene_number> duration <seconds>
```

**Examples:**

```
supermanim> set scene 1 duration 12.5
supermanim> set scene 2 duration 18.5
supermanim> set scene 3 duration 16.8
supermanim> set scene 4 duration 7.0
supermanim> set scene 5 duration 5.5
```

**What the tool prints back:**

```
supermanim> set scene 1 duration 12.5

  Scene 1 duration set to 12.5 seconds.

  Scene 1 | Duration: 12.5s | Code: not set | Audio: not set | synced_with_audio: False

supermanim>
```

**What happens if you set all 5 durations:**

After you set all your scene durations, the tool can show you the total.

```
supermanim> set scene 5 duration 5.5

  Scene 5 duration set to 5.5 seconds.

  Duration summary:
  Scene 1:  12.5s
  Scene 2:  18.5s
  Scene 3:  16.8s
  Scene 4:   7.0s
  Scene 5:   5.5s
  ----------------------
  Total:    60.3 seconds

supermanim>
```

If you have an audio file loaded, the tool will also check if the total duration matches the audio length.
If they do not match, it will warn you — but it will not stop you. It is just a helpful warning.

---

##### Subsubsection 0.4.4.5 — `set scene <n> code`

**What it does:**

This command assigns a Python code file to a specific scene.
The code file is the file that tells the animation engine (like Manim or Pygame) what to draw for that scene.

When you run this command, the tool does two things:
1. It saves the path to the code file in the database so it knows where to find it later during rendering.
2. It computes a SHA-256 hash of the file — a unique fingerprint — and saves that fingerprint too.
   This fingerprint is used later to detect if you changed the code. If the fingerprint is the same
   as last time, the tool knows the code did not change and can skip re-rendering that scene.

You can use a relative path (a path starting from where you ran SuperManim) or a full absolute path.
Both work exactly the same.

**Syntax:**

```
set scene <scene_number> code <path_to_code_file>
```

**Examples:**

```
supermanim> set scene 1 code my_scenes/intro.py
supermanim> set scene 2 code my_scenes/main_concept.py
supermanim> set scene 3 code my_scenes/example.py
supermanim> set scene 4 code my_scenes/conclusion.py
supermanim> set scene 5 code my_scenes/credits.py
```

**What the tool prints back:**

```
supermanim> set scene 1 code my_scenes/intro.py

  Scene 1 code file assigned.
  File:        my_scenes/intro.py
  Fingerprint: a3f8c2d1e4b9...  (saved for change detection)
  Status:      pending  (ready to render when you want)

supermanim>
```

**What if the file path does not exist?**

```
supermanim> set scene 1 code wrong_path/intro.py

  ERROR: File not found: wrong_path/intro.py
  Please check the path and try again.

supermanim>
```

The tool will not accept a code file that does not exist on your computer.
It checks the file is really there before saving it.

---

##### Subsubsection 0.4.4.6 — `list scenes`

**What it does:**

This command shows you a table of all the scenes in your current project.
For each scene it shows the scene number, the duration, the render status, the code file,
the audio clip, whether it is synced with audio, and any error if the last render failed.

You will use this command very often — it is the quickest way to see the state of your whole project.

**Syntax:**

```
list scenes
```

**What the tool prints back:**

```
supermanim> list scenes

  Scenes in project "MyAnimation":

  +-------+----------+-----------+--------------------+-----------------+--------------------+
  | Scene | Duration | Status    | Code File          | Audio Clip      | synced_with_audio  |
  +-------+----------+-----------+--------------------+-----------------+--------------------+
  |   1   | 12.5s    | rendered  | intro.py           | clip_001.mp3    | True               |
  |   2   | 18.5s    | rendered  | main_concept.py    | clip_002.mp3    | True               |
  |   3   | 16.8s    | rendered  | example.py         | clip_003.mp3    | True               |
  |   4   |  7.0s    | pending   | conclusion.py      | not set         | False              |
  |   5   |  5.5s    | FAILED    | credits.py         | not set         | False              |
  +-------+----------+-----------+--------------------+-----------------+--------------------+

  Total duration: 60.3 seconds
  Rendered: 3  |  Pending: 1  |  Failed: 1

supermanim>
```

---

##### Subsubsection 0.4.4.7 — `show scene <n> info`

**What it does:**

This command shows you the complete, detailed information about one specific scene.
It shows everything the database knows about that scene.

Use this when you want to look closely at one scene — check its duration, its code file,
whether it has audio, whether it is synced, and what its render status is.

**Syntax:**

```
show scene <scene_number> info
```

**Example:**

```
supermanim> show scene 3 info 
```

**What the tool prints back:**

```
supermanim> scene info 3

  ==========================================
  Scene 3 — Full Details
  ==========================================
  Scene Number:        3
  Duration:            16.8 seconds
  Status:              rendered

  CODE FILE
  ---------
  Path:                my_scenes/example.py
  Fingerprint:         c9a1b3e7f2d4...
  Changed since last render: No

  AUDIO
  -----
  Audio clip:          audio_clips/clip_003.mp3
  Audio clip duration: 16.8 seconds
  synced_with_audio:   True

  OUTPUT VIDEO
  ------------
  Path:     output/scene_03/scene_03.mp4
  Rendered: 2024-11-12 at 14:22

  ==========================================

supermanim>
```

---

##### Subsubsection 0.4.4.8 — `delete scene`

**What it does:**
This command permanently removes a scene from your project completely. It deletes two things
at the same time: the scene record from the database, and the scene's physical folder from
your computer's file system. Nothing is kept — the scene duration, the code file path, the
linked audio clip reference, and the entire scene folder are all gone after this command runs.

After deletion, SuperManim automatically reorders all remaining scenes so that the scene
numbers stay continuous with no gaps — both in the database and in the file system folders.

**Syntax:**
```
delete scene <scene_number>
```

**Example:**
```
supermanim> delete scene 2
```

Suppose your project currently has 4 scenes stored in the database and 4 folders on disk:

Database:
```
scene_id    scene_duration    scene_code_path    scene_audio_clip
scene 1     ...               ...                ...
scene 2     ...               ...                ...
scene 3     ...               ...                ...
scene 4     ...               ...                ...
```

File system:
```
scenes/
├── scene_01/
├── scene_02/
├── scene_03/
└── scene_04/
```

After running `delete scene 2`, the tool deletes Scene 2 completely — its database record
and its `scene_02/` folder — then reorders everything that remains:

Database:
```
scene_id    scene_duration    scene_code_path    scene_audio_clip
scene 1     ...               ...                ...
scene 2     ...               ...                ...
scene 3     ...               ...                ...
```

File system:
```
scenes/
├── scene_01/
├── scene_02/
└── scene_03/
```

The old Scene 3 is now Scene 2, and the old Scene 4 is now Scene 3 — in both the database
and on disk. The project has shrunk from 4 scenes to 3 scenes.

**What the tool prints back:**
```
supermanim> delete scene 5
  Scene 5 removed from the project.
  The scene folder has been deleted from your computer.
  The project now has 4 scenes.
supermanim>
```

---

##### Subsubsection 0.4.4.9 — `move scene`

**What it does:**
This command moves a scene from its current position to a new position in the scene order.
The move affects two things at the same time: the scene records inside the database, and the
scene folders on your computer's file system. Both are fully reordered after every move.

When you move a scene, SuperManim does not simply swap two scenes. Instead, it shifts all
the scenes between the old position and the new position to fill the gap cleanly. The result
is a continuous, gap-free order — in the database and on disk.

For example: if you have 5 scenes and you move Scene 5 to position 2, the scene that was
in position 5 becomes the new Scene 2. Every scene that was between position 2 and position 4
shifts one step forward to fill the gap left behind.

**Syntax:**
```
move scene <scene_number> to <new_position>
```

**Example:**
```
supermanim> move scene 5 to 2
```

Suppose your project currently has 5 scenes in the database and 5 folders on disk:

Database (before):
```
scene_id    scene_duration    scene_code_path    scene_audio_clip
scene 1     ...               ...                ...
scene 2     ...               ...                ...
scene 3     ...               ...                ...
scene 4     ...               ...                ...
scene 5     ...               ...                ...
```

File system (before):
```
scenes/
├── scene_01/
├── scene_02/
├── scene_03/
├── scene_04/
└── scene_05/
```

After running `move scene 5 to 2`, SuperManim takes the old Scene 5 and inserts it at
position 2. Every scene that was at position 2 or later shifts one step forward to
accommodate it:

Database (after):
```
scene_id    scene_duration    scene_code_path    scene_audio_clip
scene 1     ...               ...                ...      <- unchanged
scene 2     ...               ...                ...      <- was scene 5
scene 3     ...               ...                ...      <- was scene 2
scene 4     ...               ...                ...      <- was scene 3
scene 5     ...               ...                ...      <- was scene 4
```

File system (after):
```
scenes/
├── scene_01/    <- unchanged
├── scene_02/    <- was scene_05/
├── scene_03/    <- was scene_02/
├── scene_04/    <- was scene_03/
└── scene_05/    <- was scene_04/
```

The total number of scenes does not change. No scene is lost. Only the order changes.

**What the tool prints back:**
```
supermanim> move scene 5 to 2
  Scene 5 moved to position 2.
  All scenes renumbered in the database and on disk.
  New order:
  +----------+-------------------+
  | New Num  | Was Scene Number  |
  +----------+-------------------+
  |    1     |       1           |
  |    2     |       5  <-- moved|
  |    3     |       2           |
  |    4     |       3           |
  |    5     |       4           |
  +----------+-------------------+
supermanim>
```

---

---

##### Subsubsection 0.4.4.10 — `swap scenes`

**What it does:**

This command swaps the positions of two scenes.
Scene A goes where Scene B was, and Scene B goes where Scene A was.
Nothing else moves.

This is simpler than `move scene` when you just want to exchange exactly two scenes.

**Syntax:**

```
swap scenes <scene_number_a> <scene_number_b>
```

**Example:**

```
supermanim> swap scenes 2 4
```

**What the tool prints back:**

```
supermanim> swap scenes 2 4

  Scene 2 and Scene 4 have been swapped.

  Scene 2 now contains: what was previously in Scene 4.
  Scene 4 now contains: what was previously in Scene 2.

supermanim>
```

---

##### Subsubsection 0.4.4.11 — `duplicate scene`

**What it does:**

This command makes a copy of an existing scene and adds it as a new scene at the end of your project.
The copy gets the next available scene number.

The copy starts with the same code file path as the original, but its render status is reset to `pending`
because it has never been rendered.Its audio clip is not copied — audio must be assigned separately.

This is useful when two or more scenes use the same code file as a starting point.
You duplicate one, then make small changes to the copy.

**Syntax:**

```
duplicate scene <scene_number>
```

**Example:**

```
supermanim> duplicate scene 3
```

**What the tool prints back:**

```
supermanim> duplicate scene 3

  Scene 3 duplicated.

  New scene created: Scene 6
  Code file:         my_scenes/example.py  (copied from Scene 3)
  Duration:          16.8 seconds          (copied from Scene 3)
  Audio clip:        not set               (must be assigned separately)
  synced_with_audio: False
  Status:            pending

supermanim>
```

---

---

#### Subsection 0.4.5 — Category 3: Audio Commands

##### Subsubsection 0.4.5.1 — What Are Audio Commands?

Audio commands are the commands you use to work with audio files in your project.

They let you do two different kinds of things:

**Kind 1 — Audio File Editing:**
You can use SuperManim to edit an audio file by itself, without any animation.
You can cut it, split it into pieces, change its format, or check how long it is.
This works like a simple audio editing tool.

**Kind 2 — Audio for Animation:**
You can add an audio file to your project and link each piece of it to a scene.
Later, when you render a scene that has been linked to audio and marked as synced,
the tool will include that audio in the rendered video.

Both kinds need the same starting point: you must have a project open first.
Before anything else, understand this rule. It applies to every audio command and every render:

```
+------------------------------------------------------------------+
|                  THE GOLDEN RULE                                 |
|                                                                  |
|  If a scene has an audio clip AND is synced with it:            |
|                                                                  |
|  Scene duration  ==  Audio clip duration                         |
|                                                                  |
|  Example:                                                        |
|  Scene 3 duration:        16.8 seconds                           |
|  Scene 3 audio clip:      16.8 seconds                           |
|                                                                  |
|  They must be IDENTICAL.                                         |
|  Not 16.7. Not 16.9. Exactly 16.8.                               |
|                                                                  |
|  If they are different:                                          |
|  The tool will REFUSE to render and will tell you what is wrong. |
|                                                                  |
+------------------------------------------------------------------+
```

Why? Because if the video is 16.8 seconds but the audio is 17.2 seconds,
the video will end before the audio finishes. They will not match.
The tool prevents this from happening by checking before every render.

---

**The `synced_with_audio` Flag**

Every scene in the database has a column called `synced_with_audio`.
It holds one of two values: `True` or `False`.

```
+----------------------------------------------------------+
|  synced_with_audio = False  (default for all new scenes) |
|                                                          |
|  This scene has NO audio linked to it.                   |
|  When rendered, it will produce a video with NO sound.   |
|                                                          |
+----------------------------------------------------------+
|  synced_with_audio = True                                |
|                                                          |
|  This scene IS linked to an audio clip.                  |
|  The durations have been verified to match.              |
|  When rendered, it will produce a video WITH sound.      |
|                                                          |
+----------------------------------------------------------+
```

This flag is what the render system checks before every render.
You change this flag using the Sync Commands (covered in Subsection 0.4.6).

The audio commands below are what you use to add and manage the audio files themselves.
The sync commands are what you use to link those audio files to scenes and set this flag.

---

**Before Every Audio Command**

Every audio command checks two things before doing anything:

```
CHECK 1: Is a project open?
    YES --> continue.
    NO  --> stop. Print "No project is open. Please open a project first."

CHECK 2: Is an audio file loaded in this project?
    (only for commands that need it — not for "add audio")
    YES --> continue.
    NO  --> stop. Print "No audio file has been added to this project yet.
                         Use: add audio <path_to_audio_file>"
```

---

##### Subsubsection 0.4.5.2 — `add audio` or `add audio_file`

**What it does:**

This command loads your audio file into the project.This is the first audio command you will ever run
in a project.Before you split audio, before you sync anything — you must add the audio file first.

When you run this command, the tool:
1. Copies your audio file into the project's `audio_clips/` folder.
   It saves it there as `original_audio` with the same file extension you gave it.
2. Reads the total duration of the audio file in seconds.
3. Saves the file path and the duration in the project database.

After this command, the tool knows about your audio file.
You can then split it, edit it, or link it to scenes.

**Syntax:**

```
add audio <path_to_audio_file>
```

You can also write:

```
add audio_file <path_to_audio_file>
```

Both forms do exactly the same thing. The second form is just an alternative way to write it.

**Examples:**

```
supermanim> add audio voice.mp3
```

```
supermanim> add audio /home/user/recordings/narration.wav
```

```
supermanim> add audio_file C:/Users/Ahmed/Desktop/lecture.mp3
```

**What the tool prints back:**

```
supermanim> add audio voice.mp3

  Audio file added successfully.

  Copied to:   audio_clips/original_audio.mp3
  Format:      mp3
  Duration:    60.3 seconds
  Channels:    mono
  Sample rate: 44100 Hz

  What you can do next:
  - Edit this file:    change audio_format wav
  - Split it:          split audio auto
  - Split manually:    split audio half
                       split audio duration 12.5 18.5 16.8 7.0 5.5

supermanim>
```

---

##### Subsubsection 0.4.5.3 — `change audio_format`

**What it does:**

This command converts the audio file from its current format to a new format.
For example, you can convert an `.mp3` file to a `.wav` file, or a `.wav` to an `.ogg`.

You might want to do this because:
- Your animation engine works better with a specific format.
- You want a lossless format like `.wav` for higher quality.
- You want to reduce file size by converting to a more compressed format.

The tool converts the original audio file and saves the new version in the `audio_clips/` folder.
The old file is kept unless you ask the tool to replace it.

**Syntax:**

```
change audio_format <new_format>
```


**Examples:**

```
supermanim> change audio_format wav
```

```
supermanim> change audio_format ogg
```

```
supermanim> change audio_format mp3
```

**Supported formats:** `mp3`, `wav`, `ogg`, `aac`, `flac`, `m4a`

**What the tool prints back:**

```
supermanim> change audio_format wav

  Converting: original_audio.mp3  -->  original_audio.wav
  Format:     mp3 (lossy, compressed)  -->  wav (lossless, uncompressed)
  Old size:   4.2 MB
  New size:   31.8 MB

  Conversion complete.
  New file saved: audio_clips/original_audio.wav

supermanim>
```

---

##### Subsubsection 0.4.5.4 — `split audio auto`

**What it does:**

This command listens to your audio file and splits it into pieces automatically.
The tool finds the quiet parts — the silences — and treats each silence as the border
between one scene and the next.

Think of it like this: your narration sounds like this:
```
[...speaking for 12 seconds...] [silence] [speaking for 18 seconds] [silence] [speaking for 17 seconds]
```

The tool hears that there are two silences in between the speaking parts.
So it decides there are three sections, and it cuts the audio at those silences.
Each section becomes the audio clip for one scene.

After the tool finishes, it:
- Creates scene slots in the database for however many sections it found.
- Sets each scene's duration to match the length of its audio section.
- Saves each audio section as a separate clip file in the `audio_clips/` folder.

**Syntax:**

```
split audio auto
```

You can also adjust the sensitivity of the silence detection:

```
split audio auto --min_silence 0.5 --threshold -40
```

- `--min_silence 0.5` means: a silent gap must be at least 0.5 seconds long to count as a scene boundary.
  If you set this too low, every tiny pause becomes a new scene. If you set it too high, some boundaries get missed.
- `--threshold -40` means: anything quieter than -40 decibels is counted as silence.The more negative the number,
 the stricter the definition of silence.

If you do not include these options, the tool uses its default values, which work well for most voice recordings.

**What the tool prints back:**

```
supermanim> split audio auto

  Analyzing: audio_clips/original_audio.mp3 (60.3 seconds)
  Scanning for silence regions...

  Found 5 speech segments:

  +----------+---------+---------+-----------+
  | Segment  | Start   | End     | Duration  |
  +----------+---------+---------+-----------+
  |    1     |  0.0s   | 12.5s   |  12.5s    |
  |    2     | 12.5s   | 31.0s   |  18.5s    |
  |    3     | 31.0s   | 47.8s   |  16.8s    |
  |    4     | 47.8s   | 54.8s   |   7.0s    |
  |    5     | 54.8s   | 60.3s   |   5.5s    |
  +----------+---------+---------+-----------+

  Cutting audio into 5 clips...

  clip_001.mp3 saved  (12.5 sec)
  clip_002.mp3 saved  (18.5 sec)
  clip_003.mp3 saved  (16.8 sec)
  clip_004.mp3 saved   (7.0 sec)
  clip_005.mp3 saved   (5.5 sec)

  5 scenes created. Durations set automatically.
  Total: 60.3 seconds (matches original audio length exactly).

  Note: Scenes are created but NOT yet synced with audio.
  Use:  sync all   to sync all scenes with their clips.
  Or:   sync scene <n> audio_clip <n>   to sync one by one.

supermanim>
```

---

##### Subsubsection 0.4.5.5 — `split audio half`

**What it does:**

This command cuts the audio file exactly in half.The result is two equal pieces.
Each piece is exactly half the length of the original.

For example: if your audio is 60 seconds long, this command creates:
- Clip 1: 0.0 seconds to 30.0 seconds (30 seconds long).
- Clip 2: 30.0 seconds to 60.0 seconds (30 seconds long).

Use this when you have two scenes and you want to divide the audio equally between them.

**Syntax:**

```
split audio half
```

**What the tool prints back:**

```
supermanim> split audio half

  Splitting audio_clips/original_audio.mp3 into two equal halves.
  Original duration: 60.3 seconds
  Each half:         30.15 seconds

  clip_001.mp3 saved  (0.0s to 30.15s  |  30.15 sec)
  clip_002.mp3 saved  (30.15s to 60.3s |  30.15 sec)

  2 scenes created. Durations set automatically.
  Total: 60.3 seconds.

  Note: Scenes are created but NOT yet synced with audio.
  Use:  sync all   to link scenes to their clips.

supermanim>
```

---

##### Subsubsection 0.4.5.6 — `split audio duration`

**What it does:**

This command lets you split the audio into pieces of specific lengths that you choose yourself.
You provide the duration (length in seconds) of each piece you want.

The tool will cut the audio into that many pieces with those exact lengths.
The durations you provide must add up to the total length of the audio file.
If they do not add up, the tool will stop and tell you.

For example: your audio is 60.3 seconds and you want 5 pieces of specific lengths.
You tell the tool: `split audio duration 12.5 18.5 16.8 7.0 5.5`
That adds up to 12.5 + 18.5 + 16.8 + 7.0 + 5.5 = 60.3 seconds. It matches. The tool will proceed.

**Syntax:**

```
split audio duration <d1> <d2> <d3> ...
```

You provide as many durations as you need. Each number is in seconds.

**Example:**

```
supermanim> split audio duration 12.5 18.5 16.8 7.0 5.5
```

**What the tool does step by step:**

1. Adds up all the numbers you provided: 12.5 + 18.5 + 16.8 + 7.0 + 5.5 = 60.3 seconds.
2. Checks if that total matches the audio file's duration (60.3 seconds).
3. If they match, it cuts the audio.
4. If they do NOT match, it stops and tells you the difference.

**What the tool prints back (success):**

```
supermanim> split audio duration 12.5 18.5 16.8 7.0 5.5

  Checking durations...
  Your total:   60.3 seconds
  Audio length: 60.3 seconds
  Match: YES

  Cutting audio into 5 clips...

  +----------+---------+---------+-----------+----------------------+
  | Clip     | Start   | End     | Duration  | File                 |
  +----------+---------+---------+-----------+----------------------+
  |    1     |  0.0s   | 12.5s   |  12.5s    | clip_001.mp3         |
  |    2     | 12.5s   | 31.0s   |  18.5s    | clip_002.mp3         |
  |    3     | 31.0s   | 47.8s   |  16.8s    | clip_003.mp3         |
  |    4     | 47.8s   | 54.8s   |   7.0s    | clip_004.mp3         |
  |    5     | 54.8s   | 60.3s   |   5.5s    | clip_005.mp3         |
  +----------+---------+---------+-----------+----------------------+

  5 scenes created. Durations set automatically.

  Note: Scenes are created but NOT yet synced with audio.
  Use:  sync all   to link scenes to their clips.

supermanim>
```

**What the tool prints back (durations do not match):**

```
supermanim> split audio duration 12.5 18.5 16.8 7.0 10.0

  Checking durations...
  Your total:   64.8 seconds
  Audio length: 60.3 seconds
  Difference:  +4.5 seconds (your total is too long)

  ERROR: The durations you provided do not add up to the audio length.
  Please fix the numbers and try again.

supermanim>
```

---

##### Subsubsection 0.4.5.7 — `show audio info`

**What it does:**

This command shows you a complete overview of the audio situation in your project.
It shows the original audio file, its length, and for each scene: which audio clip is assigned,
what time range it covers, and whether the scene is synced with the audio.

Use this command to check the current state of your audio before syncing or rendering.

**Syntax:**

```
audio info
```

or

```
show audio info
```



**What the tool prints back:**

```
supermanim> audio info

  AUDIO OVERVIEW — Project: MyAnimation
  ========================================
  Original file       :   audio_clips/original_audio.mp3
  Total audio duration:   60.3 seconds
  Format              :   mp3

  SCENE AUDIO MAP
  +---------+-----------+-----------+-----------+-----------------+--------------------+
  | Scene   | Start     | End       | Duration  | Clip File       | synced_with_audio  |
  +---------+-----------+-----------+-----------+-----------------+--------------------+
  |   1     |   0.0s    |  12.5s    |  12.5s    | clip_001.mp3    | True               |
  |   2     |  12.5s    |  31.0s    |  18.5s    | clip_002.mp3    | True               |
  |   3     |  31.0s    |  47.8s    |  16.8s    | clip_003.mp3    | True               |
  |   4     |  47.8s    |  54.8s    |   7.0s    | not set         | False              |
  |   5     |  54.8s    |  60.3s    |   5.5s    | not set         | False              |
  +---------+-----------+-----------+-----------+-----------------+--------------------+

  Synced scenes:    3 out of 5
  Unsynced scenes:  2 (Scenes 4 and 5 have no audio clip assigned)

supermanim>
```

---

---

#### Subsection 0.4.6 — Category 4: Render Commands

##### Subsubsection 0.4.6.1 — What Are Render Commands?

Rendering is the process of turning your Python code file into a real video file.

When you render a scene, the tool runs your code through an animation engine like Manim.
The engine reads your code, draws all the shapes and animations you wrote, and produces
an `.mp4` video file. That file is saved in the `output/` folder of your project.

Render commands control everything about this process:
- Which scenes to render.
- Whether to skip scenes that have not changed.
- Whether to force a re-render even if nothing changed.
- Whether to generate a fast, low-quality preview instead of the final render.
- What to do with scenes that failed.

---

**Before Every Render: What the Tool Always Checks**

Before the tool renders anything, it runs through a checklist.
If any check fails, the tool stops and tells you exactly what needs to be fixed.

```
+--------------------------------------------------------------------+
|  RENDER CHECKLIST — runs before EVERY render command              |
|                                                                    |
|  CHECK 1: Is a project open?                                       |
|  YES --> continue.                                                 |
|  NO  --> STOP. "No project is open."                               |
|                                                                    |
|  CHECK 2: Does this scene have a code file assigned?               |
|  YES --> continue.                                                 |
|  NO  --> STOP. "Scene X has no code file. Use: set scene X code." |
|                                                                    |
|  CHECK 3: Is synced_with_audio = True for this scene?              |
|  YES --> also check audio duration matches scene duration.         |
|          If they match   --> render WITH audio.                    |
|          If they don't   --> STOP. "Duration mismatch."            |
|  NO  --> render WITHOUT audio. (Silent video. That is fine.)      |
|                                                                    |
|  CHECK 4: Has the code changed since the last render?              |
|  (Checked by comparing the current file fingerprint                |
|   to the stored fingerprint in the database.)                      |
|  YES, changed    --> render.                                       |
|  NO, unchanged   --> skip render. Use the old video. Save time.    |
|                                                                    |
+--------------------------------------------------------------------+
```

This checklist is the heart of SuperManim's smart behavior.
It is what makes SuperManim faster than running Manim directly.

---

**How the Tool Knows If Code Changed (The Fingerprint System)**

Every time you assign a code file to a scene, the tool computes a SHA-256 hash of that file.
Think of a hash as a unique fingerprint — like a person's fingerprint, but for a file.

```
+----------------------------------------------------------+
|  HOW THE FINGERPRINT SYSTEM WORKS                        |
|                                                          |
|  You assign a code file to Scene 3.                      |
|  The tool reads the file and computes its fingerprint:   |
|  Fingerprint = "a3f8c2d1e4b9..."                         |
|  This fingerprint is saved in the database.              |
|                                                          |
|  You render Scene 3. It succeeds.                        |
|                                                          |
|  Later, you run "render scene 3" again.                  |
|  The tool reads the file again and computes a new print: |
|  New fingerprint = "a3f8c2d1e4b9..."  (same as before!)  |
|                                                          |
|  The file did not change. Skip the render.               |
|                                                          |
|  ---                                                     |
|                                                          |
|  Now you edit scene3.py and change one line.             |
|  You run "render scene 3" again.                         |
|  New fingerprint = "f7c3a9e1b2d8..."  (DIFFERENT!)       |
|                                                          |
|  The file changed. Render it.                            |
|                                                          |
+----------------------------------------------------------+
```

This is why SuperManim can save you hours of rendering time.
It only renders the scenes that actually changed.

---

##### Subsubsection 0.4.6.2 — `render scene`

**What it does:**

This command renders one specific scene.

The tool first runs the render checklist described above.
If the code has not changed since the last render, the tool skips it and tells you.
If the code changed, the tool runs the animation engine to produce a new video clip.

**Syntax:**

```
render scene <scene_number>
```

**Example:**

```
supermanim> render scene 3
```

**What the tool prints back — when the scene needs rendering:**

```
supermanim> render scene 3

  Render checklist for Scene 3:
  [OK] Project is open.
  [OK] Code file assigned: my_scenes/example.py
  [OK] Code has changed since last render. (fingerprint different)
  [OK] synced_with_audio: True  |  Durations match: 16.8s == 16.8s

  Rendering Scene 3 with audio...
  Running animation engine...
  [===========================================] 100%  (Elapsed: 4m 12s)

  Scene 3 rendered successfully.
  Output:   output/scene_03/scene_03.mp4
  Duration: 16.8 seconds  (matches expected duration)
  Audio:    clip_003.mp3 included.

supermanim>
```

**What the tool prints back — when the scene has NOT changed:**

```
supermanim> render scene 3

  Render checklist for Scene 3:
  [OK] Project is open.
  [OK] Code file assigned: my_scenes/example.py
  [--] Code unchanged (fingerprint matches). Skipping render.

  Scene 3 skipped. (Saved approximately 4 minutes of rendering time.)

supermanim>
```

**What the tool prints back — when the scene has audio but durations do not match:**

```
supermanim> render scene 4

  Render checklist for Scene 4:
  [OK] Project is open.
  [OK] Code file assigned: my_scenes/conclusion.py
  [OK] Code has changed since last render.
  [!!] synced_with_audio: True  |  Duration mismatch!
       Scene duration:      7.0 seconds
       Audio clip duration: 9.3 seconds
       Difference:          2.3 seconds

  ERROR: Cannot render Scene 4.
  The scene duration and audio clip duration do not match.
  Fix the scene duration:  set scene 4 duration 9.3
  Or fix the sync:         unsync scene 4

supermanim>
```

**What the tool prints back — when synced_with_audio is False:**

```
supermanim> render scene 4

  Render checklist for Scene 4:
  [OK] Project is open.
  [OK] Code file assigned: my_scenes/conclusion.py
  [OK] Code has changed since last render.
  [  ] synced_with_audio: False  -->  Rendering WITHOUT audio (silent video).

  Rendering Scene 4 without audio...
  [===========================================] 100%  (Elapsed: 2m 03s)

  Scene 4 rendered successfully (silent video).
  Output:   output/scene_04/scene_04.mp4
  Duration: 7.0 seconds
  Audio:    none.

supermanim>
```

---

##### Subsubsection 0.4.6.3 — `render all`

**What it does:**

This command goes through every scene in your project and renders the ones that need it.
It is the most commonly used render command.

For each scene, the tool runs the full render checklist.
Scenes whose code has not changed since the last render are skipped automatically.
Only the scenes whose code actually changed get rendered.

This is the command you will type the most often in your workflow.
After making changes to one or two scenes, you type `render all` and the tool handles everything.

**Syntax:**

```
render all
```

**What the tool prints back:**

```
supermanim> render all

  Checking all 5 scenes...

  +-------+-----------------------------+--------------------+
  | Scene | Code Changed?               | Action             |
  +-------+-----------------------------+--------------------+
  |   1   | No  (fingerprint matches)   | SKIP               |
  |   2   | No  (fingerprint matches)   | SKIP               |
  |   3   | No  (fingerprint matches)   | SKIP               |
  |   4   | YES (fingerprint changed)   | RENDER             |
  |   5   | No  (fingerprint matches)   | SKIP               |
  +-------+-----------------------------+--------------------+

  Rendering Scene 4...
  [===========================================] 100%  (Elapsed: 2m 03s)
  Scene 4 rendered. Output: output/scene_04/scene_04.mp4

  Render complete.
  Rendered:     1 scene  (Scene 4)
  Skipped:      4 scenes (no changes detected)
  Time saved:   approximately 17 minutes

supermanim>
```

---

##### Subsubsection 0.4.6.4 — `render changed`

**What it does:**

This command renders only the scenes whose status is `pending` or `failed`.
It does not re-check the fingerprint — it simply looks at the status field in the database
and renders anything that is not already marked as `rendered`.

This is different from `render all` in a subtle way:
- `render all` checks the fingerprint. If the code is unchanged, it skips even if status is `pending`.
- `render changed` skips the fingerprint check and just looks at the status.

Use `render changed` when you want to render all the scenes that are waiting,
without worrying about whether the code changed or not.

**Syntax:**

```
render changed
```

**What the tool prints back:**

```
supermanim> render changed

  Scanning for pending or failed scenes...

  Found:
    Scene 4 — status: pending
    Scene 5 — status: failed

  Rendering Scene 4...
  [===========================================] 100%  (Elapsed: 2m 03s)
  Scene 4 rendered successfully.

  Rendering Scene 5 (retrying after previous failure)...
  [===========================================] 100%  (Elapsed: 1m 44s)
  Scene 5 rendered successfully.

  All pending and failed scenes have been rendered.

supermanim>
```

---

##### Subsubsection 0.4.6.5 — `force render scene`

**What it does:**

This command forces a specific scene to be rendered again, even if the code has not changed.

Normally, the tool skips scenes whose fingerprint has not changed.This command overrides that skip completely.

Use this when:
- You changed an asset file that your code uses (like an image or a font),
  but the Python code file itself stayed the same.
  The fingerprint check would say "unchanged" — but the actual output would be different.
  So you force the render.
- You want a completely fresh render for any other reason.

**Syntax:**

```
force render scene <scene_number>
```

**Example:**

```
supermanim> force render scene 3
```

**What the tool prints back:**

```
supermanim> force render scene 3

  Force rendering Scene 3. (Ignoring fingerprint check.)

  Render checklist for Scene 3:
  [OK] Project is open.
  [OK] Code file assigned: my_scenes/example.py
  [OK] synced_with_audio: True  |  Durations match: 16.8s == 16.8s

  Rendering Scene 3 with audio...
  [===========================================] 100%  (Elapsed: 4m 22s)

  Scene 3 rendered successfully.
  Output: output/scene_03/scene_03.mp4

supermanim>
```

---

##### Subsubsection 0.4.6.6 — `force render all`

**What it does:**

This command forces every single scene to be re-rendered from scratch.
It wipes the stored fingerprints for all scenes, marks every scene as `pending`,
and then renders them all.

This is the "burn it all down and start fresh" command for rendering.

Use this when:
- You changed a global setting that affects all scenes, like the output video resolution or the frame rate.
- Something seems wrong with your rendered videos and you want a completely clean rebuild.
- You just want to be absolutely sure that every single scene is fresh.

This command takes a long time if you have many scenes. The tool will warn you before it starts
and ask you to confirm.

**Syntax:**

```
force render all
```

**What the tool prints back:**

```
supermanim> force render all

  WARNING: This will re-render ALL 5 scenes from scratch.
  Estimated time: 18 to 25 minutes.
  This cannot be undone.

  Type "yes" to continue, or anything else to cancel:
  > yes

  Clearing all stored fingerprints...
  Resetting all scenes to pending...
  Starting full render...

  Rendering Scene 1...  [===================] 100%  (4m 10s)
  Rendering Scene 2...  [===================] 100%  (6m 02s)
  Rendering Scene 3...  [===================] 100%  (4m 22s)
  Rendering Scene 4...  [===================] 100%  (2m 03s)
  Rendering Scene 5...  [===================] 100%  (1m 44s)

  All 5 scenes rendered successfully.
  Total time: 18 minutes 21 seconds.

supermanim>
```



##### Subsubsection 0.4.6.7 — `render status`

**What it does:**

This command shows you a quick summary of where your rendering stands.
How many scenes are rendered? How many are still waiting? How many failed?
It also tells you whether the project is ready to be exported.

**Syntax:**

```
render status
```

**What the tool prints back:**

```
supermanim> render status

  Render Status — MyAnimation
  ============================
  Total scenes:   5
  Rendered:       3
  Pending:        1
  Failed:         1

  +-------+----------+-----------+--------------------+
  | Scene | Duration | Status    | Notes              |
  +-------+----------+-----------+--------------------+
  |   1   | 12.5s    | rendered  |                    |
  |   2   | 18.5s    | rendered  |                    |
  |   3   | 16.8s    | rendered  |                    |
  |   4   |  7.0s    | pending   | not yet rendered   |
  |   5   |  5.5s    | FAILED    | NameError line 12  |
  +-------+----------+-----------+--------------------+

  Ready to export: NO
  Reason: 1 scene pending, 1 scene failed.

supermanim>
```
---

##### Subsubsection 0.4.6.8 — `render failed`

**What it does:**

This command finds all the scenes that have a `failed` status and tries to render them again.

When a scene fails, the tool saves the error message in the database.
This command clears those error messages, marks the failed scenes as `pending` again,
and runs the render checklist on each one.

Use this after you have fixed whatever caused the failure —
for example, you fixed a bug in the code file that caused Manim to crash.

**Syntax:**

```
render failed
```

**What the tool prints back:**

```
supermanim> retry failed

  Found 2 failed scenes: Scene 2, Scene 5.

  Retrying Scene 2...
  Clearing previous error message...
  Running render checklist...
  [OK] Code file: my_scenes/main_concept.py
  [OK] synced_with_audio: True  |  Durations match.
  Rendering...
  [===========================================] 100%  (Elapsed: 6m 07s)
  Scene 2 rendered successfully.

  Retrying Scene 5...
  Clearing previous error message...
  Running render checklist...
  [OK] Code file: my_scenes/credits.py
  [  ] synced_with_audio: False  -->  Rendering without audio (silent).
  Rendering...
  [===========================================] 100%  (Elapsed: 1m 44s)
  Scene 5 rendered successfully (silent video).

  Both failed scenes have been rendered successfully.

supermanim>
```

---



#### Subsection 0.4.7 — Category 5: Preview Commands
##### Subsubsection 0.4.7.1 — What Are Preview Commands?

A preview is a fast, low-quality version of a rendered scene.

When you render a scene normally using `render scene`, the tool produces a high-quality
video file. That process can take several minutes per scene. If you only want to check
whether your animation looks roughly correct — whether the shapes are in the right place,
whether the motion looks right, whether the timing feels good — waiting several minutes
every time you make a small change is slow and frustrating.

Preview commands solve this by running the animation engine in a special low-quality mode.
The output is smaller, blurrier, and lower resolution than a real render. But it is ready
in seconds instead of minutes. You look at it, decide whether things look right, fix
whatever is wrong, and preview again. Once you are satisfied, you run the real render.

Preview files are saved in the `previews/` folder of your project.
They are completely separate from your final rendered video files in the `output/` folder.
Preview files are never used in the final exported video. They are for your eyes only.

---

**What "Low Quality" Means**

When the tool generates a preview, it intentionally reduces quality in several ways to
make the process faster:

```
+----------------------------------------------------------+
|  PREVIEW vs FINAL RENDER — The Differences              |
|                                                          |
|  Resolution:                                             |
|    Final render:   1080p  (1920 x 1080 pixels)          |
|    Preview:         480p  ( 854 x  480 pixels)          |
|                                                          |
|  Total pixels:                                           |
|    Final render:   2,073,600 pixels per frame            |
|    Preview:          409,920 pixels per frame            |
|    That is about 5x fewer pixels to compute.            |
|                                                          |
|  Time to render Scene 4 (7.0 seconds of animation):     |
|    Final render:   approximately 2 to 4 minutes          |
|    Preview:        approximately 15 to 20 seconds        |
|                                                          |
+----------------------------------------------------------+
```

The lower resolution is what makes the preview fast.Less pixels per frame means less work for the animation
engine.Less work means the file is ready in seconds instead of minutes.

---

**Where Preview Files Are Saved**

```
MyAnimation/
├── output/              ← Final rendered videos go here
│   ├── scene_01/
│   │   └── scene_01.mp4
│   ├── scene_02/
│   │   └── scene_02.mp4
│   └── ...
│
├── previews/            ← Preview files go here
│   ├── scene_01_preview.mp4
│   ├── scene_04_preview.mp4
│   └── ...
│
├── audio/
└── project.db
```

The `output/` folder holds your real, final, high-quality video clips.
These are the clips that get assembled when you run `export`.

The `previews/` folder holds your quick, temporary, low-quality check files.
These are never included in any export. They exist only for you to review.

---

**Before Every Preview: What the Tool Always Checks**

Before the tool generates any preview, it runs a short checklist.
If any check fails, the tool stops and tells you what needs to be fixed.

```
+--------------------------------------------------------------------+
|  PREVIEW CHECKLIST — runs before EVERY preview command            |
|                                                                    |
|  CHECK 1: Is a project open?                                       |
|  YES --> continue.                                                 |
|  NO  --> STOP. "No project is open."                               |
|                                                                    |
|  CHECK 2: Does this scene have a code file assigned?               |
|  YES --> continue.                                                 |
|  NO  --> STOP. "Scene X has no code file. Use: set scene X code." |
|                                                                    |
+--------------------------------------------------------------------+
```

Notice that the preview checklist is shorter than the render checklist.
The preview does not check audio sync or duration matching.
This is intentional — a preview is a rough visual check.
Audio synchronization is only verified during the real render.

---

##### Subsubsection 0.4.7.2 — `preview scene`

**What it does:**

This command generates a fast, low-quality preview of one specific scene.

The tool runs the animation engine in low-quality mode on that scene's code file.
The result is saved as an `.mp4` file in the `previews/` folder.
The tool does not check whether the code changed or not — it always generates a new preview
when you ask for one.

**Syntax:**

```
preview scene <scene_number>
```

**Example:**

```
supermanim> preview scene 4
```

**What the tool prints back:**

```
supermanim> preview scene 4

  Preview checklist for Scene 4:
  [OK] Project is open.
  [OK] Code file assigned: my_scenes/conclusion.py

  Generating low-quality preview for Scene 4...
  (This will be fast. Preview quality is intentionally low.)

  Running animation engine (low quality mode)...
  [===========================================] 100%  (Elapsed: 0m 18s)

  Preview ready: previews/scene_04_preview.mp4
  Duration:      7.0 seconds
  Quality:       low (480p)

  Tip: When you are happy with the preview, run:
       render scene 4
       (This produces the final high-quality version.)

supermanim>
```

**What the tool prints back — when no code file is assigned:**

```
supermanim> preview scene 4

  Preview checklist for Scene 4:
  [OK] Project is open.
  [!!] No code file assigned to Scene 4.

  ERROR: Cannot preview Scene 4.
  Assign a code file first:  set scene 4 code <path_to_file.py>

supermanim>
```

---

##### Subsubsection 0.4.7.3 — `preview all`

**What it does:**

This command generates a low-quality preview for every scene in the project, one by one.

It runs the preview checklist for each scene. If a scene has no code file assigned,
the tool skips that scene, reports it, and moves on to the next one.
It does not stop the entire operation just because one scene is not ready.

Use this when you want a quick look at your entire project from start to finish
without waiting for a full render of everything.

**Syntax:**

```
preview all
```

**What the tool prints back:**

```
supermanim> preview all

  Generating previews for all 5 scenes...

  +-------+------------------------------+--------------------+
  | Scene | Code File                    | Action             |
  +-------+------------------------------+--------------------+
  |   1   | my_scenes/intro.py           | PREVIEW            |
  |   2   | my_scenes/main_concept.py    | PREVIEW            |
  |   3   | my_scenes/example.py         | PREVIEW            |
  |   4   | my_scenes/conclusion.py      | PREVIEW            |
  |   5   | not assigned                 | SKIP               |
  +-------+------------------------------+--------------------+

  Previewing Scene 1...
  [===========================================] 100%  (Elapsed: 0m 22s)
  Preview ready: previews/scene_01_preview.mp4

  Previewing Scene 2...
  [===========================================] 100%  (Elapsed: 0m 31s)
  Preview ready: previews/scene_02_preview.mp4

  Previewing Scene 3...
  [===========================================] 100%  (Elapsed: 0m 28s)
  Preview ready: previews/scene_03_preview.mp4

  Previewing Scene 4...
  [===========================================] 100%  (Elapsed: 0m 18s)
  Preview ready: previews/scene_04_preview.mp4

  Scene 5 skipped. (No code file assigned.)

  Preview complete.
  Previewed:  4 scenes
  Skipped:    1 scene  (Scene 5 — no code file)
  Total time: 1 minute 39 seconds

  Tip: To generate the final high-quality versions of all scenes, run:
       render all

supermanim>
```

---

##### Subsubsection 0.4.7.4 — `force preview scene`

**What it does:**

This command forces a new preview to be generated for a specific scene, even if a preview
file for that scene already exists in the `previews/` folder.

Normally, `preview scene` always regenerates the preview anyway — there is no skip behavior
for previews the way there is for renders. However, `force preview scene` makes the tool
also delete the old preview file first before generating the new one.

Use this when:
- You want to make absolutely sure the old preview file is gone before the new one is created.
- You suspect the existing preview file is corrupted or incomplete.
- You want to clean up and start fresh for a specific scene's preview.

**Syntax:**

```
force preview scene <scene_number>
```

**Example:**

```
supermanim> force preview scene 3
```

**What the tool prints back:**

```
supermanim> force preview scene 3

  Force previewing Scene 3.
  Deleting existing preview file (if any): previews/scene_03_preview.mp4
  Old file deleted.

  Preview checklist for Scene 3:
  [OK] Project is open.
  [OK] Code file assigned: my_scenes/example.py

  Generating new low-quality preview for Scene 3...
  Running animation engine (low quality mode)...
  [===========================================] 100%  (Elapsed: 0m 26s)

  Preview ready: previews/scene_03_preview.mp4
  Duration:      16.8 seconds
  Quality:       low (480p)

supermanim>
```

**What the tool prints back — when no old preview file exists:**

```
supermanim> force preview scene 3

  Force previewing Scene 3.
  Deleting existing preview file (if any): previews/scene_03_preview.mp4
  No existing file found. Nothing to delete.

  Preview checklist for Scene 3:
  [OK] Project is open.
  [OK] Code file assigned: my_scenes/example.py

  Generating new low-quality preview for Scene 3...
  Running animation engine (low quality mode)...
  [===========================================] 100%  (Elapsed: 0m 26s)

  Preview ready: previews/scene_03_preview.mp4
  Duration:      16.8 seconds
  Quality:       low (480p)

supermanim>
```

---

##### Subsubsection 0.4.7.5 — `preview status`

**What it does:**

This command shows you a summary of the preview state of every scene in your project.

It does not generate any new previews. It only reports what already exists.

For each scene, it tells you:
- Whether a preview file exists in the `previews/` folder.
- The file path of that preview file, if it exists.
- Whether the scene has a code file assigned (a scene with no code file cannot be previewed).

Use this command when you want to quickly see which scenes you have already previewed
and which ones still need a preview.

**Syntax:**

```
preview status
```

**What the tool prints back:**

```
supermanim> preview status

  Preview Status — MyAnimation
  ==============================
  Total scenes:       5
  Have a preview:     3
  No preview yet:     2

  +-------+------------------------------+------------------------+--------------------+
  | Scene | Code File                    | Preview File           | Status             |
  +-------+------------------------------+------------------------+--------------------+
  |   1   | my_scenes/intro.py           | scene_01_preview.mp4   | preview exists     |
  |   2   | my_scenes/main_concept.py    | scene_02_preview.mp4   | preview exists     |
  |   3   | my_scenes/example.py         | —                      | no preview yet     |
  |   4   | my_scenes/conclusion.py      | scene_04_preview.mp4   | preview exists     |
  |   5   | not assigned                 | —                      | cannot preview     |
  +-------+------------------------------+------------------------+--------------------+

  Notes:
    Scene 3: Code file is assigned. Run "preview scene 3" to generate a preview.
    Scene 5: No code file assigned. Cannot preview until a code file is set.

supermanim>
```

---

##### Subsubsection 0.4.7.6 — `open preview`

**What it does:**

This command opens an existing preview file directly in your system's default video player.

Instead of navigating to the `previews/` folder yourself and double-clicking the file,
you can open it from inside SuperManim without leaving the tool.

If no preview file exists for the requested scene, the tool tells you and suggests
the command to generate one.

**Syntax:**

```
open preview <scene_number>
```

**Example:**

```
supermanim> open preview 4
```

**What the tool prints back — when the preview file exists:**

```
supermanim> open preview 4

  Opening preview for Scene 4...
  File: previews/scene_04_preview.mp4

  Launching system video player...
  Done. The video should now be playing in your video player.

supermanim>
```

**What the tool prints back — when no preview file exists yet:**

```
supermanim> open preview 3

  ERROR: No preview file found for Scene 3.
  Expected location: previews/scene_03_preview.mp4

  To generate a preview first, run:
  preview scene 3

supermanim>
```

---

##### Subsubsection 0.4.7.7 — `clear previews`

**What it does:**

This command deletes all preview files from the `previews/` folder.

It does not delete any real rendered videos from the `output/` folder.
It does not delete any code files, audio files, or project settings.
It only deletes the low-quality preview `.mp4` files that were generated by preview commands.

Use this when:
- Your `previews/` folder has grown large and you want to free up disk space.
- You want to clean up old preview files that are no longer relevant.
- You are done with your project and want to tidy up before archiving it.

Because this command deletes files permanently, the tool will warn you and ask you to confirm
before it does anything.

**Syntax:**

```
clear previews
```

**What the tool prints back:**

```
supermanim> clear previews

  The following preview files will be permanently deleted:

    previews/scene_01_preview.mp4   (22 MB)
    previews/scene_02_preview.mp4   (31 MB)
    previews/scene_04_preview.mp4   (18 MB)

  Total space to be freed: 71 MB
  This cannot be undone.

  Type "yes" to continue, or anything else to cancel:
  > yes

  Deleting previews/scene_01_preview.mp4...  done.
  Deleting previews/scene_02_preview.mp4...  done.
  Deleting previews/scene_04_preview.mp4...  done.

  All preview files deleted.
  3 files removed.  71 MB freed.

supermanim>
```

**What the tool prints back — when the previews folder is already empty:**

```
supermanim> clear previews

  No preview files found in previews/.
  Nothing to delete.

supermanim>
```

---

##### Subsubsection 0.4.7.8 — `clear preview scene`

**What it does:**

This command deletes the preview file for one specific scene only.

It is the single-scene version of `clear previews`.
Use this when you want to remove the preview for one particular scene
without touching the preview files of any other scene.

**Syntax:**

```
clear preview scene <scene_number>
```

**Example:**

```
supermanim> clear preview scene 3
```

**What the tool prints back — when the preview file exists:**

```
supermanim> clear preview scene 3

  Deleting preview file for Scene 3...
  File: previews/scene_03_preview.mp4  (26 MB)

  Deleted.
  To generate a new preview later, run:  preview scene 3

supermanim>
```

**What the tool prints back — when no preview file exists for that scene:**

```
supermanim> clear preview scene 3

  No preview file found for Scene 3.
  Expected location: previews/scene_03_preview.mp4
  Nothing to delete.

supermanim>
```

#### Subsection 0.4.8 — Category 6: Sync Commands

##### Subsubsection 0.4.8.1 — What Are Sync Commands?

Sync commands are the commands that link a scene to its audio clip.

Remember the `synced_with_audio` flag from the scene table?
This flag is `False` by default for every new scene.
Sync commands are the ONLY way to change this flag to `True`.

```
+----------------------------------------------------------+
|  What "syncing" means:                                   |
|                                                          |
|  You have Scene 3.                                       |
|  You have clip_003.mp3.                                  |
|                                                          |
|  Syncing links them together:                            |
|  "Scene 3 uses clip_003.mp3 as its audio."               |
|                                                          |
|  The tool checks:                                        |
|  Scene 3 duration == clip_003.mp3 duration?              |
|  16.8 seconds     == 16.8 seconds?                       |
|  YES --> Link confirmed. synced_with_audio = True.       |
|  NO  --> Refuse. Tell you the difference.                |
|                                                          |
|  From now on, when Scene 3 is rendered,                  |
|  it will include clip_003.mp3 in the output video.       |
|                                                          |
+----------------------------------------------------------+
```

Sync commands let you:
- Sync one scene with its audio clip.
- Sync all scenes at once.
- Remove the sync from one scene (if you want it to render silently).
- Remove the sync from all scenes at once.
- Check the sync status of all scenes.

---
Every sync command checks:

```
CHECK 1: Is a project open?
    YES --> continue.
    NO  --> stop. "No project is open."

CHECK 2: Does the project have an audio file?
    YES --> continue.
    NO  --> stop. "No audio file loaded. Use: add audio <path>"
```

---

##### Subsubsection 0.4.8.2 — `sync scene`

**What it does:**

This command links one specific scene to one specific audio clip.

When you run it, the tool:
1. Checks that the scene exists.
2. Checks that the audio clip file exists.
3. Measures the duration of the audio clip.
4. Compares it to the scene's duration.
5. If they match exactly → sets `synced_with_audio = True` for that scene.
6. If they do NOT match → refuses and shows you the difference.

**Syntax:**

```
sync scene <scene_number> audio_clip <clip_number>
```

**Examples:**

```
supermanim> sync scene 1 audio_clip 1
supermanim> sync scene 2 audio_clip 2
supermanim> sync scene 3 audio_clip 3
```

**What the tool prints back (success):**

```
supermanim> sync scene 3 audio_clip 3

  Syncing Scene 3 with clip_003.mp3...

  Checking durations:
  Scene 3 duration:        16.8 seconds
  clip_003.mp3 duration:   16.8 seconds
  Match: YES

  synced_with_audio = True  for Scene 3.
  From now on, rendering Scene 3 will produce a video with audio.

supermanim>
```

**What the tool prints back (duration mismatch):**

```
supermanim> sync scene 4 audio_clip 4

  Syncing Scene 4 with clip_004.mp3...

  Checking durations:
  Scene 4 duration:        7.0 seconds
  clip_004.mp3 duration:   9.3 seconds
  Match: NO  (difference: 2.3 seconds)

  ERROR: Cannot sync. Durations do not match.

  Fix options:
    Option A: Change the scene duration to match the audio:
              set scene 4 duration 9.3

    Option B: Re-cut the audio clip to match the scene:
              split audio duration 12.5 18.5 16.8 7.0 5.5
              (adjust the 4th number to 7.0)

supermanim>
```

---

##### Subsubsection 0.4.8.3 — `sync all`

**What it does:**

This command tries to sync every scene in the project with its matching audio clip all at once.

The tool assumes that Scene 1 goes with Clip 1, Scene 2 goes with Clip 2, and so on.
This is the natural order — the clips were created to match the scenes.

For each scene, the tool:
1. Checks if a matching clip exists.
2. Compares the scene duration to the clip duration.
3. If they match → sets `synced_with_audio = True`.
4. If they do NOT match → marks that scene as "sync failed" and moves to the next.

At the end, the tool prints a full report showing which scenes synced successfully
and which ones failed (and why).

**Syntax:**

```
sync all
```

**What the tool prints back:**

```
supermanim> sync all

  Attempting to sync all 5 scenes...

  +-------+-----------------+-----------------+----------+-------------------+
  | Scene | Scene Duration  | Clip Duration   | Match?   | Result            |
  +-------+-----------------+-----------------+----------+-------------------+
  |   1   | 12.5s           | 12.5s           | YES      | synced = True     |
  |   2   | 18.5s           | 18.5s           | YES      | synced = True     |
  |   3   | 16.8s           | 16.8s           | YES      | synced = True     |
  |   4   |  7.0s           |  9.3s           | NO       | synced = False    |
  |   5   |  5.5s           | no clip found   | NO       | synced = False    |
  +-------+-----------------+-----------------+----------+-------------------+

  Synced successfully: 3 scenes  (Scenes 1, 2, 3)
  Failed to sync:      2 scenes  (Scenes 4 and 5)

  Scene 4: Duration mismatch. Scene=7.0s, Clip=9.3s. Difference=2.3s.
  Scene 5: No audio clip assigned to this scene.

  To fix Scene 4: set scene 4 duration 9.3
  To fix Scene 5: assign a clip first, then try again.

supermanim>
```

---

##### Subsubsection 0.4.8.4 — `unsync scene`

**What it does:**

This command removes the audio link from one specific scene.
It sets `synced_with_audio = False` for that scene.

After you run this command, that scene will render as a silent video — no audio included —
even if it has an audio clip file assigned.

Use this when:
- You want to render one scene without its audio for testing purposes.
- The scene's audio is wrong and you want to disconnect it while you fix things.
- You just changed your mind and want this scene to be silent.

**Syntax:**

```
unsync scene <scene_number>
```

**Example:**

```
supermanim> unsync scene 4
```

**What the tool prints back:**

```
supermanim> unsync scene 4

  Scene 4 unsynced.
  synced_with_audio = False  for Scene 4.

  Scene 4 will now render as a silent video.
  The audio clip file (clip_004.mp3) is still saved — just not linked.
  To re-link it later, use: sync scene 4 audio_clip 4

supermanim>
```

---

##### Subsubsection 0.4.8.5 — `unsync all`

**What it does:**

This command removes the audio link from every single scene at once.
It sets `synced_with_audio = False` for all scenes.

After you run this command, every scene will render as a silent video.
All the audio clip files are still saved in the `audio_clips/` folder — they are not deleted.
You can re-sync them later.

Use this when you want to do a test render of the entire project without any audio.

**Syntax:**

```
unsync all
```

**What the tool prints back:**

```
supermanim> unsync all

  Removing audio sync from all 5 scenes...

  Scene 1:  synced_with_audio = False
  Scene 2:  synced_with_audio = False
  Scene 3:  synced_with_audio = False
  Scene 4:  synced_with_audio = False
  Scene 5:  synced_with_audio = False

  All scenes unsynced.
  All audio clip files are still saved. Nothing was deleted.
  To re-sync everything, use: sync all

supermanim>
```

---

##### Subsubsection 0.4.8.6 — `sync status`

**What it does:**

This command shows you a table of all scenes and their current sync status.
It tells you which scenes are synced with audio, which are not, and for the synced ones,
it confirms that the durations still match.

Run this command any time you want to quickly check the sync state of your project
before rendering or exporting.

**Syntax:**

```
sync status
```

**What the tool prints back:**

```
supermanim> sync status

  Sync Status — Project: MyAnimation
  =====================================

  +-------+----------+------------------+--------------------+--------------------+
  | Scene | Duration | Audio Clip       | Clip Duration      | synced_with_audio  |
  +-------+----------+------------------+--------------------+--------------------+
  |   1   | 12.5s    | clip_001.mp3     | 12.5s  (MATCH OK)  | True               |
  |   2   | 18.5s    | clip_002.mp3     | 18.5s  (MATCH OK)  | True               |
  |   3   | 16.8s    | clip_003.mp3     | 16.8s  (MATCH OK)  | True               |
  |   4   |  7.0s    | clip_004.mp3     |  9.3s  (MISMATCH!) | False              |
  |   5   |  5.5s    | not assigned     | --                 | False              |
  +-------+----------+------------------+--------------------+--------------------+

  Fully synced:   3 scenes  (Scenes 1, 2, 3 — will render WITH audio)
  Not synced:     2 scenes  (Scenes 4 and 5 — will render WITHOUT audio)

  WARNING: Scene 4 has a duration mismatch. Fix before syncing.
  WARNING: Scene 5 has no audio clip assigned.

supermanim>
```


## Subsection 4.0.8 — Category 6: Export and Utility Commands

### Subsubsection 4.0.8.1 — What Are Export and Utility Commands?

Export commands handle the final step of the workflow: taking all the rendered scene clips and assembling them into one final video file — with or without audio.

Utility commands are helpful tools for general use: validating the project, clearing the cache, showing help, and quitting the tool.

---

### Subsubsection 4.0.8.2 — `export`

**What it does:**

This is the final command in the workflow. After all scenes are rendered, this command assembles them into one single video file. It stitches Scene 1's video clip to Scene 2's video clip to Scene 3's video clip and so on, in order.

In `supermanim` mode, it also merges the audio: Scene 1's video plays with Scene 1's audio clip at the same time, and so on for all scenes. The result is one final video where the animation and the narration are perfectly synchronized.

The final video is saved in the `output/` folder of the project.

Before running `export`, all scenes must be in the `rendered` state. If any scene is still `pending` or `failed`, the command will warn you and stop.

**Syntax:**

```
export
```

You can also specify options:

```
export --format mp4
export --with-audio
export --without-audio
export --output my_final_video.mp4
```

- `--format mp4` sets the output format. Default is `mp4`. You can also use `avi` or `mov`.
- `--with-audio` includes the audio track (default in `supermanim` mode).
- `--without-audio` creates a video-only file with no sound.
- `--output my_final_video.mp4` lets you choose the exact name and location of the output file.

**What the tool prints back:**

```
supermanim> export

  Checking all scenes are rendered...
  All 5 scenes are rendered. Proceeding.

  Assembling final video from 5 clips...
  Merging audio tracks...

  Clip 1 (12.5s) + Audio Clip 1 (12.5s) --> OK
  Clip 2 (18.5s) + Audio Clip 2 (18.5s) --> OK
  Clip 3 (16.8s) + Audio Clip 3 (16.8s) --> OK
  Clip 4  (7.0s) + Audio Clip 4  (7.0s) --> OK
  Clip 5  (5.5s) + Audio Clip 5  (5.5s) --> OK

  Joining all clips...

  Export complete!
  Final video: output/MyAnimation_final.mp4
  Total duration: 60.3 seconds
  File size: 47.2 MB

supermanim>
```

---

### Subsubsection 4.0.8.3 — `package project`

**What it does:**

This command creates a zip archive of your entire project folder and puts it in the `exports/` subfolder.
You can send this zip file to someone else (a collaborator, a client, a backup service) and they will have everything they need to open and continue working on the project.

**Syntax:**

```
package project
```

You can also give the zip file a custom name:

```
package project --name MyAnimation_backup_nov12
```

**What the tool prints back:**

```
supermanim> package project

  Packaging project "MyAnimation"...
  Including: scenes, audio_clips, output, project_data.db, assets

  Created: exports/MyAnimation_2024-11-12.zip
  Size: 312 MB

  You can share this zip file with anyone who has SuperManim installed.

supermanim>
```

---

### Subsubsection 4.0.8.4 — `validate project`

**What it does:**

This command checks the entire project for any problems before you start a big render or an export.
It looks for:
- Scenes with no code file assigned.
- Scenes with no audio clip assigned (in `supermanim` mode).
- Scene durations that do not add up to the audio length.
- Code files that are listed in the database but are missing from the file system.
- Rendered video files that are listed in the database but are missing from the file system.

It is a good habit to run this command before starting a long render session.

**Syntax:**

```
validate project
```

**What the tool prints back (no problems found):**

```
supermanim> validate project

  Validating project "MyAnimation"...

  Checking scene code files...       OK
  Checking scene audio clips...      OK
  Checking duration sums...          OK (60.3 seconds matches audio)
  Checking rendered video files...   OK

  Project is valid. No problems found.
  You are ready to render and export.

supermanim>
```

**What the tool prints back (problems found):**

```
supermanim> validate project

  Validating project "MyAnimation"...

  Checking scene code files...       PROBLEM
    Scene 4 has no code file assigned.
    Fix: set scene 4 code path/to/your/code.py

  Checking scene audio clips...      OK

  Checking duration sums...          PROBLEM
    Scene durations total: 62.0 seconds
    Audio file length:     60.3 seconds
    Difference: 1.7 seconds  <-- scenes are longer than the audio

  Checking rendered video files...   OK

  Found 2 problems. Please fix them before rendering.

supermanim>
```

---

### Subsubsection 4.0.8.5 — `invalidate cache`

**What it does:**

This command clears the stored hash for a specific scene, or for all scenes, without re-rendering anything.
After you run this command, the next render will treat the affected scenes as if they were never rendered,
so they will be re-rendered even if the code has not changed.

This is useful when something other than the Python code changed — for example, an image file that the scene uses was updated, but the `.py` file itself stayed the same. The hash check would not detect this change, so you need to manually tell the tool "this scene needs to be re-rendered."

**Syntax:**

To clear the cache for one scene:
```
invalidate cache scene <scene_number>
```

To clear the cache for all scenes at once:
```
invalidate cache all
```

**Examples:**

```
supermanim> invalidate cache scene 3
```

```
supermanim> invalidate cache all
```

**What the tool prints back:**

```
supermanim> invalidate cache scene 3

  Cache cleared for Scene 3.
  Scene 3 is now marked as pending.
  The next render will re-render this scene even if the code is unchanged.

supermanim>
```

---

### Subsubsection 4.0.8.6 — `help`

**What it does:**

This command shows you a list of all available commands. It is built into the `cmd` library automatically.
If you type `help` by itself, you see all commands. If you type `help` followed by a command name, you see
detailed information about that specific command.

**Syntax:**

```
help
```

or:

```
help <command_name>
```

**Examples:**

```
supermanim> help
```

```
supermanim> help render
```

```
supermanim> help add audio
```

**What the tool prints back for `help`:**

```
supermanim> help

  Available commands (type "help <command>" for details):

  PROJECT COMMANDS:
    new project        Create a new project
    open project       Open an existing project
    list projects      List all projects
    project info       Show current project details
    close project      Close the current project
    delete project     Delete a project permanently

  MODE COMMANDS:
    set mode           Set the project mode (normal / simplemanim / supermanim)
    show mode          Show the current mode

  SCENE COMMANDS:
    set scenes_number  Set the total number of scenes
    add scene          Add one new scene
    set scene          Set properties of a scene (duration, code, etc.)
    list scenes        Show all scenes and their status
    scene info         Show detailed info about one scene
    delete scene       Delete a scene
    move scene         Move a scene to a new position
    swap scenes        Swap two scenes
    duplicate scene    Copy a scene

  AUDIO COMMANDS:
    add audio          Add the main audio file
    split audio auto   Auto-detect silences and split audio
    split audio manual Split audio at specific timestamps
    map audio          Manually assign an audio range to a scene
    audio info         Show all audio assignments
    add video          Add a video file (normal mode)

  RENDER COMMANDS:
    render scene       Render one specific scene
    render all         Render all scenes (smart skip unchanged)
    render changed     Render only pending or failed scenes
    force render       Force render ignoring cache
    preview scene      Generate a fast low-quality preview
    retry failed       Retry all failed scenes
    render status      Show render progress summary

  EXPORT AND UTILITY:
    export             Assemble final video from all scenes
    package project    Create a zip archive of the project
    validate project   Check project for problems
    invalidate cache   Clear the smart-skip cache
    help               Show this help message
    exit / quit        Close SuperManim

supermanim>
```

---

### Subsubsection 4.0.8.7 — `exit` and `quit`

**What it does:**

These two commands both do the same thing: they close the SuperManim interactive shell and return you to your normal terminal.

Before closing, the tool makes sure all data is saved to the project database. You will not lose any work.

**Syntax:**

```
exit
```

or:

```
quit
```

**What the tool prints back:**

```
supermanim> exit

  Saving project data...
  All changes saved.

  Goodbye.

$
```

The `$` at the end is your normal terminal prompt. You are back in your regular shell.

---

---

## Subsection 4.0.9 — A Complete Workflow Example

### Subsubsection 4.0.9.1 — From Zero to Final Video: Every Command in Order

This section shows you what a full SuperManim session looks like from start to finish,
using real commands in the exact order you would type them.

**The goal:** Make a 5-scene educational animation with a 60.3-second narration audio, synchronized perfectly.

```
$ python supermanim.py

supermanim>

--- STEP 1: Create the project ---

supermanim> new project MyAnimation

  Project "MyAnimation" created successfully.

--- STEP 2: Set the mode ---

supermanim> set mode supermanim

  Mode set to: supermanim

--- STEP 3: Add the audio file ---

supermanim> add audio voice.mp3

  Audio added. Duration: 60.3 seconds.

--- STEP 4: Automatically split the audio into scenes ---

supermanim> split audio auto

  Found 5 speech segments. Created 5 scenes. Audio clips saved.

--- STEP 5: Assign Manim code files to each scene ---

supermanim> set scene 1 code scenes/intro.py

  Scene 1 code assigned.

supermanim> set scene 2 code scenes/main_concept.py

  Scene 2 code assigned.

supermanim> set scene 3 code scenes/example.py

  Scene 3 code assigned.

supermanim> set scene 4 code scenes/conclusion.py

  Scene 4 code assigned.

supermanim> set scene 5 code scenes/credits.py

  Scene 5 code assigned.

--- STEP 6: Validate the project before rendering ---

supermanim> validate project

  All checks passed. Project is ready.

--- STEP 7: Preview one scene to check it quickly ---

supermanim> preview scene 1

  Preview ready: previews/scene_01_preview.mp4 (done in 18 seconds)

--- STEP 8: Render everything ---

supermanim> render all

  Scene 1 | CHANGED | rendering...  done (4m 10s)
  Scene 2 | CHANGED | rendering...  done (6m 02s)
  Scene 3 | CHANGED | rendering...  done (4m 22s)
  Scene 4 | CHANGED | rendering...  done (2m 03s)
  Scene 5 | CHANGED | rendering...  done (1m 44s)

  All 5 scenes rendered. Total time: 18 minutes 21 seconds.

--- STEP 9: Fix a mistake in Scene 3 ---
--- (You edit your scene3.py file outside of SuperManim) ---

supermanim> render scene 3

  Code changed. Rendering Scene 3 again...  done (4m 15s)
  Scenes 1, 2, 4, 5: skipped (no changes).

--- STEP 10: Export the final video ---

supermanim> export

  All scenes rendered. Assembling final video...
  Final video: output/MyAnimation_final.mp4
  Duration: 60.3 seconds

--- STEP 11: Exit ---

supermanim> exit

  All changes saved. Goodbye.

$
```

This is the complete SuperManim workflow. Notice how in Step 9, fixing one scene and re-rendering
only took 4 minutes instead of 18 — because SuperManim skipped the 4 unchanged scenes automatically.
That is the core value of the tool in action.

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
The Core is the centerpiece of Hexagonal Architecture.It contains all the **real logic** of SuperManim
the decisions, the rules, the calculations. It is pure Python.It does not import `os`, `sqlite3`,
`subprocess`, or anything external.

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

The Core only ever calls `save_scene()`, `load_scene()`, `all_scenes()`. It never asks "are you using SQLite?"
or "are you using a JSON file?" It does not know. It does not care.

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

An Adapter takes the Core's clean request and translates it into whatever the specific external technology needs.

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

---

---

######  GROUP 1 — Repository Ports (Data Persistence)
Think of this group as SuperManim's **long-term memory**. Without this group, every time you close the program,
everything is forgotten — all your scenes, all your audio clips, all your render history. The Repository Ports
make sure that data is saved to disk and can be retrieved later, exactly as you left it.

Every port in this group follows the same idea:
- `save_something(...)` — write data to storage
- `load_something(...)` — read data back
- `delete_something(...)` — remove data
- `list_all(...)` — get everything

The core logic does not know if it is talking to a SQLite file, a JSON file, a YAML file, or even a remote server.
It only talks to the Port.

Port 1.1 — SceneRepositoryPort
-----------------------------------
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
- Duration in seconds (e.g., 12.5 seconds)
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
| 3 | scene_exists(scene_id)              | Safe check — returns True/False, never raises            |
| 4 | delete_scene(scene_id)              | Remove one scene record from storage                     |
| 5 | delete_all_scenes()                 | Wipe every scene record in the project                   |
+---+-------------------------------------+----------------------------------------------------------+
|   | --- QUERY ---                        |                                                          |
| 6 | all_scenes()                        | Return every scene, ordered by ID                        |
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
