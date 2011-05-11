# -*- coding: utf-8 -*-
# Copyright (c) 2011    Nils Dagsson Moskopp <nils@dieweltistgarnichtso.net>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

import IPython.ipapi
ip = IPython.ipapi.get()

import ipy_defaults


def main():
    import ipy_profile_sh

    o = ip.options

    o.autocall = 1
    o.system_verbose = 0

    import os
    from datetime import date

    # this is not elegant at all
    GIT_BRACKET_OPEN = \
"""
os.popen(" \
    git branch >/dev/null 2>/dev/null && echo '('; \
    ").read().rstrip()
"""

    GIT_BRACKET_CLOSE = \
"""
os.popen(" \
    git branch >/dev/null 2>/dev/null && echo ')'; \
    ").read().rstrip()
"""

    GIT_BRANCH = \
"""
os.popen(" \
    git name-rev --name-only --always HEAD 2>/dev/null; \
    ").read().rstrip()
"""

    GIT_COLON = \
"""
os.popen(" \
    git branch >/dev/null 2>/dev/null && echo ':'; \
    ").read().rstrip()
"""

    GIT_MODIFIED = \
"""
os.popen(' \
    diff=`git diff 2>/dev/null`; \
    test -n "$diff" && echo "!"; \
    ').read().rstrip()
"""

    GIT_ON = \
"""
os.popen(" \
    git branch >/dev/null 2>/dev/null && echo 'on'; \
    ").read().rstrip()
"""

    GIT_REVSTRING = \
"""
os.popen(" \
    git describe --tags --always 2>/dev/null; \
    ").read().rstrip()
"""

    GIT_STAGED = \
"""
os.popen(' \
    diff=`git diff --cached 2>/dev/null`; \
    test -n "$diff" && echo "+"; \
    ').read().rstrip()
"""

    GIT_UNTRACKED = \
"""
os.popen(' \
    filelist=`git ls-files --others --exclude-standard 2>/dev/null`; \
    test -n "$filelist" && echo "?"; \
    ').read().rstrip()
"""

    o.prompt_in1 = r"\C_Green\h \C_Cyan\Y5\C_Normal ${%s} \C_Cyan${%s}\C_Brown${%s}${%s}${%s}\n\C_Green\N \C_Normal\Y1\C_Normal${%s}\C_Cyan${%s}\C_LightGreen${%s}\C_LightRed${%s}${%s} \C_Brown★ " % \
(
GIT_ON,
GIT_BRANCH,
GIT_BRACKET_OPEN,
GIT_REVSTRING,
GIT_BRACKET_CLOSE,
GIT_COLON,
GIT_BRANCH,
GIT_STAGED,
GIT_MODIFIED,
GIT_UNTRACKED
)
    o.prompt_in2 = r'\C_Brown⋮ '
    o.prompt_out = r'\# ➜ '

    o.confirm_exit = 0
    o.banner = 0

    # for sane integer division that converts to float (1/2 == 0.5)
    o.autoexec.append('from __future__ import division')

    # get return values of commands
    STATUS_FUNCTION = \
"""
def system_return_code(cmd):
    status = os.system(cmd) >> 8  # high-order byte is the exit status
    if (status != 0):
        return status

def magic_cd_fallback_system(cmd):
    if os.path.isdir(os.path.expanduser(cmd)):
        _ip.magic('%cd ' + cmd)
        return

    system_return_code(cmd)

_ip.system=magic_cd_fallback_system
"""

    o.autoexec.append(STATUS_FUNCTION)

    # For %tasks and %kill
    import jobctrl

    # Tab completer that is not quite so picky (i.e.
    # "foo".<TAB> and str(2).<TAB> will work). Complete
    # at your own risk!
    import ipy_greedycompleter


main()
