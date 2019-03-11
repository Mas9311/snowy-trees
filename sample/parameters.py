import argparse
import calendar
import platform
import time

import numpy as np
import sys

from sample import Tree

py_cmd = ('python3', 'python.exe')[platform.system() == 'Windows'] + ' run.py'


def retrieve():
    """Retrieves the parameters from the console if provided.
    Returns the parameters in dict format.
    If an unknown argument is passed, print the --help screen.
    If no arguments are passed, then print the intro Welcome screen."""
    if '--config' in sys.argv:
        config_argument()
        return
    cmd_description = ('             ╔══════════════════════════════════════════════════╗            ┃\n'
                       '             ║   Loops a snowy tree much like a gif wallpaper   ║            ┃\n'
                       '             ╚══════════════════════════════════════════════════╝            ┃\n'
                       '                                                                             ┃\n'
                       'If you are unsure about what value to set an optional argument to, watch the ┃\n'
                       '    demonstration by typing --config after any one of the optional arguments.┃\n'
                       '                                                                             ┃\n'
                       '─ I recommend that everyone starts with configuring the width which can be   ┃\n'
                       '    executed with the command:                                               ┃\n'
                       '$ ' + py_cmd + ' -w --config                                                 ┃\n'
                       '                                                                             ┃\n'
                       '─ Or you can just chain them together as shown in:                           ┃\n'
                       '$ ' + py_cmd + ' -w --config -s --config -d --config -t --config             ┃\n'
                       '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛')

    parser = argparse.ArgumentParser(usage=py_cmd + ' [options]                                              ┃',
                                     description=cmd_description,
                                     add_help=False,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-w', '--width',
                        type=int,
                        metavar='',
                        default=125,
                        help=('WIDTH of the terminal window: (default = 125)               '
                              '   271 => characters printed on a single line on a 32-inch  '
                              '          monitor in landscape orientation                  '
                              '   151 => characters printed on a single line on a 32-inch  '
                              '          monitor in portrait orientation'))

    parser.add_argument('-s', '--speed',
                        type=str,
                        default='slow',
                        metavar='',
                        choices=['ultra', 'fast', 'average', 'slow'],
                        help=('valid choices=[ultra, fast, average, slow]                  '
                              'SPEED of the refresh: (default = slow)                      '
                              '   slow => the snow falling will print every second'))

    parser.add_argument('-d', '--density',
                        type=str,
                        default='average',
                        metavar='',
                        choices=['ultra', 'heavy', 'average', 'thin'],
                        help=('valid choices=[ultra, fast, average, slow] which equates    '
                              'to percent of [ 75.0, 51.2,    12.8,  3.6] chance of snow.  '
                              'DENSITY of the snow: (default = average)                    '
                              '   average => 12.8 percent chance of snow'))

    parser.add_argument('-t', '--tiers',
                        type=int,
                        default=4,
                        metavar='',
                        choices=range(1, 14),
                        help=('valid range of [1, 13] inclusive                            '
                              'TIERS of tree: (default = 4)                                '
                              '   4 => Tree has 4 triangular tiers'))

    ornaments = parser.add_mutually_exclusive_group(required=False)
    ornaments.add_argument('-y', '--yes',
                           action='store_true',
                           dest='ornaments',
                           help='YES, display the ornaments on the tree')

    ornaments.add_argument('-n', '--no',
                           action='store_false',
                           dest='ornaments',
                           help='NO ornaments. Ornaments will not be displayed on the tree')

    vrs_description = ('                                                    \n'
                       '              *   snowy-trees v0.1   *              \n'
                       'Check out if there are any new releases for this at:\n'
                       '\thttps://github.com/Mas9311/snowy-trees/releases')
    parser.add_argument('-v', '--version',
                        action='version',
                        version=vrs_description)

    parser.add_argument('-h', '--help',
                        metavar='',
                        help='show this help message and exit')

    known_args, unknown_args = parser.parse_known_args()

    arg_dict = {'width': known_args.width,
                'speed': known_args.speed,
                'density': known_args.density,
                'tiers': known_args.tiers,
                'ornaments': known_args.ornaments,
                'list_len': 25}

    if unknown_args:
        # user added unknown args, so print the --help screen
        parser.print_help()
        print()
        if len(unknown_args) is 1:
            unrecognized = ' \'' + unknown_args[0] + '\' is'
        else:
            unrecognized = 's ' + str(unknown_args) + ' are'
        input('\nThe argument' + unrecognized + ' not valid.\n\nPress [Enter] to quit\n>')
        parser.parse_args()  # prints error message and stops execution
        raise Exception('Unknown arguments')  # redundantly raised an Exception to ensure failure

    if len(sys.argv) == 1:
        # no arguments were provided, print the welcome screen
        print_welcome(parser, arg_dict)

    return arg_dict


def print_welcome(parser, arg_dict):
    """This function is called when the user does not include any additional arguments.
    This almost seems counter-productive, but at the very least, the default width
    should not be used. Instead, the user is informed how to run the --config demo.
    After the Welcome screen is printed, it will print the --help option."""
    h_option = ' --help'
    d_option = ' -w --config'
    help_flags = h_option + ' ' * (27 - len(py_cmd + h_option))
    demo_flags = d_option + ' ' * (27 - len(py_cmd + d_option))

    print('╭┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┲━━━━━━┱┈┈┈╮\n'
          '┊                     ╔═════════════════════════════╗             ┃ v0.1 ┃   ┊\n'
          '┊                     ║   Welcome to snowy-trees!   ║             ┗━━━━━━┛   ┊\n'
          '┊                     ╚═════════════════════════════╝                        ┊\n'
          '┊                                                                            ┊\n'
          '┊ You do not have any additional arguments, so this is intended to inform    ┊\n'
          '┊    you how to access the configurable options.                             ┊\n'
          '┊                                                                            ┊\n'
          '┊ If you ever need help, just type -h or --help, such as                     ┊\n'
          '┊    $ ' + py_cmd + help_flags + '                                           ┊\n'
          '┊                                                                            ┊\n'
          '┊ If you are uncertain about what value to put after an argument, i.e. width ┊\n'
          '┊    you can type --config after any argument such as:                       ┊\n'
          '┊    $ ' + py_cmd + demo_flags + '                                           ┊\n'
          '┊                                                                            ┊\n'
          '┊ The --config argument will give you a short demonstration in order to      ┊\n'
          '┊    better prepare you for the intended argument\'s configurable value.      ┊\n'
          '╰┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈╯')
    input('\nPress [Enter] to print --help:\n>')

    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓')
    parser.print_help()
    input(f'\nPress [Enter] to run with the options set to:\n{arg_dict}\n>')
    print()


def config_argument():
    """This function is called when the user specifies to run the --config demo on
    one or more optional arguments.
    It will remove the areuments, call the corresponding function associated to the
    argument, and loop until no more --config arguments are left.
        Note: the user cannot group arguments such as '-wsdt --config', but should instead
        run them separately as in '-w --config -s --config -d --config -t --config'"""
    try:
        while sys.argv.index('--config') is not None:
            config_loc = sys.argv.index('--config') - 1
            valid_config = ['-w', '--width', '-s', '--speed', '-d', '--density', '-t', '--tiers']
            arg_to_config = ''
            for curr_arg in np.linspace(config_loc, 1, config_loc, dtype=int):
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
    print('┌─────────────────────┬──────────────────────────────┬───────────────────────┐\n'
          '│                     │ Width --config Demonstration │                       │\n'
          '│                     └──────────────────────────────┘                       │\n'
          '│ In order to find the best WIDTH, or number of character to print, you      │\n'
          '│     should now adjust the Terminal window to your desired width.           │\n'
          '│                                                                            │\n'
          '│ The goal is to find the line that ends exactly at the end of your window.  │\n'
          '├ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┤\n'
          '│ First, it will print line lengths of 400 to 50 in increments of 50 get     │\n'
          '│     you in the general area.                                               │\n'
          '│ Then, you will guess the width, and it will print ± 10 of the guess.       │\n'
          '│     Guessing will continue until you are satisfied.                        │\n'
          '└────────────────────────────────────────────────────────────────────────────┘')
    input('\nPress [Enter] to print the varying widths\n>')

    fir_char = '+'
    sec_char = '-'
    char = fir_char
    for line_len in np.linspace(400, 50, 8, dtype=int):
        char = (fir_char, sec_char)[char == fir_char]
        line = char * (line_len - len(str(line_len)) - 1)
        print(str(line_len) + ' ' + line)

    while True:
        guess = retrieve_int('What\'s your best guess of the width of this current window:')
        char = fir_char

        for line_len in range(guess-10, guess+11):
            char = (fir_char, sec_char)[char == fir_char]
            line = char * (line_len - len(str(line_len)) - 1)
            print(str(line_len) + ' ' + line)
        answer = input('Did you find the number? Enter [Y]/[N]\n>').lower().strip()
        if answer and answer[0] == 'y':
            input(f'\nPerfect. Now run it with\n\t$ {py_cmd} -w ###\nPress [Enter] to continue.\n>')
            break


def speed_demo():
    """Called when the user specifies they wish to run the SPEED --config demo"""
    print('┌────────────────────────────────────────────────────────────────────────────┐\n'
          '│                       Speed --config Demonstration                         │\n'
          '│                                                                            │\n'
          '│ There are 4 SPEEDs with varying refresh rates ranging from 1 to .1 seconds │\n'
          '│                                                                            │\n'
          '│ The goal is to find what refresh rate you are most comfortable with.       │\n'
          '├ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┤\n'
          '│ They will be printed in order of slowest to fastest for a total of 5       │\n'
          '│     seconds each.                                                          │\n'
          '│ It can keep looping if you indicate you do not understand the speeds.      │\n'
          '└────────────────────────────────────────────────────────────────────────────┘')

    speed_list = ['a \'slow\'', 'an \'average\'', 'a \'fast\'', 'an \'ultra\'']
    trees = [Tree.Tree({'speed': 'slow', 'width': 150, 'density': 'average', 'tiers': 4, 'ornaments': False}),
             Tree.Tree({'speed': 'average', 'width': 150, 'density': 'average', 'tiers': 4, 'ornaments': False}),
             Tree.Tree({'speed': 'fast', 'width': 150, 'density': 'average', 'tiers': 4, 'ornaments': False}),
             Tree.Tree({'speed': 'ultra', 'width': 150, 'density': 'average', 'tiers': 4, 'ornaments': False})]
    first_round = True
    while True:
        for curr in range(4):
            if first_round:
                input('Press [Enter] to start printing at ' + speed_list[curr] + ' speed.\n>')
            curr_tree = trees[curr]

            start = calendar.timegm(time.gmtime())
            while calendar.timegm(time.gmtime()) - start < 5:
                print(curr_tree)
                print('This is ' + speed_list[curr] + ' speed')
                time.sleep(curr_tree.sleep_time)

        first_round = False
        answer = input('Do you understand the speeds? [Y]/[N]\n>').lower().strip()
        if answer and answer[0] == 'y':
            input(f'\nGlad to hear it. Now run it with\n\t$ {py_cmd} -s desired_speed\nPress [Enter] to continue.\n> ')
            break


def density_demo():
    """Called when the user specifies they wish to run the DENSITY --config demo"""
    print('┌────────────────────────────────────────────────────────────────────────────┐\n'
          '│                       Density --config Demonstration                       │\n'
          '│                                                                            │\n'
          '│ There are 4 DENSITYs with varying chances (in %) to print a snowflake.     │\n'
          '│                                                                            │\n'
          '│ The goal is to find which density is the most appealing.                   │\n'
          '├ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┤\n'
          '│ They will be printed in order of lightest to heaviest snowfall for a total │\n'
          '│     of 5 seconds each.                                                     │\n'
          '│ After it has finished, you can redo the demo you indicate you do not       │\n'
          '│     understand the densities.                                              │\n'
          '└────────────────────────────────────────────────────────────────────────────┘')

    density_list = ['a \'thin\'', 'an \'average\'', 'a \'heavy\'', 'an \'ultra\'']
    trees = [Tree.Tree({'density': 'thin', 'width': 150, 'speed': 'average', 'tiers': 4, 'ornaments': False}),
             Tree.Tree({'density': 'average', 'width': 150, 'speed': 'average', 'tiers': 4, 'ornaments': False}),
             Tree.Tree({'density': 'heavy', 'width': 150, 'speed': 'average', 'tiers': 4, 'ornaments': False}),
             Tree.Tree({'density': 'ultra', 'width': 150, 'speed': 'average', 'tiers': 4, 'ornaments': False})]
    input('Press [Enter] to start printing snowfall with density from \'thin\' to \'ultra\'.\n>')
    while True:
        for curr in range(4):
            curr_tree = trees[curr]

            start = calendar.timegm(time.gmtime())
            while calendar.timegm(time.gmtime()) - start < 5:
                print(curr_tree)
                print('This is ' + density_list[curr] + ' speed')
                time.sleep(curr_tree.sleep_time)

        answer = input('Do you understand the densities? [Y]/[N]\n>').lower().strip()
        if answer and answer[0] == 'y':
            input(f'\nGlad to hear it. Now run it with\n\t$ {py_cmd} -s desired_density\nPress [Enter] to continue.\n> ')
            break


def tiers_demo():
    """Called when the user specifies they wish to run the TIERS --config demo"""
    print('┌────────────────────────────────────────────────────────────────────────────┐\n'
          '│                        Tiers --config Demonstration                        │\n'
          '│                                                                            │\n'
          '│ The TIERS (or number of triangles of a tree) range from 1 to 13 inclusive. │\n'
          '│                                                                            │\n'
          '│ The goal is to find which tier number looks the most appealing for the     │\n'
          '│     height of your Terminal window. Note: Ornaments are not set by default.│\n'
          '├ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┤\n'
          '│ They will be printed in order of smallest to largest for 3 seconds each.   │\n'
          '│ After it has finished, you can redo the demo if you indicate you do not    │\n'
          '│     understand the tiers.                                                  │\n'
          '└────────────────────────────────────────────────────────────────────────────┘')

    trees = [Tree.Tree({'tiers': 1, 'width': 150, 'speed': 'fast', 'density': 'average', 'ornaments': True}),
             Tree.Tree({'tiers': 2, 'width': 150, 'speed': 'fast', 'density': 'average', 'ornaments': True}),
             Tree.Tree({'tiers': 3, 'width': 150, 'speed': 'fast', 'density': 'average', 'ornaments': True}),
             Tree.Tree({'tiers': 4, 'width': 150, 'speed': 'fast', 'density': 'average', 'ornaments': True}),
             Tree.Tree({'tiers': 5, 'width': 150, 'speed': 'fast', 'density': 'average', 'ornaments': True}),
             Tree.Tree({'tiers': 6, 'width': 150, 'speed': 'fast', 'density': 'average', 'ornaments': True}),
             Tree.Tree({'tiers': 7, 'width': 150, 'speed': 'fast', 'density': 'average', 'ornaments': True}),
             Tree.Tree({'tiers': 8, 'width': 150, 'speed': 'fast', 'density': 'average', 'ornaments': True}),
             Tree.Tree({'tiers': 9, 'width': 150, 'speed': 'fast', 'density': 'average', 'ornaments': True}),
             Tree.Tree({'tiers': 10, 'width': 150, 'speed': 'fast', 'density': 'average', 'ornaments': True}),
             Tree.Tree({'tiers': 11, 'width': 150, 'speed': 'fast', 'density': 'average', 'ornaments': True}),
             Tree.Tree({'tiers': 12, 'width': 150, 'speed': 'fast', 'density': 'average', 'ornaments': True}),
             Tree.Tree({'tiers': 13, 'width': 150, 'speed': 'fast', 'density': 'average', 'ornaments': True})]
    input('Press [Enter] to start printing the tiers from 1 to 13.\n>')
    while True:
        for curr in range(0, 13):
            curr_tree = trees[curr]

            start = calendar.timegm(time.gmtime())
            while calendar.timegm(time.gmtime()) - start < 3:
                print(curr_tree)
                print(f'This tree has {curr + 1} tiers')
                time.sleep(curr_tree.sleep_time)
        answer = input('Do you understand the tiers? [Y]/[N]\n>').lower().strip()
        if answer and answer[0] == 'y':
            input(f'\nAwesome. Now run it with\n\t$ {py_cmd} -t #\nPress [Enter] to quit.\n> ')
            break


def retrieve_int(message):
    """A simple function to retrieve a valid integer."""
    while True:
        input_str = input(message + '\n>').strip()
        try:
            return int(input_str)
        except ValueError:
            print(f' ** {input_str} is not a valid number **')
            pass
