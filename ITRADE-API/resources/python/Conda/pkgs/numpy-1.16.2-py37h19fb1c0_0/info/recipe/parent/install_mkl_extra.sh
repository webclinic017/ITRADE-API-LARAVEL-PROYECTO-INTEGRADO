pushd $PKG_NAME
cp $PREFIX/site.cfg site.cfg
python setup.py build install --single-version-externally-managed --record=record.txt
