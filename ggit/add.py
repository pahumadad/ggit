import os
import sys

from ggit.core.common import get_file
from ggit.core.common import get_files
from ggit.core.common import FILE_TYPE_NO_ENC
from ggit.core.git import Git
from ggit.core.gpg import GPG


def add(path):
    files = []
    if not path:
        sys.exit((
            "Nothing specified, nothing added.\n"
            "Maybe you wanted to say 'git add .'?"
        ))
    elif path[0] == ".":
        files = get_files(new=True, file_type=FILE_TYPE_NO_ENC)
    else:
        for p in path:
            if os.path.isfile(p):
                f = get_file(p)
                if not f:
                    continue
                files.append(get_file(p))
            elif os.path.isdir(p):
                files.extend(
                    get_files(p, new=True, file_type=FILE_TYPE_NO_ENC)
                )
            else:
                sys.exit(f"path not found: {p}")

    # encrypt and add
    gpg = GPG()
    git = Git()
    for file in files:
        print(file)
        enc_file = gpg.encrypt(file)
        git.add(enc_file)
