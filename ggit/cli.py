import argparse

import argcomplete

from ggit.add import add
from ggit.commit import commit
from ggit.diff import diff
from ggit.push import push
from ggit.restore import restore
from ggit.status import status


def get_args():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # add
    p_add = subparsers.add_parser("add")
    p_add.add_argument("paths", nargs="*")
    p_add.set_defaults(func=add)

    # commit
    p_commit = subparsers.add_parser("commit")
    p_commit.add_argument("paths", nargs="*")
    p_commit.add_argument("-a", "--all", action="store_true",
                          help="commit all changed files")
    p_commit.add_argument("-m", "--message", help="commit message")
    p_commit.set_defaults(func=commit)

    # diff
    p_diff = subparsers.add_parser("diff")
    p_diff.add_argument("paths", nargs="*")
    p_diff.set_defaults(func=diff)

    # push
    p_push = subparsers.add_parser("push")
    p_push.set_defaults(func=push)

    # restore
    p_restore = subparsers.add_parser("restore")
    p_restore.add_argument("paths", nargs="*")
    p_restore.set_defaults(func=restore)

    # status
    p_status = subparsers.add_parser("status")
    p_status.set_defaults(func=status)

    # autocomplete
    argcomplete.autocomplete(parser)

    return parser.parse_args()
