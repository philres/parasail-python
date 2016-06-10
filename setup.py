import codecs
import os
import platform
import re
import shutil
import stat
import subprocess
import sys
import urllib
import zipfile

from setuptools import setup, Distribution


###############################################################################

NAME = "parasail"
PACKAGES = ['parasail']
META_PATH = os.path.join("parasail", "__init__.py")
KEYWORDS = ["Smith-Waterman", "Needleman-Wunsch"]
CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Science/Research",
    "Natural Language :: English",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: C",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.5",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.0",
    "Programming Language :: Python :: 3.1",
    "Programming Language :: Python :: 3.2",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
INSTALL_REQUIRES = ["numpy"]

###############################################################################

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


META_FILE = read(META_PATH)


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta),
        META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


URI = find_meta("uri")

class BinaryDistribution(Distribution):
    def is_pure(self):
        return False

def get_libname():
    libname = "libparasail.so"
    if platform.system() == "Darwin":
        libname = "libparasail.dylib"
    elif platform.system() == "Windows":
        libname = "parasail.dll"
    return libname

def unzip(archive, destdir):
    thefile=zipfile.ZipFile(archive)
    thefile.extractall(destdir)
    thefile.close()

def find_file(filename, start="."):
    for root, dirs, files in os.walk(start, topdown=False):
        for name in files:
            if name == filename:
                return root
    return None

# attempt to run parallel make with at most 8 workers
def cpu_count():
    try:
        import multiprocessing
        return min(8, multiprocessing.cpu_count())
    except:
        return 1

# unzipping parasail C library zip file does not preserve executable permissions
def fix_permissions(start):
    execmode = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    filenames = [
        "version.sh",
        "func_group_rowcols.py",
        "codegen.py",
        "satcheck.py",
        "func_group_tables.py",
        "tester.py",
        "diff_all.sh",
        "names.py",
        "dispatcher.py",
        "isastubs.py",
        "funcs.py",
        "makedef.py",
        "gap_tester.py",
        "func_groups.py",
        "configure",
        "install-sh",
        "config.sub",
        "test-driver",
        "config.guess",
        "compile",
        "missing",
        "depcomp",
        ]
    for root, dirs, files in os.walk(start, topdown=False):
        for name in files:
            if name in filenames:
                fullpath = os.path.join(root,name)
                st = os.stat(fullpath)
                os.chmod(fullpath, st.st_mode | execmode)

# Download, unzip, configure, and make parasail C library from github.
# Attempt to skip steps that may have already completed.
def build_parasail(libname):
    archive = 'parasail-master.zip'
    destdir = 'parasail-master'

    if not os.path.exists(archive):
        print("Downloading latest parasail master")
        theurl = 'https://github.com/jeffdaily/parasail/archive/master.zip'
        name,hdrs = urllib.urlretrieve(theurl, archive)
    else:
        print("Archive '{}' already downloaded".format(archive))

    if not os.path.exists(destdir):
        print("Unzipping parasail master archive")
        unzip(archive, destdir)
    else:
        print("Archive '{}' already unzipped to {}".format(archive,destdir))

    root = find_file('configure')
    if root is None:
        raise RuntimeError("Unable to find configure script")

    if not os.access(os.path.join(root,'configure'), os.X_OK):
        print("fixing executable bits after unzipping")
        fix_permissions(root)
    else:
        print("parasail archive executable permissions ok")

    if find_file('config.status') is None:
        print("configuring parasail in directory {}".format(root))
        retcode = subprocess.Popen([
            './configure',
            '--enable-shared',
            '--disable-static'
            ], cwd=root).wait()
        if 0 != retcode:
            raise RuntimeError("configure failed")
    else:
        print("parasail already configured in directory {}".format(root))

    if find_file(libname) is None:
        print("making parasail")
        retcode = subprocess.Popen([
            'make',
            '-j',
            str(cpu_count())
            ], cwd=root).wait()
        if 0 != retcode:
            raise RuntimeError("make failed")
    else:
        print("parasail library '{}' already made".format(libname))
    src = os.path.join(root, '.libs', libname)
    dst = 'parasail'
    print("copying {} to {}".format(src,dst))
    shutil.copy(src,dst)

distclass = Distribution
package_data = {}

if "bdist_wheel" in sys.argv:
    distclass = BinaryDistribution
    libname = get_libname()
    package_data = {"parasail": [libname]}
    if not os.path.exists(os.path.join("parasail", libname)):
        build_parasail(libname)
    if not os.path.exists(os.path.join("parasail", libname)):
        raise RuntimeError("Unable to find shared library {lib}.".format(lib=libname))

if __name__ == "__main__":
    setup(
        name=NAME,
        description=find_meta("description"),
        license=find_meta("license"),
        url=URI,
        version=find_meta("version"),
        author=find_meta("author"),
        author_email=find_meta("email"),
        maintainer=find_meta("author"),
        maintainer_email=find_meta("email"),
        keywords=KEYWORDS,
        packages=PACKAGES,
        package_data=package_data,
        distclass=distclass,
        zip_safe=False,
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
    )

