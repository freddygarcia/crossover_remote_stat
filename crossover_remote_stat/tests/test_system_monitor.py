import unittest

from crossover_remote_stat.app.client_side.client import SystemMonitor

class TestSystemMonitor(unittest.TestCase):
	"""docstring for TestSystemMonitor"""

	def test_get_system_state(self):
		systemmonitor = SystemMonitor().retrieve_statistics()
		self.assertIsNot(systemmonitor.uptime, None)
		self.assertIsNot(systemmonitor.event_logs, None)
		self.assertIsInstance(systemmonitor.platform, str)
		self.assertIsInstance(systemmonitor.cpu_percent, float)
		self.assertIsInstance(systemmonitor.memory_usage, float)
		self.assertIsInstance(systemmonitor.hostname, str)
