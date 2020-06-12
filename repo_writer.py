import util
import contextlib
import os
import math
import random


class UnwritableError(Exception):
    pass


class GitRepoWriter:
    def __init__(self, path, dummy_file='.dummy_file', branch='dummy_branch'):
        import git

        self.repo = git.Repo(path)
        self.dummy_file = dummy_file
        self.branch = branch

    def write(self, commit_count):
        if commit_count < 1:
            return

        with util.Defer() as defer:
            if self.repo.is_dirty():
                self.repo.git.stash()
                defer + (lambda: self.repo.git.stash('apply'))

            dummy_path = os.path.join(
                self.repo.working_tree_dir, self.dummy_file
            )

            active = self.repo.active_branch
            if active.name == self.branch:
                checkout = active
            else:
                checkout = util.find(
                    self.repo.branches, lambda x: x.name == self.branch
                )

            if checkout == None:
                checkout = self.repo.create_head(self.branch)

            checkout.checkout()
            defer + (lambda: active.checkout())

            self.write_commits(self.repo.index, commit_count, dummy_path)

    def write_commits(self, index, count, dummy_path):
        for _ in range(count):
            util.toggle_file(
                dummy_path,
                on_create=lambda: index.add(dummy_path),
                on_delete=lambda: index.remove(dummy_path)
            )
            index.commit('Just looking busy')

    def push(self):
        self.repo.remote().push(self.branch + ':' + self.branch)
