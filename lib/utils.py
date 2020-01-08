bcolors = {
    'header' : '\033[95m',
    'blue' : '\033[94m',
    'green' : '\033[92m',
    'warning' : '\033[93m',
    'fail' : '\033[91m',
    'end' : '\033[0m',
    'bold' : '\033[1m',
    'underline' : '\033[4m',
}

def cprint(*args, color='green', **kwargs):
    """ Colorful printing """

    if color and bcolors.get(color):
        print(bcolors[color], end='')
        print(*args, **kwargs)
        print(bcolors[color], end='')
