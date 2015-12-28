import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sisv2.settings")

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))


from bettersis.models import MonitorCPU

def get_host_list():
    for host in MonitorCPU.objects.values('host').distinct():
        yield host['host'].lower()



if __name__ == '__main__':
    host_list = list(get_host_list())
    host_list.sort()

    for host in host_list:
        print(host)