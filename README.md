# Random Snow and Happy Trees #

I made this little loop to minimize the light emitted from a monitor at night.<br>
The [CHRISTMA EXEC](https://en.wikipedia.org/wiki/Christmas_Tree_EXEC) worm from 1987 was the inspiration for the design and I have  added snow for effect.

## Usage ##
Simply <code>cd</code> into the __/snowy-tree*/__ folder and execute the <code>run.py</code> file.<br>
By default, the options are set to <code>--width 271</code> <code>--speed average</code> <code>--density average</code> <code>--tiers 4</code> <code>--no</code>

 - python3 run.py \[-w int] \[-s str] \[-d str] \[-t int] \[-y | -n] \[--help] \[--version]

### Create a Desktop launcher ###
###### Linux users ######
I set the geometry offset option to my configuration, but feel free to modify the options provided:

 Landscape monitors:
   - Command: <code>x-terminal-emulator -geometry 271x68+0+0 & -e "python3 run.py -w 271 -s average -d heavy -t 6 -y"</code>
   - Working Directory: /path/to/snowy-trees
   
 Portrait monitors:
   - Command: <code>x-terminal-emulator -geometry 151x130+0+0 & -e "python3 run.py -w 151 -s slow -d light -t 10 -n"</code>
   - Working Directory: /path/to/snowy-trees
