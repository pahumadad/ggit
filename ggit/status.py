from ggit.core.common import get_dir
from ggit.core.common import get_files
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
    files_no_enc = get_files(FILE_TYPE_NO_ENC)
    for f in files_no_enc:
        if not gpg.exist_enc(f):
            new_files.append(f)
        else:
            changed_files.append(f)

    # print git status header
    for line in git.status_header():
        print(line)
    print()

    # print git status changes to be committed
    index = 1
    for line in git.status_to_commit():
        if index == 2:
            print(line + BC_GREEN)
        else:
            print(line)
        index += 1
    print(BC_END)

    # print changed files

    # print new files
    index = len(get_dir()) + 1
    if new_files:
        print((
            "Untracked files:\n"
            "  (use 'git add <file>...' to include in what will be committed)"
            f"{BC_RED}"
        ))
        for f in new_files:
            print(f"\t{f[index:]}")
        print((
            "\n"
            f"{BC_END}"
            "no changes added to commit "
            "(use 'git add' and/or 'git commit -a')"
        ))
