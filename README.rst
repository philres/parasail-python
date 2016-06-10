parasail-python: Python Bindings for the Parasail C Library
===========================================================

Author: Jeff Daily (jeff.daily@pnnl.gov)

Table of Contents
-----------------

-  `Installation <#installation>`__
-  `Citing parasail <#citing-parasail>`__
-  `License: Battelle BSD-style <#license-battelle-bsd-style>`__

This package contains Python bindings for
`parasail <https://github.com/jeffdaily/parasail>`__. Parasail is a SIMD
C (C99) library containing implementations of the Smith-Waterman
(local), Needleman-Wunsch (global), and semi-global pairwise sequence
alignment algorithms.

Installation
------------

`back to top <#parasail-python-python-bindings-for-the-parasail-c-library>`__

Using pip
+++++++++

The recommended way of installing is to use the latest version available via pip.

::

    pip install parasail
    
Binaries for Windows and OSX should be available via pip.  Using pip on a Linux platform will first download the latest version of the parasail C library sources and then compile them automatically into a shared library.  For an installation from sources, or to learn how the pip installation works on Linux, please read on.

Building from Source
++++++++++++++++++++

The parasail python bindings are based on ctypes.  Unfortunately, best practices are not firmly established for providing cross-platform and user-friendly python bindings based on ctypes.  The approach with parasail-python is to install the parasail shared library as "package data" and use a relative path from the parasail/__init__.py in order to locate the shared library.

There are two approaches currently supported.  First, you can compile your own parasail shared library using one of the recommended build processes described in the parasail C library README.md, then copy the parasail.dll (Windows), libparasail.so (Linux), or libparasail.dylib (OSX) shared library to parasail-python/parasail -- the same folder location as parasasail-python/parasail/__init__.py.

The second approach is to let the setup.py script attempt to download and compile the parasail C library for you using the configure script that comes with it.  This happens as a side effect of the bdist_wheel target.

::

    python setup.py bdist_wheel

The bdist_wheel target will first look for the shared library.  If it exists, it will happily install it as package data.  Otherwise, the latest parasail master branch from github will be downloaded, unzipped, configured, made, and the shared library will be copied into the appropriate location for package data installation.

Example
-------

The Python interface only includes bindings for the dispatching
functions, not the low-level instruction set-specific function calls.
The Python interface also includes wrappers for the various PAM and
BLOSUM matrices included in the distribution.

Gap open and extension penalties are specified as positive integers.

.. code:: python

    import parasail
    result = parasail.sw_scan_16("asdf", "asdf", 11, 1, parasail.blosum62)
    result = parasail.sw_stats_striped_8("asdf", "asdf", 11, 1, parasail.pam100)

Citing parasail
---------------

`back to top <#parasail-python-python-bindings-for-the-parasail-c-library>`__

If needed, please cite the following paper.

Daily, Jeff. (2016). Parasail: SIMD C library for global, semi-global,
and local pairwise sequence alignments. *BMC Bioinformatics*, 17(1),
1-11. doi:10.1186/s12859-016-0930-z

http://dx.doi.org/10.1186/s12859-016-0930-z

License: Battelle BSD-style
---------------------------

`back to top <#parasail-python-python-bindings-for-the-parasail-c-library>`__

Copyright (c) 2015, Battelle Memorial Institute

1. Battelle Memorial Institute (hereinafter Battelle) hereby grants
   permission to any person or entity lawfully obtaining a copy of this
   software and associated documentation files (hereinafter “the
   Software”) to redistribute and use the Software in source and binary
   forms, with or without modification. Such person or entity may use,
   copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and may permit others to do so, subject to
   the following conditions:

   -  Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimers.

   -  Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in
      the documentation and/or other materials provided with the
      distribution.

   -  Other than as used herein, neither the name Battelle Memorial
      Institute or Battelle may be used in any form whatsoever without
      the express written consent of Battelle.

   -  Redistributions of the software in any form, and publications
      based on work performed using the software should include the
      following citation as a reference:

   Daily, Jeff. (2016). Parasail: SIMD C library for global,
   semi-global, and local pairwise sequence alignments. *BMC
   Bioinformatics*, 17(1), 1-11. doi:10.1186/s12859-016-0930-z

2. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
   "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
   LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
   A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL BATTELLE OR
   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
   PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
   OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
   OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

