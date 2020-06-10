import arrow
import time as t

LOGFILE = None


def log(text):
    print(text)
    timestamp = arrow.get().format('DD-MMM-YYYY HH:mm:ss')

    if LOGFILE:
        with open(LOGFILE, 'a') as f:
            f.write(timestamp + ' - ' + text)
            f.write("\n")
    else:
        raise FileNotFoundError('LOGFILE variable not assigned.')