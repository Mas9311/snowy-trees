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

I originally made this little loop to minimize the light emitted from a monitor at night.<br>
The [CHRISTMA EXEC](https://en.wikipedia.org/wiki/Christmas_Tree_EXEC) worm from 1987 was the inspiration for the design and I have  added snow for effect.

## Usage ##
 1. [Download this repo](https://github.com/Mas9311/snowy-trees/archive/v0.1.zip) <br>
 1. Extract or <code>unzip</code> the snowy-trees-0.1.zip file, then delete the zip.
 1. A one-liner *can* be executed with:<br>
        <code>$ cd _/path/to/snowy-trees-0.1/_ && python3 run.py</code><br>
        but that will print the welcome screen for using the defaults.<br>
 - **Note**: By default, the options are set to: <br>
          <code>--width 125</code> <code>--speed average</code> <code>--density average</code> <code>--tiers 4</code> <code>--no</code>

 - usage: **python3 run.py \[-w int] \[-s str] \[-d str] \[-t int] \[-y | -n] \[--version] \[--help]**
### Demos for configuration ###

I have added demonstrations for the values follow the width, speed, density, and tiers arguments.<br>
After any of the aforementioned argument, you can add --config after to view the demo.<br>
**Note**: they can be chained together to execute each demo in left-to-right order such as:<br>
<code>$ python3 run.py -w --config -s --config -d --config -t --config</code>

### Create a Desktop launcher ###

Before creating a Launcher, I recommend fine-tuning your configurations first via Terminal.<br>

###### Linux users #####

I have provided my configurations as a baseline *template* for you to get you started.<br>
I use the Xubuntu distro, which comes with <code>xfce4-terminal</code> as the default Terminal application, so change the application to your Terminal emulator of choice.<br>
*Most* Terminal emulators come with the optional arguments stated below, i.e. --geometry, --maximize, ...<br>
The geometry offsets, <code>+0+0</code> and <code>-0+0</code>, are the easiest way to assign it to the left and right monitors respectively.

 Portrait monitors:
 
   - Command: <code>xfce4-terminal --geometry=154x65+0+0 --maximize --hide-menubar --hide-toolbar --hide-scrollbar -e 'python3 run.py -w 154 -s slow -d thin -t 4 -n'</code>
   - Working Directory: _/full/path/to/snowy-trees_
   - Icon: <img src="/assets/icons/tree_icon.png"
                 alt="Snowy Tree icon" 
                 height="30" /> which can be found in */snowy-trees-0.2/assets/icons/tree_icon.png*
   
 Landscape monitors: 
 
   - Command: <code>xfce4-terminal --geometry=274x34-0+0 --maximize --hide-menubar --hide-toolbar --hide-scrollbar -e "python3 run.py -w 274 -s average -d heavy -t 6 -y"</code>
   - Working Directory: _/full/path/to/snowy-trees_
   - Icon: <img src="/assets/icons/tree_icon.png"
                 alt="Snowy Tree icon" 
                 height="30" /> which can be found in */snowy-trees-0.2/assets/icons/tree_icon.png*
