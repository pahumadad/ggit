import os

from ggit.core.gpg import GPG

BC_RED = "\033[91m"
BC_END = "\033[0m"
BLACKLIST = (
    ".git",
    ".gitignore",
    "README.md",
)
FILE_TYPE_ALL = "all"
FILE_TYPE_ENC = "encrypted"
FILE_TYPE_NO_ENC = "no_encrypted"


def get_dir():
    return os.path.abspath(os.getcwd())


def get_files(file_type=FILE_TYPE_ALL):
    if file_type not in (FILE_TYPE_ALL, FILE_TYPE_ENC, FILE_TYPE_NO_ENC):
        raise ValueError(
            f"file_type arg unknown: {file_type} (choose from "
            f"'{FILE_TYPE_ALL}', '{FILE_TYPE_ENC}' or '{FILE_TYPE_NO_ENC}')"
        )

    files_list = []
    root = get_dir()
    for base, _, files in os.walk(root):
        if any([el for el in BLACKLIST if el in base[len(root):]]):
            continue
        for f in files:
            if f in BLACKLIST:
                continue
            if file_type == FILE_TYPE_ENC and not f.endswith(GPG.EXT):
                continue
            if file_type == FILE_TYPE_NO_ENC and f.endswith(GPG.EXT):
                continue
            files_list.append(os.path.join(base, f))

    return files_list
