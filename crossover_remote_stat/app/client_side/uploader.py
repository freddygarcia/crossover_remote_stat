import time
from os import remove, path
from paramiko import SSHClient, AutoAddPolicy
from shutil import move
from subprocess import call
from sys import argv
from tempfile import gettempdir
from uuid import uuid4

_SYSTEM_MONITOR_FILE_NAME = 'system_monitor.py'

def show_command_result(result):
	in_, out_, err = result
	print(out_.read().decode('utf-8'))
	print(err.read().decode('utf-8'))

def upload_and_execute(connection_params):
	
	# define ssh transport stream

	ssh_client = SSHClient()
	ssh_client.set_missing_host_key_policy(AutoAddPolicy())
	ssh_client.connect(hostname=connection_params['hostname'],
						username=connection_params['username'],
						password=connection_params['password'])
	sftp_client  = ssh_client.open_sftp()

	tmp_folder = 'tmp_folder{}/'.format(str(uuid4())[:4])
	system_monitor_path = path.join(tmp_folder, _SYSTEM_MONITOR_FILE_NAME)
	# # create temp dir
	sftp_client.mkdir(tmp_folder)
	# # upload script
	# upload remote file to temp folder
	sftp_client.put(_SYSTEM_MONITOR_FILE_NAME, system_monitor_path)
	# execute remote script
	show_command_result(ssh_client.exec_command('python {}'.format(system_monitor_path)))
	# remove script and temp folder
	sftp_client.remove(system_monitor_path)
	sftp_client.rmdir(tmp_folder)
	# close connections
	sftp_client.close()
	ssh_client.close()

connection_params = {
	'hostname':'104.236.235.68',
	'username':'freddie',
	'password':'toor',
	'port':22
}

if __name__ == '__main__':
	upload_and_execute(connection_params)
