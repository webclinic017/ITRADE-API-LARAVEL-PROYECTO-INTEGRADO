import os
import sys
import numpy

import numpy.core.multiarray
import numpy.core.numeric
import numpy.core.umath
import numpy.core.umath_tests
import numpy.fft.fftpack_lite
import numpy.linalg.lapack_lite
import numpy.random.mtrand

try:
    from numpy.fft import using_mklfft
    print('USING MKLFFT: %s' % using_mklfft)
except ImportError:
    print("Not using MKLFFT")

try:
    print('MKL: %r' % numpy.__mkl_version__)
except AttributeError:
    print('NO MKL')

if sys.platform == 'darwin':
    os.environ['LDFLAGS'] = ' '.join((os.getenv('LDFLAGS', ''), " -undefined dynamic_lookup"))
elif sys.platform.startswith('linux'):
    os.environ['LDFLAGS'] = ' '.join((os.getenv('LDFLAGS', ''), '-shared'))
    os.environ['FFLAGS'] = ' '.join((os.getenv('FFLAGS', ''), '-Wl,-shared'))
result = numpy.test()
sys.exit(not result)
