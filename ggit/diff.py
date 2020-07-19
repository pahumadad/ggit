import os
import sys
from ggit.core.common import get_diff
from ggit.core.common import get_file
from ggit.core.common import get_files
from ggit.core.common import BC_BOLD
from ggit.core.common import BC_CYAN
from ggit.core.common import BC_END
from ggit.core.common import BC_GREEN
from ggit.core.common import BC_RED
from ggit.core.common import FILE_TYPE_NO_ENC


def diff(paths):
    files = []
    if not paths:
        files = get_files(file_type=FILE_TYPE_NO_ENC)
    else:
        for p in paths:
            if os.path.isfile(p):
                f = get_file(p)
                if not f:
                    continue
                files.append(get_file(p))
            elif os.path.isdir(p):
                files.extend(
                    get_files(p, file_type=FILE_TYPE_NO_ENC)
                )
            else:
                sys.exit(f"path not found: {p}")

    # get diff for all files
    for f in files:
        resp = get_diff(f)
        if not resp:
            continue
        for line in resp:
            if line.startswith("+++") or line.startswith("---"):
                sys.stdout.write(BC_BOLD + line + BC_END)
            elif line.startswith("@@"):
                sys.stdout.write(BC_CYAN + line + BC_END)
            elif line.startswith("+"):
                sys.stdout.write(BC_GREEN + line + BC_END)
            elif line.startswith("-"):
                sys.stdout.write(BC_RED + line + BC_END)
            else:
                sys.stdout.write(line)
