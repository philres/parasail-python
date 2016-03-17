# parasail-python: Python Bindings for the Parasail C Library

Author: Jeff Daily (jeff.daily@pnnl.gov)

This package contains Python bindings for [parasail](https://github.com/jeffdaily/parasail). Parasail is a SIMD C (C99) library containing implementations of the Smith-Waterman (local), Needleman-Wunsch (global), and semi-global pairwise sequence alignment algorithms.  

## Installation

Once you have installed parasail into --prefix=$PREFIX, you can also compile the Python bindings.  Don't forget to add $PREFIX/lib to your LD_LIBRARY_PATH, if needed.  The Python bindings are in the <parasail>/bindings/python directory.  To build, run:

```
PARASAIL_PREFIX=$PREFIX python setup.py build
```

This will correctly setup the necessary CPPFLAGS, LDFLAGS, and LIBS variables during the build.  Because the parasail.h header uses C99 keywords, e.g., restrict, the setup.py process will test your C compiler for the correct use of restrict, automatically.

The Python interface only includes bindings for the dispatching functions, not the low-level instruction set-specific function calls.  The Python interface also includes wrappers for the various PAM and BLOSUM matrices included in the distribution.

Example:

```python
import parasail
result = parasail.sw_scan_16("asdf", "asdf", -11, -1, parasail.blosum62)
result = parasail.sw_stats_striped_8("asdf", "asdf", -11, -1, parasail.pam100)
```

