import os
import sys
from ggit.core.common import get_diff
from ggit.core.common import get_file
from ggit.core.common import get_files
from ggit.core.common import FILE_TYPE_NO_ENC
from ggit.core.git import Git
from ggit.core.gpg import GPG
from ggit.status import status


def commit(paths, message, all):

    # check args
    if paths and all:
        sys.exit(f"fatal: paths '{paths[0]} ...' with -a does not make sense")

    # encrypt modified files
    git = Git()
    gpg = GPG()
    files = []
    if not paths and not all and not git.status_to_commit():
        return status()
    elif not message:
        sys.exit("ggit commit: error: the following arguments are required: -m/--message")  # noqa
    elif all:
        files_list = get_files(file_type=FILE_TYPE_NO_ENC)
        for f in files_list:
            if not gpg.exist_enc(f):
                continue
            if not get_diff(f):
                continue
            gpg.encrypt(f)
    else:
        for p in paths:
            if os.path.isfile(p):
                f = get_file(p)
                if not f:
                    continue
                if not gpg.exist_enc(f):
                    continue
                if not get_diff(f):
                    continue
                f = gpg.encrypt(f)
                files.append(f)
            elif os.path.isdir(p):
                for f in get_files(p, file_type=FILE_TYPE_NO_ENC):
                    if not gpg.exist_enc(f):
                        continue
                    if not get_diff(f):
                        continue
                    f = gpg.encrypt(f)
                    files.append(f)
            else:
                sys.exit(f"path not found: {p}")

    # prepare commit args
    args = files
    args.extend(["--message", message])
    if all:
        args.extend(["--all"])

    git.commit(args)
