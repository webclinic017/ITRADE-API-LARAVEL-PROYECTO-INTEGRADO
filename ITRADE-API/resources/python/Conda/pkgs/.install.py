# (c) 2012-2016 Anaconda, Inc. / https://anaconda.com
# All Rights Reserved
#
# conda is distributed under the terms of the BSD 3-clause license.
# Consult LICENSE.txt or http://opensource.org/licenses/BSD-3-Clause.
'''
We use the following conventions in this module:

    dist:        canonical package name, e.g. 'numpy-1.6.2-py26_0'

    ROOT_PREFIX: the prefix to the root environment, e.g. /opt/anaconda

    PKGS_DIR:    the "package cache directory", e.g. '/opt/anaconda/pkgs'
                 this is always equal to ROOT_PREFIX/pkgs

    prefix:      the prefix of a particular environment, which may also
                 be the root environment

Also, this module is directly invoked by the (self extracting) tarball
installer to create the initial environment, therefore it needs to be
standalone, i.e. not import any other parts of `conda` (only depend on
the standard library).
'''
import os
import re
import sys
import json
import shutil
import stat
from os.path import abspath, dirname, exists, isdir, isfile, islink, join
from optparse import OptionParser


on_win = bool(sys.platform == 'win32')
try:
    FORCE = bool(int(os.getenv('FORCE', 0)))
except ValueError:
    FORCE = False

LINK_HARD = 1
LINK_SOFT = 2  # never used during the install process
LINK_COPY = 3
link_name_map = {
    LINK_HARD: 'hard-link',
    LINK_SOFT: 'soft-link',
    LINK_COPY: 'copy',
}
SPECIAL_ASCII = '$!&\%^|{}[]<>~`"\':;?@*#'

# these may be changed in main()
ROOT_PREFIX = sys.prefix
PKGS_DIR = join(ROOT_PREFIX, 'pkgs')
SKIP_SCRIPTS = False
IDISTS = {
  "_ipyw_jlab_nb_ext_conf-0.1.0-py37_0": {
    "md5": "ad2da510ac9200a117ddaee414def1fe",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/_ipyw_jlab_nb_ext_conf-0.1.0-py37_0.tar.bz2"
  },
  "alabaster-0.7.12-py37_0": {
    "md5": "c5ab2f2e8efcb480587c948d17fbb1d5",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/alabaster-0.7.12-py37_0.tar.bz2"
  },
  "anaconda-2019.03-py37_0": {
    "md5": "60998b459d288c9484c255d32d7fdbfd",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/anaconda-2019.03-py37_0.tar.bz2"
  },
  "anaconda-client-1.7.2-py37_0": {
    "md5": "8fbd774bbe6993e1bc59d8938945ba7c",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/anaconda-client-1.7.2-py37_0.tar.bz2"
  },
  "anaconda-navigator-1.9.7-py37_0": {
    "md5": "99a054fa6ce029c99f68a716c3c89b3d",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/anaconda-navigator-1.9.7-py37_0.tar.bz2"
  },
  "anaconda-project-0.8.2-py37_0": {
    "md5": "9ada40a291e64a3a8a1a593003286dd0",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/anaconda-project-0.8.2-py37_0.tar.bz2"
  },
  "asn1crypto-0.24.0-py37_0": {
    "md5": "3a4916054f7d730b17e5d8a4343d9b59",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/asn1crypto-0.24.0-py37_0.tar.bz2"
  },
  "astroid-2.2.5-py37_0": {
    "md5": "91dcf282ac4396fb3172b19b512d899a",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/astroid-2.2.5-py37_0.tar.bz2"
  },
  "astropy-3.1.2-py37he774522_0": {
    "md5": "7c8bd2645effb3f62b6c10528dbd10f4",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/astropy-3.1.2-py37he774522_0.tar.bz2"
  },
  "atomicwrites-1.3.0-py37_1": {
    "md5": "ce1e3da20961d8352449db7c2c74a221",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/atomicwrites-1.3.0-py37_1.tar.bz2"
  },
  "attrs-19.1.0-py37_1": {
    "md5": "cbddefbd2cd97fa4f73781c79a3a4e75",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/attrs-19.1.0-py37_1.tar.bz2"
  },
  "babel-2.6.0-py37_0": {
    "md5": "2121d4826d63811ed0cd165c173a3eac",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/babel-2.6.0-py37_0.tar.bz2"
  },
  "backcall-0.1.0-py37_0": {
    "md5": "a0083ed4f8002e79c949744682e50cf9",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/backcall-0.1.0-py37_0.tar.bz2"
  },
  "backports-1.0-py37_1": {
    "md5": "42aabb3d56010d537a1254352a4df670",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/backports-1.0-py37_1.tar.bz2"
  },
  "backports.os-0.1.1-py37_0": {
    "md5": "90d2ac616dc1cf63b617696ee0f104b9",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/backports.os-0.1.1-py37_0.tar.bz2"
  },
  "backports.shutil_get_terminal_size-1.0.0-py37_2": {
    "md5": "20903a914b18f4b31d4b821c19642e0b",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/backports.shutil_get_terminal_size-1.0.0-py37_2.tar.bz2"
  },
  "beautifulsoup4-4.7.1-py37_1": {
    "md5": "b8f8429b121e59ae347d82821661e707",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/beautifulsoup4-4.7.1-py37_1.tar.bz2"
  },
  "bitarray-0.8.3-py37hfa6e2cd_0": {
    "md5": "c92ed175859add55207c786352225e44",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/bitarray-0.8.3-py37hfa6e2cd_0.tar.bz2"
  },
  "bkcharts-0.2-py37_0": {
    "md5": "8b6573180af0719bdadd49737a06c10b",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/bkcharts-0.2-py37_0.tar.bz2"
  },
  "blas-1.0-mkl": {
    "md5": "e8aa6b7daaf0925245c148aaeaa0722e",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/blas-1.0-mkl.tar.bz2"
  },
  "bleach-3.1.0-py37_0": {
    "md5": "aeb2ffbf7d850ae5908a6c65d4ee1d7b",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/bleach-3.1.0-py37_0.tar.bz2"
  },
  "blosc-1.15.0-h7bd577a_0": {
    "md5": "e1fa36f2f1a18020c385dbde9eb8c71c",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/blosc-1.15.0-h7bd577a_0.tar.bz2"
  },
  "bokeh-1.0.4-py37_0": {
    "md5": "3102e7ef0c2ae3b87fee234b7f625f8e",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/bokeh-1.0.4-py37_0.tar.bz2"
  },
  "boto-2.49.0-py37_0": {
    "md5": "eaf64d1c6abcf107ffeed0770022450b",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/boto-2.49.0-py37_0.tar.bz2"
  },
  "bottleneck-1.2.1-py37h452e1ab_1": {
    "md5": "52acb67a4e35e50de332caf2f0de38c8",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/bottleneck-1.2.1-py37h452e1ab_1.tar.bz2"
  },
  "bzip2-1.0.6-hfa6e2cd_5": {
    "md5": "b287049cca8255f5023f8fc5f0afe47d",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/bzip2-1.0.6-hfa6e2cd_5.tar.bz2"
  },
  "ca-certificates-2019.1.23-0": {
    "md5": "f51beb89e3b35de34ff33a5e652adce4",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/ca-certificates-2019.1.23-0.tar.bz2"
  },
  "certifi-2019.3.9-py37_0": {
    "md5": "5807c9c1b64980de9b0d1e9807d1a4af",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/certifi-2019.3.9-py37_0.tar.bz2"
  },
  "cffi-1.12.2-py37h7a1dbc1_1": {
    "md5": "196f869e5ba381d731c1e296c890649e",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/cffi-1.12.2-py37h7a1dbc1_1.tar.bz2"
  },
  "chardet-3.0.4-py37_1": {
    "md5": "fa614ba863adbffcc5d5d449a8a19add",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/chardet-3.0.4-py37_1.tar.bz2"
  },
  "click-7.0-py37_0": {
    "md5": "51e9c115051907a3fbe955a0dafbe967",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/click-7.0-py37_0.tar.bz2"
  },
  "cloudpickle-0.8.0-py37_0": {
    "md5": "15c77dfafa61a30cac52aea729101c32",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/cloudpickle-0.8.0-py37_0.tar.bz2"
  },
  "clyent-1.2.2-py37_1": {
    "md5": "fd6e6ad741a36b337801f5ce91a56893",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/clyent-1.2.2-py37_1.tar.bz2"
  },
  "colorama-0.4.1-py37_0": {
    "md5": "d9a9a8c0fe48c9d911da4a155a1e297b",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/colorama-0.4.1-py37_0.tar.bz2"
  },
  "comtypes-1.1.7-py37_0": {
    "md5": "6b104a8088452328ba4d62c16ace0a3a",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/comtypes-1.1.7-py37_0.tar.bz2"
  },
  "conda-4.6.11-py37_0": {
    "md5": "6ee1989302f778ba563f5df018298ba1",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/conda-4.6.11-py37_0.tar.bz2"
  },
  "conda-build-3.17.8-py37_0": {
    "md5": "026111304ad8cbda6b5126aa3e479499",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/conda-build-3.17.8-py37_0.tar.bz2"
  },
  "conda-env-2.6.0-1": {
    "md5": "0f615892c0a17b46e5619deeb0103b5b",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/conda-env-2.6.0-1.tar.bz2"
  },
  "conda-verify-3.1.1-py37_0": {
    "md5": "f37e64074b61b8ffdbf6f17c98a50331",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/conda-verify-3.1.1-py37_0.tar.bz2"
  },
  "console_shortcut-0.1.1-3": {
    "md5": "aaad91749d7bb128bd51c0df273285e6",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/console_shortcut-0.1.1-3.tar.bz2"
  },
  "contextlib2-0.5.5-py37_0": {
    "md5": "0bf1ceea8db50ad51e68879b47bba96f",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/contextlib2-0.5.5-py37_0.tar.bz2"
  },
  "cryptography-2.6.1-py37h7a1dbc1_0": {
    "md5": "672f60d49c7f231d9f5c2a2cb6041214",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/cryptography-2.6.1-py37h7a1dbc1_0.tar.bz2"
  },
  "curl-7.64.0-h2a8f88b_2": {
    "md5": "5a2b5937483842cac5adcb63c6c44a1a",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/curl-7.64.0-h2a8f88b_2.tar.bz2"
  },
  "cycler-0.10.0-py37_0": {
    "md5": "3eec141b33187571e45435262bd838d3",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/cycler-0.10.0-py37_0.tar.bz2"
  },
  "cython-0.29.6-py37ha925a31_0": {
    "md5": "d37c3bf9c1d488b2b35ecc87a5713967",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/cython-0.29.6-py37ha925a31_0.tar.bz2"
  },
  "cytoolz-0.9.0.1-py37hfa6e2cd_1": {
    "md5": "ac1c1760065021318e56d56ef49394ed",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/cytoolz-0.9.0.1-py37hfa6e2cd_1.tar.bz2"
  },
  "dask-1.1.4-py37_1": {
    "md5": "656ff5579cfb1809fc7354dc3fce56c6",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/dask-1.1.4-py37_1.tar.bz2"
  },
  "dask-core-1.1.4-py37_1": {
    "md5": "b0d11d4399c4b2e13a50ee6193c8a21a",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/dask-core-1.1.4-py37_1.tar.bz2"
  },
  "decorator-4.4.0-py37_1": {
    "md5": "b7f4606453e755788ed9f942a1d41d45",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/decorator-4.4.0-py37_1.tar.bz2"
  },
  "defusedxml-0.5.0-py37_1": {
    "md5": "403e47a3d7dc86ca8db89d8ecfc2091a",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/defusedxml-0.5.0-py37_1.tar.bz2"
  },
  "distributed-1.26.0-py37_1": {
    "md5": "c0dd94753f795d69294ced3dd23dcbca",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/distributed-1.26.0-py37_1.tar.bz2"
  },
  "docutils-0.14-py37_0": {
    "md5": "cedc22322ad349200be3ef66b1b8df43",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/docutils-0.14-py37_0.tar.bz2"
  },
  "entrypoints-0.3-py37_0": {
    "md5": "d241512c739460a48c83562e0a814808",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/entrypoints-0.3-py37_0.tar.bz2"
  },
  "et_xmlfile-1.0.1-py37_0": {
    "md5": "4d9dddc51f15d4f5b070f642cc28ed10",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/et_xmlfile-1.0.1-py37_0.tar.bz2"
  },
  "fastcache-1.0.2-py37hfa6e2cd_2": {
    "md5": "41945afbe4e44edea27728dd1f308565",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/fastcache-1.0.2-py37hfa6e2cd_2.tar.bz2"
  },
  "filelock-3.0.10-py37_0": {
    "md5": "04acec28b606e2ae76425c171f1de467",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/filelock-3.0.10-py37_0.tar.bz2"
  },
  "flask-1.0.2-py37_1": {
    "md5": "9d1ef2a65f19c18d68681c607e42af87",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/flask-1.0.2-py37_1.tar.bz2"
  },
  "freetype-2.9.1-ha9979f8_1": {
    "md5": "f3263f3249686ede2d2bea458e30e61f",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/freetype-2.9.1-ha9979f8_1.tar.bz2"
  },
  "future-0.17.1-py37_0": {
    "md5": "6c9c54e95383956acff6c8a9f2b19059",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/future-0.17.1-py37_0.tar.bz2"
  },
  "get_terminal_size-1.0.0-h38e98db_0": {
    "md5": "d97df1f48a67f30346b8df55f494e1ad",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/get_terminal_size-1.0.0-h38e98db_0.tar.bz2"
  },
  "gevent-1.4.0-py37he774522_0": {
    "md5": "1d59614230cba73ae25e5731dec738b1",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/gevent-1.4.0-py37he774522_0.tar.bz2"
  },
  "glob2-0.6-py37_1": {
    "md5": "6c46218bf5b129e45cb4465585fdf539",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/glob2-0.6-py37_1.tar.bz2"
  },
  "greenlet-0.4.15-py37hfa6e2cd_0": {
    "md5": "5a3254fd8da5ce213ce65ee1b92d5316",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/greenlet-0.4.15-py37hfa6e2cd_0.tar.bz2"
  },
  "h5py-2.9.0-py37h5e291fa_0": {
    "md5": "60cd72ab81b1eb0842df40a93ab7ce5b",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/h5py-2.9.0-py37h5e291fa_0.tar.bz2"
  },
  "hdf5-1.10.4-h7ebc959_0": {
    "md5": "de2d3c434711af9c473efc9741189816",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/hdf5-1.10.4-h7ebc959_0.tar.bz2"
  },
  "heapdict-1.0.0-py37_2": {
    "md5": "32856affe168e78b1848f5380101dc9b",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/heapdict-1.0.0-py37_2.tar.bz2"
  },
  "html5lib-1.0.1-py37_0": {
    "md5": "1b6cdb740516858bea7212be9a8c63dd",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/html5lib-1.0.1-py37_0.tar.bz2"
  },
  "icc_rt-2019.0.0-h0cc432a_1": {
    "md5": "ce2949c239b5cd45848a0a7865d30520",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/icc_rt-2019.0.0-h0cc432a_1.tar.bz2"
  },
  "icu-58.2-ha66f8fd_1": {
    "md5": "8b9a078b693623d58afd56f4f2a162c3",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/icu-58.2-ha66f8fd_1.tar.bz2"
  },
  "idna-2.8-py37_0": {
    "md5": "6afef2ec3bc9568cb43c92080008a802",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/idna-2.8-py37_0.tar.bz2"
  },
  "imageio-2.5.0-py37_0": {
    "md5": "39754992d4c62447ec5f76a4a62a3983",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/imageio-2.5.0-py37_0.tar.bz2"
  },
  "imagesize-1.1.0-py37_0": {
    "md5": "9d9b57b95dcfd7c5848fc40275a5ee35",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/imagesize-1.1.0-py37_0.tar.bz2"
  },
  "importlib_metadata-0.8-py37_0": {
    "md5": "01c9012027a2a4b7a7f4f51589b94c79",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/importlib_metadata-0.8-py37_0.tar.bz2"
  },
  "intel-openmp-2019.3-203": {
    "md5": "521484064fa841f1fe0e3ce009b12281",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/intel-openmp-2019.3-203.tar.bz2"
  },
  "ipykernel-5.1.0-py37h39e3cac_0": {
    "md5": "aaba26513406abacf583830549fab611",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/ipykernel-5.1.0-py37h39e3cac_0.tar.bz2"
  },
  "ipython-7.4.0-py37h39e3cac_0": {
    "md5": "a2424b8881a85255315ccf283a7fed20",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/ipython-7.4.0-py37h39e3cac_0.tar.bz2"
  },
  "ipython_genutils-0.2.0-py37_0": {
    "md5": "b9ccc37762257642d3c835867cf9aa88",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/ipython_genutils-0.2.0-py37_0.tar.bz2"
  },
  "ipywidgets-7.4.2-py37_0": {
    "md5": "b689f39dd2031f28225c47aaed111ca3",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/ipywidgets-7.4.2-py37_0.tar.bz2"
  },
  "isort-4.3.16-py37_0": {
    "md5": "9dc667ddcecf6585da2bf020a724255d",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/isort-4.3.16-py37_0.tar.bz2"
  },
  "itsdangerous-1.1.0-py37_0": {
    "md5": "2dd63e2ea5d5671405eb13f807482377",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/itsdangerous-1.1.0-py37_0.tar.bz2"
  },
  "jdcal-1.4-py37_0": {
    "md5": "1097cd884d93e6a86cfab89812179953",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/jdcal-1.4-py37_0.tar.bz2"
  },
  "jedi-0.13.3-py37_0": {
    "md5": "afafb3c03c00e837f84356dc3b36fc0d",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/jedi-0.13.3-py37_0.tar.bz2"
  },
  "jinja2-2.10-py37_0": {
    "md5": "2f692f463da82e93fbcfb758d777f238",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/jinja2-2.10-py37_0.tar.bz2"
  },
  "jpeg-9b-hb83a4c4_2": {
    "md5": "7abafa9f9a2c609e1b77424f5ffa6a8a",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/jpeg-9b-hb83a4c4_2.tar.bz2"
  },
  "jsonschema-3.0.1-py37_0": {
    "md5": "718e1dbad3b54924ca610e9e6b29c026",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/jsonschema-3.0.1-py37_0.tar.bz2"
  },
  "jupyter-1.0.0-py37_7": {
    "md5": "6806e2413e432237e566a914d3b7a518",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/jupyter-1.0.0-py37_7.tar.bz2"
  },
  "jupyter_client-5.2.4-py37_0": {
    "md5": "152b1baa0416bb47fe130bbab6a32373",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/jupyter_client-5.2.4-py37_0.tar.bz2"
  },
  "jupyter_console-6.0.0-py37_0": {
    "md5": "98da08955006bd1e332af5305d0970e8",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/jupyter_console-6.0.0-py37_0.tar.bz2"
  },
  "jupyter_core-4.4.0-py37_0": {
    "md5": "21781b355fa614e062f0615d5d57a141",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/jupyter_core-4.4.0-py37_0.tar.bz2"
  },
  "jupyterlab-0.35.4-py37hf63ae98_0": {
    "md5": "7cc30df7d95f2d22c456f37f704dba2b",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/jupyterlab-0.35.4-py37hf63ae98_0.tar.bz2"
  },
  "jupyterlab_server-0.2.0-py37_0": {
    "md5": "4108018ec7b82445c2156062077b8dd5",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/jupyterlab_server-0.2.0-py37_0.tar.bz2"
  },
  "keyring-18.0.0-py37_0": {
    "md5": "2f70dc005a4ec7156559267728a681b8",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/keyring-18.0.0-py37_0.tar.bz2"
  },
  "kiwisolver-1.0.1-py37h6538335_0": {
    "md5": "7d1f622f9ff7c381f7d2ca845860cd2f",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/kiwisolver-1.0.1-py37h6538335_0.tar.bz2"
  },
  "krb5-1.16.1-hc04afaa_7": {
    "md5": "f0687132c6724acfaff40d71e3a896ff",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/krb5-1.16.1-hc04afaa_7.tar.bz2"
  },
  "lazy-object-proxy-1.3.1-py37hfa6e2cd_2": {
    "md5": "dad411e571d17a8b60c6e650cc3c622b",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/lazy-object-proxy-1.3.1-py37hfa6e2cd_2.tar.bz2"
  },
  "libarchive-3.3.3-h0643e63_5": {
    "md5": "9aea3ac3665d98a485eec423aeeaf66f",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/libarchive-3.3.3-h0643e63_5.tar.bz2"
  },
  "libcurl-7.64.0-h2a8f88b_2": {
    "md5": "288fc03bf18358bf51584a54b73f6969",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/libcurl-7.64.0-h2a8f88b_2.tar.bz2"
  },
  "libiconv-1.15-h1df5818_7": {
    "md5": "cf3a121e3e744f0520d8fee6acdd2869",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/libiconv-1.15-h1df5818_7.tar.bz2"
  },
  "liblief-0.9.0-ha925a31_2": {
    "md5": "29a6c016bf60c2f51537f433d1a16af3",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/liblief-0.9.0-ha925a31_2.tar.bz2"
  },
  "libpng-1.6.36-h2a8f88b_0": {
    "md5": "bbb0e007322ca784e9021d4fa35efccc",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/libpng-1.6.36-h2a8f88b_0.tar.bz2"
  },
  "libsodium-1.0.16-h9d3ae62_0": {
    "md5": "069059358796f84bbcba9015e840d694",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/libsodium-1.0.16-h9d3ae62_0.tar.bz2"
  },
  "libssh2-1.8.0-h7a1dbc1_4": {
    "md5": "2233c15e0e9c85aea6f6f54399887637",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/libssh2-1.8.0-h7a1dbc1_4.tar.bz2"
  },
  "libtiff-4.0.10-hb898794_2": {
    "md5": "181742712383c04626ec76353dee85ba",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/libtiff-4.0.10-hb898794_2.tar.bz2"
  },
  "libxml2-2.9.9-h464c3ec_0": {
    "md5": "6ed19ec01f8b50c99b09e9134742a478",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/libxml2-2.9.9-h464c3ec_0.tar.bz2"
  },
  "libxslt-1.1.33-h579f668_0": {
    "md5": "4e42cbcd9fc9d8cda0a73bb21ffbf2c5",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/libxslt-1.1.33-h579f668_0.tar.bz2"
  },
  "llvmlite-0.28.0-py37ha925a31_0": {
    "md5": "5f3a09346ab5e039f7f1126ded4c8653",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/llvmlite-0.28.0-py37ha925a31_0.tar.bz2"
  },
  "locket-0.2.0-py37_1": {
    "md5": "50c8bd67b44a93e4b7bc659ed6307a05",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/locket-0.2.0-py37_1.tar.bz2"
  },
  "lxml-4.3.2-py37h1350720_0": {
    "md5": "ca0dc2a499f336991d8412c90382a725",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/lxml-4.3.2-py37h1350720_0.tar.bz2"
  },
  "lz4-c-1.8.1.2-h2fa13f4_0": {
    "md5": "51ac6ef55a7c1515e812d0d4693efa17",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/lz4-c-1.8.1.2-h2fa13f4_0.tar.bz2"
  },
  "lzo-2.10-h6df0209_2": {
    "md5": "df1d264574ac1767afe7aaff92aa5f15",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/lzo-2.10-h6df0209_2.tar.bz2"
  },
  "m2w64-gcc-libgfortran-5.3.0-6": {
    "md5": "de1b7f7c8221028f6bbe103df4c53bed",
    "url": "https://repo.anaconda.com/pkgs/msys2/win-64/m2w64-gcc-libgfortran-5.3.0-6.tar.bz2"
  },
  "m2w64-gcc-libs-5.3.0-7": {
    "md5": "0b9caac6747002340b057a222af705b2",
    "url": "https://repo.anaconda.com/pkgs/msys2/win-64/m2w64-gcc-libs-5.3.0-7.tar.bz2"
  },
  "m2w64-gcc-libs-core-5.3.0-7": {
    "md5": "276d396bfe8d958f71173b7134f739fa",
    "url": "https://repo.anaconda.com/pkgs/msys2/win-64/m2w64-gcc-libs-core-5.3.0-7.tar.bz2"
  },
  "m2w64-gmp-6.1.0-2": {
    "md5": "fec04371463ec68eb8f5752a22c5b030",
    "url": "https://repo.anaconda.com/pkgs/msys2/win-64/m2w64-gmp-6.1.0-2.tar.bz2"
  },
  "m2w64-libwinpthread-git-5.0.0.4634.697f757-2": {
    "md5": "67e61e700eb27424979778fae9293f13",
    "url": "https://repo.anaconda.com/pkgs/msys2/win-64/m2w64-libwinpthread-git-5.0.0.4634.697f757-2.tar.bz2"
  },
  "markupsafe-1.1.1-py37he774522_0": {
    "md5": "bbf0415dfb6f925caa625e98efd9ca97",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/markupsafe-1.1.1-py37he774522_0.tar.bz2"
  },
  "matplotlib-3.0.3-py37hc8f65d3_0": {
    "md5": "00ab40cd8cdfab91c122321f339b1af1",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/matplotlib-3.0.3-py37hc8f65d3_0.tar.bz2"
  },
  "mccabe-0.6.1-py37_1": {
    "md5": "d09148d583175973ca13fa8352c1758d",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/mccabe-0.6.1-py37_1.tar.bz2"
  },
  "menuinst-1.4.16-py37he774522_0": {
    "md5": "90c96852dd3e41ee18c7c7def9c5f26e",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/menuinst-1.4.16-py37he774522_0.tar.bz2"
  },
  "mistune-0.8.4-py37he774522_0": {
    "md5": "c76b44e5f5b9e5b08d49c1725e10d753",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/mistune-0.8.4-py37he774522_0.tar.bz2"
  },
  "mkl-2019.3-203": {
    "md5": "621018a685432c994422ca4dd2dc94f3",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/mkl-2019.3-203.tar.bz2"
  },
  "mkl-service-1.1.2-py37hb782905_5": {
    "md5": "ea952e4a2f69a7dfe6391e6e53f5ea03",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/mkl-service-1.1.2-py37hb782905_5.tar.bz2"
  },
  "mkl_fft-1.0.10-py37h14836fe_0": {
    "md5": "7ed7b58baac4318c8909465eec2bfa6a",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/mkl_fft-1.0.10-py37h14836fe_0.tar.bz2"
  },
  "mkl_random-1.0.2-py37h343c172_0": {
    "md5": "d45af154246685f482763506afd9cea0",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/mkl_random-1.0.2-py37h343c172_0.tar.bz2"
  },
  "more-itertools-6.0.0-py37_0": {
    "md5": "fe42e76ef3f1aadf7f0e28a4a24ae510",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/more-itertools-6.0.0-py37_0.tar.bz2"
  },
  "mpmath-1.1.0-py37_0": {
    "md5": "03da5b47dfa69f92bccf268e3642ee35",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/mpmath-1.1.0-py37_0.tar.bz2"
  },
  "msgpack-python-0.6.1-py37h74a9793_1": {
    "md5": "7edf8c6a3d779d03790793b1421e78e0",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/msgpack-python-0.6.1-py37h74a9793_1.tar.bz2"
  },
  "msys2-conda-epoch-20160418-1": {
    "md5": "6eaef3074f65f715ed1ca6b8a08be3aa",
    "url": "https://repo.anaconda.com/pkgs/msys2/win-64/msys2-conda-epoch-20160418-1.tar.bz2"
  },
  "multipledispatch-0.6.0-py37_0": {
    "md5": "124b4c7b6cc6b0f41c5792d130f7ba55",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/multipledispatch-0.6.0-py37_0.tar.bz2"
  },
  "navigator-updater-0.2.1-py37_0": {
    "md5": "d053b0a5b8cd865863dd88f0e56d7861",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/navigator-updater-0.2.1-py37_0.tar.bz2"
  },
  "nbconvert-5.4.1-py37_3": {
    "md5": "850a43214885c04d57063b25ebc0edb7",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/nbconvert-5.4.1-py37_3.tar.bz2"
  },
  "nbformat-4.4.0-py37_0": {
    "md5": "fcb1fb9c57d91232d61c373ca0b08a62",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/nbformat-4.4.0-py37_0.tar.bz2"
  },
  "networkx-2.2-py37_1": {
    "md5": "a27d603be5bd1bf858ee888a62b8d9f0",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/networkx-2.2-py37_1.tar.bz2"
  },
  "nltk-3.4-py37_1": {
    "md5": "b946b4125d9c45aad29253d94f9bd407",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/nltk-3.4-py37_1.tar.bz2"
  },
  "nose-1.3.7-py37_2": {
    "md5": "000fd4177399fea7b6cac1831d55605c",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/nose-1.3.7-py37_2.tar.bz2"
  },
  "notebook-5.7.8-py37_0": {
    "md5": "7ad49bf27730230d5d4ed98471b86c43",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/notebook-5.7.8-py37_0.tar.bz2"
  },
  "numba-0.43.1-py37hf9181ef_0": {
    "md5": "31cd47226f598e360b770161c870cbef",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/numba-0.43.1-py37hf9181ef_0.tar.bz2"
  },
  "numexpr-2.6.9-py37hdce8814_0": {
    "md5": "17099f5c336cb388d5a306b1f2c85a26",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/numexpr-2.6.9-py37hdce8814_0.tar.bz2"
  },
  "numpy-1.16.2-py37h19fb1c0_0": {
    "md5": "64118f6bf157d1039396e60aac8f214f",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/numpy-1.16.2-py37h19fb1c0_0.tar.bz2"
  },
  "numpy-base-1.16.2-py37hc3f5095_0": {
    "md5": "0f54e2eed0ed80e0733a02b5a0e6442b",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/numpy-base-1.16.2-py37hc3f5095_0.tar.bz2"
  },
  "numpydoc-0.8.0-py37_0": {
    "md5": "122cd189812992856af010465c5e8bb2",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/numpydoc-0.8.0-py37_0.tar.bz2"
  },
  "olefile-0.46-py37_0": {
    "md5": "1b98cdb7836ace32e351cbb9e497934d",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/olefile-0.46-py37_0.tar.bz2"
  },
  "openpyxl-2.6.1-py37_1": {
    "md5": "2f18cd0433b609e48d12d03c583fc612",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/openpyxl-2.6.1-py37_1.tar.bz2"
  },
  "openssl-1.1.1b-he774522_1": {
    "md5": "de52a7d28c27da8e682a1810d4616c52",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/openssl-1.1.1b-he774522_1.tar.bz2"
  },
  "packaging-19.0-py37_0": {
    "md5": "a43d097385e8bbbcaff64053ea185f5f",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/packaging-19.0-py37_0.tar.bz2"
  },
  "pandas-0.24.2-py37ha925a31_0": {
    "md5": "4cb3552d1ff22a1fd76c2cf9bbc53f24",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pandas-0.24.2-py37ha925a31_0.tar.bz2"
  },
  "pandoc-2.2.3.2-0": {
    "md5": "d1b05fec62c52d7ba554dc0515898f92",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pandoc-2.2.3.2-0.tar.bz2"
  },
  "pandocfilters-1.4.2-py37_1": {
    "md5": "eac47f0391172a63533ec85dec6e4371",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pandocfilters-1.4.2-py37_1.tar.bz2"
  },
  "parso-0.3.4-py37_0": {
    "md5": "e9505bb9e79de4b054320544fcf95354",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/parso-0.3.4-py37_0.tar.bz2"
  },
  "partd-0.3.10-py37_1": {
    "md5": "615314a16f4ceb355aac772e56693c4b",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/partd-0.3.10-py37_1.tar.bz2"
  },
  "path.py-11.5.0-py37_0": {
    "md5": "c567c52bb20f585d9429b7d3c7955c0e",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/path.py-11.5.0-py37_0.tar.bz2"
  },
  "pathlib2-2.3.3-py37_0": {
    "md5": "cadf63895b813e6dac791090158f0d2b",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pathlib2-2.3.3-py37_0.tar.bz2"
  },
  "patsy-0.5.1-py37_0": {
    "md5": "5187a6c6d89dcb73fbe4d0de70b8caa7",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/patsy-0.5.1-py37_0.tar.bz2"
  },
  "pep8-1.7.1-py37_0": {
    "md5": "6a62532d438643adc77081e125d80d18",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pep8-1.7.1-py37_0.tar.bz2"
  },
  "pickleshare-0.7.5-py37_0": {
    "md5": "b0eebf28454bd73122df899fc9d15007",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pickleshare-0.7.5-py37_0.tar.bz2"
  },
  "pillow-5.4.1-py37hdc69c19_0": {
    "md5": "7d1e3f42f9605c7d86c9f2ed3a7b9f13",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pillow-5.4.1-py37hdc69c19_0.tar.bz2"
  },
  "pip-19.0.3-py37_0": {
    "md5": "1f21b49908e49809c4c599bcbf7675ed",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pip-19.0.3-py37_0.tar.bz2"
  },
  "pkginfo-1.5.0.1-py37_0": {
    "md5": "39eb398b9bef8c151886d9b791258a02",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pkginfo-1.5.0.1-py37_0.tar.bz2"
  },
  "pluggy-0.9.0-py37_0": {
    "md5": "260e6a458109f2c5a22a11237610df3e",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pluggy-0.9.0-py37_0.tar.bz2"
  },
  "ply-3.11-py37_0": {
    "md5": "2ee3d063a971324a4506e3d0b6e1ff62",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/ply-3.11-py37_0.tar.bz2"
  },
  "powershell_shortcut-0.0.1-2": {
    "md5": "6f70b49b7c7ce51e3fdce9256f4fd83c",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/powershell_shortcut-0.0.1-2.tar.bz2"
  },
  "prometheus_client-0.6.0-py37_0": {
    "md5": "204d3097fa30d3f3d2edcc5a4dcf1e25",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/prometheus_client-0.6.0-py37_0.tar.bz2"
  },
  "prompt_toolkit-2.0.9-py37_0": {
    "md5": "2c29d664e96ccc8b9c68832d6bb76dcd",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/prompt_toolkit-2.0.9-py37_0.tar.bz2"
  },
  "psutil-5.6.1-py37he774522_0": {
    "md5": "4e40674e48b6b1573b3998911455a307",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/psutil-5.6.1-py37he774522_0.tar.bz2"
  },
  "py-1.8.0-py37_0": {
    "md5": "f9af1860237198385801bef9a537fba8",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/py-1.8.0-py37_0.tar.bz2"
  },
  "py-lief-0.9.0-py37ha925a31_2": {
    "md5": "01c5d30790652d042b4eb44e0a54705a",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/py-lief-0.9.0-py37ha925a31_2.tar.bz2"
  },
  "pycodestyle-2.5.0-py37_0": {
    "md5": "0c66c550c90b58f597893d34b482f8c8",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pycodestyle-2.5.0-py37_0.tar.bz2"
  },
  "pycosat-0.6.3-py37hfa6e2cd_0": {
    "md5": "0286cada8369b363e53969d840b58f27",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pycosat-0.6.3-py37hfa6e2cd_0.tar.bz2"
  },
  "pycparser-2.19-py37_0": {
    "md5": "0cd552bb636e7933b51d0acef7a03304",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pycparser-2.19-py37_0.tar.bz2"
  },
  "pycrypto-2.6.1-py37hfa6e2cd_9": {
    "md5": "28a89dbaf9ddc6cb9e48e71d6f2e4cf5",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pycrypto-2.6.1-py37hfa6e2cd_9.tar.bz2"
  },
  "pycurl-7.43.0.2-py37h7a1dbc1_0": {
    "md5": "e6e8aa563e10043b9f1b6c32f35d560f",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pycurl-7.43.0.2-py37h7a1dbc1_0.tar.bz2"
  },
  "pyflakes-2.1.1-py37_0": {
    "md5": "b70d0567ec0de2fde43f651fab338714",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pyflakes-2.1.1-py37_0.tar.bz2"
  },
  "pygments-2.3.1-py37_0": {
    "md5": "50e2bb6219b28321cba27b10ce36e5a6",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pygments-2.3.1-py37_0.tar.bz2"
  },
  "pylint-2.3.1-py37_0": {
    "md5": "d924f8cd8b074e537a133365eee2c468",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pylint-2.3.1-py37_0.tar.bz2"
  },
  "pyodbc-4.0.26-py37ha925a31_0": {
    "md5": "af4459ac87a3f64f33e81e83c94e8c16",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pyodbc-4.0.26-py37ha925a31_0.tar.bz2"
  },
  "pyopenssl-19.0.0-py37_0": {
    "md5": "c5d8afb5521012da459f88b62e0dfcc7",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pyopenssl-19.0.0-py37_0.tar.bz2"
  },
  "pyparsing-2.3.1-py37_0": {
    "md5": "0511c37da6e2d2ec5d540b8c4f608bb9",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pyparsing-2.3.1-py37_0.tar.bz2"
  },
  "pyqt-5.9.2-py37h6538335_2": {
    "md5": "e6802caccb172f1d7e5a9ba855050085",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pyqt-5.9.2-py37h6538335_2.tar.bz2"
  },
  "pyreadline-2.1-py37_1": {
    "md5": "ad6e2a3e2e7eebb38cf66aeb27d73afd",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pyreadline-2.1-py37_1.tar.bz2"
  },
  "pyrsistent-0.14.11-py37he774522_0": {
    "md5": "4d010d7a5bf53659e72b095f9f2a0953",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pyrsistent-0.14.11-py37he774522_0.tar.bz2"
  },
  "pysocks-1.6.8-py37_0": {
    "md5": "dc3eb2cfe5f40ca5984fe7164c8e312b",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pysocks-1.6.8-py37_0.tar.bz2"
  },
  "pytables-3.5.1-py37h1da0976_0": {
    "md5": "f7bf5b7009cfc572956c52dd8aa9ceef",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pytables-3.5.1-py37h1da0976_0.tar.bz2"
  },
  "pytest-4.3.1-py37_0": {
    "md5": "3a0884a0c08bb7c364cbb627c9c37857",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pytest-4.3.1-py37_0.tar.bz2"
  },
  "pytest-arraydiff-0.3-py37h39e3cac_0": {
    "md5": "c6eed2d584ecae0cdc4aa14d10932e67",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pytest-arraydiff-0.3-py37h39e3cac_0.tar.bz2"
  },
  "pytest-astropy-0.5.0-py37_0": {
    "md5": "2f92d9dfd76b9aab46f841b407ca6382",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pytest-astropy-0.5.0-py37_0.tar.bz2"
  },
  "pytest-doctestplus-0.3.0-py37_0": {
    "md5": "f99897243f7ba4ed817ebe5da8dbec4f",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pytest-doctestplus-0.3.0-py37_0.tar.bz2"
  },
  "pytest-openfiles-0.3.2-py37_0": {
    "md5": "001cf095d393ae175bb9c681666b4fae",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pytest-openfiles-0.3.2-py37_0.tar.bz2"
  },
  "pytest-remotedata-0.3.1-py37_0": {
    "md5": "c90ef40fd23ee3932a0b828451c1f904",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pytest-remotedata-0.3.1-py37_0.tar.bz2"
  },
  "python-3.7.3-h8c8aaf0_0": {
    "md5": "ac23bd1b28dea675e56ca62e5f76a68f",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/python-3.7.3-h8c8aaf0_0.tar.bz2"
  },
  "python-dateutil-2.8.0-py37_0": {
    "md5": "53b54049965b8e0f0c1eed2e240fab86",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/python-dateutil-2.8.0-py37_0.tar.bz2"
  },
  "python-libarchive-c-2.8-py37_6": {
    "md5": "cbe9433eb088a66b1e2954cb8879de68",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/python-libarchive-c-2.8-py37_6.tar.bz2"
  },
  "pytz-2018.9-py37_0": {
    "md5": "3307cf0dd41c2e02039bfc1a8bd87447",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pytz-2018.9-py37_0.tar.bz2"
  },
  "pywavelets-1.0.2-py37h8c2d366_0": {
    "md5": "68c5fe9202fc1587acfd1f6cb1c4c017",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pywavelets-1.0.2-py37h8c2d366_0.tar.bz2"
  },
  "pywin32-223-py37hfa6e2cd_1": {
    "md5": "f109e28513833e67c4e0ef4a5cdb9cae",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pywin32-223-py37hfa6e2cd_1.tar.bz2"
  },
  "pywinpty-0.5.5-py37_1000": {
    "md5": "f9edbe0e1e6795367580e93e9fa60d5a",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pywinpty-0.5.5-py37_1000.tar.bz2"
  },
  "pyyaml-5.1-py37he774522_0": {
    "md5": "24b28824a430d0ed794899b6730b6e23",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pyyaml-5.1-py37he774522_0.tar.bz2"
  },
  "pyzmq-18.0.0-py37ha925a31_0": {
    "md5": "149cd3887896fb08609ea872f58d0882",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/pyzmq-18.0.0-py37ha925a31_0.tar.bz2"
  },
  "qt-5.9.7-vc14h73c81de_0": {
    "md5": "2c80f3edd65223da2062f84292c9eac9",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/qt-5.9.7-vc14h73c81de_0.tar.bz2"
  },
  "qtawesome-0.5.7-py37_1": {
    "md5": "a5be71a10baf74b4c6bbbddbd173580b",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/qtawesome-0.5.7-py37_1.tar.bz2"
  },
  "qtconsole-4.4.3-py37_0": {
    "md5": "db38579da468a1331eb79cf0b21bb821",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/qtconsole-4.4.3-py37_0.tar.bz2"
  },
  "qtpy-1.7.0-py37_1": {
    "md5": "7bb34b3e224d0a6acbe5ee6ee1f045f6",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/qtpy-1.7.0-py37_1.tar.bz2"
  },
  "requests-2.21.0-py37_0": {
    "md5": "277e7d78bf4ea9fc5812f6b345b13c87",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/requests-2.21.0-py37_0.tar.bz2"
  },
  "rope-0.12.0-py37_0": {
    "md5": "60c202db994d7d76bd17ab454056a9d8",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/rope-0.12.0-py37_0.tar.bz2"
  },
  "ruamel_yaml-0.15.46-py37hfa6e2cd_0": {
    "md5": "163e6e1230812be0d46c0b8a0e1734ff",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/ruamel_yaml-0.15.46-py37hfa6e2cd_0.tar.bz2"
  },
  "scikit-image-0.14.2-py37ha925a31_0": {
    "md5": "db8a8ee5af25dbd50aefae7b55675061",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/scikit-image-0.14.2-py37ha925a31_0.tar.bz2"
  },
  "scikit-learn-0.20.3-py37h343c172_0": {
    "md5": "29d812b77563c729b63080f8bdf80a28",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/scikit-learn-0.20.3-py37h343c172_0.tar.bz2"
  },
  "scipy-1.2.1-py37h29ff71c_0": {
    "md5": "fae54ecf33fbb4c9bee7d42e41bcb915",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/scipy-1.2.1-py37h29ff71c_0.tar.bz2"
  },
  "seaborn-0.9.0-py37_0": {
    "md5": "54e8660d9286b4724af1262886b6a08c",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/seaborn-0.9.0-py37_0.tar.bz2"
  },
  "send2trash-1.5.0-py37_0": {
    "md5": "6650dc9abf3b4d7c2722c83d952de4f9",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/send2trash-1.5.0-py37_0.tar.bz2"
  },
  "setuptools-40.8.0-py37_0": {
    "md5": "bc0e88cf20342714d752f05240cdba0a",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/setuptools-40.8.0-py37_0.tar.bz2"
  },
  "simplegeneric-0.8.1-py37_2": {
    "md5": "83c3c21d9bdeb3a060027efaf6801e93",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/simplegeneric-0.8.1-py37_2.tar.bz2"
  },
  "singledispatch-3.4.0.3-py37_0": {
    "md5": "cfb78c738d939cfb19045f07037007ac",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/singledispatch-3.4.0.3-py37_0.tar.bz2"
  },
  "sip-4.19.8-py37h6538335_0": {
    "md5": "bc320ab7c6c8c8562913a06c5646aaa5",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/sip-4.19.8-py37h6538335_0.tar.bz2"
  },
  "six-1.12.0-py37_0": {
    "md5": "f5721c7381878ad9882026f356f5233a",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/six-1.12.0-py37_0.tar.bz2"
  },
  "snappy-1.1.7-h777316e_3": {
    "md5": "ea5b218d4285511d48a0515b88979123",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/snappy-1.1.7-h777316e_3.tar.bz2"
  },
  "snowballstemmer-1.2.1-py37_0": {
    "md5": "2a4beab37306767772479bca86ec5b63",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/snowballstemmer-1.2.1-py37_0.tar.bz2"
  },
  "sortedcollections-1.1.2-py37_0": {
    "md5": "d96ecf2a35393f714d4fc5f8aa9fec9b",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/sortedcollections-1.1.2-py37_0.tar.bz2"
  },
  "sortedcontainers-2.1.0-py37_0": {
    "md5": "a02b57b8cb003940e0f16bd9d229e67f",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/sortedcontainers-2.1.0-py37_0.tar.bz2"
  },
  "soupsieve-1.8-py37_0": {
    "md5": "2b1a802618fe1017fc896066e3af03db",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/soupsieve-1.8-py37_0.tar.bz2"
  },
  "sphinx-1.8.5-py37_0": {
    "md5": "8e01f419eac9c5783d335e99b416ca9d",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/sphinx-1.8.5-py37_0.tar.bz2"
  },
  "sphinxcontrib-1.0-py37_1": {
    "md5": "16efb04fdb575537dbf5525133f8361a",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/sphinxcontrib-1.0-py37_1.tar.bz2"
  },
  "sphinxcontrib-websupport-1.1.0-py37_1": {
    "md5": "88baf0f12027ceff5aa58a43879e9251",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/sphinxcontrib-websupport-1.1.0-py37_1.tar.bz2"
  },
  "spyder-3.3.3-py37_0": {
    "md5": "e708098048caec76c4f7df9afc73292c",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/spyder-3.3.3-py37_0.tar.bz2"
  },
  "spyder-kernels-0.4.2-py37_0": {
    "md5": "3ae1c096ed866c0f9aec695b2203ac63",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/spyder-kernels-0.4.2-py37_0.tar.bz2"
  },
  "sqlalchemy-1.3.1-py37he774522_0": {
    "md5": "0b48bd57a0fbb046a20fb6afc49023ba",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/sqlalchemy-1.3.1-py37he774522_0.tar.bz2"
  },
  "sqlite-3.27.2-he774522_0": {
    "md5": "7706950b659147fc9180d254d48ac9c8",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/sqlite-3.27.2-he774522_0.tar.bz2"
  },
  "statsmodels-0.9.0-py37h452e1ab_0": {
    "md5": "4008678e11364f65da20c3f75bd7195d",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/statsmodels-0.9.0-py37h452e1ab_0.tar.bz2"
  },
  "sympy-1.3-py37_0": {
    "md5": "0f82e0de3a83b1e9e311621a603e9d2e",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/sympy-1.3-py37_0.tar.bz2"
  },
  "tblib-1.3.2-py37_0": {
    "md5": "0ee6929e4adc51ccc4ac253aaf896b5f",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/tblib-1.3.2-py37_0.tar.bz2"
  },
  "terminado-0.8.1-py37_1": {
    "md5": "dc0b2974851a7dffc71fe3e4b8c4560f",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/terminado-0.8.1-py37_1.tar.bz2"
  },
  "testpath-0.4.2-py37_0": {
    "md5": "205374350c93cfb6ac715422cc516db6",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/testpath-0.4.2-py37_0.tar.bz2"
  },
  "tk-8.6.8-hfa6e2cd_0": {
    "md5": "13cd026af1b90010901b7339bf19c35a",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/tk-8.6.8-hfa6e2cd_0.tar.bz2"
  },
  "toolz-0.9.0-py37_0": {
    "md5": "5832102c7a0f86855b146667d9794f23",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/toolz-0.9.0-py37_0.tar.bz2"
  },
  "tornado-6.0.2-py37he774522_0": {
    "md5": "816f0be83d19203e32d5034288e44fe9",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/tornado-6.0.2-py37he774522_0.tar.bz2"
  },
  "tqdm-4.31.1-py37_1": {
    "md5": "985a4d693a96d49946029e7ba3dc2b8d",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/tqdm-4.31.1-py37_1.tar.bz2"
  },
  "traitlets-4.3.2-py37_0": {
    "md5": "7d4582d8f5164c5cf3e1fbb6bd859e8d",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/traitlets-4.3.2-py37_0.tar.bz2"
  },
  "unicodecsv-0.14.1-py37_0": {
    "md5": "e29db768d321af2ae1ab5e12b75fb3ad",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/unicodecsv-0.14.1-py37_0.tar.bz2"
  },
  "urllib3-1.24.1-py37_0": {
    "md5": "a644bdbbec23fbd8356d8aedd299a33a",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/urllib3-1.24.1-py37_0.tar.bz2"
  },
  "vc-14.1-h0510ff6_4": {
    "md5": "00bfe39f46f67409a376939cd2ab5039",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/vc-14.1-h0510ff6_4.tar.bz2"
  },
  "vs2015_runtime-14.15.26706-h3a45250_0": {
    "md5": "6a9e60c0d113a7d1e9f72c38e4f6c05d",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/vs2015_runtime-14.15.26706-h3a45250_0.tar.bz2"
  },
  "wcwidth-0.1.7-py37_0": {
    "md5": "7537d6f2374b6da32906c00d4c595bc4",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/wcwidth-0.1.7-py37_0.tar.bz2"
  },
  "webencodings-0.5.1-py37_1": {
    "md5": "9183f6d094790f77027304d9e4bd080b",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/webencodings-0.5.1-py37_1.tar.bz2"
  },
  "werkzeug-0.14.1-py37_0": {
    "md5": "35f7581220bcbce2b7f4076470787b16",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/werkzeug-0.14.1-py37_0.tar.bz2"
  },
  "wheel-0.33.1-py37_0": {
    "md5": "a914a982bdd7eae517b761583f8d8527",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/wheel-0.33.1-py37_0.tar.bz2"
  },
  "widgetsnbextension-3.4.2-py37_0": {
    "md5": "bf740e10a3667d34ed832dab9babc3a5",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/widgetsnbextension-3.4.2-py37_0.tar.bz2"
  },
  "win_inet_pton-1.1.0-py37_0": {
    "md5": "4ec69295c06d6bb5d7735b98ecb393e6",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/win_inet_pton-1.1.0-py37_0.tar.bz2"
  },
  "win_unicode_console-0.5-py37_0": {
    "md5": "804103f94133d23f85f325f33df15d9e",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/win_unicode_console-0.5-py37_0.tar.bz2"
  },
  "wincertstore-0.2-py37_0": {
    "md5": "0418cf653523e6ef0174c259efaa78b4",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/wincertstore-0.2-py37_0.tar.bz2"
  },
  "winpty-0.4.3-4": {
    "md5": "c5bdb727945bad906d23e44199144746",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/winpty-0.4.3-4.tar.bz2"
  },
  "wrapt-1.11.1-py37he774522_0": {
    "md5": "77e5e3d8cad07e9d3016447f82ce8489",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/wrapt-1.11.1-py37he774522_0.tar.bz2"
  },
  "xlrd-1.2.0-py37_0": {
    "md5": "36d44771689dd30b02cf14b66c9ffcdd",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/xlrd-1.2.0-py37_0.tar.bz2"
  },
  "xlsxwriter-1.1.5-py37_0": {
    "md5": "cd422d4594d844b6bff46f389781899c",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/xlsxwriter-1.1.5-py37_0.tar.bz2"
  },
  "xlwings-0.15.4-py37_0": {
    "md5": "8259e82f9077514a17a3e4a8413e10d2",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/xlwings-0.15.4-py37_0.tar.bz2"
  },
  "xlwt-1.3.0-py37_0": {
    "md5": "6bbc3c341f052b279981adeea955c162",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/xlwt-1.3.0-py37_0.tar.bz2"
  },
  "xz-5.2.4-h2fa13f4_4": {
    "md5": "4d85f36274b4d66be67bb1fffd81613f",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/xz-5.2.4-h2fa13f4_4.tar.bz2"
  },
  "yaml-0.1.7-hc54c509_2": {
    "md5": "eaeee418b8ac33d392ea03bb9b6f389d",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/yaml-0.1.7-hc54c509_2.tar.bz2"
  },
  "zeromq-4.3.1-h33f27b4_3": {
    "md5": "74ee385a0ce9d7e352da6a3e4b1c4083",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/zeromq-4.3.1-h33f27b4_3.tar.bz2"
  },
  "zict-0.1.4-py37_0": {
    "md5": "be243b3536a1dff5b6dab8d8111a3b53",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/zict-0.1.4-py37_0.tar.bz2"
  },
  "zipp-0.3.3-py37_1": {
    "md5": "18fb6d4e34fdd0cb78a88dd39201b1c9",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/zipp-0.3.3-py37_1.tar.bz2"
  },
  "zlib-1.2.11-h62dcd97_3": {
    "md5": "6f96fd91475cc78aabf76d2e1a9ed91f",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/zlib-1.2.11-h62dcd97_3.tar.bz2"
  },
  "zstd-1.3.7-h508b16e_0": {
    "md5": "251803bb127a0b26ee8c92106d3ab1ae",
    "url": "https://repo.anaconda.com/pkgs/main/win-64/zstd-1.3.7-h508b16e_0.tar.bz2"
  }
}
C_ENVS = {
  "root": [
    "python-3.7.3-h8c8aaf0_0",
    "conda-env-2.6.0-1",
    "blas-1.0-mkl",
    "ca-certificates-2019.1.23-0",
    "icc_rt-2019.0.0-h0cc432a_1",
    "intel-openmp-2019.3-203",
    "msys2-conda-epoch-20160418-1",
    "pandoc-2.2.3.2-0",
    "vs2015_runtime-14.15.26706-h3a45250_0",
    "winpty-0.4.3-4",
    "m2w64-gmp-6.1.0-2",
    "m2w64-libwinpthread-git-5.0.0.4634.697f757-2",
    "mkl-2019.3-203",
    "vc-14.1-h0510ff6_4",
    "bzip2-1.0.6-hfa6e2cd_5",
    "icu-58.2-ha66f8fd_1",
    "jpeg-9b-hb83a4c4_2",
    "libiconv-1.15-h1df5818_7",
    "liblief-0.9.0-ha925a31_2",
    "libsodium-1.0.16-h9d3ae62_0",
    "lz4-c-1.8.1.2-h2fa13f4_0",
    "lzo-2.10-h6df0209_2",
    "m2w64-gcc-libs-core-5.3.0-7",
    "openssl-1.1.1b-he774522_1",
    "snappy-1.1.7-h777316e_3",
    "sqlite-3.27.2-he774522_0",
    "tk-8.6.8-hfa6e2cd_0",
    "xz-5.2.4-h2fa13f4_4",
    "yaml-0.1.7-hc54c509_2",
    "zlib-1.2.11-h62dcd97_3",
    "blosc-1.15.0-h7bd577a_0",
    "hdf5-1.10.4-h7ebc959_0",
    "krb5-1.16.1-hc04afaa_7",
    "libpng-1.6.36-h2a8f88b_0",
    "libssh2-1.8.0-h7a1dbc1_4",
    "libxml2-2.9.9-h464c3ec_0",
    "m2w64-gcc-libgfortran-5.3.0-6",
    "zeromq-4.3.1-h33f27b4_3",
    "zstd-1.3.7-h508b16e_0",
    "freetype-2.9.1-ha9979f8_1",
    "libarchive-3.3.3-h0643e63_5",
    "libcurl-7.64.0-h2a8f88b_2",
    "libtiff-4.0.10-hb898794_2",
    "libxslt-1.1.33-h579f668_0",
    "m2w64-gcc-libs-5.3.0-7",
    "pywin32-223-py37hfa6e2cd_1",
    "qt-5.9.7-vc14h73c81de_0",
    "curl-7.64.0-h2a8f88b_2",
    "menuinst-1.4.16-py37he774522_0",
    "alabaster-0.7.12-py37_0",
    "asn1crypto-0.24.0-py37_0",
    "atomicwrites-1.3.0-py37_1",
    "attrs-19.1.0-py37_1",
    "backcall-0.1.0-py37_0",
    "backports-1.0-py37_1",
    "bitarray-0.8.3-py37hfa6e2cd_0",
    "boto-2.49.0-py37_0",
    "certifi-2019.3.9-py37_0",
    "chardet-3.0.4-py37_1",
    "click-7.0-py37_0",
    "cloudpickle-0.8.0-py37_0",
    "colorama-0.4.1-py37_0",
    "comtypes-1.1.7-py37_0",
    "console_shortcut-0.1.1-3",
    "contextlib2-0.5.5-py37_0",
    "dask-core-1.1.4-py37_1",
    "decorator-4.4.0-py37_1",
    "defusedxml-0.5.0-py37_1",
    "docutils-0.14-py37_0",
    "entrypoints-0.3-py37_0",
    "et_xmlfile-1.0.1-py37_0",
    "fastcache-1.0.2-py37hfa6e2cd_2",
    "filelock-3.0.10-py37_0",
    "future-0.17.1-py37_0",
    "glob2-0.6-py37_1",
    "greenlet-0.4.15-py37hfa6e2cd_0",
    "heapdict-1.0.0-py37_2",
    "idna-2.8-py37_0",
    "imagesize-1.1.0-py37_0",
    "ipython_genutils-0.2.0-py37_0",
    "itsdangerous-1.1.0-py37_0",
    "jdcal-1.4-py37_0",
    "kiwisolver-1.0.1-py37h6538335_0",
    "lazy-object-proxy-1.3.1-py37hfa6e2cd_2",
    "llvmlite-0.28.0-py37ha925a31_0",
    "locket-0.2.0-py37_1",
    "lxml-4.3.2-py37h1350720_0",
    "markupsafe-1.1.1-py37he774522_0",
    "mccabe-0.6.1-py37_1",
    "mistune-0.8.4-py37he774522_0",
    "mkl-service-1.1.2-py37hb782905_5",
    "more-itertools-6.0.0-py37_0",
    "mpmath-1.1.0-py37_0",
    "msgpack-python-0.6.1-py37h74a9793_1",
    "numpy-base-1.16.2-py37hc3f5095_0",
    "olefile-0.46-py37_0",
    "pandocfilters-1.4.2-py37_1",
    "parso-0.3.4-py37_0",
    "pep8-1.7.1-py37_0",
    "pickleshare-0.7.5-py37_0",
    "pkginfo-1.5.0.1-py37_0",
    "pluggy-0.9.0-py37_0",
    "ply-3.11-py37_0",
    "powershell_shortcut-0.0.1-2",
    "prometheus_client-0.6.0-py37_0",
    "psutil-5.6.1-py37he774522_0",
    "py-1.8.0-py37_0",
    "py-lief-0.9.0-py37ha925a31_2",
    "pycodestyle-2.5.0-py37_0",
    "pycosat-0.6.3-py37hfa6e2cd_0",
    "pycparser-2.19-py37_0",
    "pycrypto-2.6.1-py37hfa6e2cd_9",
    "pycurl-7.43.0.2-py37h7a1dbc1_0",
    "pyflakes-2.1.1-py37_0",
    "pyodbc-4.0.26-py37ha925a31_0",
    "pyparsing-2.3.1-py37_0",
    "pyreadline-2.1-py37_1",
    "python-libarchive-c-2.8-py37_6",
    "pytz-2018.9-py37_0",
    "pywinpty-0.5.5-py37_1000",
    "pyyaml-5.1-py37he774522_0",
    "pyzmq-18.0.0-py37ha925a31_0",
    "qtpy-1.7.0-py37_1",
    "rope-0.12.0-py37_0",
    "ruamel_yaml-0.15.46-py37hfa6e2cd_0",
    "send2trash-1.5.0-py37_0",
    "simplegeneric-0.8.1-py37_2",
    "sip-4.19.8-py37h6538335_0",
    "six-1.12.0-py37_0",
    "snowballstemmer-1.2.1-py37_0",
    "sortedcontainers-2.1.0-py37_0",
    "soupsieve-1.8-py37_0",
    "sphinxcontrib-1.0-py37_1",
    "sqlalchemy-1.3.1-py37he774522_0",
    "tblib-1.3.2-py37_0",
    "testpath-0.4.2-py37_0",
    "toolz-0.9.0-py37_0",
    "tornado-6.0.2-py37he774522_0",
    "tqdm-4.31.1-py37_1",
    "unicodecsv-0.14.1-py37_0",
    "wcwidth-0.1.7-py37_0",
    "webencodings-0.5.1-py37_1",
    "werkzeug-0.14.1-py37_0",
    "win_inet_pton-1.1.0-py37_0",
    "win_unicode_console-0.5-py37_0",
    "wincertstore-0.2-py37_0",
    "wrapt-1.11.1-py37he774522_0",
    "xlrd-1.2.0-py37_0",
    "xlsxwriter-1.1.5-py37_0",
    "xlwt-1.3.0-py37_0",
    "zipp-0.3.3-py37_1",
    "babel-2.6.0-py37_0",
    "backports.os-0.1.1-py37_0",
    "backports.shutil_get_terminal_size-1.0.0-py37_2",
    "beautifulsoup4-4.7.1-py37_1",
    "cffi-1.12.2-py37h7a1dbc1_1",
    "cycler-0.10.0-py37_0",
    "cytoolz-0.9.0.1-py37hfa6e2cd_1",
    "html5lib-1.0.1-py37_0",
    "importlib_metadata-0.8-py37_0",
    "jedi-0.13.3-py37_0",
    "keyring-18.0.0-py37_0",
    "mkl_random-1.0.2-py37h343c172_0",
    "multipledispatch-0.6.0-py37_0",
    "nltk-3.4-py37_1",
    "openpyxl-2.6.1-py37_1",
    "packaging-19.0-py37_0",
    "partd-0.3.10-py37_1",
    "pathlib2-2.3.3-py37_0",
    "pillow-5.4.1-py37hdc69c19_0",
    "pyqt-5.9.2-py37h6538335_2",
    "pyrsistent-0.14.11-py37he774522_0",
    "pysocks-1.6.8-py37_0",
    "python-dateutil-2.8.0-py37_0",
    "qtawesome-0.5.7-py37_1",
    "setuptools-40.8.0-py37_0",
    "singledispatch-3.4.0.3-py37_0",
    "sortedcollections-1.1.2-py37_0",
    "sphinxcontrib-websupport-1.1.0-py37_1",
    "sympy-1.3-py37_0",
    "terminado-0.8.1-py37_1",
    "traitlets-4.3.2-py37_0",
    "xlwings-0.15.4-py37_0",
    "zict-0.1.4-py37_0",
    "astroid-2.2.5-py37_0",
    "bleach-3.1.0-py37_0",
    "clyent-1.2.2-py37_1",
    "cryptography-2.6.1-py37h7a1dbc1_0",
    "cython-0.29.6-py37ha925a31_0",
    "distributed-1.26.0-py37_1",
    "get_terminal_size-1.0.0-h38e98db_0",
    "gevent-1.4.0-py37he774522_0",
    "isort-4.3.16-py37_0",
    "jinja2-2.10-py37_0",
    "jsonschema-3.0.1-py37_0",
    "jupyter_core-4.4.0-py37_0",
    "navigator-updater-0.2.1-py37_0",
    "networkx-2.2-py37_1",
    "nose-1.3.7-py37_2",
    "path.py-11.5.0-py37_0",
    "pygments-2.3.1-py37_0",
    "pytest-4.3.1-py37_0",
    "wheel-0.33.1-py37_0",
    "conda-verify-3.1.1-py37_0",
    "flask-1.0.2-py37_1",
    "jupyter_client-5.2.4-py37_0",
    "nbformat-4.4.0-py37_0",
    "pip-19.0.3-py37_0",
    "prompt_toolkit-2.0.9-py37_0",
    "pylint-2.3.1-py37_0",
    "pyopenssl-19.0.0-py37_0",
    "pytest-openfiles-0.3.2-py37_0",
    "pytest-remotedata-0.3.1-py37_0",
    "ipython-7.4.0-py37h39e3cac_0",
    "nbconvert-5.4.1-py37_3",
    "urllib3-1.24.1-py37_0",
    "ipykernel-5.1.0-py37h39e3cac_0",
    "requests-2.21.0-py37_0",
    "anaconda-client-1.7.2-py37_0",
    "conda-4.6.11-py37_0",
    "jupyter_console-6.0.0-py37_0",
    "notebook-5.7.8-py37_0",
    "qtconsole-4.4.3-py37_0",
    "sphinx-1.8.5-py37_0",
    "spyder-kernels-0.4.2-py37_0",
    "anaconda-navigator-1.9.7-py37_0",
    "anaconda-project-0.8.2-py37_0",
    "conda-build-3.17.8-py37_0",
    "jupyterlab_server-0.2.0-py37_0",
    "numpydoc-0.8.0-py37_0",
    "widgetsnbextension-3.4.2-py37_0",
    "ipywidgets-7.4.2-py37_0",
    "jupyterlab-0.35.4-py37hf63ae98_0",
    "spyder-3.3.3-py37_0",
    "_ipyw_jlab_nb_ext_conf-0.1.0-py37_0",
    "jupyter-1.0.0-py37_7",
    "bokeh-1.0.4-py37_0",
    "bottleneck-1.2.1-py37h452e1ab_1",
    "h5py-2.9.0-py37h5e291fa_0",
    "imageio-2.5.0-py37_0",
    "matplotlib-3.0.3-py37hc8f65d3_0",
    "mkl_fft-1.0.10-py37h14836fe_0",
    "numpy-1.16.2-py37h19fb1c0_0",
    "numba-0.43.1-py37hf9181ef_0",
    "numexpr-2.6.9-py37hdce8814_0",
    "pandas-0.24.2-py37ha925a31_0",
    "pytest-arraydiff-0.3-py37h39e3cac_0",
    "pytest-doctestplus-0.3.0-py37_0",
    "pywavelets-1.0.2-py37h8c2d366_0",
    "scipy-1.2.1-py37h29ff71c_0",
    "bkcharts-0.2-py37_0",
    "dask-1.1.4-py37_1",
    "patsy-0.5.1-py37_0",
    "pytables-3.5.1-py37h1da0976_0",
    "pytest-astropy-0.5.0-py37_0",
    "scikit-image-0.14.2-py37ha925a31_0",
    "scikit-learn-0.20.3-py37h343c172_0",
    "astropy-3.1.2-py37he774522_0",
    "statsmodels-0.9.0-py37h452e1ab_0",
    "seaborn-0.9.0-py37_0",
    "anaconda-2019.03-py37_0"
  ]
}



def _link(src, dst, linktype=LINK_HARD):
    if linktype == LINK_HARD:
        if on_win:
            from ctypes import windll, wintypes
            CreateHardLink = windll.kernel32.CreateHardLinkW
            CreateHardLink.restype = wintypes.BOOL
            CreateHardLink.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR,
                                       wintypes.LPVOID]
            if not CreateHardLink(dst, src, None):
                raise OSError('win32 hard link failed')
        else:
            os.link(src, dst)
    elif linktype == LINK_COPY:
        # copy relative symlinks as symlinks
        if islink(src) and not os.readlink(src).startswith(os.path.sep):
            os.symlink(os.readlink(src), dst)
        else:
            shutil.copy2(src, dst)
    else:
        raise Exception("Did not expect linktype=%r" % linktype)


def rm_rf(path):
    """
    try to delete path, but never fail
    """
    try:
        if islink(path) or isfile(path):
            # Note that we have to check if the destination is a link because
            # exists('/path/to/dead-link') will return False, although
            # islink('/path/to/dead-link') is True.
            os.unlink(path)
        elif isdir(path):
            shutil.rmtree(path)
    except (OSError, IOError):
        pass


def yield_lines(path):
    for line in open(path):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        yield line


prefix_placeholder = ('/opt/anaconda1anaconda2'
                      # this is intentionally split into parts,
                      # such that running this program on itself
                      # will leave it unchanged
                      'anaconda3')

def read_has_prefix(path):
    """
    reads `has_prefix` file and return dict mapping filenames to
    tuples(placeholder, mode)
    """
    import shlex

    res = {}
    try:
        for line in yield_lines(path):
            try:
                parts = [x.strip('"\'') for x in shlex.split(line, posix=False)]
                # assumption: placeholder and mode will never have a space
                placeholder, mode, f = parts[0], parts[1], ' '.join(parts[2:])
                res[f] = (placeholder, mode)
            except (ValueError, IndexError):
                res[line] = (prefix_placeholder, 'text')
    except IOError:
        pass
    return res


def exp_backoff_fn(fn, *args):
    """
    for retrying file operations that fail on Windows due to virus scanners
    """
    if not on_win:
        return fn(*args)

    import time
    import errno
    max_tries = 6  # max total time = 6.4 sec
    for n in range(max_tries):
        try:
            result = fn(*args)
        except (OSError, IOError) as e:
            if e.errno in (errno.EPERM, errno.EACCES):
                if n == max_tries - 1:
                    raise Exception("max_tries=%d reached" % max_tries)
                time.sleep(0.1 * (2 ** n))
            else:
                raise e
        else:
            return result


class PaddingError(Exception):
    pass


def binary_replace(data, a, b):
    """
    Perform a binary replacement of `data`, where the placeholder `a` is
    replaced with `b` and the remaining string is padded with null characters.
    All input arguments are expected to be bytes objects.
    """
    def replace(match):
        occurances = match.group().count(a)
        padding = (len(a) - len(b)) * occurances
        if padding < 0:
            raise PaddingError(a, b, padding)
        return match.group().replace(a, b) + b'\0' * padding

    pat = re.compile(re.escape(a) + b'([^\0]*?)\0')
    res = pat.sub(replace, data)
    assert len(res) == len(data)
    return res


def update_prefix(path, new_prefix, placeholder, mode):
    if on_win:
        # force all prefix replacements to forward slashes to simplify need
        # to escape backslashes - replace with unix-style path separators
        new_prefix = new_prefix.replace('\\', '/')

    path = os.path.realpath(path)
    with open(path, 'rb') as fi:
        data = fi.read()
    if mode == 'text':
        new_data = data.replace(placeholder.encode('utf-8'),
                                new_prefix.encode('utf-8'))
    elif mode == 'binary':
        if on_win:
            # anaconda-verify will not allow binary placeholder on Windows.
            # However, since some packages might be created wrong (and a
            # binary placeholder would break the package, we just skip here.
            return
        new_data = binary_replace(data, placeholder.encode('utf-8'),
                                  new_prefix.encode('utf-8'))
    else:
        sys.exit("Invalid mode:" % mode)

    if new_data == data:
        return
    st = os.lstat(path)
    # unlink in case the file is memory mapped
    exp_backoff_fn(os.unlink, path)
    with open(path, 'wb') as fo:
        fo.write(new_data)
    os.chmod(path, stat.S_IMODE(st.st_mode))


def name_dist(dist):
    if hasattr(dist, 'name'):
        return dist.name
    else:
        return dist.rsplit('-', 2)[0]


def create_meta(prefix, dist, info_dir, extra_info):
    """
    Create the conda metadata, in a given prefix, for a given package.
    """
    # read info/repodata_record.json first
    with open(join(info_dir, 'repodata_record.json')) as fi:
        meta = json.load(fi)
    # add extra info
    meta.update(extra_info)
    # write into <prefix>/conda-meta/<dist>.json
    meta_dir = join(prefix, 'conda-meta')
    if not isdir(meta_dir):
        os.makedirs(meta_dir)
    with open(join(meta_dir, dist + '.json'), 'w') as fo:
        json.dump(meta, fo, indent=2, sort_keys=True)


def run_script(prefix, dist, action='post-link'):
    """
    call the post-link (or pre-unlink) script, and return True on success,
    False on failure
    """
    path = join(prefix, 'Scripts' if on_win else 'bin', '.%s-%s.%s' % (
            name_dist(dist),
            action,
            'bat' if on_win else 'sh'))
    if not isfile(path):
        return True
    if SKIP_SCRIPTS:
        print("WARNING: skipping %s script by user request" % action)
        return True

    if on_win:
        cmd_exe = os.path.join(os.environ['SystemRoot'], 'System32', 'cmd.exe')
        if not os.path.isfile(cmd_exe):
            cmd_exe = os.path.join(os.environ['windir'], 'System32', 'cmd.exe')
        if not os.path.isfile(cmd_exe):
            print("Error: running %s failed.  cmd.exe could not be found.  "
                "Looked in SystemRoot and windir env vars.\n" % path)
            return False
        args = [cmd_exe, '/d', '/c', path]
    else:
        shell_path = '/bin/sh' if 'bsd' in sys.platform else '/bin/bash'
        args = [shell_path, path]

    env = os.environ
    env['PREFIX'] = prefix

    import subprocess
    try:
        subprocess.check_call(args, env=env)
    except subprocess.CalledProcessError:
        return False
    return True


url_pat = re.compile(r'''
(?P<baseurl>\S+/)                 # base URL
(?P<fn>[^\s#/]+)                  # filename
([#](?P<md5>[0-9a-f]{32}))?       # optional MD5
$                                 # EOL
''', re.VERBOSE)

def read_urls(dist):
    try:
        data = open(join(PKGS_DIR, 'urls')).read()
        for line in data.split()[::-1]:
            m = url_pat.match(line)
            if m is None:
                continue
            if m.group('fn') == '%s.tar.bz2' % dist:
                return {'url': m.group('baseurl') + m.group('fn'),
                        'md5': m.group('md5')}
    except IOError:
        pass
    return {}


def read_no_link(info_dir):
    res = set()
    for fn in 'no_link', 'no_softlink':
        try:
            res.update(set(yield_lines(join(info_dir, fn))))
        except IOError:
            pass
    return res


def linked(prefix):
    """
    Return the (set of canonical names) of linked packages in prefix.
    """
    meta_dir = join(prefix, 'conda-meta')
    if not isdir(meta_dir):
        return set()
    return set(fn[:-5] for fn in os.listdir(meta_dir) if fn.endswith('.json'))


def link(prefix, dist, linktype=LINK_HARD, info_dir=None):
    '''
    Link a package in a specified prefix.  We assume that the packacge has
    been extra_info in either
      - <PKGS_DIR>/dist
      - <ROOT_PREFIX>/ (when the linktype is None)
    '''
    if linktype:
        source_dir = join(PKGS_DIR, dist)
        info_dir = join(source_dir, 'info')
        no_link = read_no_link(info_dir)
    else:
        info_dir = info_dir or join(prefix, 'info')

    files = list(yield_lines(join(info_dir, 'files')))
    # TODO: Use paths.json, if available or fall back to this method
    has_prefix_files = read_has_prefix(join(info_dir, 'has_prefix'))

    if linktype:
        for f in files:
            src = join(source_dir, f)
            dst = join(prefix, f)
            dst_dir = dirname(dst)
            if not isdir(dst_dir):
                os.makedirs(dst_dir)
            if exists(dst):
                if FORCE:
                    rm_rf(dst)
                else:
                    raise Exception("dst exists: %r" % dst)
            lt = linktype
            if f in has_prefix_files or f in no_link or islink(src):
                lt = LINK_COPY
            try:
                _link(src, dst, lt)
            except OSError:
                pass

    for f in sorted(has_prefix_files):
        placeholder, mode = has_prefix_files[f]
        try:
            update_prefix(join(prefix, f), prefix, placeholder, mode)
        except PaddingError:
            sys.exit("ERROR: placeholder '%s' too short in: %s\n" %
                     (placeholder, dist))

    if not run_script(prefix, dist, 'post-link'):
        sys.exit("Error: post-link failed for: %s" % dist)

    meta = {
        'files': files,
        'link': ({'source': source_dir,
                  'type': link_name_map.get(linktype)}
                 if linktype else None),
    }
    try:    # add URL and MD5
        meta.update(IDISTS[dist])
    except KeyError:
        meta.update(read_urls(dist))
    meta['installed_by'] = 'Anaconda3-2019.03-Windows-x86_64.exe'
    create_meta(prefix, dist, info_dir, meta)


def duplicates_to_remove(linked_dists, keep_dists):
    """
    Returns the (sorted) list of distributions to be removed, such that
    only one distribution (for each name) remains.  `keep_dists` is an
    interable of distributions (which are not allowed to be removed).
    """
    from collections import defaultdict

    keep_dists = set(keep_dists)
    ldists = defaultdict(set) # map names to set of distributions
    for dist in linked_dists:
        name = name_dist(dist)
        ldists[name].add(dist)

    res = set()
    for dists in ldists.values():
        # `dists` is the group of packages with the same name
        if len(dists) == 1:
            # if there is only one package, nothing has to be removed
            continue
        if dists & keep_dists:
            # if the group has packages which are have to be kept, we just
            # take the set of packages which are in group but not in the
            # ones which have to be kept
            res.update(dists - keep_dists)
        else:
            # otherwise, we take lowest (n-1) (sorted) packages
            res.update(sorted(dists)[:-1])
    return sorted(res)


def yield_idists():
    for line in open(join(PKGS_DIR, 'urls')):
        m = url_pat.match(line)
        if m:
            fn = m.group('fn')
            yield fn[:-8]


def remove_duplicates():
    idists = list(yield_idists())
    keep_files = set()
    for dist in idists:
        with open(join(ROOT_PREFIX, 'conda-meta', dist + '.json')) as fi:
            meta = json.load(fi)
        keep_files.update(meta['files'])

    for dist in duplicates_to_remove(linked(ROOT_PREFIX), idists):
        print("unlinking: %s" % dist)
        meta_path = join(ROOT_PREFIX, 'conda-meta', dist + '.json')
        with open(meta_path) as fi:
            meta = json.load(fi)
        for f in meta['files']:
            if f not in keep_files:
                rm_rf(join(ROOT_PREFIX, f))
        rm_rf(meta_path)


def determine_link_type_capability():
    src = join(PKGS_DIR, 'urls')
    dst = join(ROOT_PREFIX, '.hard-link')
    assert isfile(src), src
    assert not isfile(dst), dst
    try:
        _link(src, dst, LINK_HARD)
        linktype = LINK_HARD
    except OSError:
        linktype = LINK_COPY
    finally:
        rm_rf(dst)
    return linktype


def link_dist(dist, linktype=None):
    if not linktype:
        linktype = determine_link_type_capability()
    prefix = prefix_env('root')
    link(prefix, dist, linktype)


def link_idists():
    linktype = determine_link_type_capability()
    for env_name in sorted(C_ENVS):
        dists = C_ENVS[env_name]
        assert isinstance(dists, list)
        if len(dists) == 0:
            continue

        prefix = prefix_env(env_name)
        for dist in dists:
            assert dist in IDISTS
            link_dist(dist, linktype)

        for dist in duplicates_to_remove(linked(prefix), dists):
            meta_path = join(prefix, 'conda-meta', dist + '.json')
            print("WARNING: unlinking: %s" % meta_path)
            try:
                os.rename(meta_path, meta_path + '.bak')
            except OSError:
                rm_rf(meta_path)


def prefix_env(env_name):
    if env_name == 'root':
        return ROOT_PREFIX
    else:
        return join(ROOT_PREFIX, 'envs', env_name)


def post_extract(env_name='root'):
    """
    assuming that the package is extracted in the environment `env_name`,
    this function does everything link() does except the actual linking,
    i.e. update prefix files, run 'post-link', creates the conda metadata,
    and removed the info/ directory afterwards.
    """
    prefix = prefix_env(env_name)
    info_dir = join(prefix, 'info')
    with open(join(info_dir, 'index.json')) as fi:
        meta = json.load(fi)
    dist = '%(name)s-%(version)s-%(build)s' % meta
    if FORCE:
        run_script(prefix, dist, 'pre-unlink')
    link(prefix, dist, linktype=None)
    shutil.rmtree(info_dir)


def multi_post_extract():
    # This function is called when using the --multi option, when building
    # .pkg packages on OSX.  I tried avoiding this extra option by running
    # the post extract step on each individual package (like it is done for
    # the .sh and .exe installers), by adding a postinstall script to each
    # conda .pkg file, but this did not work as expected.  Running all the
    # post extracts at end is also faster and could be considered for the
    # other installer types as well.
    for dist in yield_idists():
        info_dir = join(ROOT_PREFIX, 'info', dist)
        with open(join(info_dir, 'index.json')) as fi:
            meta = json.load(fi)
        dist = '%(name)s-%(version)s-%(build)s' % meta
        link(ROOT_PREFIX, dist, linktype=None, info_dir=info_dir)


def main():
    global SKIP_SCRIPTS, ROOT_PREFIX, PKGS_DIR

    p = OptionParser(description="conda post extract tool used by installers")

    p.add_option('--skip-scripts',
                 action="store_true",
                 help="skip running pre/post-link scripts")

    p.add_option('--rm-dup',
                 action="store_true",
                 help="remove duplicates")

    p.add_option('--multi',
                 action="store_true",
                 help="multi post extract usecase")

    p.add_option('--link-dist',
                 action="store",
                 default=None,
                 help="link dist")

    p.add_option('--root-prefix',
                 action="store",
                 default=abspath(join(__file__, '..', '..')),
                 help="root prefix (defaults to %default)")

    p.add_option('--post',
                 action="store",
                 help="perform post extract (on a single package), "
                      "in environment NAME",
                 metavar='NAME')

    opts, args = p.parse_args()
    ROOT_PREFIX = opts.root_prefix.replace('//', '/')
    PKGS_DIR = join(ROOT_PREFIX, 'pkgs')

    if args:
        p.error('no arguments expected')

    if FORCE:
        print("using -f (force) option")

    if opts.post:
        post_extract(opts.post)
        return

    if opts.skip_scripts:
        SKIP_SCRIPTS = True

    if opts.rm_dup:
        remove_duplicates()
        return

    if opts.multi:
        multi_post_extract()
        return

    if opts.link_dist:
        link_dist(opts.link_dist)
        return

    if IDISTS:
        link_idists()
    else:
        post_extract()


def warn_on_special_chrs():
    if on_win:
        return
    for c in SPECIAL_ASCII:
        if c in ROOT_PREFIX:
            print("WARNING: found '%s' in install prefix." % c)


if __name__ == '__main__':
    main()
    warn_on_special_chrs()
