

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
The tool can be used in dfferent usage:

#### Subsection 0.3.1 The Normal Media Editor

##### Subsubsection 0.3.1.1 Definition of this mode:

This usage is for fixing videos and songs you already have. Think of it like a simple cutting table.
If you have a long video and want to make it shorter, or if you have a song and want to cut out
the quiet parts, you use this mode.

##### Subsubsection 0.3.1.2 How to use it:

###### 1. Create Your Project Space**
Before you start working, the tool needs a place to save your work. It creates a "project folder structure.
" Imagine this like opening a new folder on your desk to keep all your papers organized so they don't get lost.

###### 2. Add Your Files**
Now you need to give the tool the file you want to fix. It is like handing a photo to a friend to look at.

**If you want to edit sound:**
You tell the tool where the sound file lives on your computer.
Command: `add audio "path to audio"` or `add audio_file "path to audio"`

**If you want to edit a movie:**
You tell the tool where the video file is.
Command: `add video "path to video"` or `add video_file "path to video"`

###### 3. Perform Operations:**
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

This usage  is for creating cartoons using code. It is built on a tool called "Manim.
" Think of this mode as a robot that draws pictures for you. It creates "silent movies"
because it makes video scenes without any sound or music to match.

##### Subsubsection 0.3.2.2 How to use it:
###### 1. Create Your Project Space**
Just like the other mode, the tool sets up a folder to keep your work safe.

###### 2. Choose the Number of Scenes**
A scene is like one page in a storybook. You tell the tool how many pages you want in your story.
Command: `set scenes_number 2` (for two scenes)
Or     : `set scene` (for just one scene)

###### 3. Set the Duration**
You must tell the tool how long each page stays on the screen. You count this in seconds.
Command: `set scene 1 duration 3.4` (Scene 1 plays for 3.4 seconds)
Command: `set scene 3 duration 5` (Scene 3 plays for 5 seconds)

###### 4. Add Your Code**
Now you give the tool the instructions for what to draw. You give it a file with the code.
Command: `set scene 1 code "path to the manim code"`

###### 5. Preview or Render**
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

##### Subsubsection 0.3.3.1 Definition of this usage:

This is the most powerful usage. It is like a movie director.It does everything the Simple Editor does,
but it adds a superpower: **Synchronization**. It makes sure the video matches the sound perfectly.
If a ball bounces on screen, the sound "BOING" plays at the exact same time.

##### Subsubsection 0.3.3.2 How to use it:

###### 1. Create Your Project Space
The tool creates a folder that keeps your sound and video plans together.


###### 2. Add Your Sound
Because the video needs to match the sound, you must give the tool the sound file first.
This is usually a voice recording or music.

Command: `add audio_file "path to voiceover"`

###### 3. Map the video 
The tool helps you split your video into scenes to match the sound. There are two ways to do this: 

**Method 1: The Manual Way**
You tell the tool exactly how many scenes you want.Then, you set the duration (time) for each scene. 
Rule: The total time of all your scenes added together must be exactly the same as the length of the audio file.
     
**Method 2: The Automatic Way**
If you do not enter the number of scenes or times, the tool will do it for you.
It listens to the audio and looks for silence (the quiet parts).
It automatically cuts a new scene every time it hears a pause in the sound. 

###### 4. Add Your Code
You give the tool the drawing instructions for each time section.
Command: `set scene 1 code "path to code"`

###### 5. Render the Final Video
You tell the tool to combine the video and sound into one movie.
Command: `render all`

##### Subsubsection 0.3.3.3 Diagram of Super Editor:

```
  [ You run SuperManim ]
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
#### Subsection 0.4.9 — Category 6: Export Commands

##### Subsubsection 0.4.9.1 — What Are Export Commands?

Exporting is the final step in the SuperManim workflow.

Up until this point, everything you have done has been preparation. You created a project.
You added an audio file. You set up your scenes. You wrote Python code for each scene.
You rendered each scene into an individual `.mp4` clip. All of those clips are sitting
in the `output/` folder of your project, each one in its own subfolder.

But those individual clips are not your finished video. They are the pieces.
Exporting is the step that takes all those pieces and assembles them into one single
complete video file — the final product you can share, upload, or keep.

During export, the tool does several things in sequence:

```
+------------------------------------------------------------------+
|  WHAT HAPPENS DURING EXPORT                                      |
|                                                                  |
|  Step 1: Check that every scene has been rendered successfully.  |
|          If any scene is pending or failed, stop. Report which.  |
|                                                                  |
|  Step 2: Read the scene order from the project database.         |
|          Scenes are assembled in order: 1, 2, 3, 4, 5...        |
|                                                                  |
|  Step 3: For scenes with synced_with_audio = True,               |
|          combine the video clip with its audio clip.             |
|                                                                  |
|  Step 4: Concatenate all scene clips into one video file         |
|          using FFmpeg.                                           |
|                                                                  |
|  Step 5: Save the finished file to the output/ folder.           |
|          Default name: <ProjectName>_final.mp4                   |
|                                                                  |
|  Step 6: Report the total duration and file size.                |
|                                                                  |
+------------------------------------------------------------------+
```

Export commands control everything about this process:
- Whether the project is ready to export.
- What format the output file uses.
- What quality level the final file uses.
- Where the final file is saved.

---

**Before Every Export: What the Tool Always Checks**

Before the tool exports anything, it runs through a checklist.
If any check fails, the tool stops and tells you exactly what needs to be fixed.

```
+--------------------------------------------------------------------+
|  EXPORT CHECKLIST — runs before EVERY export command             |
|                                                                    |
|  CHECK 1: Is a project open?                                       |
|  YES --> continue.                                                 |
|  NO  --> STOP. "No project is open."                               |
|                                                                    |
|  CHECK 2: Does the project have at least one scene?               |
|  YES --> continue.                                                 |
|  NO  --> STOP. "Project has no scenes. Nothing to export."         |
|                                                                    |
|  CHECK 3: Is every scene in a "rendered" status?                  |
|  YES --> continue.                                                 |
|  NO  --> STOP. List every scene that is "pending" or "failed".    |
|          "Cannot export. These scenes are not yet rendered."       |
|                                                                    |
|  CHECK 4: Does every rendered clip file actually exist on disk?   |
|  YES --> continue.                                                 |
|  NO  --> STOP. "Clip file missing for Scene X. Re-render it."     |
|                                                                    |
+--------------------------------------------------------------------+
```

This checklist ensures the tool never tries to assemble a video from incomplete pieces.
Every single scene must be fully rendered before the export can begin.

---

##### Subsubsection 0.4.9.2 — `export`

**What it does:**

This command assembles all rendered scene clips into one final complete video file.

The tool runs the export checklist first. If all scenes are rendered and all clip files
exist on disk, the tool calls FFmpeg to concatenate the clips in order and write the
final output file.

The final file is saved inside the `output/` folder of your project.
The default filename is your project name followed by `_final.mp4`.

**Syntax:**

```
export
```

**What the tool prints back — when the export succeeds:**

```
supermanim> export

  Export checklist:
  [OK] Project is open: MyAnimation
  [OK] Project has 5 scenes.
  [OK] All 5 scenes have status: rendered.
  [OK] All 5 clip files exist on disk.

  Assembling final video...

  Step 1/3: Merging audio into scene clips...
    Scene 1: merging clip_001.mp3 + scene_01.mp4...  done.
    Scene 2: merging clip_002.mp3 + scene_02.mp4...  done.
    Scene 3: merging clip_003.mp3 + scene_03.mp4...  done.
    Scene 4: silent (no audio clip).                 done.
    Scene 5: silent (no audio clip).                 done.

  Step 2/3: Concatenating all 5 scenes into one file...
  [===========================================] 100%  (Elapsed: 0m 42s)

  Step 3/3: Writing final output file...
  Done.

  Export complete.
  Output file:    output/MyAnimation_final.mp4
  Duration:       60.3 seconds
  File size:      214 MB
  Format:         mp4
  Quality:        high (1080p)

supermanim>
```

**What the tool prints back — when a scene is not yet rendered:**

```
supermanim> export

  Export checklist:
  [OK] Project is open: MyAnimation
  [OK] Project has 5 scenes.
  [!!] Not all scenes are rendered.

  Cannot export. The following scenes are not ready:

    Scene 4 — status: pending   (not yet rendered)
    Scene 5 — status: FAILED    (last error: NameError at line 12)

  Fix these scenes first, then run export again.
  Suggested commands:
    render scene 4
    render failed

supermanim>
```

**What the tool prints back — when a clip file is missing from disk:**

```
supermanim> export

  Export checklist:
  [OK] Project is open: MyAnimation
  [OK] Project has 5 scenes.
  [OK] All 5 scenes have status: rendered.
  [!!] Missing clip file detected.

  Cannot export. The following clip files were not found on disk:

    Scene 2: output/scene_02/scene_02.mp4  — FILE NOT FOUND

  The database says Scene 2 was rendered, but the file is gone.
  This can happen if the file was accidentally deleted.
  Fix:  force render scene 2

supermanim>
```

---

##### Subsubsection 0.4.9.3 — `export status`

**What it does:**

This command shows you whether the project is ready to export, without actually
starting the export process.

It runs the export checklist and reports the result of each check.
It also shows you a summary table of every scene and its current render status.

Use this command when you want to know what is still standing between you and
a finished exported video, without committing to any action.

**Syntax:**

```
export status
```

**What the tool prints back — when the project is ready:**

```
supermanim> export status

  Export Status — MyAnimation
  ============================

  Checking export readiness...

  [OK] Project is open.
  [OK] Project has 5 scenes.
  [OK] All 5 scenes are rendered.
  [OK] All 5 clip files exist on disk.

  +-------+----------+-----------+------------------------------+
  | Scene | Duration | Status    | Clip File                    |
  +-------+----------+-----------+------------------------------+
  |   1   | 12.5s    | rendered  | output/scene_01/scene_01.mp4 |
  |   2   | 18.5s    | rendered  | output/scene_02/scene_02.mp4 |
  |   3   | 16.8s    | rendered  | output/scene_03/scene_03.mp4 |
  |   4   |  7.0s    | rendered  | output/scene_04/scene_04.mp4 |
  |   5   |  5.5s    | rendered  | output/scene_05/scene_05.mp4 |
  +-------+----------+-----------+------------------------------+

  Total duration:   60.3 seconds
  Ready to export:  YES

  Run "export" to assemble the final video.

supermanim>
```

**What the tool prints back — when the project is NOT ready:**

```
supermanim> export status

  Export Status — MyAnimation
  ============================

  Checking export readiness...

  [OK] Project is open.
  [OK] Project has 5 scenes.
  [!!] Not all scenes are rendered.

  +-------+----------+-----------+------------------------------+
  | Scene | Duration | Status    | Notes                        |
  +-------+----------+-----------+------------------------------+
  |   1   | 12.5s    | rendered  |                              |
  |   2   | 18.5s    | rendered  |                              |
  |   3   | 16.8s    | rendered  |                              |
  |   4   |  7.0s    | pending   | not yet rendered             |
  |   5   |  5.5s    | FAILED    | NameError line 12            |
  +-------+----------+-----------+------------------------------+

  Ready to export:  NO
  Reason:           1 scene pending, 1 scene failed.

  Fix these scenes first:
    render scene 4
    render failed

supermanim>
```

---

##### Subsubsection 0.4.9.4 — `set export format`

**What it does:**

This command sets the file format that the `export` command will use when it writes
the final output file.

By default, SuperManim exports to `.mp4` format, which is the most widely supported
video format and works on almost every device and platform. However, you may have a
reason to export in a different format — for example, if you are uploading to a platform
that requires `.webm`, or if you need a `.mov` file for video editing software.

The format setting is saved in the project database. Once you set it, every future
`export` command in this project will use the format you chose, until you change it again.

Supported formats:

```
+------------+----------------------------------------------------------+
| Format     | Notes                                                    |
+------------+----------------------------------------------------------+
| mp4        | Default. Works everywhere. Best choice for most uses.    |
| webm       | Open format. Good for web. Slightly smaller file size.   |
| mov        | Apple format. Used in professional video editing tools.  |
| avi        | Older format. Large file size. Avoid unless required.    |
+------------+----------------------------------------------------------+
```

**Syntax:**

```
set export format <format>
```

**Examples:**

```
supermanim> set export format mp4
supermanim> set export format webm
supermanim> set export format mov
```

**What the tool prints back:**

```
supermanim> set export format webm

  Export format updated.
  Format:   webm
  Output file will be named:  MyAnimation_final.webm

  Note: The next time you run "export", the output will be in webm format.
  To switch back:  set export format mp4

supermanim>
```

**What the tool prints back — when an unsupported format is given:**

```
supermanim> set export format flv

  ERROR: "flv" is not a supported export format.

  Supported formats:
    mp4   (recommended)
    webm
    mov
    avi

supermanim>
```

---

##### Subsubsection 0.4.9.5 — `set export quality`

**What it does:**

This command sets the quality level that the `export` command will use when assembling
the final video file.

Quality in this context refers to the video resolution and the bitrate — how much data
is used per second of video. Higher quality means a sharper, clearer video, but also a
larger file size. Lower quality means a smaller file, but the video will look softer.

The quality setting is saved in the project database. Once you set it, every future
`export` command in this project will use this quality level, until you change it.

Available quality levels:

```
+----------+------------------+------------------------------+-------------------+
| Level    | Resolution       | Typical File Size (60s video)| Use Case          |
+----------+------------------+------------------------------+-------------------+
| low      | 480p  (854x480)  | ~  40 MB                     | Quick sharing,    |
|          |                  |                              | testing only.     |
+----------+------------------+------------------------------+-------------------+
| medium   | 720p  (1280x720) | ~  90 MB                     | Web uploads,      |
|          |                  |                              | general use.      |
+----------+------------------+------------------------------+-------------------+
| high     | 1080p (1920x1080)| ~ 214 MB                     | Default. Best for |
|          |                  |                              | most purposes.    |
+----------+------------------+------------------------------+-------------------+
| ultra    | 4K    (3840x2160)| ~ 850 MB                     | Professional use, |
|          |                  |                              | large screens.    |
+----------+------------------+------------------------------+-------------------+
```

**Syntax:**

```
set export quality <level>
```

**Examples:**

```
supermanim> set export quality high
supermanim> set export quality medium
supermanim> set export quality ultra
```

**What the tool prints back:**

```
supermanim> set export quality medium

  Export quality updated.
  Quality:     medium (720p)
  Estimated final file size for this project:  ~90 MB

  Note: This setting only affects the export step.
        Your rendered scene clips in output/ are always produced at full quality.
        Export quality controls how the final assembled file is written.

  To change back:  set export quality high

supermanim>
```

**What the tool prints back — when an invalid level is given:**

```
supermanim> set export quality extreme

  ERROR: "extreme" is not a recognized quality level.

  Available quality levels:
    low      (480p)
    medium   (720p)
    high     (1080p)  ← default
    ultra    (4K)

supermanim>
```

---

##### Subsubsection 0.4.9.6 — `set export name`

**What it does:**

This command sets a custom filename for the final exported video file.

By default, SuperManim names the output file using your project name followed by `_final`.
For example, if your project is called `MyAnimation`, the default output filename is
`MyAnimation_final.mp4`.

You can change this to any name you prefer. You do not need to include the file extension
in the name you provide — the tool adds the correct extension automatically based on the
format setting.

The name setting is saved in the project database.

**Syntax:**

```
set export name <filename>
```

**Examples:**

```
supermanim> set export name IntroductionToCalculus_Episode1
supermanim> set export name FinalVersion_v3
supermanim> set export name upload_ready
```

**What the tool prints back:**

```
supermanim> set export name IntroductionToCalculus_Episode1

  Export filename updated.
  New output file will be:  output/IntroductionToCalculus_Episode1.mp4

  (Extension is added automatically based on your export format setting.)

supermanim>
```

---

##### Subsubsection 0.4.9.7 — `show export settings`

**What it does:**

This command shows you all the current export settings for the open project in one place.

It does not start an export. It does not change any settings.
It only shows you what settings are currently saved so you can review them before running
the actual `export` command.

**Syntax:**

```
shoe export settings
```

**What the tool prints back:**

```
supermanim> export settings

  Export Settings — MyAnimation
  ================================
  Output filename:    IntroductionToCalculus_Episode1
  Format:             mp4
  Quality:            high (1080p)
  Full output path:   output/IntroductionToCalculus_Episode1.mp4

  Estimated file size for this project:  ~214 MB
  Total assembled duration:              60.3 seconds

  To change these settings:
    set export name     <filename>
    set export format   <format>
    set export quality  <level>

  To run the export:
    export

supermanim>
```

---

---

#### Subsection 0.4.10 — Category 7: Utility Commands

##### Subsubsection 0.4.10.1 — What Are Utility Commands?

Utility commands are commands that do not belong to any one specific part of the workflow.
They are general-purpose tools that help you manage the health of your project, understand
the state of your work, get help when you are stuck, and interact with the tool itself.

You will use utility commands throughout your entire workflow — not just at the beginning
or the end. They are always available, regardless of whether a project is open or not.

Utility commands cover several different types of tasks:

```
+------------------------------------------------------------------+
|  TYPES OF UTILITY COMMANDS                                       |
|                                                                  |
|  Project Health:                                                 |
|    validate project  — Check that the project has no problems.  |
|    clean project     — Delete temporary and leftover files.      |
|                                                                  |
|  Information & Help:                                             |
|    help              — Show a list of all available commands.   |
|    help <command>    — Show detailed help for one command.       |
|    version           — Show the SuperManim version number.       |
|    history           — Show your recently typed commands.        |
|                                                                  |
|  Session Control:                                                |
|    exit              — Save everything and close the tool.       |
|    quit              — Alias for exit. Does the same thing.      |
|                                                                  |
+------------------------------------------------------------------+
```

None of the utility commands perform rendering, previewing, or exporting.
They are the maintenance and navigation layer of the tool.

---

##### Subsubsection 0.4.10.2 — `validate project`

**What it does:**

This command runs a complete health check on the open project and reports any problems it finds.

It does not fix anything. It only looks, checks, and reports.
If everything is fine, it tells you the project is ready.
If something is wrong, it tells you exactly what is wrong and how to fix it.

The validation check covers every part of the project:

```
+--------------------------------------------------------------------+
|  VALIDATION CHECKLIST — what validate project checks             |
|                                                                    |
|  PROJECT LEVEL:                                                    |
|    - Is a project open?                                            |
|    - Does the project database file exist?                         |
|    - Is the project database readable and not corrupted?           |
|                                                                    |
|  AUDIO LEVEL:                                                      |
|    - If an audio file is set, does it exist on disk?              |
|    - If audio clips were generated, do they exist on disk?         |
|    - Do the audio clip durations add up to the total audio length? |
|                                                                    |
|  SCENE LEVEL (checked for every scene):                           |
|    - Does the scene have a code file assigned?                     |
|    - Does that code file actually exist on disk?                   |
|    - If synced_with_audio = True, does the scene have a clip?      |
|    - Do the scene duration and clip duration match exactly?        |
|    - If status = "rendered", does the clip file exist on disk?     |
|                                                                    |
|  EXPORT LEVEL:                                                     |
|    - Are all scenes rendered? (Is the project export-ready?)       |
|                                                                    |
+--------------------------------------------------------------------+
```

Use `validate project` before you start a long rendering session, before you export,
or any time you suspect something might be wrong with your project.

**Syntax:**

```
validate project
```

**What the tool prints back — when everything passes:**

```
supermanim> validate project

  Validating project: MyAnimation
  =================================

  Project level:
  [OK] Project database found and readable.

  Audio level:
  [OK] Audio file:  audio/voice.mp3  (exists on disk)
  [OK] Audio clips: 3 clips generated.  All clip files exist on disk.
  [OK] Clip durations sum (47.8s) + unclipped duration (12.5s) = total (60.3s). Match.

  Scene level:
  [OK] Scene 1: code file assigned.  File exists.  synced.  Durations match.
  [OK] Scene 2: code file assigned.  File exists.  synced.  Durations match.
  [OK] Scene 3: code file assigned.  File exists.  synced.  Durations match.
  [OK] Scene 4: code file assigned.  File exists.  not synced (silent). OK.
  [OK] Scene 5: code file assigned.  File exists.  not synced (silent). OK.

  Render level:
  [OK] All 5 scenes have status: rendered.
  [OK] All 5 clip files exist on disk.

  Export level:
  [OK] Project is ready to export.

  ================================
  Result: ALL CHECKS PASSED.
  Your project is in good shape.
  ================================

supermanim>
```

**What the tool prints back — when problems are found:**

```
supermanim> validate project

  Validating project: MyAnimation
  =================================

  Project level:
  [OK] Project database found and readable.

  Audio level:
  [OK] Audio file:  audio/voice.mp3  (exists on disk)
  [!!] Audio clip file missing:  audio/clips/clip_002.mp3  — FILE NOT FOUND

  Scene level:
  [OK] Scene 1: code file assigned.  File exists.  synced.  Durations match.
  [!!] Scene 2: code file assigned.  File exists.  synced.  Duration MISMATCH.
       Scene duration:  18.5s
       Clip duration:   20.1s
       Difference:       1.6s
  [!!] Scene 3: NO code file assigned.
  [OK] Scene 4: code file assigned.  File exists.  not synced (silent). OK.
  [OK] Scene 5: code file assigned.  File exists.  not synced (silent). OK.

  Export level:
  [!!] Project is NOT ready to export.

  ================================
  Result: 3 PROBLEMS FOUND.
  ================================

  How to fix each problem:

  Problem 1 — Missing audio clip file for clip 2:
    Re-run audio splitting to regenerate the clips:
    split audio duration 12.5 18.5 16.8 7.0 5.5

  Problem 2 — Duration mismatch for Scene 2:
    Option A: Change the scene duration to match the clip:
              set scene 2 duration 20.1
    Option B: Re-split audio with corrected durations.

  Problem 3 — No code file for Scene 3:
    Assign a code file:  set scene 3 code <path_to_file.py>

supermanim>
```


##### Subsubsection 0.4.10.3 — `clean project`

**What it does:**

This command deletes temporary files and leftover working files that accumulate
inside your project folder during normal use.

SuperManim creates various temporary files while it works — intermediate files that
FFmpeg produces during audio merging, partial render outputs, and other scratch files
that are no longer needed once a step finishes. Normally these files are deleted
automatically. But sometimes — if a command was interrupted, if the tool crashed,
or if something went wrong mid-process — these temporary files get left behind.

Over time, they take up disk space unnecessarily.

`clean project` finds and removes all of them.

**What it deletes and what it keeps:**

```
+------------------------------------------------------------------+
|  clean project — DELETES:                                        |
|                                                                  |
|    - Temporary working files in temp/ folder                     |
|    - Partial render outputs (incomplete .mp4 files)              |
|    - Intermediate FFmpeg files used during audio merging         |
|    - Any file ending in .tmp inside the project folder           |
|    - Empty subfolders inside output/                             |
|                                                                  |
|  clean project — KEEPS:                                          |
|                                                                  |
|    - The project database (project.db)                           |
|    - All fully rendered scene clips in output/                   |
|    - All preview files in previews/                              |
|    - All audio files in audio/                                   |
|    - All your Python code files                                  |
|    - The final exported video (if it exists)                     |
|                                                                  |
+------------------------------------------------------------------+
```

The command will show you exactly what it is about to delete and ask you to confirm
before it deletes anything.

**Syntax:**

```
clean project
```

**What the tool prints back — when temporary files are found:**

```
supermanim> clean project

  Scanning project folder for temporary and leftover files...

  Found the following files to delete:

    temp/ffmpeg_merge_scene02_audio.tmp    (4 MB)
    temp/ffmpeg_merge_scene03_audio.tmp    (6 MB)
    output/scene_04/scene_04_partial.mp4   (2 MB)
    temp/render_scratch_20240312.tmp       (1 MB)

  Total space to be freed:  13 MB
  These files are safe to delete. They are not part of your final output.
  This cannot be undone.

  Type "yes" to continue, or anything else to cancel:
  > yes

  Deleting temp/ffmpeg_merge_scene02_audio.tmp...   done.
  Deleting temp/ffmpeg_merge_scene03_audio.tmp...   done.
  Deleting output/scene_04/scene_04_partial.mp4...  done.
  Deleting temp/render_scratch_20240312.tmp...      done.

  Project cleaned.
  4 files deleted.  13 MB freed.

supermanim>
```

**What the tool prints back — when no temporary files are found:**

```
supermanim> clean project

  Scanning project folder for temporary and leftover files...

  No temporary files found.
  Your project folder is already clean.

supermanim>
```

---

##### Subsubsection 0.4.10.4 — `help`

**What it does:**

This command shows you a list of all available SuperManim commands, organized by category.

You can run `help` by itself to see the full list of all commands.
You can also run `help` followed by a specific command name to see detailed information
about that one command — its purpose, its syntax, its examples, and all the variations
of its output.

This command is always available. It works even when no project is open.

**Syntax:**

```
help
help <command_name>
```

**Examples:**

```
supermanim> help
supermanim> help render scene
supermanim> help export
supermanim> help validate project
```

**What the tool prints back — for `help` with no arguments:**

```
supermanim> help

  SuperManim — Command Reference
  ================================

  CATEGORY 1: Project Commands
    new project <name>               Create a new animation project.
    open project <name>              Open an existing project.
    close project                    Close the current project.
    list projects                    List all projects on this machine.
    delete project <name>            Delete a project permanently.
    project info                     Show details about the open project.

  CATEGORY 2: Audio Commands
    add audio <path>                 Load an audio file into the project.
    split audio duration <d1 d2 ...> Cut audio into clips by duration.
    split audio silence              Cut audio at silent gaps automatically.
    audio info                       Show details about the loaded audio file.
    audio clips                      List all generated audio clips.

  CATEGORY 3: Scene Commands
    set scenes_number <n>            Set how many scenes the project has.
    set scene <n> duration <d>       Set the duration of one scene.
    set scene <n> code <path>        Assign a Python code file to a scene.
    list scenes                      Show all scenes and their settings.
    scene info <n>                   Show full details about one scene.

  CATEGORY 4: Render Commands
    render scene <n>                 Render one specific scene.
    render all                       Render all scenes that have changed.
    render changed                   Render all pending or failed scenes.
    render failed                    Re-render all failed scenes.
    render status                    Show the render status of all scenes.
    force render scene <n>           Force re-render one scene.
    force render all                 Force re-render every scene.

  CATEGORY 5: Preview Commands
    preview scene <n>                Generate a fast low-quality preview.
    preview all                      Generate previews for all scenes.
    force preview scene <n>          Regenerate preview, deleting old one first.
    preview status                   Show which scenes have previews.
    open preview <n>                 Open a preview file in your video player.
    clear previews                   Delete all preview files.
    clear preview scene <n>          Delete the preview file for one scene.

  CATEGORY 6: Export Commands
    export                           Assemble all scenes into one final video.
    export status                    Check if the project is ready to export.
    export settings                  Show current export settings.
    set export format <format>       Set the output file format.
    set export quality <level>       Set the output quality level.
    set export name <filename>       Set the output filename.

  CATEGORY 7: Utility Commands
    validate project                 Run a full health check on the project.
    clean project                    Delete temporary and leftover files.
    status                           Show a full overview of the entire project.
    clear                            Clear the terminal screen.
    open output                      Open the output/ folder in your file manager.
    open project folder              Open the full project folder in your file manager.
    open log                         Open the project log file in your text editor.
    reset project                    Reset the project back to its initial state.
    help                             Show this command list.
    help <command>                   Show help for one specific command.
    version                          Show the SuperManim version number.
    history                          Show your recently typed commands.
    exit                             Save and close the tool.
    quit                             Same as exit.

  For detailed help on any command:
    help <command name>
  Example:
    help render scene

supermanim>
```

**What the tool prints back — for `help <command_name>`:**

```
supermanim> help render scene

  Command: render scene
  Category: Render Commands
  -------------------------

  What it does:
    Renders one specific scene by running its code file through the animation engine.
    Before rendering, the tool runs the render checklist:
      - Checks that a project is open.
      - Checks that a code file is assigned to the scene.
      - Checks whether the code has changed since the last render.
      - Checks audio sync and duration matching.
    If the code has not changed, the scene is skipped automatically.

  Syntax:
    render scene <scene_number>

  Examples:
    render scene 1
    render scene 4

  Related commands:
    render all          Render all scenes that have changed.
    force render scene  Render even if the code has not changed.
    render status       Check which scenes are rendered and which are not.
    preview scene       Generate a fast low-quality preview instead.

supermanim>
```

**What the tool prints back — when the command is not recognized:**

```
supermanim> help fly away

  ERROR: "fly away" is not a recognized SuperManim command.

  To see all available commands:
    help

supermanim>
```

---

##### Subsubsection 0.4.10.5 — `version`

**What it does:**

This command shows you the version number of the SuperManim tool that is currently installed
on your machine, along with the versions of the external tools it depends on.

This is useful when:
- You want to make sure you are running the latest version of SuperManim.
- You are reporting a bug and need to include version information.
- You are checking that all required external dependencies are installed and working.

This command works even when no project is open.

**Syntax:**

```
version
```

**What the tool prints back:**

```
supermanim> version

  SuperManim
  ===========
  Version:         1.4.2
  Release date:    2024-03-01
  Python:          3.11.4

  External dependencies:
    Manim:         0.18.0    [OK — found]
    FFmpeg:        6.1.0     [OK — found]
    PyDub:         0.25.1    [OK — found]

  All dependencies are installed and working.

supermanim>
```

**What the tool prints back — when a dependency is missing:**

```
supermanim> version

  SuperManim
  ===========
  Version:         1.4.2
  Release date:    2024-03-01
  Python:          3.11.4

  External dependencies:
    Manim:         0.18.0    [OK — found]
    FFmpeg:        NOT FOUND [!!]
    PyDub:         0.25.1    [OK — found]

  WARNING: FFmpeg is not installed or not found in your system PATH.
  SuperManim cannot render videos or export without FFmpeg.
  Install FFmpeg and make sure it is accessible from the terminal.

supermanim>
```

---

##### Subsubsection 0.4.10.6 — `history`

**What it does:**

This command shows you a list of the commands you have typed recently in this session
and in previous sessions.

SuperManim keeps a log of every command you type. This log is saved in the project
database (if a project is open) and in a global history file for commands typed outside
of any project.

Use `history` when:
- You forgot exactly which command you used to accomplish something earlier.
- You want to retrace your steps to understand what happened in a previous session.
- You want to copy a command you used before without typing it again from scratch.

**Syntax:**

```
history
history <n>
```

Running `history` with no argument shows the last 20 commands.
Running `history <n>` shows the last `n` commands, where `n` is any number you choose.

**Examples:**

```
supermanim> history
supermanim> history 5
supermanim> history 50
```

**What the tool prints back — for `history` with no argument:**

```
supermanim> history

  Recent command history (last 20 commands):

  #    Time               Command
  ---  -----------------  -----------------------------------------------
   1   2024-03-12 09:01   new project MyAnimation
   2   2024-03-12 09:02   add audio audio/voice.mp3
   3   2024-03-12 09:03   set scenes_number 5
   4   2024-03-12 09:04   split audio silence
   5   2024-03-12 09:07   set scene 1 code scenes/intro.py
   6   2024-03-12 09:08   set scene 2 code scenes/main_concept.py
   7   2024-03-12 09:09   set scene 3 code scenes/example.py
   8   2024-03-12 09:10   set scene 4 code scenes/conclusion.py
   9   2024-03-12 09:11   set scene 5 code scenes/credits.py
  10   2024-03-12 09:12   validate project
  11   2024-03-12 09:13   preview scene 1
  12   2024-03-12 09:14   preview scene 2
  13   2024-03-12 09:16   render all
  14   2024-03-12 09:35   render status
  15   2024-03-12 09:35   export status
  16   2024-03-12 09:36   export
  17   2024-03-12 09:37   history

  Showing 17 of 17 total commands in this session.

supermanim>
```

**What the tool prints back — for `history 5`:**

```
supermanim> history 5

  Recent command history (last 5 commands):

  #    Time               Command
  ---  -----------------  -----------------------------------------------
  13   2024-03-12 09:16   render all
  14   2024-03-12 09:35   render status
  15   2024-03-12 09:35   export status
  16   2024-03-12 09:36   export
  17   2024-03-12 09:37   history

supermanim>
```

---

##### Subsubsection 0.4.10.7 — `exit` and `quit`

**What it does:**

These two commands close the SuperManim tool and return you to your regular terminal prompt.

`exit` and `quit` do exactly the same thing. They are two different names for the same action.
`quit` exists as an alias because many people instinctively type `quit` to leave an
interactive tool, while others instinctively type `exit`. Both work.

Before closing, the tool saves any unsaved changes to the project database.
You do not need to manually save your work before exiting — SuperManim saves automatically
every time you run a command that changes something. The `exit` command simply makes sure
everything is fully written to disk and then closes cleanly.

**Syntax:**

```
exit
quit
```

**What the tool prints back — when a project is open:**

```
supermanim> exit

  Saving project: MyAnimation...
  All changes saved.

  Goodbye.

$
```

**What the tool prints back — when no project is open:**

```
supermanim> exit

  Goodbye.

$
```

After the tool exits, the `$` symbol means you are back in your regular terminal.
SuperManim is no longer running.

**Note on unsaved work:**
SuperManim does not have unsaved work in the traditional sense. Every command that changes
the project — adding a scene, setting a duration, assigning a code file, completing a render —
writes to the database immediately when the command finishes. There is no "Save" button
and no risk of losing changes. When you type `exit`, the tool simply closes.
The message "All changes saved" is a confirmation that the final database flush completed
without errors, not a warning that something was pending.

---

##### Subsubsection 0.4.10.8 — `clear`

**What it does:**

This command clears all the text from your terminal screen, giving you a clean, empty
screen to work from.

It works exactly the same way as the `clear` command in a normal Linux or macOS terminal,
or the `cls` command in a Windows terminal. It does not close the tool. It does not affect
your project in any way. It does not delete any files. It does not reset any settings.
It only removes the visual clutter of previous output from your screen.

Use this whenever your screen feels too crowded with old output and you want a fresh view.
This is especially useful during a long working session where you have typed many commands
and the screen has filled up with status tables, progress bars, and checklist results.

**Syntax:**

```
clear
```

**What happens when you run it:**

The terminal screen is wiped completely. The cursor moves to the top of the screen.
The SuperManim prompt appears fresh at the top, as if you just opened the tool.
No output from previous commands is visible anymore — but all of that work is still saved.
Nothing was lost. The screen is just clean now.

```
supermanim> clear

supermanim>
```

**Important:** `clear` only clears the visual display. Your project, your database,
your rendered files, your audio, your scenes — none of that is touched.
Think of it as wiping a whiteboard. The work you did is still real. The board just looks
cleaner now.

---

##### Subsubsection 0.4.10.9 — `status` *(recommended)*

**What it does:**

This command gives you a single complete overview of everything in your current project —
all in one screen, all at once.

Unlike `render status` (which only shows render information) or `export status` (which only
shows export readiness), `status` by itself shows the entire state of your project from
top to bottom: the project name, the audio file, every scene with its duration and render
status, the export settings, and whether the project is ready to export.

This is the single most useful command for answering the question: "Where am I right now,
and what do I still need to do?"

**Syntax:**

```
status
```

**What the tool prints back:**

```
supermanim> status

  Project Status — MyAnimation
  ==============================

  PROJECT:
    Name:              MyAnimation
    Created:           2024-03-12
    Total scenes:      5
    Total duration:    60.3 seconds

  AUDIO:
    File:              audio/voice.mp3   (60.3 seconds)
    Clips generated:   3 clips  (Scenes 1, 2, 3 synced)
    Unsynced scenes:   2  (Scenes 4 and 5 — silent)

  SCENES:
  +-------+----------+-----------+---------------------+---------------------+
  | Scene | Duration | Render    | Code File           | Audio               |
  +-------+----------+-----------+---------------------+---------------------+
  |   1   | 12.5s    | rendered  | scenes/intro.py     | clip_001.mp3 synced |
  |   2   | 18.5s    | rendered  | scenes/concept.py   | clip_002.mp3 synced |
  |   3   | 16.8s    | rendered  | scenes/example.py   | clip_003.mp3 synced |
  |   4   |  7.0s    | rendered  | scenes/conclusion.py| silent              |
  |   5   |  5.5s    | rendered  | scenes/credits.py   | silent              |
  +-------+----------+-----------+---------------------+---------------------+

  EXPORT:
    Format:            mp4
    Quality:           high (1080p)
    Output filename:   MyAnimation_final.mp4
    Ready to export:   YES

  Run "export" to assemble the final video.

supermanim>
```

**What the tool prints back — when things are still missing:**

```
supermanim> status

  Project Status — MyAnimation
  ==============================

  PROJECT:
    Name:              MyAnimation
    Created:           2024-03-12
    Total scenes:      5
    Total duration:    60.3 seconds

  AUDIO:
    File:              audio/voice.mp3   (60.3 seconds)
    Clips generated:   3 clips  (Scenes 1, 2, 3 synced)
    Unsynced scenes:   2  (Scenes 4 and 5 — silent)

  SCENES:
  +-------+----------+-----------+---------------------+---------------------+
  | Scene | Duration | Render    | Code File           | Audio               |
  +-------+----------+-----------+---------------------+---------------------+
  |   1   | 12.5s    | rendered  | scenes/intro.py     | clip_001.mp3 synced |
  |   2   | 18.5s    | rendered  | scenes/concept.py   | clip_002.mp3 synced |
  |   3   | 16.8s    | rendered  | scenes/example.py   | clip_003.mp3 synced |
  |   4   |  7.0s    | pending   | scenes/conclusion.py| silent              |
  |   5   |  5.5s    | FAILED    | not assigned        | silent              |
  +-------+----------+-----------+---------------------+---------------------+

  EXPORT:
    Ready to export:   NO
    Reason:            1 scene pending, 1 scene failed, 1 scene missing code file.

  What to do next:
    render scene 4
    set scene 5 code <path_to_file.py>
    render failed

supermanim>
```

---

##### Subsubsection 0.4.10.10 — `open output` *(recommended)*

**What it does:**

This command opens the `output/` folder of your project directly in your operating system's
file manager — the same window you would get if you navigated there yourself using
File Explorer on Windows, Finder on macOS, or Nautilus on Linux.

Instead of leaving SuperManim, navigating to your project folder, and opening the `output/`
subfolder by hand, you can do it with a single command without interrupting your workflow.

Use this when you want to quickly browse your rendered video files, copy them somewhere,
or open one in a video player.

**Syntax:**

```
open output
```

**What the tool prints back:**

```
supermanim> open output

  Opening output folder in your file manager...
  Folder: /home/user/projects/MyAnimation/output/

  Done.

supermanim>
```

**What the tool prints back — when the output folder is empty or does not exist yet:**

```
supermanim> open output

  WARNING: The output folder is empty. No scenes have been rendered yet.
  Folder: /home/user/projects/MyAnimation/output/

  Opening it anyway...
  Done.

supermanim>
```

---

##### Subsubsection 0.4.10.11 — `open project folder` *(recommended)*

**What it does:**

This command opens the entire root folder of your project in your operating system's
file manager.

While `open output` opens just the `output/` subfolder, `open project folder` opens
the top-level project directory — so you can see everything: the `output/` folder,
the `previews/` folder, the `audio/` folder, the `project.db` database file, and anything
else inside the project.

Use this when you need a full view of the project's files — for example, to check file
sizes, copy the whole project somewhere, or inspect the folder structure.

**Syntax:**

```
open project folder
```

**What the tool prints back:**

```
supermanim> open project folder

  Opening project folder in your file manager...
  Folder: /home/user/projects/MyAnimation/

  Done.

supermanim>
```

---

##### Subsubsection 0.4.10.12 — `open log` *(recommended)*

**What it does:**

This command opens the SuperManim log file for the current project in your system's
default text editor.

SuperManim keeps a detailed log of everything it does. Every command you type, every
render that starts and finishes, every error that occurs, every file that is created
or deleted — all of it is written to a log file called `supermanim.log` inside your
project folder.

Most of the time, you do not need to look at the log. The tool tells you everything
important directly in the terminal. But when something goes wrong in a way that is
hard to understand — a render fails with a confusing error, a file seems to appear or
disappear unexpectedly, the tool behaves in an unexpected way — the log file is where
you go to understand exactly what happened and why.

**Syntax:**

```
open log
```

**What the tool prints back:**

```
supermanim> open log

  Opening log file in your text editor...
  File: /home/user/projects/MyAnimation/supermanim.log

  Done.

supermanim>
```

**What the tool prints back — when no log file exists yet:**

```
supermanim> open log

  No log file found for this project yet.
  File: /home/user/projects/MyAnimation/supermanim.log

  A log file is created automatically the first time the tool
  performs an operation (such as rendering or exporting).
  Run a command first, then open the log.

supermanim>
```

---

##### Subsubsection 0.4.10.13 — `reset project` *(recommended)*

**What it does:**

This command resets the entire project back to the state it was in right after it was
first created — as if you just ran `new project` for the first time.

It clears everything:
- All scene render statuses are reset to `pending`.
- All stored fingerprints are deleted.
- All audio clip assignments are removed.
- All `synced_with_audio` flags are set back to `False`.
- All rendered video clips in the `output/` folder are deleted.
- All preview files in the `previews/` folder are deleted.
- All generated audio clips in the `audio/clips/` folder are deleted.

It does NOT delete:
- Your project settings (name, number of scenes, scene durations).
- Your code file assignments (which `.py` file belongs to which scene).
- Your original audio file.
- Your Python code files themselves (they are outside the project folder).

Think of `reset project` as "start the rendering process from scratch, but keep all
my settings and file assignments." You will need to re-render and re-export everything
after a reset.

Because this command is destructive and cannot be undone, the tool will warn you clearly
and ask for confirmation before doing anything.

**Syntax:**

```
reset project
```

**What the tool prints back:**

```
supermanim> reset project

  WARNING: This will reset the entire project back to its initial state.

  The following will be PERMANENTLY DELETED:
    - All rendered video clips in output/        (5 files,  ~430 MB)
    - All preview files in previews/             (4 files,  ~ 71 MB)
    - All generated audio clips in audio/clips/  (3 files,  ~  8 MB)
    - All stored render fingerprints.
    - All audio sync assignments.

  The following will be KEPT:
    - Project name and settings.
    - Scene durations.
    - Code file assignments (which .py goes to which scene).
    - Your original audio file: audio/voice.mp3

  Total data that will be deleted:  ~509 MB
  This cannot be undone.

  Type "yes" to confirm, or anything else to cancel:
  > yes

  Deleting rendered clips...    done.  (5 files removed)
  Deleting preview files...     done.  (4 files removed)
  Deleting audio clips...       done.  (3 files removed)
  Clearing fingerprints...      done.
  Clearing sync assignments...  done.
  Resetting all scene statuses to pending...  done.

  Project has been reset.
  All scenes are now pending. You will need to re-render everything.

  Suggested next step:
    render all

supermanim>
```

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

COMPONENT 3: BUSINESS LOGIC
-------------------------------
What Is Business Logic?
=========================
Business Logic is the set of step-by-step workflows that the system
executes to complete a user's request. It is the "how" — not "is this
allowed?" (that is Business Rules) and not "what is this thing?"
(that is Entities). Business Logic is the sequence of actions.

If Business Rules are the laws, and Entities are the citizens,
then Business Logic is the government — the organization that
takes a citizen's request, checks the laws, and carries out
the appropriate actions.

Business Logic Is What Connects Everything
===========================================
Business Logic is the glue between:
- Entities (the data it works with)
- Business Rules (the checks it performs)
- Ports (the external things it calls for data and output)

```
+=====================================================================+
|              WHAT BUSINESS LOGIC CONNECTS                           |
+=====================================================================+
|                                                                     |
|   Business Rules        Entities           Ports                    |
|   (is this allowed?)    (the data)         (external tools)         |
|         |                    |                   |                  |
|         |                    |                   |                  |
|         +────────────────────+───────────────────+                  |
|                              |                                      |
|                              v                                      |
|                   BUSINESS LOGIC                                    |
|                   (the step-by-step workflow)                       |
|                   "Here is what we do, in this order,              |
|                    checking these rules, using this data,           |
|                    calling these external things."                  |
|                                                                     |
+=====================================================================+
```

The Business Logic Workflows in SuperManim
===============================================
Let us walk through the complete Business Logic for three key operations.

---

Business Logic 1 — Creating a New Project
====================================================
====================================================
When the user types `new project MyAnimation`, this is the complete
workflow that Business Logic executes:

```
+=====================================================================+
|   BUSINESS LOGIC: create_project("MyAnimation")                     |
+=====================================================================+
|                                                                     |
|   STEP 1: Validate the project name.                                |
|   ────────────────────────────────────────────────────────────     |
|   Call ValidationService.project_name_is_valid("MyAnimation")       |
|   Check: does it contain spaces? Is it empty?                       |
|   If errors → send error message → STOP.                            |
|                                                                     |
|   STEP 2: Check the project does not already exist.                 |
|   ────────────────────────────────────────────────────────────     |
|   Call ProjectRepositoryPort.project_exists("MyAnimation")          |
|   If it exists → send error "project already exists" → STOP.        |
|                                                                     |
|   STEP 3: Create the folder structure on disk.                      |
|   ────────────────────────────────────────────────────────────     |
|   Call FileStoragePort.create_folder("projects/MyAnimation")         |
|   Call FileStoragePort.create_folder("projects/MyAnimation/scenes") |
|   Call FileStoragePort.create_folder("...audio_clips")              |
|   Call FileStoragePort.create_folder("...cache")                    |
|   Call FileStoragePort.create_folder("...output")                   |
|   Call FileStoragePort.create_folder("...previews")                 |
|   Call FileStoragePort.create_folder("...assets")                   |
|   Call FileStoragePort.create_folder("...temp")                     |
|   Call FileStoragePort.create_folder("...exports")                  |
|                                                                     |
|   STEP 4: Create the Project Entity.                                |
|   ────────────────────────────────────────────────────────────     |
|   project = Project(name="MyAnimation", mode=None, ...)             |
|                                                                     |
|   STEP 5: Save the Project to the database.                         |
|   ────────────────────────────────────────────────────────────     |
|   Call ProjectRepositoryPort.save_project(project)                  |
|   This creates project_data.db and writes the first record.         |
|                                                                     |
|   STEP 6: Set this as the currently active project.                 |
|   ────────────────────────────────────────────────────────────     |
|   self._current_project = project                                   |
|                                                                     |
|   STEP 7: Tell the user it worked.                                  |
|   ────────────────────────────────────────────────────────────     |
|   Call NotificationPort.send_success(                               |
|       "Project MyAnimation created successfully."                    |
|   )                                                                 |
|                                                                     |
+=====================================================================+
```

---

Business Logic 2 — Rendering a Scene
====================================================
====================================================


This is the most important piece of Business Logic in SuperManim.
It is what saves users from waiting 100 minutes when they only need 5.

```
+=====================================================================+
|   BUSINESS LOGIC: render_scene(scene_id=3)                          |
+=====================================================================+
|                                                                     |
|   STEP 1: Check a project is open.  (Business Rule 1.1)            |
|   ────────────────────────────────────────────────────────────     |
|   if self._current_project is None → error → STOP.                  |
|                                                                     |
|   STEP 2: Load the Scene Entity from the database.                  |
|   ────────────────────────────────────────────────────────────     |
|   scene = SceneRepositoryPort.load_scene(3)                         |
|   Returns a Scene object with all its fields.                        |
|                                                                     |
|   STEP 3: Validate the scene is renderable.  (Business Rule 5.2)   |
|   ────────────────────────────────────────────────────────────     |
|   errors = ValidationService.scene_is_renderable(scene)             |
|   Checks: does it have a code_path? Does it have a duration?        |
|   If errors → send each error to user → STOP.                       |
|                                                                     |
|   STEP 4: Compute the current fingerprint.   (Business Rule 3.2)   |
|   ────────────────────────────────────────────────────────────     |
|   current_hash = HashComputerPort.compute(scene.code_path)          |
|   Reads the code file. Computes SHA-256. Returns a string.          |
|                                                                     |
|   STEP 5: Load the stored fingerprint.                              |
|   ────────────────────────────────────────────────────────────     |
|   stored_hash = CacheRepositoryPort.load_hash(scene_id=3)           |
|   Reads from the database. Returns a string or None.                |
|                                                                     |
|   STEP 6: Has it changed?            (Business Rule 5.1)           |
|   ────────────────────────────────────────────────────────────     |
|   changed = HashService.has_changed(current_hash, stored_hash)      |
|                                                                     |
|   if NOT changed:                                                   |
|       NotificationPort.send_info("Scene 3 unchanged. Skipped.")     |
|       STOP. (no render needed)                                       |
|                                                                     |
|   STEP 7: If synced with audio, check durations match.             |
|   ────────────────────────────────────────────────────────────     |
|   if scene.synced_with_audio:                                       |
|       clip = AudioRepositoryPort.load_clip_for_scene(3)             |
|       errors = ValidationService.sync_is_valid(scene, clip)         |
|       if errors → send error → STOP.                                |
|                                                                     |
|   STEP 8: Call Manim.                                               |
|   ────────────────────────────────────────────────────────────     |
|   result = RenderRunnerPort.render(scene)                           |
|   This is where the actual animation rendering happens.             |
|   Manim runs. Takes minutes. Returns a RenderResult Entity.         |
|                                                                     |
|   STEP 9: Save the result.                                          |
|   ────────────────────────────────────────────────────────────     |
|   if result.succeeded:                                              |
|       SceneRepositoryPort.mark_as_rendered(3, result.video_path)   |
|       CacheRepositoryPort.save_hash(3, current_hash)                |
|       NotificationPort.send_success("Scene 3 rendered.")            |
|   else:                                                             |
|       SceneRepositoryPort.mark_as_failed(3, result.error_message)  |
|       NotificationPort.send_error("Scene 3 FAILED: ...")            |
|                                                                     |
+=====================================================================+
```

---

Business Logic 3 — Exporting the Final Video
====================================================
====================================================


```
+=====================================================================+
|   BUSINESS LOGIC: export_project()                                  |
+=====================================================================+
|                                                                     |
|   STEP 1: Check a project is open.                                  |
|                                                                     |
|   STEP 2: Load all scenes.                                          |
|   scenes = SceneRepositoryPort.load_all_scenes()                    |
|                                                                     |
|   STEP 3: Validate all scenes are rendered. (Business Rule 6.1)    |
|   errors = ValidationService.project_is_exportable(scenes)          |
|   Checks every scene has status="rendered".                         |
|   If any scene is pending or failed → list them → STOP.             |
|                                                                     |
|   STEP 4: Verify all video files exist on disk.                     |
|   For each scene, check its video_path actually exists.             |
|   If any file is missing (deleted by user?) → report it → STOP.    |
|                                                                     |
|   STEP 5: Load export settings.                                     |
|   project = ProjectRepositoryPort.load_project(...)                 |
|   format  = project.export_format    (e.g. "mp4")                  |
|   quality = project.export_quality   (e.g. "high")                 |
|   name    = project.export_name      (e.g. "MyAnimation_final")    |
|                                                                     |
|   STEP 6: Assemble the final video.                                 |
|   VideoAssemblerPort.assemble(                                      |
|       scene_video_paths = [s.video_path for s in scenes],           |
|       output_path       = f"exports/{name}.{format}",               |
|       quality           = quality                                   |
|   )                                                                 |
|   FFmpeg stitches all clips together in order.                      |
|                                                                     |
|   STEP 7: Tell the user the export is done.                         |
|   NotificationPort.send_success(                                    |
|       f"Export complete: exports/{name}.{format}"                   |
|   )                                                                 |
|                                                                     |
+=====================================================================+
```

---

# CHAPTER 5 — ALL THREE COMPONENTS TOGETHER

Now that we understand each component separately, let's see how they
work together when a user types one command.

```
+=====================================================================+
|   USER TYPES: sync scene 3 audio_clip 3                            |
+=====================================================================+
|                                                                     |
|   THE BUSINESS LOGIC (AudioService.sync_scene) RUNS:               |
|                                                                     |
|   1. Loads Scene 3 Entity from database.                            |
|      scene = SceneRepositoryPort.load_scene(3)                      |
|      scene.id=3, scene.duration=16.8, scene.synced=False           |
|                  ↑                                                  |
|           ENTITY: Scene object with its fields                      |
|                                                                     |
|   2. Loads AudioClip 3 Entity from database.                        |
|      clip = AudioRepositoryPort.load_clip(3)                        |
|      clip.duration=16.8, clip.file_path="audio_clips/clip_003.mp3"  |
|                  ↑                                                  |
|           ENTITY: AudioClip object with its fields                  |
|                                                                     |
|   3. Checks the Business Rule: do durations match?                  |
|      errors = ValidationService.sync_is_valid(scene, clip)          |
|      abs(16.8 - 16.8) = 0.0  <  0.001  →  VALID                   |
|               ↑                                                     |
|        BUSINESS RULE: Duration Matching Rule (Rule 4.1)             |
|                                                                     |
|   4. Updates the Scene Entity.                                      |
|      scene.synced_with_audio = True                                  |
|      scene.audio_clip_path   = "audio_clips/clip_003.mp3"           |
|               ↑                                                     |
|        ENTITY: Scene object updated in memory                       |
|                                                                     |
|   5. Saves the updated Entity to the database.                      |
|      SceneRepositoryPort.save_scene(scene)                          |
|                                                                     |
|   6. Tells the user it worked.                                      |
|      NotificationPort.send_success(                                  |
|          "Scene 3 synced with clip_003.mp3."                        |
|      )                                                              |
|                                                                     |
|   RESULT:                                                           |
|   Entity (Scene 3) updated.                                         |
|   Business Rule (duration match) enforced.                          |
|   Business Logic (sync workflow) completed.                         |
|                                                                     |
+=====================================================================+
```

---

# CHAPTER 6 — THE COMPLETE CORE MAP

Here is every single piece of the Core — Entities, Business Rules
(in Domain Services), and Business Logic (in Application Services)
— in one final diagram.

```
+=====================================================================+
|                    THE COMPLETE CORE OF SUPERMANIM                  |
+=====================================================================+
|                                                                     |
|  ENTITIES (core/entities/)                                          |
|  ───────────────────────────────────────────────────────────────   |
|  Scene          id, duration, code_path, status, hash,             |
|                 video_path, synced_with_audio, audio_clip_path,    |
|                 error_message                                        |
|                                                                     |
|  Project        name, mode, folder_path, created_at,               |
|                 export_format, export_quality, export_name          |
|                                                                     |
|  AudioClip      id, file_path, duration, clip_index,               |
|                 scene_id, format, sample_rate, channels             |
|                                                                     |
|  RenderResult   succeeded, video_path, error_message, elapsed_time  |
|                                                                     |
|  ───────────────────────────────────────────────────────────────   |
|                                                                     |
|  DOMAIN SERVICES — BUSINESS RULES (core/domain/)                    |
|  ───────────────────────────────────────────────────────────────   |
|  ValidationService                                                  |
|    project_name_is_valid()       Rule 1.3 — no spaces in name      |
|    scene_is_renderable()         Rule 5.2 — needs code + duration  |
|    scene_is_previewable()        Rule 5.2 variant for previews      |
|    project_is_exportable()       Rule 6.1 — all scenes rendered    |
|    sync_is_valid()               Rule 4.1 — durations must match   |
|    audio_format_is_supported()   Rule 4.4 — mp3/wav/ogg/aac only  |
|    export_format_is_supported()  Rule 6.2 — mp4/webm/mov/avi only |
|    scene_number_is_valid()       Rule 3.3 — must be 1..N          |
|                                                                     |
|  TimelineService                                                    |
|    durations_match()             Rule 4.1 — core duration check    |
|    total_duration()              Rule 4.2 — sum of all scenes      |
|    total_matches_audio()         Rule 4.2 — sum vs audio length    |
|    duration_difference()         Calculates how far off            |
|    find_unmatched_scenes()       Finds all mismatched scenes        |
|                                                                     |
|  HashService                                                        |
|    has_changed()                 Rule 5.1 — is re-render needed?   |
|    find_changed_scenes()         Rule 5.1 — which scenes changed?  |
|    all_unchanged()               Rule 5.1 — can we skip all?       |
|                                                                     |
|  ───────────────────────────────────────────────────────────────   |
|                                                                     |
|  APPLICATION SERVICES — BUSINESS LOGIC (core/application/)          |
|  ───────────────────────────────────────────────────────────────   |
|  ProjectService     create, open, close, delete, info              |
|  SceneService       set_number, add, set_duration, set_code,       |
|                     list, delete, swap, duplicate, info            |
|  AudioService       add, split_auto, split_manual,                 |
|                     change_format, sync, unsync, info              |
|  RenderService      render_scene, render_all, render_pending,      |
|                     render_failed, force_render, status, cache     |
|  PreviewService     preview_scene, preview_all, force_preview,     |
|                     open, clear, status                             |
|  ExportService      export, status, set_format, set_quality,       |
|                     set_name                                        |
|                                                                     |
+=====================================================================+
```

---

**FINAL SUMMARY**

The Core of SuperManim is a protected island of pure Python logic
that knows nothing about SQLite, Manim, FFmpeg, or the terminal.
It contains exactly three things:

**Entities** are the data shapes — the Python objects that represent
the real things in the system: Scene, Project, AudioClip, RenderResult.
They are containers of information. They hold state. They have fields.
They do not call databases or external programs.

**Business Rules** are the laws — the constraints that say what is
allowed and what is not. They live in Domain Services: ValidationService,
TimelineService, and HashService. They take Entities as input,
apply a rule, and return a yes/no or a list of errors.
They never call Ports. They are pure Python logic.

**Business Logic** is the workflow — the step-by-step instructions
for completing a user request. It lives in Application Services.
It uses Entities as its data, calls Business Rules to check validity,
and calls Ports to communicate with the outside world (database,
Manim, FFmpeg, terminal). Every public method on a Service is
the implementation of one Use Case — one thing the user wants to do.

```
+=====================================================================+
|                                                                     |
|   ENTITIES      =   WHAT the system works with                      |
|                     Scene, Project, AudioClip, RenderResult         |
|                                                                     |
|   BUSINESS      =   WHAT the system is allowed to do               |
|   RULES             ValidationService, TimelineService, HashService |
|                                                                     |
|   BUSINESS      =   HOW the system does it, step by step           |
|   LOGIC             ProjectService, SceneService, AudioService,     |
|                     RenderService, PreviewService, ExportService    |
|                                                                     |
+=====================================================================+
```

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





















###### The third component is the Adaptors:
What are the adapters:
-----------------------
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



