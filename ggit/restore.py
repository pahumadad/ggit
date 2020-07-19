import os
import sys

from ggit.core.common import get_diff
from ggit.core.common import get_file
from ggit.core.common import get_files
from ggit.core.common import FILE_TYPE_NO_ENC
from ggit.core.gpg import GPG


def restore(paths):
    # get files
    files = []
    if not paths:
        sys.exit("fatal: you must specify path(s) to restore")
    else:
        for p in paths:
            if os.path.isfile(p):
                f = get_file(p)
                if not f:
                    continue
                files.append(f)
            elif os.path.isdir(p):
                files.extend(
                    get_files(p, file_type=FILE_TYPE_NO_ENC)
                )
            else:
                sys.exit(f"path not found: {p}")

    # restore files
    gpg = GPG()
    for f in files:
        if not get_diff(f):
            continue
        # get encrypted file
        enc = gpg.get_enc_file(f)
        # remove the no encrypted file
        os.remove(f)
        # decrypt the encrypted file
        gpg.decrypt(enc)
