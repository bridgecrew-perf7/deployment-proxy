from dproxy.config import Config

#import dbus
import sys
from subprocess import check_output, check_call, Popen


def install_pkgs(packages):
    packages = [x.encode('utf-8') for x in packages]
    packages = ' '.join(packages)
    check_call("yum clean all", verbose=False)
    stat = check_call("yum -y --enablerepo=Production install {}".format(packages), verbose=False)
    if stat != 0:
        raise Exception(stat)


def restart_service(service):
    restart = "systemctl restart " + service
    Popen([sys.executable, restart])

#def restart_service(service):
#    sysbus = dbus.SystemBus()
#    systemd1 = sysbus.get_object("org.freedesktop.systemd1", "/org/freedesktop/systemd1")
#    manager = dbus.Interface(systemd1, "org.freedesktop.systemd1.Manager")
#    manager.RestartUnit(service, "fail")
