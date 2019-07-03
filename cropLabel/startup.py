import os


def process_args(args):
    new_args = []
    for arg in args:
        if arg.startswith('--params='):
            extract_parameters(arg)
        else:
            new_args.append(arg)
    return new_args


def extract_parameters(args):
    cmds = args.split('=')
    if len(cmds) >= 2:
        pairs = cmds[1].split(',')
        for pair in pairs:
            single = pair.split(':')
            if len(single) >= 2:
                os.environ[single[0]] = single[1]
                print("setting variables: {} : {}".format(single[0], single[1]))
