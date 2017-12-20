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
		log.error(e)
		return False

	# create sftp instance
	sftp_client  = None

	try:
		sftp_client  = ssh_client.open_sftp()
	except Exception as e:
		log.error(e)
		log.error('Cannot stablished sftp connection with host {}'.format(connection_params['ip']))
		return False

	remote_temporal_folder = 'tmp_folder{}/'.format(str(uuid4())[:4])
	remote_script_path = path.join(remote_temporal_folder, _SYSTEM_MONITOR_FILE_NAME)
	# upload script path
	local_script_path = path.join(path.dirname(__file__), _SYSTEM_MONITOR_FILE_NAME)
	# create temp dir
	sftp_client.mkdir(remote_temporal_folder)	
	# upload remote file to temp folder
	sftp_client.put(local_script_path, remote_script_path)
	# execute remote script
	show_command_result(ssh_client.exec_command('sudo python {}'.format(remote_script_path)), 
							connection_params['password'])
	# remove script and temp folder
	sftp_client.remove(remote_script_path)
	sftp_client.rmdir(remote_temporal_folder)
	# close connections
	sftp_client.close()
	ssh_client.close()

	return True
