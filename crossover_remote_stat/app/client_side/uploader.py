import time
from os import remove, path
from paramiko import SSHClient, AutoAddPolicy
from shutil import move
from logging import getLogger
from subprocess import call
from sys import argv
from tempfile import gettempdir
from uuid import uuid4

from crossover_remote_stat import config
from crossover_remote_stat.app.client_side.system_monitor import get_template_monitor

_SYSTEM_MONITOR_FILE_NAME = 'system_monitor.py'
log = getLogger(__name__)

def show_command_result(result):
	in_, out_, err = result
	print(out_.read().decode('utf-8'))
	print(err.read().decode('utf-8'))


def upload_and_execute(connection_params):
	ssh_client = SSHClient()
	ssh_client.set_missing_host_key_policy(AutoAddPolicy())

	try:
		ssh_client.connect(hostname=connection_params['ip'],
							username=connection_params['username'],
							password=connection_params['password'],
							port=connection_params['port'])
	except Exception as e:
		log.error(e)
		log.error('Connection cannot be established to host {}'.format(connection_params['ip']))
		return False

	# create sftp instance
	sftp_client  = None

	try:
		sftp_client  = ssh_client.open_sftp()
	except Exception as e:
		log.error(e)
		log.error('Cannot established sftp connection with host {}'.format(connection_params['ip']))
		return False

	# params to generate the script to upload
	server_address = config['SERVER']['host']
	key = connection_params['token']
	client_settings = config._sections['CLIENT']

	remote_temporal_folder = 'tmp_folder{}/'.format(str(uuid4())[:4])
	remote_script_path = path.join(remote_temporal_folder, _SYSTEM_MONITOR_FILE_NAME)
	# upload script path
	local_script_path = get_template_monitor(key, server_address, client_settings)
	# create temp dir
	sftp_client.mkdir(remote_temporal_folder)
	# upload remote file to temp folder
	sftp_client.put(local_script_path.name, remote_script_path)
	# execute remote script
	show_command_result(ssh_client.exec_command('python {}'.format(remote_script_path)))
	# close connections
	sftp_client.close()
	ssh_client.close()

	return True
