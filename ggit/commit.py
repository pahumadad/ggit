from ggit.core.git import Git


def commit(files, message, all):

    # prepare commit args
    args = files
    args.extend(["--message", message])
    if all:
        args.extend(["--all"])

    git = Git()
    git.commit(args)
