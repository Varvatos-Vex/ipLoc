import sys
import subprocess


class ServiceMonitor(object):

    def __init__(self, service):
        self.service = service

    def is_active(self):
        """Return True if service is running"""
        cmd = '/bin/systemctl status %s.service' % self.service
        proc = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,encoding='utf8')
        stdout_list = proc.communicate()[0].split('\n')
        for line in stdout_list:
            if 'Active:' in line:
                if '(running)' in line:
                    print("Kibana is Running")
                    return True
        return False

    def start(self):
        cmd = '/bin/systemctl start %s.service' % self.service
        proc = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE)
        stdout = proc.communicate()
        print(stdout)
        


if __name__ == '__main__':
    # TODO: Show usage                                                 
    monitor = ServiceMonitor(sys.argv[1])
    if not monitor.is_active():
        print("Not Running Starting")
        monitor.start()