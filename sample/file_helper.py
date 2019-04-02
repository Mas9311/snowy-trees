import os

from sample.format import Notification, py_cmd


def get_folder():
    """Returns the true path of the user's current directory (pwd bash command)
    And adds the name of the folder that saves all the saved configuration files."""
    return os.path.join(os.getcwd(), 'config_files')


def make_sure_dir_exists():
    """Creates the config_files folder if it does not exist."""
    configs = get_folder()
    if not dir_exists():
        os.mkdir(configs)
        Notification(['Created config_files folder',
                      'Your configuration files',
                      'will be saved here.',
                      '',
                      'Welcome to the club [:'])


def list_config_files():
    """Returns the alphabetically-sorted list of all configuration files in the folder.
    Returns an empty list if the folder or files within do not exist"""
    if not dir_exists():
        return []
    unsorted = os.listdir(get_folder())
    if not unsorted:
        return []
    sorted_list = []
    for file in sorted(unsorted):
        sorted_list.append(file)
    return sorted_list


def dir_exists():
    """Returns True if the configuration folder exists."""
    return os.path.exists(get_folder())


def file_exists(filepath):
    """Returns a True if the file exists, False if it does not.
    Must give it the full path to the file."""
    return os.path.exists(filepath) if dir_exists() else False


def strip_filename(name):
    """Returns the name of the file as:
     - all lowercase letters
     - no file extension (.txt)"""
    name, *_ = name.split('.')
    return name.lower()


def filename_with_extension(name):
    """Returns the name of the file as:
     - all lowercase letters
     - .txt file extension"""
    return strip_filename(name) + '.txt'


def export_file_as(name, arg_dict):
    """Prep-step before actually writing to the file.
    There are two possibilities using the filename given:
      1. No file with that name: proceeds to write the configurations to the file.
      2. File already exists: halt the GUI and ask the user to overwrite."""
    make_sure_dir_exists()

    name = strip_filename(name)
    filename = filename_with_extension(name)
    filepath = os.path.join(get_folder(), filename)
    if file_exists(filepath):
        Notification(['File already exists',
                      'Overwrite the file?',
                      '> Enter [Y] to overwrite'])
        answer = input('\n> ').strip().lower()
        print()
        if answer == 'y':
            print('File overwritten\n')
            write_file(filepath, arg_dict, name)
        else:
            print('File was not overwritten\n')
    else:
        # File does not exist, so write configurations to file
        write_file(filepath, arg_dict, name)


def write_file(filepath, arg_dict, name):
    """This is the second step to exporting a file.
    File either does not exist or user has confirmed they want to overwrite
    Writes Tree.arg_dict dictionary to the file as key {tab} value"""
    with open(filepath, 'w') as export_f:
        for key in arg_dict.keys():
            export_f.write(f'{key}\t{arg_dict[key]}\n')
        export_f.close()

    if arg_dict['verbose']:
        print(f'Saved current configurations to \n{filepath}\n')
    print(f'You can now run:\n'
          f'$ {py_cmd()} -f {name}\n'
          f'to load the current configurations.')


def import_from_file(name):
    """Read the configurations from the file given and place them into
    a dictionary format. Equivalent to parameter's ArgumentParser arg_dict.
    Values are turned from strings into their respective data types."""
    arg_dict = {}
    if dir_exists():
        name = strip_filename(name)
        filename = filename_with_extension(name)
        filepath = os.path.join(get_folder(), filename)
        # print(filepath)
        if file_exists(filepath):
            with open(filepath, 'r') as import_f:
                lines = import_f.read().splitlines()
                for line in lines:
                    key, value = line.split('\t')
                    arg_dict[key] = str_to_type(key, value)
                import_f.close()
            print(f'\'{filename}\' file successfully loaded!')
        else:
            Notification([f'File {name} does not exist',
                          f'> [Enter] to continue execution.'])
    else:
        Notification('Folder does not yet exist')

    if not arg_dict:
        input('> ')

    return arg_dict


def str_to_type(key, value):
    """Returns the correct type of value based on the key given.
    'width',  'True'  => True
    'length', '5'     => 5
    'density', 'thin' => 'thin' """
    ints = ['width', 'tiers', 'length', 'w_dim', 'h_dim', 'x_dim', 'y_dim']
    booleans = ['interface', 'ornaments', 'maximized', 'verbose']

    if key in ints:
        return int(value)
    elif key in booleans:
        return True if value == 'True' else False
    else:
        return value
