import time
from os import remove, path
from paramiko import SSHClient, AutoAddPolicy
from shutil import move
from logging import getLogger
from subprocess import call
from sys import argv
from tempfile import gettempdir
from uuid import uuid4

_SYSTEM_MONITOR_FILE_NAME = 'system_monitor.py'
log = getLogger(__name__)

def show_command_result(result, password):
	in_, out_, err = result
	print(out_.read().decode('utf-8'))
	print(err.read().decode('utf-8'))
	in_.write(password)

def upload_and_execute(connection_params):
	
	ssh_client = SSHClient()
	ssh_client.set_missing_host_key_policy(AutoAddPolicy())

	try:
		ssh_client.connect(hostname=connection_params['ip'],
							username=connection_params['username'],
							password=connection_params['password'],
							port=connection_params['port'])
	except Exception as e:
		log.error('Connection cannot be stablished to host {}'.format(connection_params['ip']))
		return False

	sftp_client  = ssh_client.open_sftp()

	tmp_folder = 'tmp_folder{}/'.format(str(uuid4())[:4])
	system_monitor_path = path.join(tmp_folder, _SYSTEM_MONITOR_FILE_NAME)
	dst = path.join(path.dirname(__file__), _SYSTEM_MONITOR_FILE_NAME)
	# # create temp dir
	sftp_client.mkdir(tmp_folder)	
	# upload remote file to temp folder
	sftp_client.put(dst, system_monitor_path)
	# execute remote script
	show_command_result(ssh_client.exec_command('sudo python {}'.format(system_monitor_path)), 
							connection_params['password'])
	# remove script and temp folder
	sftp_client.remove(system_monitor_path)
	sftp_client.rmdir(tmp_folder)
	# close connections
	sftp_client.close()
	ssh_client.close()

	return True

connection_params = {
	'ip':'192.168.100.163',
	'username':'freddie',
	'password':'zoren101!',
	'port':22
}

if __name__ == '__main__':
	upload_and_execute(connection_params)
