# Random Snow and Happy Trees #

I originally made this cozy little loop to minimize the light on the pother monitor when I'm awake at night.<br>
The inspiration for the design is the [CHRISTMA EXEC](https://en.wikipedia.org/wiki/Christmas_Tree_EXEC) worm from 1987. I have added the snow for effect.

## Usage ##
Simply <code>cd</code> into the __/snowy-tree*/__ folder and execute the <code>run.py</code> file.<br>
By default, the options are set to <code>--width 271</code> <code>--speed average</code> <code>--density average</code> <code>--tiers 4</code> <code>--no</code>

 - python3 run.py \[-w int] \[-s str] \[-d str] \[-t int] \[-y | -n] \[--help] \[--version]

### Create a Desktop launcher ###

Before creating a Launcher, I recommend fine-tuning your configurations first in another Terminal window.

###### Linux users ######
I have provided you with my configurations as a template, but feel free to change the arguments to whatever you want.
I use Xubuntu, which comes with <code>xfce4-terminal</code> as the default Terminal application, so change that to your go-to Terminal emulator.
*Most* Terminal emulators come with the additional flags \[--geometry, --maximize, ...].<br>
The geometry, <code>+0+0</code> and <code>-0+0</code>, is to access the left-most and right-most monitors respectively.

 1. Portrait monitors:
   - Command: <code>xfce4-terminal --geometry=154x65+0+0 --maximize --hide-menubar --hide-toolbar --hide-scrollbar -e 'python3 run.py -w 154 -s slow -d thin -t 4 -n'</code>
   - Working Directory: /path/to/snowy-trees
 2. Landscape monitors:
   - Command: <code>xfce4-terminal --geometry=274x34-0+0 --maximize --hide-menubar --hide-toolbar --hide-scrollbar -e "python3 run.py -w 274 -s average -d heavy -t 6 -y"</code>
   - Working Directory: /path/to/snowy-trees
