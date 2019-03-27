import os


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
    print('Saving current configurations to file', name)
    filepath = os.path.join(get_folder(), f'{name}.txt')
    with open(filepath, 'w') as export_f:
        for key in arg_dict.keys():
            export_f.write(f'{key}\t{arg_dict[key]}\n')
        export_f.close()


def import_from_file(name):
    arg_dict = {}

    filepath = os.path.join(get_folder(), f'{name}.txt')  # TODO: strip the extension, .txt,  and lower()
    ints = ['width', 'tiers', 'length']
    if file_exists(filepath):
        with open(filepath, 'r') as import_f:
            lines = import_f.read().splitlines()
            for line in lines:
                print(line)
                key, value = line.split('\t')
                if key in ints:
                    value = int(value)
                arg_dict[key] = value
            import_f.close()

    return arg_dict
