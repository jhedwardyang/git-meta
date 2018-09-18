#!/usr/bin/env python
"""
  Copyright (c) 2018, Two Sigma Open Source
  All rights reserved.

  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions are met:

  * Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.

  * Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

  * Neither the name of git-meta nor the names of its
    contributors may be used to endorse or promote products derived from
    this software without specific prior written permission.

  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
  POSSIBILITY OF SUCH DAMAGE.
"""

import os
import subprocess

from . import exceptions


class Repo(object):
    """
    Represents a clone and the available commands.

    'working_dir' is the working directory of the clone.
    'git_dir' is the .git repository directory, which is always set.
    """

    @staticmethod
    def _get_git_meta_bin():
        """Get the executable of git meta from PATH."""
        return 'git-meta'

    @staticmethod
    def _execute_git_meta_cmd(args, cwd=None):
        """
        Execute a git meta command.

        :param args: Arguments to pass to git meta command.
        :param cwd: Directory to run command in. Otherwise use cwd.
        :return: Stdout of the command.
        :raises GitMetaCommandException: Non-zero exit code from command.
        """
        cmd = [Repo._get_git_meta_bin]
        cmd.extend(args)
        pipes = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True)
        (stdout, stderr) = pipes.communicate()
        if 0 == pipes.returncode:
            return stdout.strip()
        else:
            raise exceptions.GitMetaCommandException(pipes.returncode, args,
                                                     stdout, stderr)

    @staticmethod
    def _root(cwd=None):
        """
        Run `git meta root`.

        :param cwd: Directory to run command in. Otherwise use cwd.
        :return: Root (working directory) of clone.
        :raises GitMetaCommandException: Non-zero exit code from command.
        """
        return Repo._execute_git_meta_cmd(['root'], cwd=cwd)

    @staticmethod
    def help(cwd=None):
        """
        Run `git meta help`.

        :param cwd: Directory to run command in. Otherwise use cwd.
        :return: Output of `git meta help`command.
        :raises GitMetaCommandException: Non-zero exit code from command.
        """
        return Repo._execute_git_meta_cmd(['help'], cwd=cwd)

    @staticmethod
    def version(cwd=None):
        """
        Run `git meta version`.

        :param cwd: Directory to run command in. Otherwise use cwd.
        :return: Output of `git meta version` command.
        :raises GitMetaCommandException: Non-zero exit code from command.
        """
        return Repo._execute_git_meta_cmd(['version'], cwd=cwd)

    @staticmethod
    def get_working_dir(clone_dir):
        """
        Get the working dir if inside a git meta clone.

        :param clone_dir: Directory inside a clone.
        :return: Root of git meta clone.
        :raises GitMetaCommandException: Non-zero exit code from command.
        :raises NoSuchPathException: Could not read the clone_dir.
        """
        if not os.path.exists(clone_dir):
            raise exceptions.NoSuchPathException('Could not read %s' %
                                                 clone_dir)

        try:
            return Repo._root(clone_dir)
        except exceptions.GitMetaCommandException:
            return None

    def __init__(self, clone_dir):
        """
        Create a git meta repo object.

        :param clone_dir: Directory or subdirectory of a git meta clone.
        Uses `git meta root` to determine the root of the clone.
        :raises NoSuchPathException: Could not read the clone_dir.
        :raises GitMetaCommandException: Could not determine git meta root.
        :raises MissingGitMetaCommandException: Directory is not inside a
        git meta clone.
        """
        working_dir = Repo.get_working_dir(clone_dir)
        if not working_dir:
            raise exceptions.MissingGitMetaCloneException(clone_dir)
        self.working_dir = working_dir
        self.git_dir = os.path.join(self.working_dir, '.git')

    def open(self, submodules):
        """
        Open a list of submodules.

        :param submodules: List of submodules to open relative to the root.
        :raises GitMetaCommandException: Non-zero exit code from command.
        """
        assert isinstance(submodules, list)
        cmd = ['open']
        cmd.extend(submodules)
        self._execute_git_meta_cmd(cmd, self.working_dir)

    def checkout(self, params):
        """
        Checkout command with arbitrary parameters.

        :param params: Arguments to pass to `git meta checkout`.
        :raises GitMetaCommandException: Non-zero exit code from command.
        """
        assert isinstance(params, list)
        cmd = ['checkout']
        cmd.extend(params)
        self._execute_git_meta_cmd(cmd, self.working_dir)

    def is_open(self, submodule):
        """
        Check whether or not a given submodule is open in the current clone.

        This works by checking if submodule/.git exists.
        :param submodule: Subodule to check relative to the root.
        :return: Whether or not the submodule is open.
        """
        return os.path.exists(os.path.join(self.working_dir, submodule,
                                           '.git'))
