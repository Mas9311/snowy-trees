# Random Snow and Happy Trees #

I originally made this little loop to minimize the light emitted from a monitor at night.<br>
The [CHRISTMA EXEC](https://en.wikipedia.org/wiki/Christmas_Tree_EXEC) worm from 1987 was the inspiration for the design and I have  added snow for effect.

## Usage ##
Simply <code>cd</code> into the __/snowy-tree*/__ folder and execute the <code>run.py</code> file.<br>
By default, the options are set to <code>--width 271</code> <code>--speed average</code> <code>--density average</code> <code>--tiers 4</code> <code>--no</code>

 - python3 run.py \[-w int] \[-s str] \[-d str] \[-t int] \[-y | -n] \[--help] \[--version]

### Create a Desktop launcher ###

Before creating a Launcher, I recommend fine-tuning your configurations first via Terminal.

###### Linux users #####

I have provided my configurations as a baseline *template* for you.<br>
I use the Xubuntu distro, which comes with <code>xfce4-terminal</code> as the default Terminal application, so change the application to your Terminal emulator.<br>
*Most* Terminal emulators come with the additional flags \[--geometry, --maximize, ...].<br>
The geometry offsets, <code>+0+0</code> and <code>-0+0</code>, are the easiest way to assign it to the left and right monitors respectively.

 Portrait monitors:
 
   - Command: <code>xfce4-terminal --geometry=154x65+0+0 --maximize --hide-menubar --hide-toolbar --hide-scrollbar -e 'python3 run.py -w 154 -s slow -d thin -t 4 -n'</code>
   
   - Working Directory: /path/to/snowy-trees
   
 Landscape monitors:
 
   - Command: <code>xfce4-terminal --geometry=274x34-0+0 --maximize --hide-menubar --hide-toolbar --hide-scrollbar -e "python3 run.py -w 274 -s average -d heavy -t 6 -y"</code>

   - Working Directory: /path/to/snowy-trees
