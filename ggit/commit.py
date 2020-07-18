from ggit.core.git import Git


def commit(file, message, all):

    # prepare commit args
    args = file
    args.extend(["--message", message])
    if all:
        args.extend(["--all"])

    git = Git()
    git.commit(args)
