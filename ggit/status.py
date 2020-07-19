import sys
from ggit.core.common import get_diff
from ggit.core.common import get_files
from ggit.core.common import get_rel_path
from ggit.core.common import BC_END
from ggit.core.common import BC_GREEN
from ggit.core.common import BC_RED
from ggit.core.common import FILE_TYPE_NO_ENC
from ggit.core.git import Git
from ggit.core.gpg import GPG


def status():

    git = Git()
    gpg = GPG()

    new_files = []
    changed_files = []
    files_no_enc = get_files(file_type=FILE_TYPE_NO_ENC)
    for f in files_no_enc:
        if not gpg.exist_enc(f):
            new_files.append(f)
        else:
            if not get_diff(f):
                continue
            changed_files.append(f)

    # print git status header
    for line in git.status_header():
        sys.stdout.write(line + "\n")
    sys.stdout.write("\n")

    # print git status changes to be committed
    index = 1
    resp = git.status_to_commit()
    for line in resp:
        if index == 2:
            sys.stdout.write(line + BC_GREEN + "\n")
        else:
            sys.stdout.write(line + "\n")
        index += 1
    if resp:
        sys.stdout.write(BC_END + "\n")

    # print changed files
    if changed_files:
        sys.stdout.write((
            "Changes not staged for commit:\n"
            "  (use 'ggit add <file>...' to update what will be committed)\n"
            "  (use 'ggit restore <file>...' to discard changes in working directory)\n"  # noqa
            f"{BC_RED}"
        ))
        for f in changed_files:
            sys.stdout.write(f"\tmodified:   {get_rel_path(f)}\n")
        sys.stdout.write(BC_END + "\n")

    # print new files
    if new_files:
        sys.stdout.write((
            "Untracked files:\n"
            "  (use 'git add <file>...' to include in what will be committed)"
            f"{BC_RED}\n"
        ))
        for f in new_files:
            sys.stdout.write(f"\t{get_rel_path(f)}\n")
        sys.stdout.write((
            "\n"
            f"{BC_END}"
            "no changes added to commit "
            "(use 'ggit add' and/or 'ggit commit -a')\n"
        ))

    # footer
    if not changed_files and not new_files and not resp:
        sys.stdout.write("nothing to commit, working tree clean\n")
    elif not resp:
        sys.stdout.write(
            "no changes added to commit (use 'ggit add' and/or 'ggit commit -a')\n"  # noqa
        )
