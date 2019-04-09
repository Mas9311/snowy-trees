# Random Snow and Happy Trees
<p align="center">
  <img src="/assets/icons/tree_icon.png"
       alt="Snowy Tree icon"
       height="80" />
</p>
<p align="center">
  <a href="https://www.gnu.org/licenses/gpl-3.0">
    <img src="https://img.shields.io/badge/License-GPLv3-blue.svg"
         alt="[License: GPL v3]" />
  </a>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/python-3.x-blue.svg"
         alt="[python: 3.x]" />
  </a>
</p>

#### Prerequisites
 <code>pip3 install screeninfo pyautogui</code><br>
 - If you encounter the Xlib error, <code>pip3 install Xlib</code>

## Usage

I will be using <code>python3</code> as a placeholder, but it is OS-dependent.
  - If Windows: execute python programs with <code>python.exe</code>.<br>
  - Else: execute python programs with <code>python3</code>.<br>
    
 1. Open a Terminal window and paste: <code> git clone https://www.github.com/Mas9311/snowy-trees.git </code>
 1. Extract or <code>unzip</code> the snowy-trees.zip file, then delete the zip.
 1. <code>cd path/to/snowy-trees/</code>
 1. Execute the program with: <code>python3 run.py</code><br>
    - This will print the welcome screen, because you have not added any extra arguments.<br>
 1. Try the cli and the gui to find which looks more appealing.
 
### Motivation

To minimize the light emitted from a monitor at night, I opened a maximized Terminal window.<br>
A blank screen isn't tasteful, so I made ascii art out of the
[CHRISTMA EXEC](https://en.wikipedia.org/wiki/Christmas_Tree_EXEC) worm from 1987.<br>
From there, I developed the CLI, but wasn't quite satisfied at typing the options and rerunning.<br>
I am pleased with the current state of the GUI, but as all projects go, it is never complete.<br>

## Create a Desktop launcher

Tree png can be found in _.../snowy-trees/assets/icons/tree_icon.png_

### Linux users

#### GUI
 - Command: <code>python3 run.py -f my_saved_file</code>
 - Working Directory: _/home/.../snowy-trees_
 - Icon: <img src="/assets/icons/tree_icon.png"
                 alt="Snowy Tree icon" 
                 height="30" />

#### CLI

Before creating a CLI Launcher, I recommend fine-tuning your configurations first via Terminal.<br>

I have provided my configurations as a baseline _template_ for you to get you started.<br>
I use the Xubuntu distro, which comes with <code>xfce4-terminal</code> as the default Terminal application, so change the application to your Terminal emulator of choice.<br>
**Most** Terminal emulators come with the optional arguments stated below, i.e. --geometry, --maximize, ...<br>
The geometry offsets, <code>+0+0</code> and <code>-0+0</code>, are the easiest way to assign it to the left and right monitors respectively.

 Portrait monitors:
 
   - Command: <code>xfce4-terminal --geometry=+0+0 --maximize --hide-menubar --hide-toolbar --hide-scrollbar -e 'python3 run.py -w 154 -s slow -d thin -t 4 -n'</code>
   - Working Directory: _/home/.../snowy-trees_
   - Icon: <img src="/assets/icons/tree_icon.png"
                 alt="Snowy Tree icon" 
                 height="30" />
   
 Landscape monitors: 
 
   - Command: <code>xfce4-terminal --geometry=-0+0 --maximize --hide-menubar --hide-toolbar --hide-scrollbar -e "python3 run.py -c -w 274 -s average -d average -t 6 -y"</code>
   - Working Directory: _/home/.../snowy-trees_
   - Icon: <img src="/assets/icons/tree_icon.png"
                 alt="Snowy Tree icon" 
                 height="30" />
