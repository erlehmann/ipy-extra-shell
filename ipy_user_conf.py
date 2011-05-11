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

    # uncomment if you want to get ipython -p sh behaviour
    # without having to use command line switches  
    import ipy_profile_sh

    # Configure your favourite editor?
    # Good idea e.g. for %edit os.path.isfile

    #import ipy_editors
    
    # Choose one of these:
    
    #ipy_editors.scite()
    #ipy_editors.scite('c:/opt/scite/scite.exe')
    #ipy_editors.komodo()
    #ipy_editors.idle()
    # ... or many others, try 'ipy_editors??' after import to see them
    
    # Or roll your own:
    #ipy_editors.install_editor("c:/opt/jed +$line $file")
    
    
    o = ip.options
    # An example on how to set options
    #o.autocall = 1
    o.system_verbose = 0
    
    #import_all("os sys")
    #execf('~/_ipython/ns.py')

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

    GIT_UNTRACKED = \
"""
os.popen(' \
    filelist=`git ls-files --others --exclude-standard 2>/dev/null`; \
    test -n "$filelist" && echo "?"; \
    ').read().rstrip()
"""

    o.prompt_in1 = r"\C_Brown\u\C_Normal at \C_Purple\h\C_Normal in \C_Cyan\Y5\C_Normal ${%s} \C_Cyan${%s}\C_Brown${%s}${%s}${%s}\n\C_Green\N \C_Normal\Y1\C_Normal${%s}\C_Cyan${%s}\C_LightRed${%s}${%s} \C_Brown★ " % \
(
GIT_ON,
GIT_BRANCH,
GIT_BRACKET_OPEN,
GIT_REVSTRING,
GIT_BRACKET_CLOSE,
GIT_COLON,
GIT_BRANCH,
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
    o.autoexec.append('import errno')
    o.autoexec.append('import inspect')

    STATUS_FUNCTION = \
"""
def system_return_code(cmd):
    status = os.system(cmd) >> 8  # high-order byte is the exit status
    if (status != 0):
        for e in inspect.getmembers(errno):
            if (e[1] == status):
                return e[0]
        return status

_ip.system=system_return_code
"""

    o.autoexec.append(STATUS_FUNCTION)

    # For %tasks and %kill
    import jobctrl 
    
    # Tab completer that is not quite so picky (i.e. 
    # "foo".<TAB> and str(2).<TAB> will work). Complete 
    # at your own risk!
    import ipy_greedycompleter

def terminal_size_posix():
    """ Return terminal (height, width) on Posix systems. """
    # This function is based on _terminal_size_unix() which can be found at
    # <https://bitbucket.org/robertkern/kernmagic/src/tip/kernmagic/utils.py>
    try:
        import struct
        import fcntl
        import termios

        return struct.unpack('hh',
            fcntl.ioctl(
                sys.stdout.fileno(),
                termios.TIOCGWINSZ,
                'hhww'  # length of return value (must be 4)
            )
        )

    except (ImportError, AttributeError, IOError):
        return (25, 80)

# some config helper functions you can use 
def import_all(modules):
    """ Usage: import_all("os sys") """ 
    for m in modules.split():
        ip.ex("from %s import *" % m)

def execf(fname):
    """ Execute a file in user namespace """
    ip.ex('execfile("%s")' % os.path.expanduser(fname))

main()
