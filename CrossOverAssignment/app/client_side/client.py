from datetime import datetime
from hashlib import sha1
from hmac import new as new_hmac
from platform import system, node
from pickle import dumps as pickle_dumps
from psutil import cpu_percent, virtual_memory
from subprocess import Popen, PIPE
from uptime import boottime
from requests import post

class SystemMonitor:

	def __init__(self):
		self.platform = self.determine_os()
		self.uptime = self.get_uptime()
		self.cpu_percent = self.get_cpu_percent()
		self.memory_usage = self.get_memory_usage()
		self.hostname = self.determine_hostname()

	def determine_os(self):
		"""Get host OS"""
		return system()

	def determine_hostname(self):
		"""Get host name"""
		return node()

	def get_cpu_percent(self):
		"""Get current system wide cpu usage as a percentage"""
		return cpu_percent(interval=1)

	def get_memory_usage(self):
		"""Statistic about system memory usage (lib calculate usage depending on de platform)"""
		return virtual_memory().percent

	def get_uptime(self):
		uptime = None

		if self.platform == 'Windows':
			try:
				p = Popen("net stats Workstation", shell=True, stdin=PIPE, stdout=PIPE)
				(child_stdin, child_stdout) = (p.stdin, p.stdout)
				lines = child_stdout.readlines()
				child_stdin.close()
				child_stdout.close() 

				info_cad = str(list(filter(lambda x: b'Statistics since' in x, lines))[0])

				date, time, ampm = info_cad.split()[2:5]
				date = date.replace(',', '')

				m, d, y = [int(v) for v in date.split('/')]
				H, M, S = [int(v) for v in time.split(':')]

				uptime = datetime(y, m, d, H, M, S)
			except Exception as e:
				uptime = None
		else:
			uptime = boottime()

		return uptime

	def __dict__(self):
		return {
			'os' : self.platform,
			'uptime' : self.uptime,
			'hostname' : self.hostname,
			'cpu_percent' : self.cpu_percent,
			'memory_usage' : self.memory_usage
		}



class Sender:

	def __init__(self, key):
		self.key = key

	def obtain_statistics(self):
		systemmonitor = SystemMonitor()
		return systemmonitor

	def encrypt(self, serialized_data):
		ENCODE = 'utf-8'
		key_bytes = bytes(self.key, ENCODE)
		hex_digest = new_hmac(key_bytes, serialized_data, sha1).hexdigest()
		header = bytes(hex_digest, ENCODE)
		return header + b' ' + serialized_data

	def send(self):
		SERVER_ADDR = 'http://127.0.0.1:5000/'
		HEADERS = {'content-type' : 'application/octet-stream'}

		statistics = self.obtain_statistics()
		serialized_data = pickle_dumps(statistics.__dict__())
		encrypted_data = self.encrypt(serialized_data)

		response = post(SERVER_ADDR, data=encrypted_data, headers=HEADERS)
		return response

