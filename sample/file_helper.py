import os

from sample import parameters


def get_folder():
    return os.path.join(os.getcwd(), 'config_files')


def make_sure_dir_exists():
    """Creates the config_files folder if it does not exist."""
    configs = get_folder()
    if not os.path.exists(configs):
        os.mkdir(configs)
        print('\tFirst time creating a config file. Welcome to the club [:')


def file_exists(name):
    configs = get_folder()
    if os.path.exists(configs) and os.path.exists(name):
        return True
    return False


def export_file_as(name, arg_dict):
    make_sure_dir_exists()

    filename = format_filename(name)
    filepath = os.path.join(get_folder(), filename)
    with open(filepath, 'w') as export_f:
        for key in arg_dict.keys():
            export_f.write(f'{key}\t{arg_dict[key]}\n')
        export_f.close()
    # print(f'Saved current configurations to \n{filepath}')
    print(f'You can now run:\n'
          f'$ {parameters.py_cmd} -f {name}\n'
          f'to load the current configurations.')


def import_from_file(name):
    arg_dict = {}

    filename = format_filename(name)
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
        input(f'\'{filename}\' file loading failed ]:\n'
              f'Press [Enter] to restore defaults.\n>')

    return arg_dict


def format_filename(name):
    name, *_ = name.split('.')
    filename = f'{name.lower()}.txt'
    return filename


def str_to_type(key, value):
    """Returns the correct type of value based on the key given.
    'width',  'True'  => True
    'length', '5'     => 5
    'density', 'thin' => 'thin' """
    ints = ['width', 'tiers', 'length']
    booleans = ['interface', 'ornaments', 'verbose']

    if key in ints:
        return int(value)
    elif key in booleans:
        if value == 'True':
            return True
        else:
            return False
    else:
        return value
