__author__ = "Kirito"
import random
import sys
import threading
from queue import Queue
from optparse import OptionParser

try:
    import requests
except Exception:
    print("[!] You Need to Install requests module !")
    print("[!] Usage:pip install requests ")
    exit()


class WebDirScan:
    def __init__(self, options):
        self.url = options.url
        self.file_name = options.file_name
        self.count = options.count


    class DirScan(threading.Thread):
        def __init__(self, queue, total):
            threading.Thread.__init__(self)
            self._queue = queue
            self._total = total

        def run(self):
            while not self._queue.empty():
                url = self._queue.get()
                threading.Thread(target=self.msg).start()
                try:
                    r = requests.get(url=url, headers=get_user_agent(), timeout=5)
                    if r.status_code == 200:
                        sys.stdout.write('/r' + '[+]%s\t\t\n' % url)
                    result = open('result.html', 'a+')
                    result.write('<a href="' + url + '" rel="external nofollow" target="_blank">' + url + '</a>')
                    result.write('\r\n</br>')
                    result.close()
                except Exception:
                    pass

        def msg(self):
            per = 100 - (float(self._queue.qsize()) / float(self._total) * 100)
            percent = "%s Finished| %s All| Scan in %1.f %s" % ((self._total - self._queue.qsize()), self._total, per, '%')
            sys.stdout.write('\r' + '[*]' + percent)

    def start(self):
        result = open('result.html', 'w')
        result.close()
        queue = Queue()
        f = open('dict.txt', 'r')
        for i in f.readlines():
            queue.put(self.url + "/" + i.rstrip('\n'))
            total = queue.qsize()
            threads = []
            thread_count = int(self.count)
        for i in range(thread_count):
            threads.append(self.DirScan(queue, total))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()


def get_user_agent():
    user_agent_list = [
        {},
        {},
        {},
        {},
    ]
    return random.choice(user_agent_list)


def main():
    print('''
    
    
    
    
    Welcome to WebDirscan
    Version:1.0 Author:%s
    '''%__author__)
    parser = OptionParser('python WebDirScan.py -u <Target URL> -f <Dictionary file name> [-t <Thread_count>]')
    parser.add_option('-u', '--url', dest='url', type='string', help='target url for scan')
    parser.add_option('-f', '--file', dest='file_name', type='string', help='dictionary filename')
    parser.add_option('-t', '--thread', dest='count', type='int', default=10, help='scan thread count')
    options, args = parser.parse_args()
    if options.url and options.file_name:
        dirscan = WebDirScan(options)
        dirscan.start()
        sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
