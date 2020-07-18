import sys
from subprocess import PIPE
from subprocess import run


class Git:

    def __exec_git(self, args=[]):
        cmd = ["git"] + args
        r = run(cmd, stdout=PIPE, stderr=PIPE)
        if r.returncode != 0:
            sys.exit(r.stderr.decode("utf-8").rstrip())
        return r.stdout.decode("utf-8")

    def add(self, file):
        self.__exec_git(["add", file])

    def commit(self, args):
        return self.__exec_git(["commit"] + args)

    def push(self):
        return self.__exec_git(["push"])

    def status_header(self):
        out = []
        resp = self.__exec_git(["status"])
        for line in resp.splitlines():
            if line == "":
                break
            out.append(line)
        return out

    def status_to_commit(self):
        out = []
        get_msg = False
        resp = self.__exec_git(["status"])
        for line in resp.splitlines():
            if get_msg and line == "":
                break
            if line == "Changes to be committed:":
                get_msg = True
            if get_msg:
                out.append(line)
        return out
