import os
import sys
from difflib import unified_diff

from ggit.core.gpg import GPG

BC_BOLD = "\033[1m"
BC_CYAN = "\033[96m"
BC_END = "\033[0m"
BC_GREEN = "\033[92m"
BC_RED = "\033[91m"
BLACKLIST = (
    ".git",
    ".gitignore",
    "README.md",
)
FILE_TYPE_ALL = "all"
FILE_TYPE_ENC = "encrypted"
FILE_TYPE_NO_ENC = "no_encrypted"


def get_diff(file_2):
    gpg = GPG()
    file_1 = gpg.get_enc_file(file_2)
    if not os.path.isfile(file_1):
        return None

    file_1 = gpg.decrypt(file_1, tmp=True)

    # open files
    text_1 = open(file_1).readlines()
    text_2 = open(file_2).readlines()

    # compare
    resp = []
    file = get_rel_path(file_2)
    for line in unified_diff(text_1, text_2, fromfile=file, tofile=file):
        resp.append(line)

    # delete temp file
    os.remove(file_1)
    return resp


def get_dir():
    return os.path.abspath(os.getcwd())


def get_file(file):
    if file in BLACKLIST:
        return
    file = os.path.join(get_dir(), file)
    if not os.path.isfile(file):
        sys.exit(f"file not found: f{file}")
    return file


def get_files(folder=None, file_type=FILE_TYPE_ALL, new=False):
    if file_type not in (FILE_TYPE_ALL, FILE_TYPE_ENC, FILE_TYPE_NO_ENC):
        sys.exit(
            f"file_type arg unknown: {file_type} (choose from "
            f"'{FILE_TYPE_ALL}', '{FILE_TYPE_ENC}' or '{FILE_TYPE_NO_ENC}')"
        )

    if not folder:
        root = get_dir()
    elif folder and os.path.isdir(folder):
        root = os.path.abspath(folder)
    else:
        sys.exit(f"folder not found: {folder}")

    files_list = []
    for base, _, files in os.walk(root):
        if any([el for el in BLACKLIST if el in base[len(root):]]):
            continue
        for filename in files:
            if filename in BLACKLIST:
                continue
            if file_type == FILE_TYPE_ENC and not filename.endswith(GPG.EXT):
                continue
            if file_type == FILE_TYPE_NO_ENC and filename.endswith(GPG.EXT):
                continue
            path = os.path.join(base, filename)
            if os.path.islink(path):
                continue
            if new and not filename.endswith(GPG.EXT) and GPG.exist_enc(path):
                continue
            files_list.append(path)

    return files_list


def get_rel_path(file):
    root = get_dir()
    return file[len(root) + 1:]
