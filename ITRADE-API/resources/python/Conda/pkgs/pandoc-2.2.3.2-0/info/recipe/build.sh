#!/bin/bash

mkdir -p ${PREFIX}/bin
if [[ $(uname) == Linux ]] && [[ $(uname -m) == x86_64 ]]; then
    ar vx pandoc*.deb
    tar --extract --xz --verbose --file=data.tar.xz
    mv usr/bin/* ${PREFIX}/bin/
elif [[ $(uname) == Linux ]] && ( [[ $(uname -m) == i686 ]] || [[ $(uname -m) == ppc64le ]] ); then
    RPMS=$(find . -name "*.rpm")
    for RPM in ${RPMS}; do
        rpm2cpio ${RPM} | cpio -idv
    done
    mv usr/bin/* ${PREFIX}/bin/
    for EXE in pandoc pandoc-citeproc; do
        if [[ -f ${PREFIX}/bin/${EXE} ]]; then
            patchelf --replace-needed libgmp.so.3 libgmp.so.10 ${PREFIX}/bin/${EXE}
            patchelf --replace-needed libffi.so.5 libffi.so.6  ${PREFIX}/bin/${EXE}
        fi
    done
elif [[ $(uname) == Darwin ]]; then
    pkgutil --expand pandoc-${PKG_VERSION}-macOS.pkg pandoc
    cpio -i -I pandoc/pandoc.pkg/Payload
    cp usr/local/bin/* ${PREFIX}/bin/
fi
