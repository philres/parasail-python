#!/usr/bin/env python

# Creates the parasail.py file used for the python bindings.

import sys

def myprint(arg):
    sys.stdout.write(arg+"\n")

myprint("""
import ctypes
import platform
import os
import sys

import numpy

__version__ = "1.0.1"
__title__ = "parasail"
__description__ = "pairwise sequence alignment library"
__uri__ = "https://github.com/jeffdaily/parasail-python"
__author__ = "Jeff Daily"
__email__ = "jeff.daily@pnnl.gov"
__license__ = "BSD"
__copyright__ = "Copyright (c) 2016 Jeff Daily"

_libname = "libparasail.so"
if platform.system() == 'Darwin':
    _libname = "libparasail.dylib"
elif platform.system() == 'Windows':
    _libname = "parasail.dll"
_libpath = os.path.join(os.path.dirname(__file__), _libname)

_lib = None
if os.path.exists(_libpath):
    _lib = ctypes.CDLL(_libpath)
else:
    _lib = ctypes.CDLL(_libname)

if sys.version_info.major < 3:
    def b(x):
        return x
else:
    import codecs
    def b(x):
        return codecs.latin_1_encode(x)[0]

def _make_nd_array(c_pointer, shape, dtype=numpy.intc, order='C', own_data=True):
    arr_size = numpy.prod(shape[:]) * numpy.dtype(dtype).itemsize 
    if sys.version_info.major >= 3:
        buf_from_mem = ctypes.pythonapi.PyMemoryView_FromMemory
        buf_from_mem.restype = ctypes.py_object
        buf_from_mem.argtypes = (ctypes.c_void_p, ctypes.c_int, ctypes.c_int)
        buffer = buf_from_mem(c_pointer, arr_size, 0x100)
    else:
        buf_from_mem = ctypes.pythonapi.PyBuffer_FromMemory
        buf_from_mem.restype = ctypes.py_object
        buffer = buf_from_mem(c_pointer, arr_size)
    return numpy.ndarray(tuple(shape[:]), dtype, buffer, order=order)

c_int_p = ctypes.POINTER(ctypes.c_int)

class result_t(ctypes.Structure):
    _fields_ = [
       ("saturated",     ctypes.c_int),
       ("score",         ctypes.c_int),
       ("matches",       ctypes.c_int),
       ("similar",       ctypes.c_int),
       ("length",        ctypes.c_int),
       ("end_query",     ctypes.c_int),
       ("end_ref",       ctypes.c_int),
       ("score_table",   c_int_p),
       ("matches_table", c_int_p),
       ("similar_table", c_int_p),
       ("length_table",  c_int_p),
       ("score_row",     c_int_p),
       ("matches_row",   c_int_p),
       ("similar_row",   c_int_p),
       ("length_row",    c_int_p),
       ("score_col",     c_int_p),
       ("matches_col",   c_int_p),
       ("similar_col",   c_int_p),
       ("length_col",    c_int_p)
       ]

c_result_p = ctypes.POINTER(result_t)

class Result:
    def __init__(self, pointer, len_query, len_ref):
        self.pointer = pointer
        self.len_query = len_query
        self.len_ref = len_ref
        self._as_parameter_ = pointer
    def __del__(self):
        _lib.parasail_result_free(self.pointer)
    @property
    def saturated(self):
        return self.pointer[0].saturated != 0
    @property
    def score(self):
        return self.pointer[0].score
    @property
    def matches(self):
        return self.pointer[0].matches
    @property
    def similar(self):
        return self.pointer[0].similar
    @property
    def length(self):
        return self.pointer[0].length
    @property
    def end_query(self):
        return self.pointer[0].end_query
    @property
    def end_ref(self):
        return self.pointer[0].end_ref
    @property
    def score_table(self):
        return _make_nd_array(
            self.pointer[0].score_table,
            (self.len_query, self.len_ref))
    @property
    def matches_table(self):
        return _make_nd_array(
            self.pointer[0].matches_table,
            (self.len_query, self.len_ref))
    @property
    def similar_table(self):
        return _make_nd_array(
            self.pointer[0].similar_table,
            (self.len_query, self.len_ref))
    @property
    def length_table(self):
        return _make_nd_array(
            self.pointer[0].length_table,
            (self.len_query, self.len_ref))
    @property
    def score_row(self):
        return _make_nd_array(
            self.pointer[0].score_row,
            (self.len_ref,))
    @property
    def matches_row(self):
        return _make_nd_array(
            self.pointer[0].matches_row,
            (self.len_ref,))
    @property
    def similar_row(self):
        return _make_nd_array(
            self.pointer[0].similar_row,
            (self.len_ref,))
    @property
    def length_row(self):
        return _make_nd_array(
            self.pointer[0].length_row,
            (self.len_ref,))
    @property
    def score_col(self):
        return _make_nd_array(
            self.pointer[0].score_col,
            (self.len_query,))
    @property
    def matches_col(self):
        return _make_nd_array(
            self.pointer[0].matches_col,
            (self.len_query,))
    @property
    def similar_col(self):
        return _make_nd_array(
            self.pointer[0].similar_col,
            (self.len_query,))
    @property
    def length_col(self):
        return _make_nd_array(
            self.pointer[0].length_col,
            (self.len_query,))

class matrix_t(ctypes.Structure):
    _fields_ = [
        ("name",      ctypes.c_char_p),
        ("matrix",    c_int_p),
        ("mapper",    c_int_p),
        ("size",      ctypes.c_int),
        ("max",       ctypes.c_int),
        ("min",       ctypes.c_int),
        ("need_free", ctypes.c_int)
        ]

c_matrix_p = ctypes.POINTER(matrix_t)

class Matrix:
    def __init__(self, pointer):
        self.pointer = pointer
        self._as_parameter_ = pointer
    def __del__(self):
        if self.pointer[0].need_free:
            _lib.parasail_matrix_free(self.pointer)
    @property
    def name(self):
        return self.pointer[0].name
    @property
    def matrix(self):
        return _make_nd_array(
            self.pointer[0].matrix,
            (self.pointer[0].size, self.pointer[0].size))
    @property
    def size(self):
        return self.pointer[0].size
    @property
    def max(self):
        return self.pointer[0].max
    @property
    def min(self):
        return self.pointer[0].min

class profile_data_t(ctypes.Structure):
    _fields_ = [
        ("score", ctypes.c_void_p),
        ("matches", ctypes.c_void_p),
        ("similar", ctypes.c_void_p)
    ]

class profile_t(ctypes.Structure):
    _fields_ = [
        ("s1", ctypes.c_char_p),
        ("s1Len", ctypes.c_int),
        ("matrix", c_matrix_p),
        ("profile8", profile_data_t),
        ("profile16", profile_data_t),
        ("profile32", profile_data_t),
        ("profile64", profile_data_t),
        ("free", ctypes.c_void_p),
        ("stop", ctypes.c_int)
        ]

c_profile_p = ctypes.POINTER(profile_t)

class Profile:
    def __init__(self, pointer, matrix):
        self.pointer = pointer
        self.matrix_ = matrix
        self._as_parameter_ = pointer
    def __del__(self):
        _lib.parasail_profile_free(self.pointer)
    @property
    def s1(self):
        return self.pointer[0].s1
    @property
    def s1Len(self):
        return self.pointer[0].s1Len
    @property
    def matrix(self):
        return self.matrix_

_profile_create_argtypes = [ctypes.c_char_p, ctypes.c_int, c_matrix_p]

_lib.parasail_profile_create_8.argtypes = _profile_create_argtypes
_lib.parasail_profile_create_8.restype = c_profile_p

_lib.parasail_profile_create_16.argtypes = _profile_create_argtypes
_lib.parasail_profile_create_16.restype = c_profile_p

_lib.parasail_profile_create_32.argtypes = _profile_create_argtypes
_lib.parasail_profile_create_32.restype = c_profile_p

_lib.parasail_profile_create_64.argtypes = _profile_create_argtypes
_lib.parasail_profile_create_64.restype = c_profile_p

_lib.parasail_profile_create_sat.argtypes = _profile_create_argtypes
_lib.parasail_profile_create_sat.restype = c_profile_p

_lib.parasail_profile_create_stats_8.argtypes = _profile_create_argtypes
_lib.parasail_profile_create_stats_8.restype = c_profile_p

_lib.parasail_profile_create_stats_16.argtypes = _profile_create_argtypes
_lib.parasail_profile_create_stats_16.restype = c_profile_p

_lib.parasail_profile_create_stats_32.argtypes = _profile_create_argtypes
_lib.parasail_profile_create_stats_32.restype = c_profile_p

_lib.parasail_profile_create_stats_64.argtypes = _profile_create_argtypes
_lib.parasail_profile_create_stats_64.restype = c_profile_p

_lib.parasail_profile_create_stats_sat.argtypes = _profile_create_argtypes
_lib.parasail_profile_create_stats_sat.restype = c_profile_p

def profile_create_8(s1, matrix):
    return Profile(_lib.parasail_profile_create_8(b(s1), len(s1), matrix), matrix)

def profile_create_16(s1, matrix):
    return Profile(_lib.parasail_profile_create_16(b(s1), len(s1), matrix), matrix)

def profile_create_32(s1, matrix):
    return Profile(_lib.parasail_profile_create_32(b(s1), len(s1), matrix), matrix)

def profile_create_64(s1, matrix):
    return Profile(_lib.parasail_profile_create_64(b(s1), len(s1), matrix), matrix)

def profile_create_sat(s1, matrix):
    return Profile(_lib.parasail_profile_create_sat(b(s1), len(s1), matrix), matrix)

def profile_create_stats_8(s1, matrix):
    return Profile(_lib.parasail_profile_create_stats_8(b(s1), len(s1), matrix), matrix)

def profile_create_stats_16(s1, matrix):
    return Profile(_lib.parasail_profile_create_stats_16(b(s1), len(s1), matrix), matrix)

def profile_create_stats_32(s1, matrix):
    return Profile(_lib.parasail_profile_create_stats_32(b(s1), len(s1), matrix), matrix)

def profile_create_stats_64(s1, matrix):
    return Profile(_lib.parasail_profile_create_stats_64(b(s1), len(s1), matrix), matrix)

def profile_create_stats_sat(s1, matrix):
    return Profile(_lib.parasail_profile_create_stats_sat(b(s1), len(s1), matrix), matrix)

def can_use_avx2():
    return bool(_lib.parasail_can_use_avx2())

def can_use_sse41():
    return bool(_lib.parasail_can_use_sse41())

def can_use_sse2():
    return bool(_lib.parasail_can_use_sse2())

# begin non-alignment functions defined here

# parasail_profile_free is not exposed.
# Memory is managed by the Profile class.
_lib.parasail_profile_free.argtypes = [c_profile_p]
_lib.parasail_profile_free.restype = None

# parasail_result_free is not exposed.
# Memory is managed by the Result class.
_lib.parasail_result_free.argtypes = [c_result_p]
_lib.parasail_result_free.restype = None

_lib.parasail_version.argtypes = [c_int_p, c_int_p, c_int_p]
_lib.parasail_version.restype = None

def version():
    major = ctypes.c_int()
    minor = ctypes.c_int()
    patch = ctypes.c_int()
    _lib.parasail_version(
            ctypes.byref(major),
            ctypes.byref(minor),
            ctypes.byref(patch))
    return major.value, minor.value, patch.value

_lib.parasail_time.argtypes = []
_lib.parasail_time.restype = ctypes.c_double

def time():
    return _lib.parasail_time()

_lib.parasail_matrix_lookup
_lib.parasail_matrix_lookup.argtypes = [ctypes.c_char_p]
_lib.parasail_matrix_lookup.restype = c_matrix_p

blosum100 = Matrix(_lib.parasail_matrix_lookup(b("blosum100")))
blosum30 = Matrix(_lib.parasail_matrix_lookup(b("blosum30")))
blosum35 = Matrix(_lib.parasail_matrix_lookup(b("blosum35")))
blosum40 = Matrix(_lib.parasail_matrix_lookup(b("blosum40")))
blosum45 = Matrix(_lib.parasail_matrix_lookup(b("blosum45")))
blosum50 = Matrix(_lib.parasail_matrix_lookup(b("blosum50")))
blosum55 = Matrix(_lib.parasail_matrix_lookup(b("blosum55")))
blosum60 = Matrix(_lib.parasail_matrix_lookup(b("blosum60")))
blosum62 = Matrix(_lib.parasail_matrix_lookup(b("blosum62")))
blosum65 = Matrix(_lib.parasail_matrix_lookup(b("blosum65")))
blosum70 = Matrix(_lib.parasail_matrix_lookup(b("blosum70")))
blosum75 = Matrix(_lib.parasail_matrix_lookup(b("blosum75")))
blosum80 = Matrix(_lib.parasail_matrix_lookup(b("blosum80")))
blosum85 = Matrix(_lib.parasail_matrix_lookup(b("blosum85")))
blosum90 = Matrix(_lib.parasail_matrix_lookup(b("blosum90")))
pam10 = Matrix(_lib.parasail_matrix_lookup(b("pam10")))
pam100 = Matrix(_lib.parasail_matrix_lookup(b("pam100")))
pam110 = Matrix(_lib.parasail_matrix_lookup(b("pam110")))
pam120 = Matrix(_lib.parasail_matrix_lookup(b("pam120")))
pam130 = Matrix(_lib.parasail_matrix_lookup(b("pam130")))
pam140 = Matrix(_lib.parasail_matrix_lookup(b("pam140")))
pam150 = Matrix(_lib.parasail_matrix_lookup(b("pam150")))
pam160 = Matrix(_lib.parasail_matrix_lookup(b("pam160")))
pam170 = Matrix(_lib.parasail_matrix_lookup(b("pam170")))
pam180 = Matrix(_lib.parasail_matrix_lookup(b("pam180")))
pam190 = Matrix(_lib.parasail_matrix_lookup(b("pam190")))
pam20 = Matrix(_lib.parasail_matrix_lookup(b("pam20")))
pam200 = Matrix(_lib.parasail_matrix_lookup(b("pam200")))
pam210 = Matrix(_lib.parasail_matrix_lookup(b("pam210")))
pam220 = Matrix(_lib.parasail_matrix_lookup(b("pam220")))
pam230 = Matrix(_lib.parasail_matrix_lookup(b("pam230")))
pam240 = Matrix(_lib.parasail_matrix_lookup(b("pam240")))
pam250 = Matrix(_lib.parasail_matrix_lookup(b("pam250")))
pam260 = Matrix(_lib.parasail_matrix_lookup(b("pam260")))
pam270 = Matrix(_lib.parasail_matrix_lookup(b("pam270")))
pam280 = Matrix(_lib.parasail_matrix_lookup(b("pam280")))
pam290 = Matrix(_lib.parasail_matrix_lookup(b("pam290")))
pam30 = Matrix(_lib.parasail_matrix_lookup(b("pam30")))
pam300 = Matrix(_lib.parasail_matrix_lookup(b("pam300")))
pam310 = Matrix(_lib.parasail_matrix_lookup(b("pam310")))
pam320 = Matrix(_lib.parasail_matrix_lookup(b("pam320")))
pam330 = Matrix(_lib.parasail_matrix_lookup(b("pam330")))
pam340 = Matrix(_lib.parasail_matrix_lookup(b("pam340")))
pam350 = Matrix(_lib.parasail_matrix_lookup(b("pam350")))
pam360 = Matrix(_lib.parasail_matrix_lookup(b("pam360")))
pam370 = Matrix(_lib.parasail_matrix_lookup(b("pam370")))
pam380 = Matrix(_lib.parasail_matrix_lookup(b("pam380")))
pam390 = Matrix(_lib.parasail_matrix_lookup(b("pam390")))
pam40 = Matrix(_lib.parasail_matrix_lookup(b("pam40")))
pam400 = Matrix(_lib.parasail_matrix_lookup(b("pam400")))
pam410 = Matrix(_lib.parasail_matrix_lookup(b("pam410")))
pam420 = Matrix(_lib.parasail_matrix_lookup(b("pam420")))
pam430 = Matrix(_lib.parasail_matrix_lookup(b("pam430")))
pam440 = Matrix(_lib.parasail_matrix_lookup(b("pam440")))
pam450 = Matrix(_lib.parasail_matrix_lookup(b("pam450")))
pam460 = Matrix(_lib.parasail_matrix_lookup(b("pam460")))
pam470 = Matrix(_lib.parasail_matrix_lookup(b("pam470")))
pam480 = Matrix(_lib.parasail_matrix_lookup(b("pam480")))
pam490 = Matrix(_lib.parasail_matrix_lookup(b("pam490")))
pam50 = Matrix(_lib.parasail_matrix_lookup(b("pam50")))
pam500 = Matrix(_lib.parasail_matrix_lookup(b("pam500")))
pam60 = Matrix(_lib.parasail_matrix_lookup(b("pam60")))
pam70 = Matrix(_lib.parasail_matrix_lookup(b("pam70")))
pam80 = Matrix(_lib.parasail_matrix_lookup(b("pam80")))
pam90 = Matrix(_lib.parasail_matrix_lookup(b("pam90")))

_lib.parasail_matrix_create.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
_lib.parasail_matrix_create.restype = c_matrix_p

def matrix_create(alphabet, match, mismatch):
    return Matrix(_lib.parasail_matrix_create(b(alphabet), match, mismatch))

# parasail_matrix_free is not exposed.
# Memory is managed by the Matrix class.
_lib.parasail_matrix_free.argtypes = [c_matrix_p]
_lib.parasail_matrix_free.restype = None

# begin generated names here

_argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, c_matrix_p]
""")

# serial reference implementations (3x2x3 = 18 impl)
alg = ["nw", "sg", "sw"]
stats = ["", "_stats"]
table = ["", "_table", "_rowcol"]
for a in alg:
    for s in stats:
        for t in table:
            myprint("")
            myprint("_lib.parasail_"+a+s+t+".argtypes = _argtypes")
            myprint("_lib.parasail_"+a+s+t+".restype = c_result_p")
            myprint("def "+a+s+t+"(s1, s2, open, extend, matrix):")
            myprint(" "*4+"return Result(_lib.parasail_"+a+s+t+"(")
            myprint(" "*8+"b(s1), len(s1), b(s2), len(s2), open, extend, matrix),")
            myprint(" "*8+"len(s1), len(s2))")

## serial scan reference implementations (3x2x3 = 18 impl)
alg = ["nw", "sg", "sw"]
stats = ["", "_stats"]
table = ["", "_table", "_rowcol"]
for a in alg:
    for s in stats:
        for t in table:
            myprint("")
            myprint("_lib.parasail_"+a+s+t+"_scan.argtypes = _argtypes")
            myprint("_lib.parasail_"+a+s+t+"_scan.restype = c_result_p")
            myprint("def "+a+s+t+"_scan(s1, s2, open, extend, matrix):")
            myprint(" "*4+"return Result(_lib.parasail_"+a+s+t+"_scan(")
            myprint(" "*8+"b(s1), len(s1), b(s2), len(s2), open, extend, matrix),")
            myprint(" "*8+"len(s1), len(s2))")

# vectorized implementations (3x2x3x3x4 = 216 impl)
alg = ["nw", "sg", "sw"]
stats = ["", "_stats"]
table = ["", "_table", "_rowcol"]
par = ["_scan", "_striped", "_diag"]
width = ["_64","_32","_16","_8","_sat"]
for a in alg:
    for s in stats:
        for t in table:
            for p in par:
                for w in width:
                    myprint("")
                    myprint("_lib.parasail_"+a+s+t+p+w+".argtypes = _argtypes")
                    myprint("_lib.parasail_"+a+s+t+p+w+".restype = c_result_p")
                    myprint("def "+a+s+t+p+w+"(s1, s2, open, extend, matrix):")
                    myprint(" "*4+"return Result(_lib.parasail_"+a+s+t+p+w+"(")
                    myprint(" "*8+"b(s1), len(s1), b(s2), len(s2), open, extend, matrix),")
                    myprint(" "*8+"len(s1), len(s2))")

myprint("""
_argtypes = [c_profile_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int]
""")

# vectorized profile implementations (3x2x3x2x4 = 144 impl)
alg = ["nw", "sg", "sw"]
stats = ["", "_stats"]
table = ["", "_table", "_rowcol"]
par = ["_scan_profile", "_striped_profile"]
width = ["_64","_32","_16","_8","_sat"]
for a in alg:
    for s in stats:
        for t in table:
            for p in par:
                for w in width:
                    myprint("")
                    myprint("_lib.parasail_"+a+s+t+p+w+".argtypes = _argtypes")
                    myprint("_lib.parasail_"+a+s+t+p+w+".restype = c_result_p")
                    myprint("def "+a+s+t+p+w+"(profile, s2, open, extend):")
                    myprint(" "*4+"return Result(_lib.parasail_"+a+s+t+p+w+"(")
                    myprint(" "*8+"profile, b(s2), len(s2), open, extend),")
                    myprint(" "*8+"profile.s1Len, len(s2))")

