import csv as c
import time as t

LOGFILE = None


def log(text):
    print(text)
    if LOGFILE:
        with open(LOGFILE, 'a') as f:
            f.write(str(t.time()) + ' - ' + text)
            f.write("\n")
    else:
        raise FileNotFoundError('LOGFILE variable not assigned.')