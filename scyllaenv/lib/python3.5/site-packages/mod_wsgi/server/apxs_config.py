
import os

WITH_TARBALL_PACKAGE = False
WITH_HTTPD_PACKAGE = False

if WITH_HTTPD_PACKAGE:
    from mod_wsgi_packages.httpd import __file__ as PACKAGES_ROOTDIR
    PACKAGES_ROOTDIR = os.path.dirname(PACKAGES_ROOTDIR)
    BINDIR = os.path.join(PACKAGES_ROOTDIR, 'bin')
    SBINDIR = BINDIR
    LIBEXECDIR = os.path.join(PACKAGES_ROOTDIR, 'modules')
    SHLIBPATH = os.path.join(PACKAGES_ROOTDIR, 'lib')
elif WITH_TARBALL_PACKAGE:
    from mod_wsgi.packages import __file__ as PACKAGES_ROOTDIR
    PACKAGES_ROOTDIR = os.path.dirname(PACKAGES_ROOTDIR)
    BINDIR = os.path.join(PACKAGES_ROOTDIR, 'apache', 'bin')
    SBINDIR = BINDIR
    LIBEXECDIR = os.path.join(PACKAGES_ROOTDIR, 'apache', 'modules')
    SHLIBPATH = []
    SHLIBPATH.append(os.path.join(PACKAGES_ROOTDIR, 'apr-util', 'lib'))
    SHLIBPATH.append(os.path.join(PACKAGES_ROOTDIR, 'apr', 'lib'))
    SHLIBPATH = ':'.join(SHLIBPATH)
else:
    BINDIR = '/usr/bin'
    SBINDIR = '/usr/sbin'
    LIBEXECDIR = '/usr/lib/apache2/modules'
    SHLIBPATH = ''

MPM_NAME = ''
PROGNAME = 'apache2'
SHLIBPATH_VAR = 'LD_LIBRARY_PATH'

if os.path.exists(os.path.join(SBINDIR, PROGNAME)):
    HTTPD = os.path.join(SBINDIR, PROGNAME)
elif os.path.exists(os.path.join(BINDIR, PROGNAME)):
    HTTPD = os.path.join(BINDIR, PROGNAME)
else:
    HTTPD = PROGNAME

if os.path.exists(os.path.join(SBINDIR, 'rotatelogs')):
    ROTATELOGS = os.path.join(SBINDIR, 'rotatelogs')
elif os.path.exists(os.path.join(BINDIR, 'rotatelogs')):
    ROTATELOGS = os.path.join(BINDIR, 'rotatelogs')
else:
    ROTATELOGS = 'rotatelogs'

