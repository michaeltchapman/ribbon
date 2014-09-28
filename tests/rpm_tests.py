from nose.tools import *
from ribbon import rpm
import mock
import subprocess

script_query = """
preinstall scriptlet (using /bin/sh):
# 163:163 for keystone (openstack-keystone) - rhbz#752842
getent group keystone >/dev/null || groupadd -r --gid 163 keystone
getent passwd keystone >/dev/null || \
useradd --uid 163 -r -g keystone -d /var/lib/keystone -s /sbin/nologin \
-c "OpenStack Keystone Daemons" keystone
exit 0
postinstall scriptlet (using /bin/sh):
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add openstack-keystone
fi
preuninstall scriptlet (using /bin/sh):
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /sbin/service openstack-keystone stop >/dev/null 2>&1
    /sbin/chkconfig --del openstack-keystone
fi
postuninstall scriptlet (using /bin/sh):
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /sbin/service openstack-keystone condrestart >/dev/null 2>&1 || :
fi
"""
def test_load_scripts():
    subprocess.call = mock.create_autospec(subprocess.call, return_value=script_query)
    scripts = rpm.load_scripts('dummy')
    print scripts
    assert 'preinstall' in scripts, 'Should be a preinstall script'
    assert 'postinstall' in scripts, 'Should be a postinstall script'
    assert 'preuninstall' in scripts, 'Should be a preuninstall script'
    assert 'postuninstall' in scripts, 'Should be a postuninstall script'


