from subprocess import PIPE
from subprocess import run


class GPG:

    def __init__(self):
        self.__get_gpg_id()

    def __exec_gpg(self, args=[]):
        cmd = ["gpg"] + args
        r = run(cmd, stdout=PIPE, stderr=PIPE)
        if r.returncode != 0:
            raise RuntimeError(r.stderr.decode("utf-8").rstrip())
        return r.stdout.decode("utf-8")

    def __get_gpg_id(self):
        resp = self.__exec_gpg(["--list-secret-keys", "--with-colons"])
        for line in resp.splitlines():
            if not line.startswith("sec"):
                continue
            self.id = line.split(":")[4]
            break
