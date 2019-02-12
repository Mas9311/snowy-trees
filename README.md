# Random Snow and Happy Trees #

I made this cozy little loop to distract me when I'm awake at night on my computer.<br>
I got the inspiration from the *CHRISTMA EXEC* worm from back in 1987, but don't worry for this is not a worm.

## Usage ##
As with all of my programs, you simply have to cd into the folder and execute the run.py file.<br>
By default, the options are <code>wide</code> <code>slow</code> <code>light</code> <code>none</code>
If you want to use the options, be sure to input them in the given order for now:<br>
monitor_aspect snow_speed snow_density show_the_ornaments

 - python3 run.py \[wide, tall] \[slow, average, fast, ultra] \[heavy, moderate, light] \[none]

### Create a Desktop launcher ###
###### Linux users ######
I set the offsets to my configuration, but feel free to modify the options provided
 1. Portrait monitors
   - Command: x-terminal-emulator -geometry 151x130+0+0 & -e "python3 run.py tall slow light none"
   - Working Directory: /path/to/snowy-trees
 2. Landscape monitors
   - x-terminal-emulator -geometry 271x68+1080+600 & -e "python3 run.py wide average heavy useThem!"
   - Working Directory: /path/to/snowy-trees
