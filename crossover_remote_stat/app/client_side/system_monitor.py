from datetime import datetime
from sys import argv
from cryptography.fernet import Fernet
from platform import system, node
from pickle import dumps as pickle_dumps
from psutil import cpu_percent, virtual_memory
from subprocess import Popen, PIPE
from uptime import boottime
from requests import post
import win32con
import win32evtlog
import win32evtlogutil
import winerror

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
		return cpu_percent(interval=1)

	def get_memory_usage(self):
		"""Statistic about system memory usage (lib calculate usage depending on de platform)"""
		return virtual_memory().percent

	def get_uptime(self):
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

		SERVER = 'localhost'
		LOGTYPE = 'Security'

		hand = None

		try:
			hand = win32evtlog.OpenEventLog(SERVER,LOGTYPE)
		except Exception as e:
			return False

		flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
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
		ENCODE = 'utf-8'
		key_bytes = bytes(self.key, ENCODE)
		serialized_data = pickle_dumps(statistics.__dict__())
		encrypted_data = Fernet(self.key).encrypt(serialized_data)
		return encrypted_data

	def send_statistics(self):
		SERVER_ADDR = 'http://104.236.235.68:5000/'
		HEADERS = {'content-type' : 'application/octet-stream'}

		monitor = SystemMonitor()
		statistics = monitor.retrieve_statistics()

		encrypted_data = self.encrypt(statistics)
		response = post(SERVER_ADDR, data=encrypted_data, headers=HEADERS)

		with ('log_python_system_monitor.log', 'w') as f:
			f.write(response.text)


if __name__ == '__main__':
	key = argv[0]
	monitorconnector = MonitorConnector(key)
	monitorconnector.send_statistics()
