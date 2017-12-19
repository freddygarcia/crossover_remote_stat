dfrom uuid import uuid4
from os import remove
from shutil import move
from subprocess import call
from sys import argv
from tempfile import gettempdir
from os import path

_SYSTEM_MONITOR_FILE_NAME = 'system_monitor.py'

# get temp folder
temp_dir = gettempdir()
# generate temp path
temp_path = path.join(temp_dir, _SYSTEM_MONITOR_FILE_NAME)
# empty file
file = None
# read file as template
with open(_SYSTEM_MONITOR_FILE_NAME) as f: file = f.read()
# put key in file
new_content = file.replace('__key__', 'asdsa')
# new file name
new_file_name = _SYSTEM_MONITOR_FILE_NAME + str(uuid4())[:4]
# save new file 
with open(new_file_name, 'w') as f: f.write(new_content)
# move system monitor to temp path
# move(_SYSTEM_MONITOR_FILE_NAME, temp_path)
# execute system monitor
# call(["python", temp_path, argv[1]])
# auto destroy file after execution
remove(new_file_name)