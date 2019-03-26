import argparse
import calendar
import platform
import time

import numpy as np
import sys

from sample import Tree

py_cmd = ('python3', 'python.exe')[platform.system() == 'Windows'] + ' run.py'


def default_settings():
    return {
        'width': 125,
        'speed': 'slow',
        'density': 'average',
        'tiers': 4,
        'ornaments': True,
        'length': 5,
        'textbox': 'medium',
        'toolbar': 'large',
        'windows': 'large',
        'interface': True
    }


def speed_dict():
    return {'slow': 0.9810000, 'average': 0.7265000, 'fast': 0.465000, 'ultra': 0.1}  # ultra=0.05 minimum


def speed_choices():
    return [s for s in speed_dict().keys()]


def density_dict():
    return {'thin': 36, 'average': 128, 'thick': 512, 'ultra': 733}


def density_choices():
    return [d for d in density_dict().keys()]


def font_dict():
    return {
        'textbox': {
            'small': ('fixed', -11),
            'medium': 'fixed',
            'large': ('fixed', -15)
        },
        'toolbar': {
            'small': ('Courier New', 10, 'bold'),
            'large': ('Courier', 25)
        },
        'windows': {
            'small': ('Times Roman', 9, 'bold'),
            'large': ('Times New Roman', 18, 'bold')
        }
    }


def textbox_font_choices():
    return [t for t in font_dict()['textbox'].keys()]


def toolbar_font_choices():
    return [b for b in font_dict()['toolbar'].keys()]


def windows_font_choices():
    return [w for w in font_dict()['windows'].keys()]


def retrieve():
    """Retrieves the parameters from the console if provided.
    Returns the parameters in dict format.
    If an unknown argument is passed, print the --help screen.
    If no arguments are passed, then print the intro Welcome screen."""
    if '--config' in sys.argv:
        config_argument()
        sys.exit()

    defaults = default_settings()
                                                        # TODO
    cmd_description = ('             ╔══════════════════════════════════════════════════╗            ┃\n'
                       '             ║   Loops a snowy tree much like a gif wallpaper   ║            ┃\n'
                       '             ╚══════════════════════════════════════════════════╝            ┃\n'
                       '                                                                             ┃\n'
                       ' If you are unsure about what value to set an optional argument to, watch the┃\n'
                       '    demonstration by typing --config after a configurable* argument.         ┃\n'
                       '                                                                             ┃\n'
                       ' Configurable* arguments include {width, speed, density, tiers}              ┃\n'
                       '    To see the demo, type --config after one of the configurable arguments   ┃\n'
                       '                                                                             ┃\n'
                       ' Note: Configurable options can be chained together as shown with:           ┃\n'
                       '$ ' + py_cmd + ' -w --config -s --config -d --config -t --config             ┃\n'
                       '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛')

    parser = argparse.ArgumentParser(usage=py_cmd + ' [options]                                              ┃',
                                     description=cmd_description,
                                     add_help=False,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-w', '--width',
                        type=int,
                        metavar='',
                        default=defaults['width'],
                        help=(f'WIDTH of the terminal window: (default=%(default)s)                '
                              '   271 => characters printed on a single line on a 32-inch '
                              '          monitor in landscape orientation                 '
                              '   151 => characters printed on a single line on a 32-inch '
                              '          monitor in portrait orientation'))

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
                        help=('TEXTBOX font size: (default=%(default)s)                        '
                              'The textbox is location of the Tree to be displayed.       '
                              'Valid choices are [%(choices)s]'))

    parser.add_argument('-bf', '--toolbar',
                        type=str,
                        default=defaults['toolbar'],
                        metavar='',
                        dest='toolbar',
                        choices=toolbar_font_choices(),
                        help=('TOOLBAR buttons font size: (default=%(default)s)                 '
                              'These are the toolbar buttons located at the top-left.     '
                              'Valid choices are [%(choices)s]'))

    parser.add_argument('-wf', '--window',
                        type=str,
                        default=defaults['windows'],
                        metavar='',
                        dest='windows',
                        choices=windows_font_choices(),
                        help=('WINDOW manager buttons font size: (default=%(default)s)          '
                              'These are the − + × buttons located at the top-right.      '
                              'Valid choices are [%(choices)s]'))

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

    interface = parser.add_mutually_exclusive_group(required=False)
    interface.add_argument('-g', '--gui',
                           action='store_true',
                           default=defaults['interface'],
                           dest='interface',
                           help='GUI printing of the tree. (default=%(default)s)')

    interface.add_argument('-c', '--cli',
                           action='store_false',
                           default=not defaults['interface'],
                           dest='interface',
                           help='CLI printing of the tree. (default=%(default)s)')

    vrs_description = ('                                                    \n'
                       '              *   snowy-trees v1.0   *              \n'
                       'Check out if there are any new releases for this at:\n'
                       '\thttps://github.com/Mas9311/snowy-trees/releases')
    parser.add_argument('-v', '--version',
                        action='version',
                        version=vrs_description)

    parser.add_argument('-h', '--help',
                        metavar='',
                        help='show this help message and exit')

    known_args, unknown_args = parser.parse_known_args()

    # converts the arguments from a Namespace type => dictionary
    arg_dict = {'width': known_args.width,
                'speed': known_args.speed,
                'density': known_args.density,
                'tiers': known_args.tiers,
                'ornaments': known_args.ornaments,
                'interface': known_args.interface,
                'length': known_args.length,
                'textbox': known_args.textbox,
                'toolbar': known_args.toolbar,
                'windows': known_args.windows}

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
        print_welcome(parser)

    return arg_dict


def length_list_type(length_input):
    length_input = int(length_input)
    length_min = default_settings()['length']
    if length_input < length_min:
        print(f'List argument must be >= {length_min}. Resorting to the default of {length_min}.')
    return length_input


def print_welcome(parser):
    """This function is called when the user does not include any additional arguments.
    This almost seems counter-productive, but at the very least, the default width
    should not be used. Instead, the user is informed how to run the --config demo.
    After the Welcome screen is printed, it will print the --help option."""
    h_option = ' --help'
    d_option = ' -w --config'
    help_flags = h_option + ' ' * (27 - len(py_cmd + h_option))
    demo_flags = d_option + ' ' * (27 - len(py_cmd + d_option))
                                            # TODO
    print('╭┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┲━━━━━━┱┈┈┈┈╮\n'
          '┊                     ╔════════════════════════════╗             ┃ v1.0 ┃    ┊\n'
          '┊                     ║   Welcome to Snowy Trees   ║             ┗━━━━━━┛    ┊\n'
          '┊                     ╚════════════════════════════╝                         ┊\n'
          '┊                                                                            ┊\n'
          '┊ You do not have any additional arguments, so this is intended to inform    ┊\n'
          '┊    you how to access the *Configurable* options.                           ┊\n'
          '┊                                                                            ┊\n'
          '┊ If you ever need help, just type -h or --help, such as                     ┊\n'
          '┊$ ' + py_cmd + help_flags + '                                               ┊\n'
          '┊                                                                            ┊\n'
          '┊ *Configurable* arguments include {width, speed, density, tiers}            ┊\n'
          '┊    To see the demo, type --config after one of the configurable arguments  ┊\n'
          '┊$ ' + py_cmd + demo_flags + '                                               ┊\n'
          '┊                                                                            ┊\n'
          '┊    The --config argument will give you a short demonstration in order to   ┊\n'
          '┊    better prepare you for the intended argument\'s configurable value.      ┊\n'
          '╰┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈╯')
    input('\nPress [Enter] to print --help:\n>')

    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓')
    parser.print_help()
    run_with = ''
    for k in ['width', 'speed', 'density', 'tiers', 'ornaments', 'length']:
        run_with += f'\t{k}: {default_settings()[k]}\n'
    input(f'\nPress [Enter] to run with cli with the default Tree of:\n{run_with}\n>')
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
            input(f'\nGlad to hear it. Now run it with\n\t$ {py_cmd} -w <###>\nPress [Enter] to continue.\n> ')
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
          '│ They will be printed in order of slowest to fastest for a 5 sec each       │\n'
          '│     Demo will repeat if you indicate you do not understand the speeds.     │\n'
          '└────────────────────────────────────────────────────────────────────────────┘')

    speed_list = ['a \'slow\'', 'an \'average\'', 'a \'fast\'', 'an \'ultra\'']
    defaults = default_settings()
    options = speed_choices()
    trees = []
    for option in options:
        defaults['speed'] = option
        trees.append(Tree.Tree(defaults))

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
            input(f'\nGlad to hear it. Now run it with:\n\t$ {py_cmd} -s <desired_speed>'
                  '\nPress [Enter] to continue.\n> ')
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

    density_list = [' \'thin\'', 'n \'average\'', ' \'thick\'', 'n \'ultra\'']
    defaults_dict = default_settings()
    defaults_dict['speed'] = 'average'
    options = density_choices()

    trees = []
    for option in options:
        defaults_dict['density'] = option
        trees.append(Tree.Tree(defaults_dict))

    input('Press [Enter] to start printing snowfall with density from \'thin\' to \'ultra\'.\n>')
    while True:
        for curr in range(len(density_list)):
            curr_tree = trees[curr]

            start_time = calendar.timegm(time.gmtime())
            while calendar.timegm(time.gmtime()) - start_time < 5:
                print(curr_tree)
                print('This is a' + density_list[curr] + ' density')
                time.sleep(curr_tree.sleep_time)

        answer = input('Do you understand the densities? [Y]/[N]\n>').lower().strip()
        if answer and answer[0] == 'y':
            input(f'\nGlad to hear it. Now run it with:\n\t$ {py_cmd} -d <desired_density>'
                  '\nPress [Enter] to continue.\n> ')
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
    defaults_dict = default_settings()
    defaults_dict['speed'] = 'average'
    options = range(1, 14)

    trees = []
    for option in options:
        defaults_dict['tiers'] = option
        trees.append(Tree.Tree(defaults_dict))

    input('Press [Enter] to start printing the tiers from 1 to 13.\n>')
    while True:
        for curr_tree in trees:
            start = calendar.timegm(time.gmtime())
            while calendar.timegm(time.gmtime()) - start < 3:
                print(curr_tree)
                print(f'This tree has {curr_tree.tree_tiers} tier{("", "s")[curr_tree.tree_tiers != 1]}')
                time.sleep(curr_tree.sleep_time)
        answer = input('Do you understand the tiers? [Y]/[N]\n>').lower().strip()
        if answer and answer[0] == 'y':
            input(f'\nGlad to hear it. Now run it with\n\t$ {py_cmd} -t <##>\nPress [Enter] to quit.\n> ')
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
