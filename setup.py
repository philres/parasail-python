import codecs
import os
import platform
import re
import shutil
import stat
import subprocess
import time
try:
    from urllib import urlretrieve
except ImportError:
    from urllib.request import urlretrieve
import zipfile

from distutils.util import get_platform
from setuptools import setup
from wheel.bdist_wheel import bdist_wheel as bdist_wheel_
from setuptools.command.install import install as install_

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


def is_python_64bit():
    import struct
    return struct.calcsize('P')*8 == 64

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
        name,hdrs = urlretrieve(theurl, archive)
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

    if find_file('config.status', root) is None:
        print("configuring parasail in directory {}".format(root))
        # force universal/fat build in OSX via CFLAGS env var
        if platform.system() == "Darwin":
            os.environ['CFLAGS']="-arch x86_64 -arch i386"
        retcode = subprocess.Popen([
            './configure',
            '--enable-shared',
            '--disable-static'
            ], cwd=root).wait()
        if 0 != retcode:
            raise RuntimeError("configure failed")
    else:
        print("parasail already configured in directory {}".format(root))

    if find_file(libname, root) is None:
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

def github_api_json(address):
    import json
    import sys
    if (sys.version_info > (3, 0)):
        import urllib.request
        with urllib.request.urlopen(address) as url:
            data = json.loads(url.read().decode())
    else:
        import urllib
        response = urllib.urlopen(address)
        data = json.loads(response.read())
    return data

def download_windows_dll():
    libname = get_libname()
    libpath = os.path.join("parasail", libname)
    print("Downloading latest parasail release info from github")
    address = "https://api.github.com/repos/jeffdaily/parasail/releases/latest"
    data = None
    for attempt in range(10):
        try:
            data = github_api_json(address)
            if not data or 'assets' not in data:
                raise RuntimeError("Unable to download github asset JSON from "+address)
        except Exception as e:
            print(repr(e))
            print("Will retry in 5 seconds")
            time.sleep(5)
        else:
            break
    else:
        # we failed all the attempts - deal with the consequences.
        raise RuntimeError("All attempts to download github asset JSON have failed")
    asset = None
    search = "win32-v140"
    if is_python_64bit():
        search = "win64-v140"
    for maybe_asset in data['assets']:
        if search in maybe_asset['browser_download_url']:
            asset = maybe_asset['browser_download_url']
            break
    if not asset:
        raise RuntimeError("Unable to determine asset URL")
    print("Downloading latest parasail release {}".format(asset))
    archive = asset.rsplit('/',1)[-1]
    for attempt in range(10):
        try:
            name,hdrs = urlretrieve(asset, archive)
        except Exception as e:
            print(repr(e))
            print("Will retry in 5 seconds")
            time.sleep(5)
        else:
            break
    else:
        # we failed all the attempts - deal with the consequences.
        raise RuntimeError("All attempts to download asset URL have failed")
    destdir = archive.rsplit('.',1)[0]
    print("Unzipping {}".format(archive))
    unzip(archive, destdir)
    print("Locating {}".format(libname))
    root = find_file(libname)
    src = os.path.join(root, libname)
    dst = 'parasail'
    print("copying {} to {}".format(src,dst))
    shutil.copy(src,dst)

def prepare_shared_lib():
    libname = get_libname()
    libpath = os.path.join("parasail", libname)
    if not os.path.exists(libpath):
        print("{} not found, attempting to build".format(libpath))
        if platform.system() == "Windows":
            download_windows_dll()
        else:
            build_parasail(libname)
    if not os.path.exists(libpath):
        raise RuntimeError("Unable to find shared library {}.".format(libname))

class bdist_wheel(bdist_wheel_):
    def run(self):
        prepare_shared_lib()
        bdist_wheel_.run(self)

    def finalize_options(self):
        bdist_wheel_.finalize_options(self)
        self.universal = True
        self.plat_name_supplied = True
        self.plat_name = get_platform()

class install(install_):
    def run(self):
        prepare_shared_lib()
        install_.run(self)


if __name__ == "__main__":
    long_description = ""
    try:
        long_description = open("README.rst", encoding="utf8").read()
    except:
        long_description = open("README.rst").read()
    setup(
        name=NAME,
        description=find_meta("description"),
        long_description=long_description,
        license=find_meta("license"),
        url=URI,
        version=find_meta("version"),
        author=find_meta("author"),
        author_email=find_meta("email"),
        maintainer=find_meta("author"),
        maintainer_email=find_meta("email"),
        keywords=KEYWORDS,
        packages=PACKAGES,
        package_data={"parasail": [get_libname()]},
        cmdclass={'bdist_wheel': bdist_wheel, 'install': install},
        zip_safe=False,
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
    )

