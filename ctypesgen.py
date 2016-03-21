#!/usr/bin/env python

# Creates the parasail.py file used for the python bindings.

print """
from ctypes import *
import platform

import numpy

_libname = "libparasail.so"
if platform.system() == 'Darwin':
    _libname = "libparasail.dylib"
elif platform.system() == 'Windows':
    _libname = "parasail"

_lib = CDLL(_libname)

c_int_p = POINTER(c_int)

class result_t(Structure):
    _fields_ = [
       ("saturated",     c_int),
       ("score",         c_int),
       ("matches",       c_int),
       ("similar",       c_int),
       ("length",        c_int),
       ("end_query",     c_int),
       ("end_ref",       c_int),
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

c_result_p = POINTER(result_t)

class Result:
    def __init__(self, pointer):
        self.pointer = pointer
        self._as_parameter_ = pointer
    def __del__(self):
        _lib.parasail_result_free(self.pointer)
    @property
    def score(self):
        return self.pointer[0].score
    @property
    def saturated(self):
        return self.pointer[0].saturated != 0

class matrix_t(Structure):
    _fields_ = [
        ("name",      c_char_p),
        ("matrix",    c_int_p),
        ("mapper",    c_int_p),
        ("size",      c_int),
        ("max",       c_int),
        ("min",       c_int),
        ("need_free", c_int)
        ]

c_matrix_p = POINTER(matrix_t)

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
        return numpy.ctypeslib.as_array(
            self.pointer[0].matrix,
            (self.pointer[0].size, self.pointer[0].size))

class profile_data_t(Structure):
    _fields_ = [
        ("score", c_void_p),
        ("matches", c_void_p),
        ("similar", c_void_p)
    ]

class profile_t(Structure):
    _fields_ = [
        ("s1", c_char_p),
        ("s1Len", c_int),
        ("matrix", c_matrix_p),
        ("profile8", profile_data_t),
        ("profile16", profile_data_t),
        ("profile32", profile_data_t),
        ("profile64", profile_data_t),
        ("free", c_void_p),
        ("stop", c_int)
        ]

c_profile_p = POINTER(profile_t)

class Profile:
    def __init__(self, pointer):
        self.pointer = pointer
        self._as_parameter_ = pointer
    def __del__(self):
        _lib.parasail_profile_free(self.pointer)
    @property
    def s1(self):
        return self.pointer[0].s1

_profile_create_argtypes = [c_char_p, c_int, c_matrix_p]

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
    return Profile(_lib.parasail_profile_create_8(s1, len(s1), matrix))

def profile_create_16(s1, matrix):
    return Profile(_lib.parasail_profile_create_16(s1, len(s1), matrix))

def profile_create_32(s1, matrix):
    return Profile(_lib.parasail_profile_create_32(s1, len(s1), matrix))

def profile_create_64(s1, matrix):
    return Profile(_lib.parasail_profile_create_64(s1, len(s1), matrix))

def profile_create_sat(s1, matrix):
    return Profile(_lib.parasail_profile_create_sat(s1, len(s1), matrix))

def profile_create_stats_8(s1, matrix):
    return Profile(_lib.parasail_profile_create_stats_8(s1, len(s1), matrix))

def profile_create_stats_16(s1, matrix):
    return Profile(_lib.parasail_profile_create_stats_16(s1, len(s1), matrix))

def profile_create_stats_32(s1, matrix):
    return Profile(_lib.parasail_profile_create_stats_32(s1, len(s1), matrix))

def profile_create_stats_64(s1, matrix):
    return Profile(_lib.parasail_profile_create_stats_64(s1, len(s1), matrix))

def profile_create_stats_sat(s1, matrix):
    return Profile(_lib.parasail_profile_create_stats_sat(s1, len(s1), matrix))

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
    major = c_int()
    minor = c_int()
    patch = c_int()
    _lib.parasail_version(byref(major), byref(minor), byref(patch))
    return major.value, minor.value, patch.value

_lib.parasail_time.argtypes = []
_lib.parasail_time.restype = c_double

def time():
    return _lib.parasail_time()

_lib.parasail_matrix_lookup
_lib.parasail_matrix_lookup.argtypes = [c_char_p]
_lib.parasail_matrix_lookup.restype = c_matrix_p

blosum100 = Matrix(_lib.parasail_matrix_lookup("blosum100"))
blosum30 = Matrix(_lib.parasail_matrix_lookup("blosum30"))
blosum35 = Matrix(_lib.parasail_matrix_lookup("blosum35"))
blosum40 = Matrix(_lib.parasail_matrix_lookup("blosum40"))
blosum45 = Matrix(_lib.parasail_matrix_lookup("blosum45"))
blosum50 = Matrix(_lib.parasail_matrix_lookup("blosum50"))
blosum55 = Matrix(_lib.parasail_matrix_lookup("blosum55"))
blosum60 = Matrix(_lib.parasail_matrix_lookup("blosum60"))
blosum62 = Matrix(_lib.parasail_matrix_lookup("blosum62"))
blosum65 = Matrix(_lib.parasail_matrix_lookup("blosum65"))
blosum70 = Matrix(_lib.parasail_matrix_lookup("blosum70"))
blosum75 = Matrix(_lib.parasail_matrix_lookup("blosum75"))
blosum80 = Matrix(_lib.parasail_matrix_lookup("blosum80"))
blosum85 = Matrix(_lib.parasail_matrix_lookup("blosum85"))
blosum90 = Matrix(_lib.parasail_matrix_lookup("blosum90"))
pam10 = Matrix(_lib.parasail_matrix_lookup("pam10"))
pam100 = Matrix(_lib.parasail_matrix_lookup("pam100"))
pam110 = Matrix(_lib.parasail_matrix_lookup("pam110"))
pam120 = Matrix(_lib.parasail_matrix_lookup("pam120"))
pam130 = Matrix(_lib.parasail_matrix_lookup("pam130"))
pam140 = Matrix(_lib.parasail_matrix_lookup("pam140"))
pam150 = Matrix(_lib.parasail_matrix_lookup("pam150"))
pam160 = Matrix(_lib.parasail_matrix_lookup("pam160"))
pam170 = Matrix(_lib.parasail_matrix_lookup("pam170"))
pam180 = Matrix(_lib.parasail_matrix_lookup("pam180"))
pam190 = Matrix(_lib.parasail_matrix_lookup("pam190"))
pam20 = Matrix(_lib.parasail_matrix_lookup("pam20"))
pam200 = Matrix(_lib.parasail_matrix_lookup("pam200"))
pam210 = Matrix(_lib.parasail_matrix_lookup("pam210"))
pam220 = Matrix(_lib.parasail_matrix_lookup("pam220"))
pam230 = Matrix(_lib.parasail_matrix_lookup("pam230"))
pam240 = Matrix(_lib.parasail_matrix_lookup("pam240"))
pam250 = Matrix(_lib.parasail_matrix_lookup("pam250"))
pam260 = Matrix(_lib.parasail_matrix_lookup("pam260"))
pam270 = Matrix(_lib.parasail_matrix_lookup("pam270"))
pam280 = Matrix(_lib.parasail_matrix_lookup("pam280"))
pam290 = Matrix(_lib.parasail_matrix_lookup("pam290"))
pam30 = Matrix(_lib.parasail_matrix_lookup("pam30"))
pam300 = Matrix(_lib.parasail_matrix_lookup("pam300"))
pam310 = Matrix(_lib.parasail_matrix_lookup("pam310"))
pam320 = Matrix(_lib.parasail_matrix_lookup("pam320"))
pam330 = Matrix(_lib.parasail_matrix_lookup("pam330"))
pam340 = Matrix(_lib.parasail_matrix_lookup("pam340"))
pam350 = Matrix(_lib.parasail_matrix_lookup("pam350"))
pam360 = Matrix(_lib.parasail_matrix_lookup("pam360"))
pam370 = Matrix(_lib.parasail_matrix_lookup("pam370"))
pam380 = Matrix(_lib.parasail_matrix_lookup("pam380"))
pam390 = Matrix(_lib.parasail_matrix_lookup("pam390"))
pam40 = Matrix(_lib.parasail_matrix_lookup("pam40"))
pam400 = Matrix(_lib.parasail_matrix_lookup("pam400"))
pam410 = Matrix(_lib.parasail_matrix_lookup("pam410"))
pam420 = Matrix(_lib.parasail_matrix_lookup("pam420"))
pam430 = Matrix(_lib.parasail_matrix_lookup("pam430"))
pam440 = Matrix(_lib.parasail_matrix_lookup("pam440"))
pam450 = Matrix(_lib.parasail_matrix_lookup("pam450"))
pam460 = Matrix(_lib.parasail_matrix_lookup("pam460"))
pam470 = Matrix(_lib.parasail_matrix_lookup("pam470"))
pam480 = Matrix(_lib.parasail_matrix_lookup("pam480"))
pam490 = Matrix(_lib.parasail_matrix_lookup("pam490"))
pam50 = Matrix(_lib.parasail_matrix_lookup("pam50"))
pam500 = Matrix(_lib.parasail_matrix_lookup("pam500"))
pam60 = Matrix(_lib.parasail_matrix_lookup("pam60"))
pam70 = Matrix(_lib.parasail_matrix_lookup("pam70"))
pam80 = Matrix(_lib.parasail_matrix_lookup("pam80"))
pam90 = Matrix(_lib.parasail_matrix_lookup("pam90"))

_lib.parasail_matrix_create.argtypes = [c_char_p, c_int, c_int]
_lib.parasail_matrix_create.restype = c_matrix_p

def matrix_create(alphabet, match, mismatch):
    return Matrix(_lib.parasail_matrix_create(alphabet, match, mismatch))

# parasail_matrix_free is not exposed.
# Memory is managed by the Matrix class.
_lib.parasail_matrix_free.argtypes = [c_matrix_p]
_lib.parasail_matrix_free.restype = None

# begin generated names here

_argtypes = [c_char_p, c_int, c_char_p, c_int, c_int, c_int, c_matrix_p]
"""

# serial reference implementations (3x2x3 = 18 impl)
alg = ["nw", "sg", "sw"]
stats = ["", "_stats"]
table = ["", "_table", "_rowcol"]
for a in alg:
    for s in stats:
        for t in table:
            print ""
            print "_lib.parasail_"+a+s+t+".argtypes = _argtypes"
            print "_lib.parasail_"+a+s+t+".restype = c_result_p"
            print "def "+a+s+t+"(s1, s2, open, extend, matrix):"
            print " "*4+"return Result(_lib.parasail_"+a+s+t+"("
            print " "*8+"s1, len(s1), s2, len(s2), open, extend, matrix))"

## serial scan reference implementations (3x2x3 = 18 impl)
alg = ["nw", "sg", "sw"]
stats = ["", "_stats"]
table = ["", "_table", "_rowcol"]
for a in alg:
    for s in stats:
        for t in table:
            print ""
            print "_lib.parasail_"+a+s+t+"_scan.argtypes = _argtypes"
            print "_lib.parasail_"+a+s+t+"_scan.restype = c_result_p"
            print "def "+a+s+t+"_scan(s1, s2, open, extend, matrix):"
            print " "*4+"return Result(_lib.parasail_"+a+s+t+"_scan("
            print " "*8+"s1, len(s1), s2, len(s2), open, extend, matrix))"

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
                    print ""
                    print "_lib.parasail_"+a+s+t+p+w+".argtypes = _argtypes"
                    print "_lib.parasail_"+a+s+t+p+w+".restype = c_result_p"
                    print "def "+a+s+t+p+w+"(s1, s2, open, extend, matrix):"
                    print " "*4+"return Result(_lib.parasail_"+a+s+t+p+w+"("
                    print " "*8+"s1, len(s1), s2, len(s2), open, extend, matrix))"

print """
_argtypes = [c_profile_p, c_char_p, c_int, c_int, c_int]
"""

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
                    print ""
                    print "_lib.parasail_"+a+s+t+p+w+".argtypes = _argtypes"
                    print "_lib.parasail_"+a+s+t+p+w+".restype = c_result_p"
                    print "def "+a+s+t+p+w+"(profile, s2, open, extend):"
                    print " "*4+"return Result(_lib.parasail_"+a+s+t+p+w+"("
                    print " "*8+"profile, s2, len(s2), open, extend))"

