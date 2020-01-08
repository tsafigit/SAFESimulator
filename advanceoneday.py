import sys
import datetime
from datetime import datetime
from datetime import timedelta

def _linux_set_time(new_time):
    import subprocess
    import shlex

#    time_string = datetime(*time_tuple).isoformat()
    time_string = new_time.isoformat();

    subprocess.call(shlex.split("timedatectl set-ntp false"))  # May be necessary
    subprocess.call(shlex.split("sudo date -s '%s'" % time_string))
    subprocess.call(shlex.split("sudo hwclock -w"))


date = datetime.today()
print("Today is")
print(date)
one_day_delta = timedelta(days=1)
date = date + one_day_delta
if date.weekday() == 5:
	date = date + one_day_delta
if date.weekday() == 6:
	date = date + one_day_delta
print("Setting to")
print(date)

_linux_set_time(date)

