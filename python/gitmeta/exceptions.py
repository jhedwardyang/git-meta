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

"""Modules containing exceptions thrown from git meta python bindings."""


class GitMetaException(Exception):
    """Base class for all package exceptions."""


class MissingGitMetaCloneException(GitMetaException):
    """No clone was found."""


class NoSuchPathException(GitMetaException, OSError):
    """Path being provided could not be read."""


class GitMetaCommandException(GitMetaException):
    """Command returned a non-zero exit code."""

    def __init__(self, returncode, args, stdout, stderr):
        """
        Exception thrown while shelling out to git meta.

        :param returncode: Return code of the command.
        :param args: Arguments being passed to git meta.
        :param stdout: Output of stdout.
        :param stderr: Output of stderr.
        """
        self.returncode = returncode
        self.args = args
        self.stdout = stdout
        self.stderr = stderr
