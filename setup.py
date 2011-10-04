# -*- coding: iso-8859-1 -*-
# -----------------------------------------------------------------------------
# setup.py - Setup script for kaa.Imlib2
# -----------------------------------------------------------------------------
# $Id$
#
# -----------------------------------------------------------------------------
# kaa.imlib2 - An imlib2 wrapper for Python
# Copyright (C) 2004-2006 Jason Tackaberry <tack@sault.org>
#
# First Edition: Jason Tackaberry <tack@sault.org>
# Maintainer:    Jason Tackaberry <tack@sault.org>
#
# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version
# 2.1 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA
#
# -----------------------------------------------------------------------------

MODULE = 'imlib2'
VERSION = '0.3.0'
REQUIRES = ['kaa-base']

# python imports
import os
import sys

if 'pip-egg-info' in sys.argv:
    # Installing via pip; ensure dependencies are visible.
    from setuptools import setup
    setup(name='kaa-' + MODULE, version=VERSION, install_requires=REQUIRES)
    sys.exit(0)


try:
    # kaa base imports
    from kaa.distribution.core import Extension, setup
except ImportError:
    print 'kaa.base not installed'
    sys.exit(1)

files = [ 'src/imlib2.c', 'src/image.c', 'src/font.c', 'src/rawformats.c' ]
libraries = []
if not os.uname()[0] in ('FreeBSD', 'Darwin'):
    libraries.append('rt')
imlib2so = Extension('kaa.imlib2._Imlib2module', files,
                     libraries = libraries, config='src/config.h')


if not imlib2so.check_library('imlib2', '1.2.1'):
    print 'Imlib2 >= 1.2.1 not found'
    print 'Download from http://enlightenment.freedesktop.org/'
    sys.exit(1)


if imlib2so.check_cc(['<fcntl.h>'], 'shm_open("foobar");', '-lrt'):
    imlib2so.config('#define HAVE_POSIX_SHMEM')
    print "POSIX shared memory enabled"
else:
    print "POSIX shared memory disabled"

if imlib2so.check_library("librsvg-2.0", "2.10.0"):
    imlib2so.config('#define HAVE_SVG')
    files.append('src/svg.c')
    print "+ svg support enabled"
else:
    print "- svg support disabled"

setup(
    module = MODULE,
    version = VERSION,
    license = 'LGPL',
    url = 'http://doc.freevo.org/api/kaa/imlib2/',
    summary = 'Python bindings for Imlib2, a powerful and efficient image processing library.',
    description = 'kaa.imlib2 provides thread-safe Python bindings for Imlib2, a featureful '
                   'and efficient image processing library, which produces high quality, '
                   'anti-aliased output.',
    rpminfo = {
        'requires': 'python-kaa-base >= 0.1.2, imlib2 >= 1.2.1',
        'build_requires': 'python-kaa-base >= 0.1.2, imlib2-devel >= 1.2.1'
    },
    ext_modules = [imlib2so],
    install_requires = REQUIRES,
    namespace_packages = ['kaa'],
)
