%define major	1
%define libname	%mklibname ldb %{major}
%define devname %mklibname -d ldb
%define libpyldbutil %mklibname pyldb-util %{major}
%define devpyldbutil %mklibname -d pyldb-util

%define check_sig() export GNUPGHOME=%{_tmppath}/rpm-gpghome \
if [ -d "$GNUPGHOME" ] \
then echo "Error, GNUPGHOME $GNUPGHOME exists, remove it and try again"; exit 1 \
fi \
install -d -m700 $GNUPGHOME \
gpg --import %{1} \
gpg --trust-model always --verify %{2} %{?3} \
rm -Rf $GNUPGHOME \

Summary:	Library implementing Samba's embedded database
Name:		ldb
Epoch:		1
Version:	1.1.16
Release:	5
Group:		System/Libraries
License:	GPLv2
Url:		http://ldb.samba.org/
Source0:	http://www.samba.org/ftp/ldb/%{name}-%{version}.tar.gz
Source1:	http://www.samba.org/ftp/ldb/%{name}-%{version}.tar.asc
Source2:	samba-pubkey.asc

BuildRequires:	docbook-style-xsl
BuildRequires:	python-tdb >= 1.2.9
BuildRequires:	python-tevent >= 1:0.9.16-0.beta8.0
BuildRequires:	xsltproc
BuildRequires:	openldap-devel
BuildRequires:	pkgconfig(popt)
BuildRequires:	pkgconfig(pytalloc-util)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(talloc)
BuildRequires:	pkgconfig(tdb)
BuildRequires:	pkgconfig(tevent)

%track
prog %{name} = {
	url = http://www.samba.org/ftp/ldb/
	version = %{version}
	regex = %{name}-(__VER__)\.tar\.gz
}

%description
Library implementing Samba's embedded database and utilities for backing up,
restoring and manipulating the database.

%package -n %{libname}
Group:		System/Libraries
Summary:	Library implementing Samba's embedded database

%description -n %{libname}
Library implementing Samba's embedded database

%package -n ldb-utils
Group:		Databases
Summary:	Tools for backing up, restoring, and manipulating Samba's embedded database
Conflicts:	samba-server < 3.3.2-2

%description -n ldb-utils
Tools for backing up, restoring, and manipulating Samba's embedded database

%package -n %{devname}
Group:		Development/C
Summary:	Library implementing Samba's embedded database
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}
# because /usr/include/ldb.h was moved from libsmbclient0-devel to libldb-devel
Conflicts:	%{mklibname smbclient 0 -d} < 3.2.6-3

%description -n %{devname}
Library implementing Samba's embedded database

%package -n python-ldb
Group:		Development/Python
Summary:	Python bindings to Samba's ldb embedded database

%description -n python-ldb
Python bindings to Samba's ldb embedded database

%package -n %{libpyldbutil}
Group:		System/Libraries
Summary:	Utility library for using tdb functions in python

%description -n %{libpyldbutil}
Utility library for using tdb functions in python.

%package -n %{devpyldbutil}
Group:		Development/Python
Summary:	Development files for utility library for using tdb functions in python
Provides:	pyldb-util-devel = %{EVRD}
Requires:	%{libpyldbutil} = %{EVRD}

%description -n %{devpyldbutil}
Development files for utility library for using tdb functions in python.

%prep
%setup -q
sed -i -e 's,http://docbook.sourceforge.net/release/xsl/current,/usr/share/sgml/docbook/xsl-stylesheets,g' docs/builddocs.sh buildtools/wafsamba/wafsamba.py buildtools/wafsamba/samba_conftests.py

# Fix unreadable files
find . -perm 0640 -exec chmod 0644 '{}' \;

%build
# The ldb linker script is incompatible with gold
export LDFLAGS="%{optflags} -fuse-ld=bfd"
%configure2_5x \
	--with-modulesdir=%{_libdir} \
	--bundled-libraries=NONE
%make

%install
%makeinstall_std

%files -n %{libname}
%{_libdir}/libldb.so.%{major}*

%files -n %{devname}
%{_libdir}/libldb.so
%{_libdir}/pkgconfig/ldb.pc
%{_includedir}/ldb*.h

%files -n ldb-utils
%{_bindir}/ldb*
%{_libdir}/ldb
%{_mandir}/man1/ldb*.1*
%{_mandir}/man3/ldb*.3*

%files -n python-ldb
%{py_platsitedir}/ldb.so

%files -n %{libpyldbutil}
%{_libdir}/libpyldb-util.so.%{major}*

%files -n %{devpyldbutil}
%{_libdir}/libpyldb-util.so
%{_includedir}/pyldb.h
%{_libdir}/pkgconfig/pyldb-util.pc

