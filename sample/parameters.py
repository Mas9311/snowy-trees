import argparse
import calendar
import time

import sys

from sample.file_helper import import_from_file
from sample.format import py_cmd, Notification
from sample.image import Tree


def default_configurations():
    return {
        'interface': True,      # True=GUI interface, False=CLI interface
        'width': 125,           # 125 characters long
        'speed': 'slow',        # slow refresh rate between printing
        'density': 'average',   # average snowfall density
        'tiers': 4,             # 4 triangles on Tree
        'ornaments': True,      # True=print ornaments, False=don't print ornaments
        'length': 5,            # 5 unique Trees in the list to print from
        'maximized': False,     # GUI: False=not maximized, True=maximized
        'textbox': 'm',         # GUI: medium-sized font of where Tree is printed
        'toolbar': 'm',         # GUI: large-sized font of the top-left buttons
        'windows': 'm',         # GUI: large-sized - + x of the top-right buttons [ − + × ]
        'w_dim': 0,             # GUI: width    of pop up window in pixels
        'h_dim': 0,             # GUI: height   of pop up window in pixels
        'x_dim': 0,             # GUI: x-offset of pop up window in pixels
        'y_dim': 0,             # GUI: y-offset of pop up window in pixels
        'verbose': False        # False=don't print every little thing, True=print everything that changes
    }


def speed_dict():
    return {
        'slow': 0.9810000,      # about a second
        'average': 0.7265000,   # about 3/4ths of a second
        'fast': 0.465000,       # about half a second
        'ultra': 0.1            # Do NOT set 'ultra' as anything lower than 0.05!
    }


def speed_choices():
    return [s for s in speed_dict().keys()]


def density_dict():
    return {
        'thin': 36,             # 03.6% chance to print a snowflake
        'average': 128,         # 12.8% chance to print a snowflake
        'thick': 512,           # 51.2% chance to print a snowflake
        'ultra': 733            # 73.3% chance to print a snowflake
    }


def density_choices():
    return [d for d in density_dict().keys()]


def font_dict():
    return {
        'textbox': {
            'xs': '"Courier New" -9',
            's': '"Courier New" -10',
            'm': 'Courier -11',
            'l': '"Courier New" 10',
            'xl': 'Courier'
        },
        'toolbar': {
            'xs': '"Courier New" 10 bold',
            's': '"Courier New" 12 bold',
            'm': '"Courier New" 15 bold',
            'l': '"Courier New" 18 bold',
            'xl': '"Courier" 25'
        },
        'windows': {
            'xs': '"Times" -10 bold',
            's': '"Times" 9 bold',
            'm': '"Times" 12 bold',
            'l': '"Times" 15 bold',
            'xl': '"Times New Roman" 18 bold'
        }
    }


def textbox_font_choices():
    return [t for t in font_dict()['textbox'].keys()]


def toolbar_font_choices():
    return [b for b in font_dict()['toolbar'].keys()]


def windows_font_choices():
    return [w for w in font_dict()['windows'].keys()]


def retrieve_parameters():
    """Retrieves the parameters from the console if provided.
    Returns the parameters in dict format.
    If an unknown argument is passed, print the --help screen.
    If no arguments are passed, then print the intro Welcome screen."""
    if '--config' in sys.argv:
        config_argument()
        sys.exit()

    defaults = default_configurations()

    cmd_description = ('             ╔══════════════════════════════════════════════════╗            ┃\n'
                       '             ║   Loops a snowy tree much like a gif wallpaper   ║            ┃\n'
                       '             ╚══════════════════════════════════════════════════╝            ┃\n'
                       '                                                                             ┃\n'
                       '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛')

    parser = argparse.ArgumentParser(usage=py_cmd('[options]') + '                                              ┃',
                                     description=cmd_description,
                                     add_help=False,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    interface = parser.add_mutually_exclusive_group(required=False)
    interface.add_argument('-g', '--gui',
                           action='store_true',
                           default=defaults['interface'],
                           dest='interface',
                           help='GUI printing of the tree. (default=%(default)s)                  '
                                'No additional argument needed.')

    interface.add_argument('-c', '--cli',
                           action='store_false',
                           default=not defaults['interface'],
                           dest='interface',
                           help='CLI printing of the tree. (default=%(default)s)                   '
                                'No additional argument needed.')

    parser.add_argument('-w', '--width',
                        type=int,
                        metavar='',
                        default=defaults['width'],
                        help=(f'WIDTH of the terminal window: (default=%(default)s)                '
                              '   271 => characters printed on a single line on a 32-inch '
                              '          monitor in landscape orientation                 '
                              '   151 => characters printed on a single line on a 32-inch '
                              '          monitor in portrait orientation'))

    parser.add_argument('-s', '--speed',
                        type=str,
                        default=defaults['speed'],
                        metavar='',
                        choices=speed_choices(),
                        help=('SPEED of the refresh: (default=%(default)s)                       '
                              '   slow => the snow falling will print every second.       '
                              'Valid choices are [%(choices)s]'))

    parser.add_argument('-d', '--density',
                        type=str,
                        default=defaults['density'],
                        metavar='',
                        choices=density_choices(),
                        help=('DENSITY of the snow: (default=%(default)s)                     '
                              '   average => 12.8 percent chance of snow.                 '
                              'Valid choices are [%(choices)s]'))

    parser.add_argument('-t', '--tiers',
                        type=int,
                        default=defaults['tiers'],
                        metavar='',
                        choices=range(1, 14),
                        help=('TIERS of tree: (default=%(default)s)                                 '
                              '   4 => Tree has 4 triangular tiers.                       '
                              'Valid choices can only be:                                 '
                              '               [%(choices)s]'))

    ornaments = parser.add_mutually_exclusive_group(required=False)
    ornaments.add_argument('-y', '--yes',
                           action='store_true',
                           default=defaults['ornaments'],
                           dest='ornaments',
                           help='YES ornaments: (default=%(default)s)                              '
                                'Ornaments will be displayed on the tree.')

    ornaments.add_argument('-n', '--no',
                           action='store_false',
                           default=not defaults['ornaments'],
                           dest='ornaments',
                           help=('NO ornaments: (default=%(default)s)                              '
                                 'Ornaments will not be displayed on the tree.'))

    parser.add_argument('-l', '--length',
                        type=length_list_type,
                        default=defaults['length'],
                        metavar='',
                        help=('LENGTH of the tree list to print: (default=%(default)s)              '
                              'Saves your device from wasting electricity to generate all '
                              'the random numbers for snow and ornament arrangement.      '
                              'Valid choices are only whole numbers >= %(default)s.'))

    parser.add_argument('-tf', '--textbox',
                        type=str,
                        default=defaults['textbox'],
                        metavar='',
                        dest='textbox',
                        choices=textbox_font_choices(),
                        help=('TEXTBOX font size of GUI: (default=%(default)s)                 '
                              'The textbox is location of the Tree to be displayed.       '
                              'Valid choices are [%(choices)s]'))

    parser.add_argument('-bf', '--toolbar',
                        type=str,
                        default=defaults['toolbar'],
                        metavar='',
                        dest='toolbar',
                        choices=toolbar_font_choices(),
                        help=('TOOLBAR buttons font size of GUI: (default=%(default)s)          '
                              'These are the toolbar buttons located at the top-left.     '
                              'Valid choices are [%(choices)s]'))

    parser.add_argument('-wf', '--window',
                        type=str,
                        default=defaults['windows'],
                        metavar='',
                        dest='windows',
                        choices=windows_font_choices(),
                        help=('WINDOW manager buttons font size of GUI: (default=%(default)s)   '
                              'These are the − + × buttons located at the top-right.      '
                              'Valid choices are [%(choices)s]'))

    parser.add_argument('--wdim',
                        type=dimension_type,
                        metavar='',
                        default=defaults['w_dim'],
                        dest='w_dim',
                        help=(f'WIDTH of the GUI window, in pixels:                        '
                              'Instead of using this option, just alter the GUI\'s width   '
                              'manually and save it to a configuration file.'))

    parser.add_argument('--hdim',
                        type=dimension_type,
                        metavar='',
                        default=defaults['h_dim'],
                        dest='h_dim',
                        help=(f'HEIGHT of the GUI window, in pixels:                       '
                              'Instead of using this argument, just alter the height of    '
                              'the GUI manually and save it to a configuration file.'))

    parser.add_argument('--xdim',
                        type=dimension_type,
                        metavar='',
                        default=defaults['x_dim'],
                        dest='x_dim',
                        help=(f'X-offset of the GUI window, in pixels:                     '
                              'Instead of using this argument, just drag the GUI to the    '
                              'x-coordinate manually and save it to a configuration file.'))

    parser.add_argument('--ydim',
                        type=dimension_type,
                        metavar='',
                        default=defaults['y_dim'],
                        dest='y_dim',
                        help=(f'Y-offset of the GUI window, in pixels:                     '
                              'Instead of using this argument, just drag the GUI to the    '
                              'y-coordinate and save it to a configuration file.'))

    parser.add_argument('-m', '--max',
                        action='store_true',
                        default=defaults['maximized'],
                        dest='maximized',
                        help=('MAXimize the GUI: (default=%(default)s)                          '
                              'When creating the GUI, maximize the GUI to the current     '
                              'monitor. This is best when used with the x-offset to       '
                              'differentiate which monitor to use.                        '
                              'No additional argument needed => Sets maximized to True.'))

    parser.add_argument('-f', '--file',
                        type=str,
                        metavar='',
                        dest='file',
                        help=('FILE name to import configurations:                        '
                              'Once you have saved the configurations to a file, you can  '
                              'now import those instead of typing all the arguments.      '
                              'Filename must be valid to be successfully imported.        '
                              'Capitalization and extensions (.txt) are superfluous.'))

    parser.add_argument('--verbose',
                        action='store_true',
                        default=defaults['verbose'],
                        dest='verbose',
                        help=('VERBOSE GUI geometry changes: (default=%(default)s)              '
                              'Use this only to debug. Prints out (in pixels) which       '
                              'dimension of the GUI (w_dim, h_dim, x, y) was altered.     '
                              'No additional argument needed => Sets the verbose to True.'))

    version_description = ('           ☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐           \n'
                           '           ☐               ☐  snowy-trees v0.2.1  ☐               ☐           \n'
                           '           ☐               ☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐               ☐           \n'
                           '           ☐                                                      ☐           \n'
                           '           ☐ Check out if there are any new releases for this at: ☐           \n'
                           '           ☐     https://github.com/Mas9311/snowy-trees/releases  ☐           \n'
                           '           ☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐           ')

    parser.add_argument('-v', '--version',
                        action='version',
                        version=version_description,
                        help='VERSION prints to console, and exits.')

    parser.add_argument('-h', '--help',
                        action='help',
                        default=argparse.SUPPRESS,
                        help='HELP message is displayed (this is the message), and exits')

    known_args, unknown_args = parser.parse_known_args()
    arg_dict = {}

    if known_args.file:
        arg_dict = import_from_file(known_args.file)

    if not arg_dict:
        # converts the arguments from a Namespace type => dictionary
        arg_dict = {
            'interface': known_args.interface,
            'width': known_args.width,
            'speed': known_args.speed,
            'density': known_args.density,
            'tiers': known_args.tiers,
            'ornaments': known_args.ornaments,
            'length': known_args.length,
            'maximized': known_args.maximized,
            'textbox': known_args.textbox,
            'toolbar': known_args.toolbar,
            'windows': known_args.windows,
            'w_dim': known_args.w_dim,
            'h_dim': known_args.h_dim,
            'x_dim': known_args.x_dim,
            'y_dim': known_args.y_dim,
            'verbose': known_args.verbose
        }

    if unknown_args:  # user added unknown args, so print the --help screen and exit
        parser.print_help()
        print()
        if len(unknown_args) is 1:
            unrecognized = ' \'' + unknown_args[0] + '\' is'
        else:
            unrecognized = 's ' + str(unknown_args) + ' are'
        Notification([
            f'Argument{"" if len(unknown_args) is 1 else "s"} not recognized',
            f'The argument{unrecognized} not valid',
            f'> [Enter] to quit'
        ])
        input('\n> ')
        print()
        parser.parse_args()  # prints error message and stops execution
        sys.exit()  # redundantly halts execution

    if len(sys.argv) == 1:  # no arguments passed => print the welcome screen
        arg_dict['interface'] = print_welcome(parser)

    return arg_dict


def length_list_type(length_input):
    length_min = default_configurations()['length']
    try:
        length_input = int(length_input)
        if length_input < length_min:
            print_arg_error('List Length', f'{length_input} must be >= {length_min}.', length_min)
        return length_input
    except ValueError:
        print_arg_error('List Length', f'{length_input} is not an int', length_min)
        return length_min


def dimension_type(dim_input):
    dim_min = default_configurations()['w_dim']  # default of 0.
    arg_type = 'Dimension (in pixels)'
    try:
        dim_input = int(dim_input)
        if dim_input < dim_min:
            print_arg_error(arg_type, f'{dim_input} must be >= {dim_min}.', dim_min)
        return dim_input
    except ValueError:
        print_arg_error(arg_type, f'{dim_input} is not an int.', dim_min)
        return dim_min


def print_arg_error(arg_type, message, default_val):
    Notification([
        f'{arg_type} argument Error',
        f'{message}',
        f'Resorting to the default of {default_val}.'
    ])


def print_welcome(parser):
    """This function is called when the user does not include any additional arguments.
    This almost seems counter-productive, but at the very least, the default width
    should not be used. Instead, the user is informed how to run the --config demo.
    After the Welcome screen is printed, it will print the --help option."""

    print('┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┱────────────────────────────────────╔════════╗─╮\n'
          '┃   Welcome to Snowy Trees   ┃                                    ║ v0.2.1 ║ │\n'
          '┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛                                    ╚════════╝ │\n'
          '│                                                                            │\n'
          '│                                                                            │\n'
          '│ No additional arguments detected, so here is the intro welcome message!    │\n'
          '│ The purpose is to show you how to configure the arguments.                 │\n'
          '│ The next screen is the --help menu to show you the arguments available.    │\n'
          '│                                                                            │\n'
          '│ First, you have to decide if you want the GUI or CLI implementation.       │\n'
          '│   - GUI is a dynamic, configurable, pop-up window.          [ RECOMMENDED ]│\n'
          '│   - CLI prints the image to the console, so you will need to manually      │\n'
          '│       configure your arguments and rerun the execution to see a change.    │\n'
          '╰────────────────────────────────────────────────────────────────────────────╯\n')
    input('> [Enter] to read the GUI and CLI descriptions.\n> ')
    print()

    print('┌────────────────────────────────────────────────────────────────────────────┐\n'
          '│                                    GUI:                                    │\n'
          '│ - Once you have your configurations set to your preference, click on the   │\n'
          '│     File > Save As... to save your configurations to a file.               │\n'
          '│ - Load your saved configurations with:                                     │\n'
          '│$ ' + py_cmd('-f tall_monitor') + '                                         │\n'
          '├────────────────────────────────────────────────────────────────────────────┤\n'
          '│                                    CLI:                                    │\n'
          '│ - You will need to run the command with something that looks like:         │\n'
          '│$ ' + py_cmd('-w 179 -s fast -d thin -t 5 -l 7') + '                        │\n'
          '│                                                                            │\n'
          '│ - In order to find your values, there are 4 demos available to help you!   │\n'
          '│     They are --width, --speed, --density, --tiers (or -w, -s, -d, -t)      │\n'
          '│ - To see the demo, type --config after an argument such as:                │\n'
          '│$ ' + py_cmd('-w --config') + '                                             │\n'
          '│     Note: demos can be chained together as shown in:                       │\n'
          '│$ ' + py_cmd('-w --config -s --config -d --config -t --config') + '         │\n'
          '╰────────────────────────────────────────────────────────────────────────────╯')
    input('> [Enter] to print the --help screen.\n> ')
    print()

    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓')
    parser.print_help()

    run_with = ''
    for k in ['width', 'speed', 'density', 'tiers', 'ornaments', 'length']:
        run_with += f'\t{k}: {default_configurations()[k]}\n'
    print(f'Will run with the configurations set to:\n{run_with}')
    Notification([
        '    [Enter] or [c] to continue    ',
        '> [Enter] to run the GUI interface',
        '--Opens in a pop up window',
        '--Customizable configurations',
        '',
        '> [c] to run the CLI interface',
        '--Prints to this console',
        '--Not customizable'
    ])
    answer = input('\n> ').strip().lower()
    print()

    if answer:
        for i in answer:
            if i == 'c':
                return False
    return True


def config_argument():
    """This function is called when the user specifies to run the --config demo on
    one or more optional arguments.
    It will remove the arguments, call the corresponding function associated to the
    argument, and loop until no more --config arguments are left.
        Note: the user cannot group arguments such as '-wsdt --config', but should instead
        run them separately as in '-w --config -s --config -d --config -t --config'"""
    try:
        while sys.argv.index('--config') is not None:
            config_loc = sys.argv.index('--config')
            valid_config = ['-w', '--width', '-s', '--speed', '-d', '--density', '-t', '--tiers']
            arg_to_config = ''
            for curr_arg in range(config_loc, 0, -1):
                if sys.argv[curr_arg] in valid_config:
                    arg_to_config = sys.argv[curr_arg].strip('-')
                    sys.argv.pop(curr_arg)
                    sys.argv.pop(sys.argv.index('--config'))
                    break

            if arg_to_config[0] is 's':
                speed_demo()
            elif arg_to_config[0] is 'd':
                density_demo()
            elif arg_to_config[0] is 't':
                tiers_demo()
            else:
                width_demo()
    except ValueError:
        # no more '--config' arguments left
        pass


def width_demo():
    """Called when the user specifies they wish to run the WIDTH --config demo"""
    print('┌─────────────────────┬────────────────────────────────┬─────────────────────┐\n'
          '│                     │ --width --config Demonstration │                     │\n'
          '│                     └────────────────────────────────┘                     │\n'
          '│ In order to find the best WIDTH (number of characters to print), please    │\n'
          '│     adjust the console window to the desired width before starting.        │\n'
          '│ The width of a line is found on the left-hand side.                        │\n'
          '│                                                                            │\n'
          '│ The goal is to find the number of characters it takes to fill the          │\n'
          '│     entire width of the current console window.                            │\n'
          '├ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┤\n'
          '│ First, it will print line lengths in increments of 50 to get you started.  │\n'
          '│ Then, you will guess the width, and it will print ± 5 of the guess given.  │\n'
          '│   - Guessing will continue until you find the number.                      │\n'
          '└────────────────────────────────────────────────────────────────────────────┘\n')
    input('> [Enter] to print the varying widths.\n'
          '> ')
    print()
    fir_char = '▆'  # ░ ▒ ▓
    sec_char = '·'  # :
    char = fir_char
    for line_len in range(400, 50, -50):
        char = (fir_char, sec_char)[char == fir_char]
        line = char * (line_len - len(str(line_len)) - 1)
        print(str(line_len) + ' ' + line)

    while True:
        guess = retrieve_int('What\'s your best guess of the width of this current console window:')
        char = fir_char

        for line_len in range(guess-5, guess+6):
            char = (fir_char, sec_char)[char == fir_char]
            line = char * (line_len - len(str(line_len)) - 1)
            print(str(line_len) + ' ' + line)
        answer = input('Did you find the number you wanted?\n'
                       '> [y] / [n]\n'
                       '> ').lower().strip()
        print()
        if answer:
            if answer[0] == 'y':
                input(f'\n  Now run it with:\n'
                      f'$ {py_cmd("-w ###")}\n'
                      f'  > [Enter] to continue.\n'
                      f'> ')
                print()
                return


def speed_demo():
    """Called when the user specifies they wish to run the SPEED --config demo"""
    print('┌────────────────────────────────────────────────────────────────────────────┐\n'
          '│                       --speed --config Demonstration                       │\n'
          '│                                                                            │\n'
          '│ There are 4 SPEEDs with varying refresh rates ranging from 1 to .1 seconds.│\n'
          '│                                                                            │\n'
          '│ The goal is to find which speed string is the most appealing to you.       │\n'
          '├ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┤\n'
          '│ They will be printed in order of slowest to fastest for 5 sec each.        │\n'
          '└────────────────────────────────────────────────────────────────────────────┘\n')

    speed_list = ['a \'slow\'', 'an \'average\'', 'a \'fast\'', 'an \'ultra\'']
    defaults_dict = default_configurations()
    options = speed_choices()
    trees = []
    for option in options:
        defaults_dict['speed'] = option
        trees.append(Tree(defaults_dict))

    input(f'> [Enter] to start printing at speeds ranging from \'slow\' to \'ultra\'.\n'
          f'> ')
    print()
    while True:
        for curr in range(4):
            curr_tree = trees[curr]

            start = calendar.timegm(time.gmtime())
            while calendar.timegm(time.gmtime()) - start < 5:
                print(curr_tree)
                print('This is ' + speed_list[curr] + ' speed')
                time.sleep(curr_tree.sleep_time)

        if user_finished('speed string', '-s <speed_string>'):
            break


def density_demo():
    """Called when the user specifies they wish to run the DENSITY --config demo"""
    print('┌────────────────────────────────────────────────────────────────────────────┐\n'
          '│                      --density --config Demonstration                      │\n'
          '│                                                                            │\n'
          '│ There are 4 DENSITYs with varying chances of printing a snowflake.         │\n'
          '│                                                                            │\n'
          '│ The goal is to find which density string is the most appealing to you.     │\n'
          '├ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┤\n'
          '│ They will be printed in order of lightest to heaviest snowfall for         │\n'
          '│     3 seconds per density.                                                 │\n'
          '│ Demo will continue until you find your preferred density string.           │\n'
          '└────────────────────────────────────────────────────────────────────────────┘\n')

    density_list = [' \'thin\'', 'n \'average\'', ' \'thick\'', 'n \'ultra\'']
    defaults_dict = default_configurations()
    defaults_dict['speed'] = 'average'
    options = density_choices()

    trees = []
    for option in options:
        defaults_dict['density'] = option
        trees.append(Tree(defaults_dict))

    input('> [Enter] to start printing snow with densities from \'thin\' to \'ultra\'.\n'
          '> ')
    print()
    while True:
        for curr in range(len(density_list)):
            curr_tree = trees[curr]

            start_time = calendar.timegm(time.gmtime())
            while calendar.timegm(time.gmtime()) - start_time < 3:
                print(curr_tree)
                print('This is a' + density_list[curr] + ' density')
                time.sleep(curr_tree.sleep_time)
        if user_finished('density string', '-d <density_string>'):
            break


def tiers_demo():
    """Called when the user specifies they wish to run the TIERS --config demo"""
    print('┌────────────────────────────────────────────────────────────────────────────┐\n'
          '│                       --tiers --config Demonstration                       │\n'
          '│                                                                            │\n'
          '│ The TIERS (or number of triangles of a tree) range from 1 to 13 inclusive. │\n'
          '│                                                                            │\n'
          '│ The goal is to find which tier number is the most appealing to you.        │\n'
          '├ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┤\n'
          '│ They will be printed in order of smallest to largest (3 times per tree).   │\n'
          '│ Demo will continue until you find the number of tiers.                     │\n'
          '└────────────────────────────────────────────────────────────────────────────┘\n')
    defaults_dict = default_configurations()
    defaults_dict['speed'] = 'average'
    options = range(1, 14)

    trees = []
    for option in options:
        defaults_dict['tiers'] = option
        trees.append(Tree(defaults_dict))

    input('> [Enter] to start printing the tiers ranging from 1 to 13.\n'
          '> ')
    while True:
        for curr_tree in trees:
            for _ in range(3):
                print(curr_tree)
                print(f'This tree has {curr_tree.tree_tiers} tier{("", "s")[curr_tree.tree_tiers != 1]}')
                time.sleep(curr_tree.sleep_time)
        if user_finished('tiers', '-t ##'):
            break


def user_finished(type_of, command_additional):
    answer = input(f'Did you find the {type_of} you wanted?\n'
                   f'> [y] / [n]\n'
                   f'> ').lower().strip()
    print()
    if answer:
        if answer[0] == 'y':
            input(f'\n  Now run it with:\n'
                  f'$ {py_cmd(command_additional)}\n\n'
                  f'> [Enter] to continue.\n'
                  f'> ')
            print()
            return True
    return False


def retrieve_int(message):
    """A simple function to retrieve a valid integer."""
    while True:
        input_str = input(message + '\n> ').strip()
        print()
        try:
            return int(input_str)
        except ValueError:
            Notification(f'\'{input_str}\' is not a valid number')
            pass
