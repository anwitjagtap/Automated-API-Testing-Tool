import sys


def get_system_arguments():
    sys_kwargs = {}
    args = []
    sys_argv = sys.argv[1:]
    i = 0
    while i < len(sys_argv):
        argv = sys_argv[i]
        if "--" in argv and i + 1 < len(sys_argv):
            sys_kwargs[argv.split("--")[1]] = sys_argv[i + 1]
            i += 2
        else:
            i += 1
            args.append(argv)

    print("sys_kwargs: ", sys_kwargs, "\nsys_args: ", args)

    return sys_kwargs, args