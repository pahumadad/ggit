import os
from subprocess import PIPE
from subprocess import run


class GPG:

    # encrypted file extension
    EXT = ".gpg"

    def __init__(self):
        self.__get_id()

    def __exec_gpg(self, args=[]):
        cmd = ["gpg"] + args
        r = run(cmd, stdout=PIPE, stderr=PIPE)
        if r.returncode != 0:
            raise RuntimeError(r.stderr.decode("utf-8").rstrip())
        return r.stdout.decode("utf-8")

    def __get_id(self):
        resp = self.__exec_gpg(["--list-secret-keys", "--with-colons"])
        for line in resp.splitlines():
            if not line.startswith("sec"):
                continue
            self.__id = line.split(":")[4]
            break

    def __get_enc_file(self, file):
        return file + self.EXT

    def __get_dec_file(self, file):
        return file.replace(self.EXT, "")

    def exist_enc(self, file):
        return os.path.isfile(self.__get_enc_file(file))

    def exist_dec(self, file):
        return os.path.isfile(self.__get_dec_file(file))

    def encrypt(self, file):
        if not os.path.isfile(file):
            raise ValueError(f"file not found: {file}")

        enc_file = self.__get_enc_file(file)
        self.__exec_gpg([
            "--use-agent",
            "--yes",
            "--trust-model=always",
            "-r", self.__id,
            "--encrypt",
            "-o", enc_file,
            file
        ])
        return enc_file

    def decrypt(self, file):
        if not os.path.isfile(file):
            raise ValueError(f"file not found: {file}")

        if not file.endswith(self.EXT):
            raise ValueError(f"file type not supported: {file}")

        self.__exec_gpg([
            "--use-agent",
            "-q",
            "--decrypt",
            "-o", self.__get_dec_file(file),
            file
        ])
