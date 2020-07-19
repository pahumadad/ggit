from ggit.core.common import get_diff
from ggit.core.common import get_files
from ggit.core.common import FILE_TYPE_NO_ENC
from ggit.core.git import Git
from ggit.core.gpg import GPG


def commit(files, message, all):

    # prepare commit args
    args = files
    args.extend(["--message", message])
    if all:
        args.extend(["--all"])

        # look for all modifed files
        files = get_files(file_type=FILE_TYPE_NO_ENC)
        gpg = GPG()
        for f in files:
            if not gpg.exist_enc(f):
                continue
            if not get_diff(f):
                continue
            gpg.encrypt(f)

    git = Git()
    git.commit(args)
