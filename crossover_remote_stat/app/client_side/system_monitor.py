from pip import get_installed_distributions, main as pip_main
from datetime import datetime
from platform import system, node
from os import path
from pickle import dumps as pickle_dumps
from subprocess import Popen, PIPE
from sys import argv
import logging


logging.basicConfig(format="[%(asctime)s] %(name)s %(levelname)s: %(message)s",
						filename='crossover_remote_stat.log',
						level=logging.DEBUG,
						datefmt="%m/%d/%Y %I:%M:%S %p")


DEPENDENCES = [
	'cryptography==2.1.4',
	'psutil==5.4.2',
	'pypiwin32==220',
	'requests==2.18.4',
	'uptime==3.0.1'
]

class SystemMonitor:

	def __init__(self):
		self.platform = None
		self.uptime = None
		self.cpu_percent = None
		self.memory_usage = None
		self.hostname = None
		self.event_logs = None

	@staticmethod
	def retrieve_statistics():
		monitor = SystemMonitor()
		monitor.obtain_statistics()
		return monitor

	def obtain_statistics(self):
		self.platform = self.determine_os()
		self.uptime = self.get_uptime()
		self.cpu_percent = self.get_cpu_percent()
		self.memory_usage = self.get_memory_usage()
		self.hostname = self.determine_hostname()
		self.event_logs = self.get_event_logs()

	def determine_os(self):
		"""Get host OS"""
		return system()

	def determine_hostname(self):
		"""Get host name"""
		return node()

	def get_cpu_percent(self):
		"""Get current system wide cpu usage as a percentage"""
		from psutil import cpu_percent
		return cpu_percent(interval=1)

	def get_memory_usage(self):
		"""Statistic about system memory usage (lib calculate usage depending on de platform)"""
		from psutil import virtual_memory
		return virtual_memory().percent

	def get_uptime(self):
		from uptime import boottime
		uptime = None

		platform = self.determine_os()

		if platform == 'Windows':
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

	def __str__(self):
		return 'SystemMonitor<hostname={hostname},os={os}>'.format(**self.__dict__()) 

	def get_event_logs(self):
		platform = self.determine_os()

		if platform != 'Windows':
			return False

		try:
			import win32con
			import win32evtlog
			import win32evtlogutil
			import winerror
			import win32evt
			logging.info('loaded windows libs')
		except Exception as e:
			logging.error(e)
			logging.error('windows libs couldn"t be loaded, may not be correctly installed or running in non-windows platform')
			return False

		SERVER = 'localhost'
		LOGTYPE = 'Security'

		hand = None

		try:
			hand = win32evtlog.OpenEventLog(SERVER,LOGTYPE)
		except Exception as e:
			logging.error(e)
			return False

		flags = win32evt.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
		events = win32evtlog.ReadEventLog(hand,flags,0)
		evt_dict={win32con.EVENTLOG_AUDIT_FAILURE:'EVENTLOG_AUDIT_FAILURE',
				  win32con.EVENTLOG_AUDIT_SUCCESS:'EVENTLOG_AUDIT_SUCCESS',
				  win32con.EVENTLOG_INFORMATION_TYPE:'EVENTLOG_INFORMATION_TYPE',
				  win32con.EVENTLOG_WARNING_TYPE:'EVENTLOG_WARNING_TYPE',
				  win32con.EVENTLOG_ERROR_TYPE:'EVENTLOG_ERROR_TYPE'}

		events_list = []
	 
		try:
			events=1
			while events:
				events=win32evtlog.ReadEventLog(hand,flags,0)
	 
				for ev_obj in events:
					event_dict = {}
					the_time = ev_obj.TimeGenerated.Format()
					evt_id = str(winerror.HRESULT_CODE(ev_obj.EventID))
					computer = str(ev_obj.ComputerName)
					cat = ev_obj.EventCategory
					record = ev_obj.RecordNumber
					msg = win32evtlogutil.SafeFormatMessage(ev_obj, LOGTYPE)
	 
					source = str(ev_obj.SourceName)
					if not ev_obj.EventType in evt_dict.keys():
						evt_type = "unknown"
					else:
						evt_type = str(evt_dict[ev_obj.EventType])

					event_dict['event_time'] = the_time
					event_dict['event_id'] = evt_id
					event_dict['event_type'] = evt_type
					event_dict['record'] = record
					event_dict['source'] = source
					event_dict['msg'] = msg

					events_list.append(event_dict)
		except:
			return None

		return events_list

	def __dict__(self):
		return {
			'os' : self.platform,
			'uptime' : self.uptime,
			'hostname' : self.hostname,
			'event_logs' : self.event_logs,
			'cpu_percent' : self.cpu_percent,
			'memory_usage' : self.memory_usage
		}

class MonitorConnector:
	def __init__(self, key):
		self.key = key

	def encrypt(self, statistics):
		from cryptography.fernet import Fernet
		ENCODE = 'utf-8'
		key_bytes = bytes(self.key, ENCODE)
		serialized_data = pickle_dumps(statistics.__dict__())
		encrypted_data = Fernet(self.key).encrypt(serialized_data)
		return encrypted_data

	def send_statistics(self):
		from requests import post
		SERVER_ADDR = 'http://192.168.100.195:5000/'
		HEADERS = {'content-type' : 'application/octet-stream'}

		monitor = SystemMonitor()
		statistics = monitor.retrieve_statistics()

		encrypted_data = self.encrypt(statistics)
		response = post(SERVER_ADDR, data=encrypted_data, headers=HEADERS)

		logging.info(response.text)

	def check_installed_libs(self):
		"""Install all dependences that arent already install in the system"""

		# get all installed packages
		installed_libs = get_installed_distributions()
		# format the installed packages list in order to compare with
		# dependences list
		libs_to_compare = [depend.project_name +  '==' +  depend.version for depend in installed_libs]
		# get the modules which arent in the system
		libs_to_install = [depend for depend in DEPENDENCES  if depend not in libs_to_compare]
		# install the dependeces
		[pip_main(['install', package]) for package in libs_to_install]


if __name__ == '__main__':
	monitorconnector = MonitorConnector('__key__')
	# Well, I don't really know if this step is necessary,
	# I'm assuming the system may not have installed the modules
	# this script needs to work.
	# if this step isen't necessary, just remove this line code
	# in order to avoid to install modules
	monitorconnector.check_installed_libs()

	# obtain statistics and send to server
	monitorconnector.send_statistics()
