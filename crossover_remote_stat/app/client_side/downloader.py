from os import remove
from shutil import copy2
from subprocess import call
from sys import argv
from tempfile import NamedTemporaryFile
from os import path

_SYSTEM_MONITOR_FILE_NAME = 'system_monitor.py'

# get temp folder
temp_dir = tempfile.gettempdir()
# generate temp path
temp_path = os.path.join(temp_dir, _SYSTEM_MONITOR_FILE_NAME)
# move system monitor to temp path
shutil.move(_SYSTEM_MONITOR_FILE_NAME, temp_path)
# execute system monitor
call(["python", temp_path])
# auto destroy file after execution
remove(argv[0])