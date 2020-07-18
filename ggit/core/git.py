from subprocess import PIPE
from subprocess import run


class Git:

    def __exec_git(self, args=[]):
        cmd = ["git"] + args
        r = run(cmd, stdout=PIPE, stderr=PIPE)
        if r.returncode != 0:
            raise RuntimeError(r.stderr.decode("utf-8").rstrip())
        return r.stdout.decode("utf-8")

    def add(self, file):
        self.__exec_git(["add", file])

    def status(self):
        out = []
        resp = self.__exec_git(["status"])
        for line in resp.splitlines():
            if line == "":
                break
            out.append(line)
        return out
