%define ldbmajor	1
%define ldbver		1.1.6
%define epoch 1

%define libldb %mklibname ldb %ldbmajor
%define ldbdevel %mklibname -d ldb

%define libpyldbutil %mklibname pyldb-util 1
%define libpyldbutildevel %mklibname -d pyldb-util

%define check_sig() export GNUPGHOME=%{_tmppath}/rpm-gpghome \
if [ -d "$GNUPGHOME" ] \
then echo "Error, GNUPGHOME $GNUPGHOME exists, remove it and try again"; exit 1 \
fi \
install -d -m700 $GNUPGHOME \
gpg --import %{1} \
gpg --trust-model always --verify %{2} %{?3} \
rm -Rf $GNUPGHOME \


Name: ldb
Version: %ldbver
# We shipped it in samba3 versioned with the samba3 version
Epoch: %epoch
Release: 1
Group: System/Libraries
License: GPLv2
URL: http://ldb.samba.org/
Summary: Library implementing Samba's embedded database
Source: http://samba.org/ftp/ldb/ldb-%{ldbver}.tar.gz
Source1: http://samba.org/ftp/ldb/ldb-%{ldbver}.tar.asc
Source2: jelmer.asc
Patch1: ldb-1.1.4-disable-pyevent-check.patch
BuildRequires: python-devel
BuildRequires: openldap-devel
BuildRequires: popt-devel
BuildRequires: tevent-devel >= 0.9.14 python-tevent >= 0.9.14
BuildRequires: talloc-devel >= 2.0.7 pytalloc-util-devel >= 2.0.7
BuildRequires: python-tdb >= 1.2.9 tdb-devel >= 1.2.9
BuildRequires: docbook-style-xsl xsltproc
BuildRoot: %{_tmppath}/%{name}-root

%description
Library implementing Samba's embedded database and utilities for backing up,
restoring and manipulating the database.

%package -n %libldb
Group: System/Libraries
Summary: Library implementing Samba's embedded database

%description -n %libldb
Library implementing Samba's embedded database

%package -n ldb-utils
Group: Databases
Summary: Tools for backing up, restoring, and manipulating Samba's embedded database
Conflicts: samba-server < 3.3.2-2

%description -n ldb-utils
Tools for backing up, restoring, and manipulating Samba's embedded database

%package -n %ldbdevel
Group: Development/C
Summary: Library implementing Samba's embedded database
Provides: ldb-devel = %{epoch}:%{version}-%{release}
#Version: %ldbver
Requires: %libldb = %{epoch}:%{version}-%{release}
# because /usr/include/ldb.h was moved from libsmbclient0-devel to libldb-devel
Conflicts: %{mklibname smbclient 0 -d} < 3.2.6-3

%description -n %ldbdevel
Library implementing Samba's embedded database

%package -n python-ldb
Group: Development/Python
Summary: Python bindings to Samba's ldb embedded database

%description -n python-ldb
Python bindings to Samba's ldb embedded database

%package -n %libpyldbutil
Group: System/Libraries
Summary: Utility library for using tdb functions in python

%description -n %libpyldbutil
Utility library for using tdb functions in python.

%package -n %libpyldbutildevel
Group: Development/Python
Summary: Development files for utility library for using tdb functions in python
Provides: pyldb-util-devel = %{version}-%{release}
Requires: %libpyldbutil = %epoch:%{version}

%description -n %libpyldbutildevel
Development files for utility library for using tdb functions in python.

%prep
#check_sig %{SOURCE2} %{SOURCE1} %{SOURCE0}

%setup -q
%patch1 -p1 -b .nopyeventver
perl -pi -e 's,http://docbook.sourceforge.net/release/xsl/current,/usr/share/sgml/docbook/xsl-stylesheets,g' docs/builddocs.sh buildtools/wafsamba/wafsamba.py buildtools/wafsamba/samba_conftests.py

%build
%configure2_5x --with-modulesdir=%{_libdir} --bundled-libraries=NONE --disable-rpath --disable-tdb2
%make

%install
rm -Rf %{buildroot}
%makeinstall_std

%clean
rm -Rf %{buildroot}

%files -n %libldb
%defattr(-,root,root)
%{_libdir}/libldb.so.%{ldbmajor}*

%files -n %ldbdevel
%defattr(-,root,root)
%{_libdir}/libldb.so
#{_libdir}/libldb.a
%{_libdir}/pkgconfig/ldb.pc
%{_includedir}/ldb*.h

%files -n ldb-utils
%defattr(-,root,root)
%{_bindir}/ldb*
%{_libdir}/ldb
%{_mandir}/man1/ldb*.1%{_extension}
%{_mandir}/man3/ldb*.3%{_extension}

%files -n python-ldb
%defattr(-,root,root)
%{py_platsitedir}/ldb.so

%files -n %libpyldbutil
%defattr(-,root,root)
%{_libdir}/libpyldb-util.so.1*

%files -n %libpyldbutildevel
%defattr(-,root,root)
%{_libdir}/libpyldb-util.so
%{_includedir}/pyldb.h
%{_libdir}/pkgconfig/pyldb-util.pc
