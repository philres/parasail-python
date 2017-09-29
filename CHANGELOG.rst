==========
Change Log
==========

All notable changes to this project will be documented in this file.
This project adheres to Semantic Versioning (http://semver.org/).

-----------
Unreleased_
-----------
The Unreleased section will be empty for tagged releases. Unreleased functionality appears in the develop branch.

- Fix seg fault, return None if SSW emulation functions return a NULL pointer.
- Change setup.py install command to also download/build shared library.
  Previously it was only the bdist_wheel command that would do so.
- Close #10. OSError: libparasail.so: cannot open shared object file:
  No such file or directory.

-------------------
1.1.5_ - 2017-09-29
-------------------
- Add travis build.
- Add CHANGELOG.rst.
- Add Cigar decode_op() decode_len() @staticmethods
- Add bindings to the ssw emulation functions.
- Add bindings to parasail_sequences_from_file(filename).
- Add tests; use with pytest.
- Fix the integer type for ssw cigar.
- Fix the profile function return values.
- Fix the table and rowcol properties.

-------------------
1.1.4_ - 2017-09-26
-------------------
- Py 2/3 compatible long_description field.

-------------------
1.1.3_ - 2017-09-26
-------------------
- Assign README.rst to long_description field.

-------------------
1.1.2_ - 2017-09-26
-------------------
- Create a new pypi release that didn't fail like the last one did.

-------------------
1.1.1_ - 2017-09-26
-------------------
- Expanded README.rst.
- pypi upload using twine now skips existing files.

-------------------
1.1.0_ - 2017-09-26
-------------------
First tagged release. The 'master' branch always represents the latest stable code. Tagged releases correspond to pypi releases.

.. _Unreleased: https://github.com/jeffdaily/parasail-python/compare/v1.1.5...master
.. _1.1.5: https://github.com/jeffdaily/parasail-python/compare/v1.1.4...v1.1.5
.. _1.1.4: https://github.com/jeffdaily/parasail-python/compare/v1.1.3...v1.1.4
.. _1.1.3: https://github.com/jeffdaily/parasail-python/compare/v1.1.2...v1.1.3
.. _1.1.2: https://github.com/jeffdaily/parasail-python/compare/v1.1.1...v1.1.2
.. _1.1.1: https://github.com/jeffdaily/parasail-python/compare/v1.1.0...v1.1.1
.. _1.1.0: https://github.com/jeffdaily/parasail-python/releases/tag/v1.1.0

