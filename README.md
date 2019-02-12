# Random Snow and Happy Trees #

I made this cozy little loop to distract me when I'm awake at night on my computer.<br>
The [CHRISTMA EXEC](https://en.wikipedia.org/wiki/Christmas_Tree_EXEC) worm from 1987 was the inspiration for the design and added snow for effect.

## Usage ##
As with all of my programs, you simply have to <code>cd</code> into the folder and execute the <code>run.py</code> file.<br>
By default, the options are <code>wide</code> <code>slow</code> <code>light</code> <code>none</code>
If you want to use the options, be sure to input them in the given order for now:<br>
monitor_aspect snow_speed snow_density show_the_ornaments

 - python3 run.py \[wide, tall] \[slow, average, fast, ultra] \[light, moderate, heavy] \[none]

### Create a Desktop launcher ###
###### Linux users ######
I set the geometry offset option to my configuration, but feel free to modify the options provided:
 1. Portrait monitors:
   - Command: x-terminal-emulator -geometry 151x130+0+0 & -e "python3 run.py tall slow light none"
   - Working Directory: /path/to/snowy-trees
 2. Landscape monitors:
   - x-terminal-emulator -geometry 271x68+1080+600 & -e "python3 run.py wide average heavy useThem!"
   - Working Directory: /path/to/snowy-trees
