configmanners
=============

[![Travis](https://travis-ci.org/mozilla/configman.png?branch=master)](https://travis-ci.org/mozilla/configman)

Copyright Mozilla, 2013 - 2015

Copyright K Lars Lohn 2021

Configmanners
-------------

Making various dispart configuration methods play politely with each other.

This is a unification of several methods of passing configuration into a Python program.
The primary feature is making a consistent interface to commandline arguments,
environment variables, and configuration files. It provides a method for declarative
configuration requirements within a program and a hierarchical system to resolve
conflicts. It can dynamically load modules creating a "poor man's" dependency
injection system. In addition to its own API, it mimics the argparse API, so in many
(not all) cases, it can substitute for argparse.

_This is the K Lars Lohn fork of configman. Since I am no longer associated with Mozilla,
I have no ownership/control/privileges on the moribund Mozilla repo. I don't think Mozilla
uses it anywhere anymore. As it it critical to my personal software work, I intend
to continue to maintain and modify it for my own purposes as this fork.  This implementation 
is likely full of problems, can't-get-there-from-here situations, or other such troubles. 
There is no warranty, no guarantee, and the author is absentee._

It is highly unlikely that I will publish it as a 'pip' installable module.


Running tests (moribund)
-------------

_K Lars Lohn comment: I suspect that none of this original testing stuff is viable any more.
I have no intention of modernizing these procedures. If somebody else has, I'll accept PRs.
Until such time, I have no qualms about doing without._

We use [nose](http://code.google.com/p/python-nose/) to run all the
unit tests and [tox](http://tox.testrun.org/latest/) to test multiple
python versions. To run the whole suite just run:

    tox

`tox` will pass arguments after `--` to `nosetests`. To run with test
coverage calculation, run `tox` like this:

    tox -- --with-coverage --cover-html --cover-package=configman

If you want to run a specific test in a testcase class, though,
you might consider just using `nosetests`:

    nosetests configman.tests.test_config_manager:TestCase.test_write_flat


Making a release  (moribund)
----------------

_K Lars Lohn comment: I have no intention of releasing this product.  If someone
wants to update, I'll accept PRs. Meanwhile, I just don't care._

Because our `.travis.yml` has all the necessary information to automatically
make a release, all you need to do is to push a commit onto master.
Most likely you will only want to do this after you have
edited the `configman/version.txt` file. Suppose you make some changes:

    git add configman/configman.py
    git commit -m "fixed something"

You might want to push that to your fork and make a pull request. Then,
to update the version and make a release, first do this:

    vim configman/version.txt
    git add configman/version.txt
    git commit -m "bump to version x.y.z"
    git push origin master

After that travis, upon a successful build will automatically make a new
tarball and wheel and upload it to [PyPI](https://pypi.python.org/pypi/configman)
