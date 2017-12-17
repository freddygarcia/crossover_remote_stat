from datetime import datetime
from hashlib import sha1
from hmac import new_hmac
from platform import system
from pickle import pickle_loads, pickle_dumps
from psutil import cpu_percent, virtual_memory
from subprocess import Popen, PIPE
from uptime import boottime

class SystemMonitor:

	def __init__(self):
		self.platform = self.determine_os()
		self.uptime = self.get_uptime()
		self.memory_usage = self.get_memory_usage()
		self.cpu_percent = self.get_cpu_percent()

	def determine_os(self):
		"""Get host OS"""
		return system()

	def get_cpu_percent(self):
		"""Get current system wide cpu usage as a percentage"""
		return cpu_percent(interval=1)

	def get_memory_usage(self):
		"""Statistic about system memory usage (lib calculate usage depending on de platform)"""
		return virtual_memory().percent

	def get_uptime(self):
		uptime = None

		if self.platform == 'Windows':
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
		else:
			uptime = boottime()

		return uptime

	def __dict__(self):
		return {
			'os' : self.platform,
			'uptime' : self.uptime,
			'memory_usage' : self.memory_usage,
			'cpu_percent' : self.cpu_percent
		}


def obtain_statistic():
	systemmonitor = SystemMonitor()
	return systemmonitor

def serialize(data):
	return dumps(data)

def encrypt(key):
	return new_hmac(key, serialized_data, sha1) + b' ' + serialized_data

