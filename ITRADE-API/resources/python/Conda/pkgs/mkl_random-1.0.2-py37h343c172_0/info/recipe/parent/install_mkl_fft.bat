pushd mkl_fft
COPY %PREFIX%/site.cfg site.cfg
python setup.py build install --single-version-externally-managed --record=record.txt