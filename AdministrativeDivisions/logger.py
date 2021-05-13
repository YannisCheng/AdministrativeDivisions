import sys


class Logger(object):
    def __init__(self, file_name='crawl_log'):
        self.terminal = sys.stdout
        self.log = open(file_name, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass
