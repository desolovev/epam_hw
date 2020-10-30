import os
import sys
import re

from fuse import FUSE, Operations


class Passthrough(Operations):
    def __init__(self, root):
        self.root = root

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    def pull_repo(self, full_path):
        if not os.path.isdir(full_path):
            full_path = os.path.dirname(full_path)
        os.system(f'git -C "{full_path}" pull origin')

    def open(self, path, flags):
        full_path = self._full_path(path)
        self.pull_repo(full_path)
        return os.open(full_path, flags)

    def readdir(self, path, fh):
        full_path = self._full_path(path)
        self.pull_repo(full_path)

        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        for r in dirents:
            yield r


def fuse_repo(git_address, dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    repo_name = re.search(r"/(\w*)\.git", git_address)
    repo_name = repo_name.group(1)
    if not os.path.exists(repo_name):
        os.mkdir(repo_name)
    os.system(f'git clone {git_address}')

    FUSE(Passthrough(repo_name), mountpoint=dir_name, nothreads=True, foreground=True)


if __name__ == '__main__':
    fuse_repo(sys.argv[1], sys.argv[2])
